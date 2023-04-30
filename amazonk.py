from amznde import check_availability
from notify import send_notification
import configparser

# Read config file
config = configparser.ConfigParser()
config.read('config.ini')

def main():
    base_url = "https://www.amazon.de/dp/"

    for user in config.sections():
        print(f"Checking products for {user}...")
        user_key = config[user]['user_key']
        service = config[user]['service']
        if service == 'pushover':
            api_key = config[user]['api_key']
            from pushover import init
            init(api_key)

        products = config[user]['products'].replace(' ', '').split(',')
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
