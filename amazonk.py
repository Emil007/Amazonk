import requests
from bs4 import BeautifulSoup
from pushover import init, Client
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

    out_of_stock = soup.find(id="outOfStock")
    return out_of_stock is None

previous_choice = None

def send_notification(product_name, url, user_key):
    global previous_choice
    client = Client(user_key)

    gates = ['1', '2', '3']
    envelopes = ['grünen', 'blauen', 'gelben', 'roten', 'ZONK!!!!!!!!!!!!']

    while True:
        if random.choice([True, False]):
            message = f"{product_name} versteckt sich hinter Tor {random.choice(gates)}"
        else:
            chosen_envelope = random.choices(envelopes, weights=[1, 1, 1, 1, 0.1], k=1)[0]
            if chosen_envelope == 'ZONK!!!!!!!!!!!!':
                message = f"{product_name} ist {chosen_envelope}"
            else:
                message = f"{product_name} ist im {chosen_envelope} Umschlag"
        
        # Check if the message is different from the previous one
        if message != previous_choice:
            previous_choice = message
            break

    print(f"Sending notification: {message}: {url}")
    client.send_message(f"{message}: {url}", title="AMAZONK!")

def main():
    base_url = "https://www.amazon.de/dp/"

    for user in config.sections():
        print(f"Checking products for {user}...")
        api_key = config[user]['api_key']
        user_key = config[user]['user_key']
        init(api_key)

        products = config[user]['products'].split(', ')
        product_dict = {name: base_url + asin for name, asin in [prod.split(';') for prod in products]}

        for name, url in product_dict.items():
            print(f"Checking availability for {name} at {url}...")
            if check_availability(url):
                print(f"{name} is available for pre-order!")
                send_notification(name, url, user_key)
            else:
                print(f"{name} is not available for pre-order.")

if __name__ == "__main__":
    main()
