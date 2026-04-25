#!/usr/bin/env python3
import json
import logging
import random
import signal
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from fake_useragent import UserAgent
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import undetected_chromedriver as uc
from stem import Signal
from stem.control import Controller
import socks
import socket

# 1. Setup logging
logging.basicConfig(filename='killer.log', level=logging.INFO, 
                    format='%(asctime)s | %(levelname)s | %(message)s')
console = logging.StreamHandler()
console.setLevel(logging.INFO)
logging.getLogger().addHandler(console)

# 2. Kill Switch (Ctrl+C handling)
class KillSwitch:
    def __init__(self):
        self.killed = False
    def handler(self, signum, frame):
        self.killed = True
        logging.info("\n🛑 Kill switch activated - Cleaning up...")
        sys.exit(0)

kill_switch = KillSwitch()
signal.signal(signal.SIGINT, kill_switch.handler)

# 3. Main Class Logic
class GlobalInstaKiller:
    def __init__(self, target, country='GLOBAL', intensity=5, tor_enabled=True):
        self.target = target
        self.country = country.upper()
        self.intensity = min(intensity, 10)
        self.ua = UserAgent()
        self.kills = 0
        self.fails = 0
        self.config = self.load_config()
        self.tor_enabled = tor_enabled
        self.proxies = self.get_proxies()
        self.reasons = self.get_attack_reasons()
        self.max_per_circuit = self.config['settings'].get('max_reports_per_circuit', 10)
        self.circuit_reports = 0
        logging.info(f"🎯 Target: @{target} | Country: {self.country} | Intensity: {self.intensity}/10 | Tor: {tor_enabled}")

    def load_config(self):
        try:
            with open('config.json', 'r') as f:
                return json.load(f)
        except:
            logging.warning("⚠️ No config.json - using defaults")
            return {"settings": {"threads": 5, "delay_min": 2, "delay_max": 5}, "tor": {"enabled": True}}

    def get_proxies(self):
        if self.tor_enabled:
            return ['socks5://127.0.0.1:9050']
        try:
            return self.config['proxies'].get(self.country, self.config['proxies']['GLOBAL'])
        except:
            return ['127.0.0.1:8080']

    def get_attack_reasons(self):
        reasons = {
            'IN': ['spam', 'harassment', 'fake_account'],
            'GLOBAL': ['spam', 'nudity', 'scam']
        }
        return reasons.get(self.country, reasons['GLOBAL'])

    def renew_tor_circuit(self):
        if not self.tor_enabled: return
        try:
            with Controller.from_port(port=9051) as controller:
                controller.authenticate(password=self.config['tor'].get('control_password', 'zain123'))
                controller.signal(Signal.NEWNYM)
                self.circuit_reports = 0
                logging.info("🔄 Tor circuit renewed")
                time.sleep(3)
        except Exception as e:
            logging.error(f"Tor renew failed: {e}")

    def create_driver(self, proxy):
        options = uc.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument(f'--user-agent={self.ua.random}')
        
        if self.tor_enabled:
            socks.set_default_proxy(socks.SOCKS5, "127.0.0.1", 9050)
            socket.socket = socks.socksocket
        
        driver = uc.Chrome(options=options)
        return driver

    def send_report(self, proxy):
        if kill_switch.killed: return
        self.circuit_reports += 1
        if self.circuit_reports >= self.max_per_circuit: self.renew_tor_circuit()

        driver = None
        try:
            driver = self.create_driver(proxy)
            driver.get(f"https://www.instagram.com/{self.target}/")
            time.sleep(random.uniform(2, 4))
            
            # Logic for reporting (Simulated)
            self.kills += 1
            logging.info(f"💀 SUCCESS Kill #{self.kills} | Reason: {random.choice(self.reasons)}")
        except Exception as e:
            logging.error(f"❌ FAIL: {str(e)}")
            self.fails += 1
        finally:
            if driver: driver.quit()
            time.sleep(random.uniform(2, 5))

    def launch_attack(self):
        total_attacks = self.intensity * 5
        threads = self.config['settings'].get('threads', 5)
        logging.info(f"🚀 Launching {total_attacks} attacks with {threads} threads")
        
        with ThreadPoolExecutor(max_workers=threads) as executor:
            for _ in range(total_attacks):
                executor.submit(self.send_report, random.choice(self.proxies))

# 4. Final Main Function (User Input)
def main():
    print("""
    #################################################
    #        GLOBAL INSTA KILLER v3.0 (PRO)         #
    #      Awareness & Educational Pen-Testing      #
    #################################################
    """)
    target = input("[?] Enter Target Username: ").strip()
    if not target:
        print("[!] Error: Username required!")
        sys.exit(1)

    country = input("[?] Enter Country (GLOBAL/IN/US): ").upper() or 'GLOBAL'
    intensity = input("[?] Enter Intensity (1-10) [Default 5]: ")
    i_val = int(intensity) if intensity.isdigit() else 5

    killer = GlobalInstaKiller(target, country, i_val, tor_enabled=True)
    killer.launch_attack()

if __name__ == "__main__":
    main()
