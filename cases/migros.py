from time import sleep

def navigate_to_sudoku_page(driver):
    url = "https://www.migros.ch/de/unternehmen/medien/publikationen/magazin/sudoku.html"
    driver.get(url)
    sleep(5)
    main = driver.find_element_by_tag_name("main")
    content_block = main.find_element_by_xpath("//div[@class='wrapper-sudoku']")
    iframes = content_block.find_elements_by_tag_name("iframe")
    for iframe in iframes:
        src = iframe.get_attribute("src")
        if src[8:22] == "static-raetsel":
            driver.get(src)
            sleep(5)
            return url, driver
    return url, None
    
