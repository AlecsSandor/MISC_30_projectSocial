from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Configure Chrome options to connect to the existing browser session
chrome_options = Options()
chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")

# Provide the path to your ChromeDriver
#chrome_driver_path = "/path/to/chromedriver"  # Adjust the path to your chromedriver

# Create a WebDriver instance and connect to the running Chrome session
driver = webdriver.Chrome(options=chrome_options)
wait = WebDriverWait(driver, 30)

# comment_box = wait.until(EC.presence_of_element_located((By.XPATH, "//textarea[@aria-label='Add a comment…']"))) #self.driver.find_element(By.CSS_SELECTOR, "textarea[aria-label='Add a comment…']")
# comment_box.send_keys('Really cool!')
# post_button = driver.find_element(By.XPATH, "//*[text()='Post']")
# post_button.click()

# followers_number_str = driver.find_elements(By.CSS_SELECTOR, "span.x5n08af.x1s688f")
# followers_number_float = int(followers_number_str[1].get_attribute('title').replace(',', ''))
# print(f"Numbers of followers {followers_number_float}.") 

# comment_box = wait.until(EC.presence_of_element_located((By.XPATH, "//textarea[@aria-label='Add a comment…']"))) #self.driver.find_element(By.CSS_SELECTOR, "textarea[aria-label='Add a comment…']")
# comment_box.send_keys('Really cool!')
# comment_box.send_keys('Really cool!')
# post_button = driver.find_element(By.XPATH, "//*[text()='Post']")
# post_button.click()
# Find and click the first post

first_post = wait.until(EC.presence_of_element_located((By.CLASS_NAME, '_ac7v')))
first_post.click()
print("Selected first post.")
time.sleep(1)  # Wait for the post to load

comment_box = None
for attempt in range(3):  # Try up to 3 times
    try:
        comment_box = wait.until(EC.visibility_of_element_located((By.XPATH, "//textarea[@aria-label='Add a comment…']")))
        #comment_box = wait.until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[8]/div[1]/div/div[3]/div/div/div/div/div[2]/div/article/div/div[2]/div/div/div[2]/section[3]/div/form/div/textarea")))
        comment_box.send_keys('Really cool!')
        post_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[text()='Post']")))
        post_button.click()
        break  # Exit loop if successful
    except Exception as e:
        print(f"Attempt {attempt+1}: Stale element. Retrying...")
        time.sleep(2)  # Wait before retrying