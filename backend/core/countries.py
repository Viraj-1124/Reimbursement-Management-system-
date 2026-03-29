import json
import urllib.request
import urllib.error

_CACHE = []

def fetch_countries():
    global _CACHE
    if _CACHE:
        return _CACHE
        
    try:
        url = "https://restcountries.com/v3.1/all?fields=name,currencies"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode('utf-8'))
            
        normalized = []
        for item in data:
            name = item.get("name", {}).get("common", "")
            currencies = item.get("currencies", {})
            if name and currencies:
                curr_code = list(currencies.keys())[0]
                curr_info = currencies[curr_code]
                normalized.append({
                    "country": name,
                    "currency_code": curr_code,
                    "currency_name": curr_info.get("name", ""),
                    "currency_symbol": curr_info.get("symbol", curr_code)
                })
        
        # Sort alphabetically
        _CACHE = sorted(normalized, key=lambda x: x["country"])
        return _CACHE
    except Exception as e:
        print(f"Error fetching countries: {e}")
        # Graceful fallback
        return [
            {"country": "United States", "currency_code": "USD", "currency_name": "United States Dollar", "currency_symbol": "$"},
            {"country": "United Kingdom", "currency_code": "GBP", "currency_name": "British Pound", "currency_symbol": "\u00a3"},
            {"country": "India", "currency_code": "INR", "currency_name": "Indian Rupee", "currency_symbol": "\u20b9"},
            {"country": "Eurozone", "currency_code": "EUR", "currency_name": "Euro", "currency_symbol": "\u20ac"}
        ]

def get_currency_for_country(country_name: str) -> str:
    if not country_name:
        return "USD"
        
    countries = fetch_countries()
    for c in countries:
        if c["country"].casefold() == country_name.casefold():
            return c["currency_code"]
    return "USD"
