from time import sleep

def navigate_to_sudoku_page(driver):
    driver.get("https://www.coopzeitung.ch/raetsel/")
    sleep(5)
    try:
        links = driver.find_element_by_xpath("//div[@class='item-list']").find_elements_by_tag_name("a")
        for link in links:
            if "sudoku" in link.get_attribute('href'):
                driver.get(link.get_attribute('href'))
                break
        sleep(5)
    except Exception as e:
        print(e)
        driver.close()
        return None, None
    
    url = driver.current_url
    try:
        main = driver.find_element_by_tag_name("main")
        content_block = main.find_element_by_xpath("//div[@class='content-block']")
        iframes = content_block.find_elements_by_tag_name("iframe")
        for iframe in iframes:
            src = iframe.get_attribute("src")
            if src[8:22] == "static-raetsel":
                driver.get(src)
                sleep(5)
                return url, driver
    except Exception as e:
        print(e)
        return url, None
