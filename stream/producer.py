# from kafka import KafkaProducer
# import time
# import random

# logs = [
#     "Failed password for invalid user root from 192.168.1.10 port 22 ssh2",
#     "Accepted password for ubuntu from 192.168.1.5 port 53722 ssh2",
#     "Invalid user admin from 10.0.0.2",
#     "Connection closed by authenticating user pi 172.16.0.15",
#     "Failed password for root from 8.8.8.8 port 2345 ssh2"
# ]

# try:
#     producer = KafkaProducer(
#         bootstrap_servers='host.docker.internal:9092',
#         value_serializer=lambda x: x.encode('utf-8')
#     )
#     print("[*] Sending test logs to Kafka topic 'logs'...")

#     for _ in range(10):
#         log = random.choice(logs)
#         future = producer.send('logs', value=log)
#         result = future.get(timeout=10)
#         print(f"[+] Sent: {log} | Offset: {result.offset}")
#         time.sleep(0.5)

#     producer.flush()
#     print("[✓] All logs sent successfully.")

# except Exception as e:
#     print(f"[!] Producer Error: {e}")
