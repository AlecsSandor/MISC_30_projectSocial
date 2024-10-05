
# Structure

## Divide the process into different functions

### Def for Logging in
### Def for inintiating a search using a hastag

### While noPosts > 0:
#### Def for iterating through posts and opening them one by one in a new tab 
#### Def for iterating through the comment section and save user accounts (only save accounts which have between 100 and 2000 followers)

# Save accounts to database, around 300 and then start:
# At randomn intervals between 4 min - 35 min:
## Def for opening account page
### Def for following
### Def for liking last 10-15 posts
### Def for leaving 2 comments

# Structure:
## Create building blocks to represent each action and use them to create a flow
## Building Blocks:

### On Feed:
#----> Go to an account - Done
#----> Go to search |zzz

### On Account
#----> Follow/Request/Unfollow - Done
#----> Get No of followers - Done
#----> Open first post - Done

### On a Post
#----> Like Post - Done
#----> Leave Comment - Done
#----> Next Post - Done
#----> Previous Post - Done
#----> Get all accounts which left a comment - Done

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from random import randint

from terminalInterface import Dashboard

class InstagramBot:

    likes = 0
    comments = 0
    follows = 0
    logs = []

    def __init__(self):
        # Initialize the WebDriver (Chrome) once for the entire class
        # self.driver = webdriver.Chrome()
        # self.driver.get('https://www.instagram.com/')
        # time.sleep(3)  # Wait for Instagram's landing page to load
        chrome_options = Options()
        chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
        self.driver = webdriver.Chrome(options=chrome_options)
        self.wait = WebDriverWait(self.driver, 30)
        self.leads = [""]

    # Use on the login page ------------------------
    def login(self, username, password):
        # Navigate to login page
        self.driver.get('https://www.instagram.com/accounts/login/')
        time.sleep(3)  # Wait for the login page to load

        # Find the username and password input fields
        username_input = self.driver.find_element(By.NAME, 'username')
        password_input = self.driver.find_element(By.NAME, 'password')

        # Enter the credentials
        username_input.send_keys(username)
        password_input.send_keys(password)

        # Press Enter to submit the login form
        password_input.send_keys(Keys.ENTER)

        # Wait for the main page to load after login
        time.sleep(5)  # Adjust this time as necessary

        # Verify login by checking for the presence of the home icon
        try:
            self.driver.find_element(By.CSS_SELECTOR, 'svg[aria-label="Home"]')
            print("Login successful!")
        except Exception as e:
            print("Login failed. Please check your credentials.")
            return False
        return True
    # ----------------------------------------------------

    # Use after you are logged in ------------------------
    def navigate_to_profile(self, profile_name):
        # Navigate to a user's profile
        profile_url = f'https://www.instagram.com/{profile_name}/'
        self.driver.get(profile_url)
        time.sleep(3)  # Wait for the profile page to load
        self.logs.append(f"Navigated to {profile_name}'s profile.")
        print(f"Navigated to {profile_name}'s profile.")
    # ----------------------------------------------------

    # Use on an account page -------------------
    def follow(self):
        try:
            follow_button = self.driver.find_element(By.CSS_SELECTOR, "button._acan._acap._acas._aj1-._ap30[type='button']")
            follow_button.click()
            self.follows += 1
            self.logs.append("Followed account.")
            print("Followed account.")
            return True
        except Exception as e:
            self.logs.append("!!! Non Critical Error occured while trying to follow - Continuing !!!")
            print("!!! Non Critical Error occured while trying to follow - Continuing !!!")
            return False

    def get_followers_numbers(self):
        try:
            followers_number_str = self.driver.find_elements(By.CSS_SELECTOR, "span.x5n08af.x1s688f") #self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "span.x5n08af.x1s688f")))
            followers_number_float = int(followers_number_str[1].get_attribute('title').replace(',', ''))
            self.logs.append(f"Numbers of followers {followers_number_float}.")
            print(f"Numbers of followers {followers_number_float}.")
            return (followers_number_float)
        except Exception as e:
            self.logs.append("!!! Non Critical Error occured while trying to get the amount of followers - Continuing !!!")
            print("!!! Non Critical Error occured while trying to get the amount of followers - Continuing !!!")
        return 0
    
    def select_first_post(self):
        try:
            # Find and click the first post
            first_post = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, '_ac7v')))
            #first_post = self.driver.find_element(By.XPATH, '//article//a')
            first_post.click()
            self.logs.append("Selected first post.")
            print("Selected first post.")
            time.sleep(2)  # Wait for the post to load
        except Exception as e:
            self.logs.append("!!! Non Critical Error occured while trying to select first post - Continuing !!!")
            print("!!! Non Critical Error occured while trying to select first post - Continuing !!!")

    def check_if_account_is_private(self):
        lock_svg = self.driver.find_elements(By.CSS_SELECTOR, 'span.x1lliihq.x1plvlek.xryxfnj.x1n2onr6.x193iq5w.xeuugli.x1fj9vlw.x13faqbe.x1vvkbs.x1s928wv.xhkezso.x1gmr53x.x1cpjm7i.x1fgarty.x1943h6x.x1i0vuye.xvs91rp.x1s688f.x5n08af.x1tu3fi.x3x7a5m.x10wh9bi.x1wdrske.x8viiok.x18hxmgj')
        if len(lock_svg) == 12:
            self.logs.append("Account is Private.")
            print("Account is Private.")
            return True
        self.logs.append("Account is public.")
        print("Account is public.")
        return False
    # ----------------------------------------------------

    # Use when there is an open post on an account' feed ------------------------   
    def like_post(self, profile_name):
        # Find the Like button and click it
        try:
            like_svg = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'svg[aria-label="Like"]'))) #self.driver.find_element(By.CSS_SELECTOR, 'svg[aria-label="Like"]')
            like_parent = like_svg.find_element(By.XPATH, "..")
            like_button = like_parent.find_element(By.XPATH, "..")
            like_button.click()
            time.sleep(1)
            like_button.click()
            self.likes += 1
            self.logs.append(f"Liked {profile_name}'s post.")
            print(f"Liked {profile_name}'s post.")
        except Exception as e:
            self.logs.append("!!! Non Critical Error occured while trying to like a post - Continuing !!!")
            print("!!! Non Critical Error occured while trying to like a post - Continuing !!!")

    def comment_on_post(self, profile_name):
        comments_list = ["Really cool! 🤙🤙", "Awesome!", "Love it! 🤙", "Niceee 😁", "Great!", "Cool, Cool.😁👍"]
        comment_box = None
        for attempt in range(3):  # Try up to 3 times
            try:
                comment_box = self.wait.until(EC.visibility_of_element_located((By.XPATH, "//textarea[@aria-label='Add a comment…']")))
                #comment_box = self.wait.until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[8]/div[1]/div/div[3]/div/div/div/div/div[2]/div/article/div/div[2]/div/div/div[2]/section[3]/div/form/div/textarea")))
                comment_box.send_keys(comments_list[randint(0, 5)])
                post_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//*[text()='Post']")))
                post_button.click()
                self.logs.append(f"Commented on {profile_name}'s post.")
                print(f"Commented on {profile_name}'s post.")
                self.comments += 1
                break  # Exit loop if successful
            except Exception as e:
                self.logs.append("!!! Non Critical Error occured while trying to leave a comment - Continuing  !!!")
                print("!!! Non Critical Error occured while trying to leave a comment - Continuing  !!!")
                self.logs.append(f"Attempt {attempt+1}: Stale element. Retrying...")
                print(f"Attempt {attempt+1}: Stale element. Retrying...")
                time.sleep(2)  # Wait before retrying

    def navigate_to_next_post(self):
        try:
            elements = self.driver.find_elements(By.CLASS_NAME, "_abl-")
            elements[1].click()
            self.logs.append("Navigated to next post.")
            print("Navigated to next post.")
        except Exception as e:
            self.logs.append("!!! Non Critical Error occured while trying to navigate to the next post - Continuing  !!!")
            print("!!! Non Critical Error occured while trying to navigate to the next post - Continuing  !!!")

    def navigate_to_previous_post(self):
        elements = self.driver.find_elements(By.CLASS_NAME, "_abl-")
        elements[0].click()
        self.logs.append("Navigated to the previous post.")
        print("Navigated to the previous post.")

    def get_all_comments_accounts(self):
        #stories = driver.find_elements(By.CSS_SELECTOR, "div._aarf._a9zp[role='button']")
        comments_accounts_parent = self.driver.find_elements(By.CLASS_NAME, "_a9zc")
        self.leads = []
        for account in comments_accounts_parent:
            self.leads.append(account.find_element(By.CSS_SELECTOR, "a").get_attribute("href"))
        self.logs.append(f"Got all {len(self.leads)} commets accounts")
        print(f"Got all {len(self.leads)} commets accounts")
    # -----------------------------------------------------------------------------

    def itemClick(self, n):
        self.leads[n].click()
        print("Clicked on item.")

    def openNewTab(self):
        self.driver.execute_script("window.open('');")
        self.logs.append("Opened Tab.")
        print("Opened Tab.")

    def swtichTab(self, tab):
        self.driver.switch_to.window(self.driver.window_handles[tab])
        self.logs.append("Switched Tab.")
        print("Switched Tab.")

    def closeCurrentTab(self):
        self.driver.close()
        self.logs.append("Closed Tab.")
        print("Closed Tab.")

    def goBack(self):
        self.driver.back()
        print("Went Back.")

    def navigateToLink(self, link):
        self.driver.get(link)
        print("Opened new link.")

    def close_browser(self):
        # Close the browser
        self.driver.quit()
        print("Browser closed.")

def updateDash(likes, comments, follows):
    new_stats = {
        "Likes": likes,
        "Comments": comments,
        "Follows": follows
    }
    return new_stats

if __name__ == '__main__':

    # Create an instance of the InstagramBot class
    bot = InstagramBot()
    dashboard = Dashboard()
    # Display the dashboard
    dashboard.display()

    def refreshDash():
        dashboard.update_stats(updateDash(likes=bot.likes, comments=bot.comments, follows=bot.follows))
        dashboard.update_logs(new_logs=bot.logs)
        dashboard.display()

    accounts_array = ["nuts.trip", "lawrencewalton_", "the_travel_kate", "jaxon_roberts", "ladyship.mahsssaaa", "marieliroy", "paresseuxcurieux", "aimietravel", "burns_ru"
                      ]

    for account in accounts_array:
        bot.navigate_to_profile(profile_name = account)
        time.sleep(1)
        bot.select_first_post()
        time.sleep(randint(1, 5))
        
        # Set number of posts to iterate over for every account in accounts, to get the users from comments
        for i in range(30):
            bot.get_all_comments_accounts()
            refreshDash()

            if len(bot.leads) > 1:
                for j in range(1, len(bot.leads)):
                    bot.openNewTab()
                    refreshDash()

                    bot.swtichTab(tab=-1)
                    refreshDash()
                    time.sleep(randint(1, 5))

                    bot.navigateToLink(link = bot.leads[j])
                    refreshDash()
                    time.sleep(randint(1, 5))

                    followers = bot.get_followers_numbers()
                    refreshDash()
                    if followers > 50 and followers < 2000:
                        if bot.follow():
                            refreshDash()
                            time.sleep(randint(1, 5))

                            if not bot.check_if_account_is_private():
                                refreshDash()
                                bot.select_first_post()
                                refreshDash()

                                # Set number of posts to iterate over for every public followed account
                                for n in range(1, 5):
                                    time.sleep(randint(5, 10))
                                    if randint(1, 10) > 6:
                                        bot.comment_on_post(profile_name = account)
                                        refreshDash()
                                        time.sleep(randint(2, 10))

                                    bot.like_post(profile_name = account)
                                    refreshDash()
                                    time.sleep(randint(1, 5))

                                    bot.navigate_to_next_post()
                                    refreshDash()
                                
                    time.sleep(randint(1, 5))
                    bot.closeCurrentTab()
                    bot.swtichTab(tab=0)
                    refreshDash()

            time.sleep(randint(1, 5))
            bot.navigate_to_next_post()
            refreshDash()
            time.sleep(5)

        bot.logs.append(f"Done with {account}'s account, waiting for 30 minn...")
        refreshDash()
        time.sleep(randint(1000, 1400))
    
                