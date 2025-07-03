# 🛡️ AutoResponder — Real-Time SIEM for SSH Threat Detection

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

- **Python** + **Kafka** + **Redis**
- **Filebeat** for log shipping
- **Telegram Bot API** for real-time alerting
- **dotenv**, **httpx**, **kafka-python**, and more

---

## 🔍 Features

✅ SSH Brute Force & Invalid Access Detection  
✅ AbuseIPDB integration for IP intelligence  
✅ Telegram Alerts for high-fidelity threat response  
✅ Redis Caching for enriched IPs (performance boost)  
✅ Modular rule engine via `rules.json`  
✅ Easy log ingestion using Filebeat & Kafka  
✅ Environment-based secret handling (`.env`)  

---
## 🛠️ Local Setup

### 1. Clone the Repo

```bash
git clone https://github.com/Suryansh-7s/AutoResponder.git
cd AutoResponder
```

### 2. Setup Python Environment

```bash
python -m venv venv
./venv/bin/Activate.ps1
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

## 🔄 Start the Pipeline

### In WSL/Ubuntu (for Filebeat logs)

```bash
sudo systemctl start filebeat
sudo systemctl status filebeat
```

### In Python (Windows or WSL)

```bash
python -m stream.consumer
```

---

## 🧪 Simulate Attacks

Use this to simulate SSH brute-force attempts:

```bash
for i in {1..6}; do ssh invaliduser@localhost; done
```

Check `/var/log/auth.log` to confirm entries are generated.

---

## 📁 Project Structure

```
AutoResponder/
├── alert/                
├── redis_cache/
├── stream/
├── .env (To be created by the user)
├── rules.json
├── requirements.txt
└── README.md
```

---

## 📈 Future Enhancements

- [ ] Add SQLite/PostgreSQL-based alert storage
- [ ] Integrate Kibana for dashboarding
- [ ] Dockerize entire pipeline
- [ ] Add a plugin system for threat enrichers

---

## 🤝 Contributing

Feel free to fork, raise PRs, or suggest new log types to monitor!