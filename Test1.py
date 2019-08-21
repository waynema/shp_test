def setup(driver_loc, url):
    driver = webdriver.Chrome(driver_loc)
    driver.get(url)

    return driver

def test(driver, xpath_begin, xpath_end, length_req, find_longest):
    row_count = len(driver.find_elements_by_xpath("/" + xpath_end))
    length_req_satisfied = False
    len_max = 0
    if find_longest:
      longest_words = []

    for i in range (1, row_count+1):
        text_xpath = xpath_begin + "[" + str(i) + "]" + xpath_end

        try:
            row_text = driver.find_element_by_xpath(text_xpath)
        except NoSuchElementException as e:
            print("NoSuchElementException when using xpath.\n%s" %e)
            driver.quit()
            sys.exit(1)

        if row_text.is_displayed():
          logging.info("Text in row %d is displayed." %i)
        else:
          logging.warning("Text in row %d is NOT displayed." %i)

        logging.info("The text in row %d is:\n%s" %(i, row_text.text))

        words = row_text.text.split()
        for word in words:
            word_len = len(word)
            if word_len < length_req and find_longest:
              if word_len > len_max:
                len_max = word_len
                longest_words = [ word ]
              elif word_len == len_max:
                longest_words.append( word )

            if word_len >= length_req:
              if (not length_req_satisfied):
                length_req_satisfied = True
                i_req_met = i
                word_req_met = word
              if find_longest:
                if word_len > len_max:
                  len_max = word_len
                  longest_words = [ word ]
                elif word_len == len_max:
                  longest_words.append( word )
              else:
                len_max = word_len  
                break

        if length_req_satisfied:
          if find_longest:
            continue
          else:
            break

    print ('RESULTS\n====================')

    #Assert that the dynamic text on the page contains a word at least %length_req characters in length
    if length_req_satisfied:
      assert length_req_satisfied, "Minimum length of %d char is found." %length_req
      print_text = "Minimum length requirement of %d char is met first time in text row %d at the word '%s'."
      print(print_text %(length_req, i_req_met, word_req_met))
    else:
      assert length_req_satisfied, "Minimum length of %d char is NOT found." %length_req

    if find_longest:
      print ("The longest (%d characters) word on the page:" %len_max)
      print (longest_words)

    return 1

def cleanup(driver):
    driver.quit()
    
    return 1

if __name__ == '__main__':
    import sys, logging

    logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.WARNING)

    # initialize selenium driver
    from selenium import webdriver
    from selenium.common.exceptions import NoSuchElementException

    # test parameters
    driver_loc = '/Users/wayne/Desktop/chromedriver'
    url = 'https://the-internet.herokuapp.com/dynamic_content'
    xpath_begin = "//div[@class='row']"
    xpath_end = "/div[@class='large-10 columns']"
    length_req = 10
    find_longest = True
    
    driver = setup(driver_loc, url)
    
    try:
        test(driver, xpath_begin, xpath_end, length_req, find_longest)
    except AssertionError as e:
        print(e)
    finally:
        cleanup(driver)
