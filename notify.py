import random
from pushover import init, Client
from pushbullet import Pushbullet


def send_notification(product_name, url, user_key, service):
    previous_choice = None

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
