#!/usr/bin/env python3
import random

def random_ipv4():
    # Standard IPv4 dotted-decimal
    return ".".join(str(random.randint(0, 255)) for _ in range(4))

def random_ipv4_octal():
    # Each octet in octal (padded to 3 digits)
    return ".".join(f"{random.randint(0,255):03o}" for _ in range(4))

def random_ipv4_shorthand():
    # Two-part IPv4 shorthand: first octet and a 24-bit integer (e.g. "127.167772161" == "127.0.0.1")
    first = random.randint(0, 255)
    remainder = random.randint(0, 256**3 - 1)
    return f"{first}.{remainder}"

def random_private_ipv4():
    # Choose a private IPv4 from one of the ranges: 10.x.x.x, 172.16.x.x to 172.31.x.x, or 192.168.x.x
    choice = random.choice([1,2,3])
    if choice == 1:
        return f"10.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(0,255)}"
    elif choice == 2:
        return f"172.{random.randint(16,31)}.{random.randint(0,255)}.{random.randint(0,255)}"
    else:
        return f"192.168.{random.randint(0,255)}.{random.randint(0,255)}"

def random_public_ipv4():
    # Generate a public IPv4 address, avoiding common private/reserved ranges
    while True:
        octets = [random.randint(0,255) for _ in range(4)]
        if (octets[0] == 10 or
            (octets[0] == 172 and 16 <= octets[1] <= 31) or
            (octets[0] == 192 and octets[1] == 168) or
            (octets[0] == 127)):
            continue
        return ".".join(str(o) for o in octets)

def random_ipv6():
    # Generic IPv6 in full notation
    return ":".join(f"{random.randint(0, 0xffff):04x}" for _ in range(8))

def random_public_ipv6():
    # Public IPv6 (global unicast) format; note: for payloads, random is fine.
    return ":".join(f"{random.randint(0, 0xffff):04x}" for _ in range(8))

def random_private_ipv6():
    # Unique local IPv6 address (starting with fd)
    groups = [f"{random.randint(0, 0xffff):04x}" for _ in range(7)]
    return "fd" + f"{random.randint(0, 0xffff):02x}:" + ":".join(groups)

def generate_ip_payload():
    generators = [
        random_ipv4,
        random_ipv4_octal,
        random_ipv4_shorthand,
        random_private_ipv4,
        random_public_ipv4,
        random_ipv6,
        random_public_ipv6,
        random_private_ipv6,
    ]
    return random.choice(generators)()

if __name__ == "__main__":
    num_ips = 200
    ip_list = [generate_ip_payload() for _ in range(num_ips)]
    
    with open("ip_payloads", "w") as f:
        for ip in ip_list:
            f.write(ip + "\n")
    
    print("Generated 200 IP addresses in 'ip_payloads.csv'")
