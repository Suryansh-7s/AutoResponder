from kafka import KafkaConsumer
from redis_cache.ip_enricher import enrich_ip_abuseipdb
from redis_cache.redis_client import get_cached_ip, cache_ip
import re
from alert.telegram_alert import send_telegram_alert
import json
from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv()

consumer = KafkaConsumer(
    'logs',
    bootstrap_servers=os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092"),
    auto_offset_reset='latest',
    group_id='log-consumer-group-prod1'
)

RULES_FILE = Path("rules/rules.json")

with open(RULES_FILE, "r") as f:
    DETECTION_RULES = json.load(f)

def enrich_ip(ip):
    print(f"[~] Enriching IP: {ip}")
    return enrich_ip_abuseipdb(ip)

def extract_ip(log_line):
    match = re.search(r'from ([\d\.]+)', log_line)
    if match:
        return match.group(1)
    return None

def detect_threat(log_line):
    triggered_rules = []
    for rule in DETECTION_RULES:
        if re.search(rule["pattern"], log_line, re.IGNORECASE):
            print(f'{rule["label"]}\nLog: `{log_line}`')
            # 🔔 Send Telegram Alert
            
            send_telegram_alert(f'{rule["label"]}\nLog: `{log_line}`')
            
            triggered_rules.append(rule["type"])
    return triggered_rules


print("[*] Starting Kafka consumer with Redis caching...")
for message in consumer:
    log = message.value.decode('utf-8')
    print(f"[+] Log Received: {log}")

    # Step 1: Run detection logic
    detect_threat(log)

    # Step 2: IP extraction and enrichment
    ip = extract_ip(log)
    if not ip:
        continue

    cached = get_cached_ip(ip)
    if cached:
        print(f"[CACHE HIT] IP {ip} → {cached}")
    else:
        enriched = enrich_ip(ip)
        cache_ip(ip, enriched)
        print(f"[CACHE MISS] IP {ip} enriched and cached.")
