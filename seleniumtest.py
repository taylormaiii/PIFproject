from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Firefox()
driver.get("https://fusioncalc.com/fun/fusion-box")
driver.implicitly_wait(0.5)
elem = driver.find_element(By.CLASS_NAME, "flex")
elem.click()
element = driver.find_element(By.CLASS_NAME, "space-y-2")
elements = driver.find_element(By.TAG_NAME, "input")


elements.send_keys("Sliggoo")
selection = driver.find_element(By.CLASS_NAME, "max-h-64")
selection.click()
elements.clear()
#driver.quit()

