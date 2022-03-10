from selenium import webdriver
from time import sleep, time
from datetime import datetime
from selenium.webdriver.common.action_chains import ActionChains


def submit_solution(prize_nrs):
	# Submitting info
	solution = "".join([str(i) for i in prize_nrs])
	surname = "Oliver"
	lastname = "Lehmann"
	address = "Querstrasse 6"
	plz = "8050"
	city = "Zurich"
	email = "lehmannoliver96@gmail.com"


	DRIVER_PATH = '/Users/Oli/Documents/Webdriver/chromedriver'
	driver = webdriver.Chrome(executable_path=DRIVER_PATH)
	driver.maximize_window()
	driver.get('https://www.coopzeitung.ch/raetsel/')
	sleep(5)

	try:
		links = driver.find_element_by_xpath("//div[@class='item-list']").find_elements_by_tag_name("a")
		for link in links:
			if "sudoku" in link.get_attribute('href'):
				link.click()
				break
		sleep(5)
	except Exception as e:
		print(e)
		driver.close()

	try:
		# Fill out submit form
		driver.find_element_by_xpath("//input[@id='loesung-sudoku']").send_keys(solution)
		gender_button = driver.find_element_by_xpath("//input[@id='anrede-0']")
		ActionChains(driver).move_to_element(gender_button).click(gender_button).perform()
		driver.find_element_by_xpath("//input[@id='loesung-sudoku']").send_keys(solution)
		driver.find_element_by_xpath("//input[@id='vorname']").send_keys(surname)
		driver.find_element_by_xpath("//input[@id='nachname']").send_keys(lastname)
		driver.find_element_by_xpath("//input[@id='adresse']").send_keys(address)
		driver.find_element_by_xpath("//input[@id='plz']").send_keys(plz)
		driver.find_element_by_xpath("//input[@id='ort']").send_keys(city)
		driver.find_element_by_xpath("//input[@id='email']").send_keys(email)
		box_privacy = driver.find_element_by_xpath("//input[@id='checkPrivacy']")
		ActionChains(driver).move_to_element(box_privacy).click(box_privacy).perform()
		submit_button = driver.find_element_by_xpath("//button[@id='btnSubmit']")
		#ActionChains(driver).move_to_element(submit_button).click(submit_button).perform()
		#driver.close()
		#return True

	except Exception as e:
		print(e)

	sleep(5)
	#driver.close()

# Submit solution manually 
submit_solution([1,2,3])