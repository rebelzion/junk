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

