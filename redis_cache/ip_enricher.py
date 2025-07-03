import os
import requests
from dotenv import load_dotenv

load_dotenv()

ABUSEIPDB_API_KEY = os.getenv("ABUSEIPDB_API_KEY")

def enrich_ip_abuseipdb(ip):
    url = "https://api.abuseipdb.com/api/v2/check"
    headers = {
        'Key': ABUSEIPDB_API_KEY,
        'Accept': 'application/json'
    }
    params = {
        'ipAddress': ip,
        'maxAgeInDays': 90
    }

    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        data = response.json()['data']
        return {
            'abuseConfidenceScore': data.get('abuseConfidenceScore'),
            'domain': data.get('domain'),
            'countryCode': data.get('countryCode'),
            'isp': data.get('isp'),
            'usageType': data.get('usageType')
        }
    else:
        return {"error": "API failure", "status": response.status_code}
