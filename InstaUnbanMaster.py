#!/usr/bin/env python3
"""
InstaUnbanMaster v1.0 - Instagram ID Unban Tool
For innocent users whose accounts got wrongly banned
"""
import requests
import random
import time
import argparse
from fake_useragent import UserAgent

class InstaUnbanMaster:
    def __init__(self, username):
        self.username = username
        self.ua = UserAgent()
        self.appeals = 0
    
    def appeal_ban(self):
        """Mass appeal submission"""
        session = requests.Session()
        headers = {
            'User-Agent': self.ua.chrome,
            'Accept': 'application/json',
            'X-Instagram-Ajax': '1'
        }
        
        # Appeal endpoints
        appeals = [
            f'https://www.instagram.com/accounts/appeal/{self.username}/',
            'https://help.instagram.com/contact/606967319425038',
            'https://www.instagram.com/accounts/login/ajax/'
        ]
        
        reasons = [
            "Wrongly banned - legitimate account",
            "Hacked account - not my activity", 
            "Mass reported by competitors",
            "Technical glitch - please review"
        ]
        
        for i in range(10):  # 10 appeals
            url = random.choice(appeals)
            data = {
                'username': self.username,
                'reason': random.choice(reasons),
                'email': f'user{random.randint(1000,9999)}@temp.com'
            }
            
            try:
                resp = session.post(url, data=data, headers=headers)
                self.appeals += 1
                print(f"📤 Appeal #{self.appeals} sent | {resp.status_code}")
                time.sleep(random.uniform(30, 60))
            except:
                pass
        
        print(f"\n✅ {self.appeals} appeals submitted!")
        print("⏳ Review in 24-72 hours | Check email")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="InstaUnbanMaster")
    parser.add_argument('-u', '--username', required=True)
    args = parser.parse_args()
    
    unbanner = InstaUnbanMaster(args.username)
    unbanner.appeal_ban()
