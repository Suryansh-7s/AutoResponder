from kafka import KafkaConsumer
import json

def start_consumer(topic_name='logs'):
    print("[*] Starting Kafka consumer...")

    consumer = KafkaConsumer(
        topic_name,
        bootstrap_servers='localhost:9092',
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        group_id='autoresponder-group',
        value_deserializer=lambda x: x.decode('utf-8')
    )

    print(f"[*] Subscribed to topic: {topic_name}")
    for message in consumer:
        log_line = message.value
        print(f"[+] Log Received: {log_line}")
        # TODO: pass log_line to detection engine here

if __name__ == "__main__":
    start_consumer()
