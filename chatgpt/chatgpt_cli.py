from chatgpt_api import ChatGPTClient
from colorama import Fore
import time

email = input("Enter email:")
chatgpt_client = ChatGPTClient(is_production=False, email=email)

def waiting(nsec: int = 2):
    print(f"{Fore.WHITE}Processing ...")
    time.sleep(nsec)


num_previous_responses = 0 # used to know when a new response was added by chatGPT
while True:

    inp = input(f"{Fore.WHITE}Ask ChatGPT (or type 'quit'):")
    if inp == 'quit':
        break

    chatgpt_client.send_message(inp)
    print(f"{Fore.YELLOW}[You]: " + inp)

    while True:
        responses = chatgpt_client.get_responses()
        if responses and len(responses) > num_previous_responses:
            num_previous_responses = len(responses)
            time.sleep(4)
            break
        else:
            time.sleep(1)

    #waiting(nsec=2)

    response = chatgpt_client.get_responses()[-1]
    print(f"{Fore.GREEN}[GPT]: " + response)


