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

    response = chatgpt_client.wait_for_response()
    print(f"{Fore.GREEN}[GPT]: " + response)


