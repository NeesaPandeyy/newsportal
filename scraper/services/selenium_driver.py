from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager


class SeleniumDriver:
    @staticmethod
    def start_selenium(url):
        options = webdriver.ChromeOptions()
        options.add_argument("--headless=new")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--disable-dev-shm-usage")
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        driver.get(url)
        return driver

    @staticmethod
    def handle_alert(driver):
        try:
            WebDriverWait(driver, 2).until(EC.alert_is_present())
            alert = driver.switch_to.alert
            alert.accept()
        except Exception:
            pass

        close_xpaths = [
            '//button[@type="button" and @class="close" and @aria-label="Close"]',
            '//*[@id="roadblock-ad"]/div/div/i',
            '//*[@id="ratopati-app"]/div[1]/section/div/div[2]/button',
            '//*[@id="onesignal-slidedown-cancel-button"]',
        ]
        for xpath in close_xpaths:
            try:
                close_button = WebDriverWait(driver, 1).until(
                    EC.element_to_be_clickable((By.XPATH, xpath))
                )
                close_button.click()
                break
            except (NoSuchElementException, TimeoutException):
                continue
