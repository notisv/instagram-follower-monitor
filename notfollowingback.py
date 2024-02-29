from selenium import webdriver
from time import sleep
from credentials import username, password
from webdriver_manager.chrome import ChromeDriverManager

sleep_duration = 5 # seconds

driver = webdriver.Chrome(ChromeDriverManager().install()) # use google chrome
driver.get("https://instagram.com")
sleep(sleep_duration)

def login():
    # accept cookies
    cookie_accept_button = driver.find_element_by_xpath("/html/body/div[4]/div/div/button[1]")
    cookie_accept_button.click()
    sleep(sleep_duration)

    # instagram login
    username_field = driver.find_element_by_xpath("/html/body/div[1]/section/main/article/div[2]/div[1]/div/form/div/div[1]/div/label/input")
    username_field.send_keys(username)
    password_field = driver.find_element_by_xpath("/html/body/div[1]/section/main/article/div[2]/div[1]/div/form/div/div[2]/div/label/input")
    password_field.send_keys(password)
    sleep(sleep_duration)
    login_button = driver.find_element_by_xpath('/html/body/div[1]/section/main/article/div[2]/div[1]/div/form/div/div[3]/button')
    login_button.click()
    sleep(sleep_duration)

def getNotFollowingBack():
    # change to your username, it must be public
    driver.get("https://www.instagram.com/iam.notis/")
    sleep(sleep_duration)

    following_button = driver.find_element_by_xpath("//a[contains(@href,'/following')]")
    following_button.click()
    following_list = getFollowing()
    sleep(sleep_duration)

    followers_button = driver.find_element_by_xpath("//a[contains(@href,'/followers')]")
    followers_button.click()
    followers_list = getFollowers()
    sleep(sleep_duration)

    not_following_back = [user for user in following_list if user not in followers_list]

    printNotFollowingBack(not_following_back)

def getFollowing():
    sleep(sleep_duration)
    scroll_box = driver.find_element_by_xpath("/html/body/div[6]/div/div/div[3]")
    prev_height, height = 0, 1

    while prev_height != height:
        prev_height = height
        sleep(sleep_duration)
        height = driver.execute_script("""
                arguments[0].scrollTo(0, arguments[0].scrollHeight); 
                return arguments[0].scrollHeight;
                """, scroll_box)
        
    links = scroll_box.find_elements_by_tag_name('a')
    following = [name.text for name in links if name.text != '']
    close_button = driver.find_element_by_xpath("/html/body/div[6]/div/div/div[1]/div/div[2]/button")
    close_button.click()
    print('Successfully fetched following list.')
    return following

def getFollowers():
    sleep(sleep_duration)
    scroll_box = driver.find_element_by_xpath("/html/body/div[6]/div/div/div[2]")
    prev_height, height = 0, 1

    while prev_height != height:
        prev_height = height
        sleep(sleep_duration)
        height = driver.execute_script("""
                arguments[0].scrollTo(0, arguments[0].scrollHeight); 
                return arguments[0].scrollHeight;
                """, scroll_box)
        
    links = scroll_box.find_elements_by_tag_name('a')
    followers = [name.text for name in links if name.text != '']
    close_button = driver.find_element_by_xpath("/html/body/div[6]/div/div/div[1]/div/div[2]/button")
    close_button.click()
    print('Successfully fetched followers list.')
    return followers

def printNotFollowingBack(not_following_back):
    txtfile = open('not_following_back.txt', 'w')
    print('The following users are not following you back:')
    for user in not_following_back:
        print('https://www.instagram.com/' + user)
        txtfile.write('https://www.instagram.com/' + user + '\n')
    txtfile.close()
    print('Created a .txt file listing users that are not following you back.')

login()
getNotFollowingBack()
driver.close()