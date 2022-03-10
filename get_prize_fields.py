from selenium import webdriver
from time import sleep, time
from datetime import datetime

def expand_shadow_element(element):
	shadow_root = driver.execute_script('return arguments[0].shadowRoot', element)
  	return shadow_root

DRIVER_PATH = '/Users/Oli/Documents/Webdriver/chromedriver'
driver = webdriver.Chrome(executable_path=DRIVER_PATH)
driver.maximize_window()
driver.get('https://www.coopzeitung.ch/raetsel/')
driver.implicitly_wait(10)

try:
	links = driver.find_element_by_xpath("//div[@class='item-list']").find_elements_by_tag_name("a")
	for link in links:
		if "sudoku" in link.get_attribute('href'):
			link.click()
			break
	sleep(3)
except Exception as e:
	print(e)
	driver.close()

try:	
	main = driver.find_element_by_tag_name("main")
	content_block = main.find_element_by_xpath("//div[@class='content-block']")
	iframes = content_block.find_elements_by_tag_name("iframe")
	for i, iframe in enumerate(iframes):
		src = iframe.get_attribute("src")
		if src[8:22] == "static-raetsel":
			driver.get(src)
			sleep(5)
			sudoku_raetsel = driver.find_element_by_tag_name('raetsel-sudoku')
			shadow_root = expand_shadow_element(sudoku_raetsel)
			game_field = shadow_root.find_element_by_css_selector("#gameField")
			prize_fields = []
			for nr, field in enumerate(game_field.find_elements_by_class_name("fieldFrame")):
				if "prizeField" in field.get_attribute("class"):
					prize_fields.append(nr)
	print(prize_fields)
except Exception as e:
	print(e)

#sleep(5)
driver.close()