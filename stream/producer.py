from kafka import KafkaProducer
import time
import random

logs = [
    "Failed password for invalid user root from 192.168.1.10 port 22 ssh2",
    "Accepted password for ubuntu from 192.168.1.5 port 53722 ssh2",
    "Invalid user admin from 10.0.0.2",
    "Connection closed by authenticating user pi 172.16.0.15",
    "Failed password for root from 8.8.8.8 port 2345 ssh2"
]

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda x: x.encode('utf-8')
)

print("[*] Sending test logs to Kafka topic 'logs'...")

for _ in range(10):
    log = random.choice(logs)
    producer.send('logs', value=log)
    print(f"[+] Sent: {log}")
    time.sleep(1)

producer.flush()
