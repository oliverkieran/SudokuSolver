# from selenium import webdriver
from seleniumwire import webdriver
from time import sleep, time
from datetime import datetime
import requests
import numpy as np
import telegram_send

from sudoku_solver import explicit_solver as solve_sudoku
from cases import coop, migros


debug = False # Will run in headless mode, if set to False
case = "coop"


def _create_initial_sudoku(sudoku_info):
    initial_sudoku = np.zeros((9, 9))
    for element in sudoku_info:
        initial_sudoku[element["row"]-1, element["column"]-1] = element["number"]
    return initial_sudoku
    

def get_initial_setup(driver):
    for request in driver.requests:
        # print(request.url)
        if request.response and request.url[8:11] == "api":
            print(request.url[8:11])
            print(request.url)
            http_response = requests.get(request.url).json()
            if http_response:
                sudoku_info = http_response["description"]
                initial_sudoku = _create_initial_sudoku(sudoku_info["hints"])
                print(initial_sudoku)
                prize_fields = [(int(elem["row"]) - 1, int(elem["column"]) - 1) for elem in sudoku_info["prizeFields"]]
                return initial_sudoku, prize_fields
    return None, None


def get_sudoku():
    DRIVER_PATH = '/Users/oli/Documents/Webdriver/chromedriver_mac64_m1'
    #DRIVER_PATH = '/usr/lib/chromium-browser/chromedriver' #for Raspberry Pi
    if debug:
        driver = webdriver.Chrome(executable_path=DRIVER_PATH)
    else:
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        options.add_argument('--no-sandbox') 
        driver = webdriver.Chrome(executable_path=DRIVER_PATH, chrome_options=options)
        print("Started webdriver at {}".format(datetime.now().strftime("%H:%M")))
    driver.maximize_window()
    if case == "migros":
        url, driver = migros.navigate_to_sudoku_page(driver)
    elif case == "coop":
        url, driver = coop.navigate_to_sudoku_page(driver)
    
    initial_sudoku, prize_fields = get_initial_setup(driver)
    print(f"Prize Fields: {prize_fields}")
    driver.close()
    return initial_sudoku, prize_fields, url


def main():
	# Get path of saved sukoku image and the prize fields
	initial_sudoku, prize_fields, url = get_sudoku()
	#sudoku_path, prize_fields, url = ("images/48_2020_sudoku_of_the_week.png", [12,13,14], "https://www.coopzeitung.ch/raetsel/2018/sudoku-aus-der-coopzeitung-137607/")

	

	# Solve the sudoku
	solution, finished = solve_sudoku(initial_sudoku.tolist())

	prize_nrs = []
	if finished:
		# Extract the prize numbers from the returned solution
		for prize_row, prize_column in prize_fields:
			prize_nrs.append(solution[prize_row][prize_column])
		# Print solution
		for row in solution:
			print(row)
		print("Prize numbers {}".format(prize_nrs))

		# Submit solution on the coop webpage
		#submitted = submit_solution(prize_nrs)
		message = """
		CONGRATS!!
		The weekly {case} sudoku was sucessfully solved! 
		The prize numbers are the following:

		{nrs}

		{url}
		""".format(case=case, nrs=prize_nrs, url=url)

	else:
		message = """
		Sudoku could NOT be solved :( 
		There might have been a problem with the digit extraction.
		This is what was extracted:

		{}
		""".format(initial_sudoku)
	telegram_send.send(messages=[message])


if __name__ == '__main__':
    #try:
    start_time = time()
    main()
    print("TAT: ", round(time() - start_time, 3))
    #except:
    #    print('[ERROR]: Image not found')
