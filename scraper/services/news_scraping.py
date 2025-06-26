from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait


class NewsScraping:
    @staticmethod
    def search_button(driver, name, rule):
        try:
            search_bar = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, rule.search_bar))
            )
            search_bar.clear()
            search_bar.send_keys(name)
            search_bar.send_keys(Keys.RETURN)
        except Exception as e:
            print(f"Error:{e}")

    @staticmethod
    def news_block(driver, rule):
        try:
            news_button = driver.find_element(By.XPATH, rule.news)
            driver.execute_script("arguments[0].click();", news_button)
        except Exception as e:
            print(f"No news tab:{e}")

    @staticmethod
    def dropdown_control(driver):
        try:
            dropdown_element = driver.find_element(
                By.XPATH,
                '//select[contains(@name, "length") or contains(@name, "Limit")]',
            )
            dropdown = Select(dropdown_element)
            value_to_select = "50"

            if value_to_select is not None:
                dropdown.select_by_value(str(value_to_select))
            else:
                print("Dropdown value is None")
        except Exception as e:
            print(f"Error in dropdown control: {e}")
