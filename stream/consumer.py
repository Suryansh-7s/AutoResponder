from kafka import KafkaConsumer
from redis_cache.ip_enricher import enrich_ip_abuseipdb
from redis_cache.redis_client import get_cached_ip, cache_ip, incr_failed_attempt, reset_failed_attempts
import re
from alert.telegram_alert import send_telegram_alert


consumer = KafkaConsumer(
    'logs',
    bootstrap_servers='localhost:9092',
    auto_offset_reset='earliest',
    group_id='log-consumer-group-test2'
)

def enrich_ip(ip):
    print(f"[~] Enriching IP: {ip}")
    return enrich_ip_abuseipdb(ip)

def extract_ip(log_line):
    match = re.search(r'from ([\d\.]+)', log_line)
    if match:
        return match.group(1)
    return None

def detect_threat(log_line, ip=None):
    log_lower = log_line.lower()

    if "failed password" in log_lower:
        print("🚨 Detection: Brute Force Attempt Detected")
        if ip:
            count = incr_failed_attempt(ip)
            print(f"[!] Failed SSH attempt from {ip} — Count: {count}")
            if count >= 5:
                alert_msg = f"🚨 Brute Force Attempt Detected\nLog: {log_line}"
                print(alert_msg)
                send_telegram_alert(alert_msg)
                reset_failed_attempts(ip)

    elif "invalid user" in log_lower:
        print("👻 Detection: Access Attempt by Invalid User")
        if ip:
            alert_msg = f"👻 Invalid user access attempt\nLog: {log_line}"
            send_telegram_alert(alert_msg)

    elif "ufw" in log_lower and "block" in log_lower:
        print("🛡️ Detection: Firewall Denied Incoming Request")
        if ip:
            alert_msg = f"🛡️ Firewall denied incoming request from {ip}"
            send_telegram_alert(alert_msg)

    elif "root" in log_lower and "login" in log_lower:
        print("⚠️ Detection: Root Login Attempt Detected")
        if ip:
            alert_msg = f"⚠️ Root login attempt detected from {ip}"
            send_telegram_alert(alert_msg)

print("[*] Starting Kafka consumer with Redis caching...")
for message in consumer:
    log = message.value.decode('utf-8')
    print(f"[+] Log Received: {log}")

    # Step 1: IP extraction
    ip = extract_ip(log)

    # Step 2: Run detection logic (pass IP if available)
    detect_threat(log, ip)

    # Step 3: Enrichment only if IP exists
    if not ip:
        continue

    cached = get_cached_ip(ip)
    if cached:
        print(f"[CACHE HIT] IP {ip} → {cached}")
    else:
        enriched = enrich_ip(ip)
        cache_ip(ip, enriched)
        print(f"[CACHE MISS] IP {ip} enriched and cached.")