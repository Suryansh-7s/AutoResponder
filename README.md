# 🛡️ AutoResponder — Real-Time SIEM for SSH Threat Detection

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python)](https://www.python.org/)
[![Redis](https://img.shields.io/badge/Redis-7.0+-red?logo=redis)](https://hub.docker.com/_/redis)
[![Kafka](https://img.shields.io/badge/Kafka-2.8+-black?logo=apachekafka)](https://kafka.apache.org/)
[![Docker](https://img.shields.io/badge/Dockerized-yes-blue?logo=docker)](https://www.docker.com/)
[![Telegram Bot](https://img.shields.io/badge/Alerts-Telegram-blue?logo=telegram)](https://core.telegram.org/bots/api)
[![Download Release](https://img.shields.io/github/v/release/Suryansh-7s/AutoResponder?style=for-the-badge)](https://github.com/Suryansh-7s/AutoResponder/releases)


> A modular, real-time log monitoring system that detects suspicious activity, enriches IPs using AbuseIPDB, and sends instant Telegram alerts — all powered by Kafka, Filebeat, Redis, and Python.

---

## 📌 Overview

AutoResponder is a lightweight, extensible SIEM (Security Information and Event Management) prototype designed to simulate real-world incident response in a Linux environment.

It consumes logs (via Kafka + Filebeat), parses them using configurable detection rules (`rules.json`), enriches source IPs via AbuseIPDB, and sends actionable alerts directly to Telegram.

---

## 🚀 Architecture

```
[Filebeat] --> [Kafka] --> [Python Consumer]
                             |--> Rule Matching (Regex)
                             |--> IP Enrichment (AbuseIPDB via Redis Cache)
                             |--> Telegram Alerting
```

---

## ⚙️ Tech Stack

- **Python**, **Kafka**, **Redis**
- **Filebeat** for log shipping
- **Telegram Bot API** for real-time alerting
- **dotenv**, **kafka-python**, **redis-py**

---

## 🔍 Features

✅ SSH Brute Force & Invalid Access Detection  
✅ AbuseIPDB Integration for IP Intelligence  
✅ Telegram Alerts for Real-Time Threat Response  
✅ Redis Caching for Enriched IPs (Performance Boost)  
✅ Modular Rule Engine via `rules.json`  
✅ Easy Log Ingestion using Filebeat + Kafka  
✅ Secret Management via `.env`  

---

## 🛠️ Local Setup

### 1. Clone the Repo

```bash
git clone https://github.com/Suryansh-7s/AutoResponder.git
cd AutoResponder
```

### 2. Install Python & Setup Virtual Environment

```bash
python -m venv venv
.\venv\Scripts\Activate.ps1    # For Windows
# source venv/bin/activate     # For Linux/macOS
pip install -r requirements.txt
```

### 3. Add Secrets in `.env`

```env
ABUSEIPDB_API_KEY=your_abuseipdb_key
TELEGRAM_BOT_TOKEN=your_bot_token
TELEGRAM_CHAT_ID=your_chat_id
KAFKA_BOOTSTRAP_SERVERS=localhost:9092
```

---

## ⚡ One-Click Setup (Recommended)

```ps1
.\setup.ps1   # Runs everything: Docker, Filebeat, VirtualEnv, and launches consumer
```

> 💡 This script checks for Docker, WSL (Ubuntu), Filebeat setup, and runs the pipeline end-to-end.

---

## 🔄 Manual Pipeline Start

### In WSL/Ubuntu

```bash
sudo systemctl start filebeat
sudo systemctl status filebeat
```

### In Windows Terminal / PowerShell

```bash
docker-compose up -d
python -m stream.consumer
```

---

## 🧪 Simulate SSH Attacks

```bash
for i in {1..6}; do ssh invaliduser@localhost; done
```

> Check `/var/log/auth.log` to confirm brute-force attempts are logged.

---

## 📁 Project Structure

```
AutoResponder/
├── alert/
│   └── telegram_alert.py
├── config/
│   └── .env.example
├── redis_cache/
│   ├── ip_enricher.py
│   ├── redis_client.py
├── rules/
│   └── rules.json
├── stream/
│   ├── consumer.py
│   └── producer.py
├── .env               # To be created by user
├── docker-compose.yml
├── LICENSE.txt
├── README.md
├── requirements.txt
└── setup.ps1
```

---

## 🤝 Contributing

PRs are welcome!  
Open issues or suggestions for more log types, rules, or enrichers are highly appreciated.

---

## 👨‍💻 Author

**Suryansh Sharma**  
🚀 [GitHub](https://github.com/Suryansh-7s)  
💼 [LinkedIn](https://www.linkedin.com/in/suryansh-sharmaseven/)  
🔮 [Portfolio](https://suryansh-sharma-portfolio.vercel.app/)
