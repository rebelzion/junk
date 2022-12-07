from collections import Counter
from typing import Optional, List
import selenium
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.common.by import By
from selenium import webdriver

class ChatGPTClient:

    URL = "https://chat.openai.com/"
    LOGGED_IN = False

    def __init__(self, email: str, is_production: bool = False):
        options = webdriver.ChromeOptions()
        options.add_argument("--ignore-certificate-errors")
        options.add_argument("--incognito")
        if is_production:
            options.add_argument("--headless")
        self.driver = webdriver.Chrome(options=options)
        self.driver.get(self.URL)

        if not self.LOGGED_IN:
            self.login(email=email)
            self.LOGGED_IN = True
        self.num_responses = 0

    def login(self, email: str):
        elem = self.driver.find_element(By.XPATH, "//*[text()='Log in']")
        elem.click()

        time.sleep(1)

        elem = self.driver.find_element(
            By.XPATH, "/html/body/main/section/div/div/div/form/div[1]/div/div/div/input")
        elem.send_keys(email)

        time.sleep(1)

        elem = self.driver.find_element(By.XPATH, "//*[text()='Continue']")
        elem.click()

        time.sleep(1)

        elem = self.driver.find_element(
            By.XPATH, "/html/body/main/section/div/div/div/form/div[1]/div/div[2]/div/input")
        pw = input("Enter password:")
        elem.send_keys(pw)
        elem.send_keys(Keys.RETURN)

        print(f"Logged In as {email}")

        time.sleep(2)

        elem = self.driver.find_element(
            By.XPATH, "//*[text()='Next']").send_keys(Keys.RETURN)
        elem = self.driver.find_element(
            By.XPATH, "//*[text()='Next']").send_keys(Keys.RETURN)
        elem = self.driver.find_element(
            By.XPATH, "//*[text()='Done']").send_keys(Keys.RETURN)

    def send_message(self, message: str):
        input_box = WebDriverWait(self.driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//textarea")))
        input_box.send_keys(message)
        input_box.send_keys(Keys.RETURN)

    def wait_for_response(self, timeout_nsec=30):
        """
        This function will wait for the latest response of ChatGPT to be created.
        It will wait for at most `timeout_nsec`, after that it will return False.
        If the character length of the last response does not change multiple times,
        then it's assumed that the ChatGPT response was created.
        """
        counter = Counter([])
        nsec = 1
        def wait_and_delay(nsec, fac=1.2):
            nsec *= fac
            time.sleep(nsec)
        start_sec = time.time()
        waiting_for_new_post = True
        while True:
            if time.time() - start_sec > timeout_nsec:
                print(f"No response received within {timeout_nsec} seconds!")
                return False
            responses = self.get_responses()
            if not responses:
                wait_and_delay(nsec)
                continue
            if len(responses) <= self.num_responses and waiting_for_new_post:
                wait_and_delay(nsec)
                continue
            else:
                self.num_responses = len(responses)
                waiting_for_new_post = False
            response_len = len(responses[-1])
            counter.update([response_len])
            mcommon = counter.most_common()
            if mcommon and mcommon[0][1] > 3:
                print(f"ChatGPT finished the response in {(time.time()-start_sec):.3f} seconds!")
                return True
            else:
                wait_and_delay(nsec)


    def get_responses(self, last_n: Optional[int] = None) -> List[str]:
        """
        Returns the list of responses from the chatbot.
        `last_n` is the number of responses to return. If None, then all responses are returned.
        """
        responses = [response.text for response in WebDriverWait(self.driver, 20).until(
            EC.presence_of_all_elements_located((By.TAG_NAME, "p"))) if response.text]
        if last_n is not None:
            responses = responses[-last_n:]
        return responses

