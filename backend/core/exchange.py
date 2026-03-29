import urllib.request
import json
from typing import Dict

# Rate API Setup for Phase 2
EXCHANGE_RATE_API_KEY = "afd1439ed0cb121fc3b0a24b"
EXCHANGE_RATE_BASE_URL = f"https://v6.exchangerate-api.com/v6/{EXCHANGE_RATE_API_KEY}/latest/"

def get_exchange_rates(base_currency: str = "USD") -> Dict[str, float]:
    """
    Fetches the latest exchange rates for a given base currency.
    Reserved for Phase 2 implementation.
    """
    try:
        url = f"{EXCHANGE_RATE_BASE_URL}{base_currency.upper()}"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode())
            if data and data.get("result") == "success":
                return data.get("conversion_rates", {})
    except Exception as e:
        print(f"Failed to fetch exchange rates: {e}")
    
    # Graceful fallback (hackathon mock data)
    return {
        "USD": 1.0,
        "EUR": 0.92,
        "GBP": 0.79,
        "INR": 83.20
    }
