import requests
from bs4 import BeautifulSoup


def check_availability(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:15.0) Gecko/20100101 Firefox/15.0.1",
        "Accept-Language": "en-US,en;q=0.5",
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")
    out_of_stock = soup.find("div", {"id": "availability"})
    try:
        return "nicht verfügbar" not in out_of_stock.text.strip().lower()
    except AttributeError:
        return False
