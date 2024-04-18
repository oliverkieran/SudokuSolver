from selenium import webdriver
from time import sleep
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.select import Select


def submit_solution(prize_nrs):
	# Submitting info
	solution = "".join([str(i) for i in prize_nrs])
	surname = "Oliver"
	lastname = "Lehmann"
	address = "Querstrasse"
	address_nr = "6"
	plz = "8050"
	city = "Zurich"
	email = "lehmannoliver96@gmail.com"


	DRIVER_PATH = '/Users/Oli/Documents/Webdriver/chromedriver_mac64_m1'
	driver = webdriver.Chrome(executable_path=DRIVER_PATH)
	driver.maximize_window()
	driver.get('https://www.migros.ch/de/unternehmen/medien/publikationen/magazin/sudoku.html')
	sleep(5)

	try:
		# Fill out submit form
		driver.find_element_by_xpath("//input[@id='ref-solution']").send_keys(solution)
		Select(driver.find_element_by_xpath("//select[@id='ref-salutation']")).select_by_value("m")
		driver.find_element_by_xpath("//input[@id='ref-firstName']").send_keys(surname)
		driver.find_element_by_xpath("//input[@id='ref-lastName']").send_keys(lastname)
		driver.find_element_by_xpath("//input[@id='ref-email']").send_keys(email)
		driver.find_element_by_xpath("//input[@id='ref-plz']").send_keys(plz)
		driver.find_element_by_xpath("//input[@id='ref-ort']").send_keys(city)
		driver.find_element_by_xpath("//input[@id='ref-strasse']").send_keys(address)
		driver.find_element_by_xpath("//input[@id='ref-hausnummer']").send_keys(address_nr)
		box_privacy = driver.find_element_by_xpath("//input[@id='ref-teilnahmebedingungen-label']")
		ActionChains(driver).move_to_element(box_privacy).click(box_privacy).perform()
		submit_button = driver.find_element_by_xpath("//button[@name='formsubmit']")
		#ActionChains(driver).move_to_element(submit_button).click(submit_button).perform()
		#driver.close()
		#return True

	except Exception as e:
		print(e)

	sleep(5)
	driver.close()

# Submit solution manually 
submit_solution([1,2,3])