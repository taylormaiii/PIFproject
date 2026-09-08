from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.webdriver.common.actions.wheel_input import ScrollOrigin


pokemonlist = ["Sliggo","Bulbasaur", "Zoroark", "Pikachu", "Necrozma"]
driver = webdriver.Firefox()
driver.get("https://fusion.nuzlocke.io/")
original_handle = driver.current_window_handle


driver.switch_to.new_window('tab')
driver.get("https://fusioncalc.com/fun/fusion-box")
driver.implicitly_wait(0.5)

elem = driver.find_element(By.CLASS_NAME, "flex")
elem.click()
for pokemon in pokemonlist:
    
    element = driver.find_element(By.CLASS_NAME, "space-y-2")
    elements = driver.find_element(By.TAG_NAME, "input")
    elements.send_keys(f"{pokemon}")
    selection = driver.find_element(By.CLASS_NAME, "max-h-64")
    selection.click()
    elements.clear()

bodymap = driver.find_element(By.XPATH, "/html/body/div[2]/main/div")
sprites = driver.find_element(By.XPATH, "/html/body/div[2]/main/div/div[5]/div")
bodymap.click()
scroll_origin = ScrollOrigin.from_element(bodymap)
ActionChains(driver)\
    .scroll_from_origin(scroll_origin, 0, 800)\
    .perform()
includeevos = driver.find_element(By.ID, "pf-auto-add-evos")
includeevos.click()