import time

from selenium import webdriver


# setup on linux guide: https://towardsdatascience.com/how-to-setup-selenium-on-a-linux-vm-cd19ee47d922

chromedriver_loc = "/usr/local/bin/chromedriver"
search_term = "playing cards"

driver = webdriver.Chrome(chromedriver_loc)

driver.get(f"https://www.google.com/search?tbm=isch&q={search_term.lower().replace('_', '+')}")

time.sleep(5) # Let the user actually see something!
# search_box = driver.find_element_by_name('q')
# search_box.send_keys('ChromeDriver')
# search_box.submit()
# time.sleep(5) # Let the user actually see something!
driver.quit()

