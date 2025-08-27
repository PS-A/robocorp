# Imports.
import requests
import time
from robocorp import workitems, vault
from robocorp.tasks import task
from datetime import datetime, timedelta

# Secrets.
credentials = vault.get_secret("NEWS_API")
API_KEY = credentials["KEY"]

# Global parameters.
NEWS_KEYWORD = "Porsche"
FROM_DATE = datetime.now() - timedelta(days=1)
SORT_BY = "popularity"
ALLOWED_SORT = {"relevancy", "popularity", "publishedAt"}

# Task and functions.
@task
def produce_news_data():
    """Gets news data from which it will generate work items."""
    define_query_parameters()

    sort = SORT_BY if SORT_BY in ALLOWED_SORT else "popularity"
    endpoint = "https://newsapi.org/v2/everything"
    params = {
        "q": NEWS_KEYWORD.strip(),
        "from": FROM_DATE.strftime("%Y-%m-%d"),
        "sortBy": sort,
        "apiKey": API_KEY,
        "pageSize": 100,  # cap payload
        "page": 1,
        "language": "en",  # optional
    }
    
    data = query_api(endpoint, params)
    payload = create_work_item_payload(data)
    save_work_item_payload(payload)

def define_query_parameters():
    """Override globals from Control Room input payload when available."""
    global NEWS_KEYWORD, FROM_DATE, SORT_BY
    wi = getattr(workitems.inputs, "current", None)
    p = wi.payload if wi else None
    if not isinstance(p, dict) or not p:
        return # Keep defaults.

    NEWS_KEYWORD = p.get("NEWS_KEYWORD") or NEWS_KEYWORD
    SORT_BY = p.get("SORT_BY") or SORT_BY
    fd = p.get("FROM_DATE")
    if fd:
        if fd.upper() in ("NOW", "TODAY"):
            FROM_DATE = datetime.now()
        elif fd.upper() in ("YESTERDAY", "DAILY"):
            FROM_DATE = datetime.now() - timedelta(days=1)
        elif fd.upper() == "WEEKLY":
            FROM_DATE = datetime.now() - timedelta(days=7)
        elif fd.upper() == "MONTHLY":
            FROM_DATE = datetime.now() - timedelta(days=30)
        else:
            try:
                FROM_DATE = datetime.strptime(fd, "%Y-%m-%d")
            except ValueError:
                pass

def query_api(url, params):
    """Queries News API."""
    for attempt in range (3):
        try:
            response = requests.get(url, params=params, timeout=15)
            if response.status_code == 200:
                data = response.json()
                if data.get("status") == "ok":
                    print("API response OK.")
                    return data
                print(f"API logical error: {data.get('code')}: {data.get('message')}")
            else:
                print(f"HTTP {response.status_code}: {response.text[:200]}")
        except requests.RequestException as e:
            print(f"Request error: {e}")
        time.sleep(10 + attempt)
    raise SystemError("API response failed 3 times in a row, failed run.")
        
def create_work_item_payload(data):
        return {
            "keyword": NEWS_KEYWORD,
            "from_date": FROM_DATE.strftime("%Y-%m-%d"),
            "sort_by": SORT_BY,
            "fetched_time": datetime.now().isoformat(),
            "total_results": data.get("totalResults"),
            "articles": data.get("articles"),
        }

def save_work_item_payload(payload):
    wi = workitems.outputs.create(payload)
    wi.save()