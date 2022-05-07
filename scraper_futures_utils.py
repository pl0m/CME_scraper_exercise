from datetime import datetime
import time
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
import undetected_chromedriver as uc


class Utils:
    def __init__(self):
        uc.TARGET_VERSION = 101
        self.driver = uc.Chrome(version_main=101)

        print("Initialized Utils")
    
    def navigate(self, url):
        self.driver.get(url)

    def find_elements(self, selector):
        return self.driver.find_elements(By.CSS_SELECTOR, selector)

    def find_element(self, selector):
        return self.driver.find_element(By.CSS_SELECTOR, selector)

    def move_to_element(self, element):
        ActionChains(self.driver).move_to_element(element).perform()

    def click_load_all(self):
        # Find the load all button on the page
        button = self.find_element('.load-all')
        
        # Scroll to the button so we can click it
        self.move_to_element(button)

        time.sleep(1)
        button.click()

        print("Clicked the load all button")
        
    def click_deny_cookies(self):
        self.find_element('#onetrust-reject-all-handler').click()

        print("Clicked the deny cookies button")

    def save_to_storage(self, name, contents):
        directory = 'storage'
        filename = 'futures-' + name + '-' + datetime.now().strftime('%Y-%m-%d_%H-%M-%S') + '.csv'
        
        # Appends the table csv to the file and creates new file if it doesn't exist
        with open(directory + '/' + filename, 'a+') as file:
            file.write(contents)