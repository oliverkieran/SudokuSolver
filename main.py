from selenium import webdriver
from time import sleep, time
from datetime import datetime
import cv2
#import requests
import telegram
from subprocess import call


from sudoku_extractor import process_image
from digitclassifier import extract_number
from sudoku_solver import explicit_solver as solve_sudoku
# from submit_solution import submit_solution

debug = False # Will run in headless mode, if set to False

def expand_shadow_element(driver, element):
	shadow_root = driver.execute_script('return arguments[0].shadowRoot', element)
	return shadow_root

def get_sudoku():
	DRIVER_PATH = '/Users/Oli/Documents/Webdriver/chromedriver'
	#DRIVER_PATH = '/usr/lib/chromium-browser/chromedriver' #for Raspberry Pi
	if debug:
		driver = webdriver.Chrome(executable_path=DRIVER_PATH)
	else:
		options = webdriver.ChromeOptions()
		options.add_argument('headless')
		driver = webdriver.Chrome(executable_path=DRIVER_PATH, chrome_options=options)
		print("Started webdriver at {}".format(datetime.now().strftime("%H:%M")))
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
		return None, None, None

	url = driver.current_url
	try:	
		main = driver.find_element_by_tag_name("main")
		content_block = main.find_element_by_xpath("//div[@class='content-block']")
		iframes = content_block.find_elements_by_tag_name("iframe")
		for i, iframe in enumerate(iframes):
			src = iframe.get_attribute("src")
			if src[8:22] == "static-raetsel":
				driver.get(src)
				sleep(5)
				week_year = datetime.now().strftime("%W_%Y")
				image_path = "images/{}_sudoku_of_the_week.png".format(week_year)
				# Take a screenshot of the sudoku and save it to disk
				driver.save_screenshot(image_path)
				print("Screenshot was taken.")

				# ONLY USE ON RASPBERRY PI
				"""
				# Upload image to dropbox folder
				Upload = "home/pi/Documents/Coding/Dropbox-Uploader/dropbox_uploader.sh upload {}".format(image_path)
				call ([Upload], shell=True)
				"""

				# Get prize fields
				sudoku_raetsel = driver.find_element_by_tag_name('raetsel-sudoku')
				shadow_root = expand_shadow_element(driver, sudoku_raetsel)
				game_field = shadow_root.find_element_by_css_selector("#gameField")
				prize_fields = []
				for nr, field in enumerate(game_field.find_elements_by_class_name("fieldFrame")):
					if "prizeField" in field.get_attribute("class"):
						prize_fields.append(nr)
				print("Prize Fields: {}".format(prize_fields))
				driver.close()
				return image_path, prize_fields, url
	except Exception as e:
		print(e)

	#sleep(5)
	driver.close()
	return None, None, None


# Function to send telegram message
def telegram_bot_send_message(bot_message=None, bot_photo=None):
    
    bot_token = '1440469607:AAGA6YvjarJyC_53edDjcIjAZdiBMqieUl8'
    bot_chatID = '1003688744'
    bot = telegram.Bot(token=bot_token)
    if bot_message is not None:
    	bot.send_message(chat_id=bot_chatID, text=bot_message)
    	return
    	#send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message
    	#response = requests.get(send_text)
    elif bot_photo is not None:
    	bot.send_photo(chat_id=bot_chatID, photo=open(bot_photo, "rb"))
    	return
    	#send_photo = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message
    	#response = requests.get(send_photo)
    else:
    	return None

    #return response.json()


def main():
	# Get path of saved sukoku image and the prize fields
	sudoku_path, prize_fields, url = get_sudoku()
	#sudoku_path, prize_fields, url = ("images/48_2020_sudoku_of_the_week.png", [12,13,14], "https://www.coopzeitung.ch/raetsel/2018/sudoku-aus-der-coopzeitung-137607/")

	# Pre process the image and isolate each sudoku cell
	if sudoku_path is not None:
		image = process_image(sudoku_path)
	else:
		print("Couldn't extract sudoku from the webpage.")
		return
	print(image.shape)

	# Extract the digits into a 2D-list using deep learning
	grid = extract_number(image)
	print(grid)

	# Solve the sudoku
	solution, finished = solve_sudoku(grid.tolist())

	prize_nrs = []
	if finished:
		# Extract the prize numbers from the returned solution
		for prize in prize_fields:
			row = prize//9
			col = prize - row*9
			prize_nrs.append(solution[row][col])
		# Print solution
		for row in solution:
			print(row)
		print("Prize numbers {}".format(prize_nrs))

		# Submit solution on the coop webpage
		#submitted = submit_solution(prize_nrs)
		message = """
		CONGRATS!!
		The weekly Coop sudoku was sucessfully solved! 
		The prize numbers are the following:

		{nrs}

		{url}
		""".format(nrs=prize_nrs, url=url)
		telegram_bot_send_message(message)

	else:
		message = """
		Sudoku could NOT be solved :( 
		There might have been a problem with the digit extraction.
		This is what was extracted:

		{}
		""".format(grid)
		telegram_bot_send_message(message)
		telegram_bot_send_message(sudoku_path)



if __name__ == '__main__':
    #try:
    start_time = time()
    main()
    print("TAT: ", round(time() - start_time, 3))
    #except:
    #    print('[ERROR]: Image not found')
