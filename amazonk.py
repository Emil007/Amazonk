import requests
from bs4 import BeautifulSoup
from pushover import init, Client
from pushbullet import Pushbullet
import configparser
import random

# Read config file
config = configparser.ConfigParser()
config.read('config.ini')

def check_availability(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:15.0) Gecko/20100101 Firefox/15.0.1",
        "Accept-Language": "en-US,en;q=0.5",
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")

    # Check for "out of stock" text in the page source
    out_of_stock = soup.find("div", {"id": "availability"})
    try:
        return "nicht verfügbar" not in out_of_stock.text.strip().lower()
    except AttributeError:
        return False

previous_choice = None

def send_notification(product_name, url, user_key, service):
    global previous_choice

    if service == 'pushover':
        client = Client(user_key)
    elif service == 'pushbullet':
        pb = Pushbullet(user_key)

    gates = ['1', '2', '3']
    envelopes = ['grünen', 'blauen', 'gelben', 'roten', 'ZONK!!!!!!!!!!!!']

    while True:
        if random.choice([True, False]):
            message = f"{product_name} versteckt sich hinter Tor {random.choice(gates)}"
        else:
            chosen_envelope = random.choices(envelopes, weights=[1, 1, 1, 0.9, 0.1], k=1)[0]
            if chosen_envelope == 'ZONK!!!!!!!!!!!!':
                message = f"{product_name} ist {chosen_envelope}"
            else:
                message = f"{product_name} steckt im {chosen_envelope} Umschlag"

        # Check if the message is different from the previous one
        if message != previous_choice:
            previous_choice = message
            break

    print(f"Sending notification: {message}: {url}")
    if service == 'pushover':
        client.send_message(f"{message}: {url}", title="AMAZONK!", html=True, sound="cashregister")
    elif service == 'pushbullet':
        pb.push_link(product_name, url, body=message)

def main():
    base_url = "https://www.amazon.de/dp/"

    for user in config.sections():
        print(f"Checking products for {user}...")
        user_key = config[user]['user_key']
        service = config[user]['service']
        if service == 'pushover':
            api_key = config[user]['api_key']
            init(api_key)

        products = config[user]['products'].split(', ')
        product_dict = {name: base_url + asin for name, asin in [prod.split(';') for prod in products]}

        for name, url in product_dict.items():
            print(f"Checking availability for {name} at {url}...")
            if check_availability(url):
                print(f"{name} is available for pre-order!")
                send_notification(name, url, user_key, service)
            else:
                print(f"{name} is not available for pre-order.")

if __name__ == "__main__":
    main()
