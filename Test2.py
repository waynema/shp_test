def setup(driver_loc, url):
    driver = webdriver.Chrome(driver_loc)
    driver.get(url)

    return driver

def test(driver, xpath_avatars, punisher, known_avatars, assign_names):
    page_avatars = []
    punisher_not_here = True
    
    avatars = driver.find_elements_by_xpath(xpath_avatars)

    for n,av in enumerate(avatars, start = 1):
        url = av.get_attribute('src')
        logging.info("Avatar(row %d) URL is: %s" %(n,url))

        f_name = 'row' + str(n) + 'avatar.jpg'
        logging.info("Avatar(row %d) image downloaded as %s file" %(n,f_name))
        with open(f_name, 'wb') as out_f:
            resp = urllib.urlopen(url) 
            shutil.copyfileobj(resp, out_f)
        size = os.path.getsize(f_name)
        logging.info("Avatar(row %d) file size is %d bytes" %(n,size))
     
        if assign_names:
            url_m = False
            size_m = False
            for known_av in known_avatars:
                if known_av['url'] == url:
                    url_m = True
                if known_av['size'] == size:
                    size_m = True
                if url_m or size_m:
                    break
                
            if url_m and size_m:
                if size == punisher['size']:
                    punisher_not_here = False
                    punisher_row = n
                page_avatars.append(known_av)
            else:
                name = url[-12:-4]
                new_av = {
                    'name': name,
                    'url' : url,
                    'size' : size
                }
                known_avatars.append(new_av)
                page_avatars.append(new_av)
                if url_m or size_m:
                    logging.warning('Only size or URL matches a known ' + \
                                    'avatar in row %d' %n)

                logging.info(known_avatars)
        else:
            if size == punisher['size'] and url == punisher['url']:
                punisher_not_here = False
                punisher_row = n
                break

    print ('RESULTS OUTPUT\n====================')
    if assign_names:
        print("%d avatars found on the page:" %len(page_avatars))
        for av in page_avatars:
            print(av['name'])
        f = open("known_avatars.json", "w")
        json.dump(known_avatars, f)
        f.close()

    assert punisher_not_here, "Punisher is last found in row %d." \
        %punisher_row

    if punisher_not_here:
        print("Punisher is NOT found on the page.")

    return 1

def cleanup(driver):
    driver.quit()
    
    return 1

if __name__ == '__main__':
    import json, logging, os, shutil, sys, urllib

    logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.WARNING)

    from selenium import webdriver
    from selenium.common.exceptions import NoSuchElementException

    driver_loc = '/Users/wayne/Desktop/chromedriver'
    url = 'https://the-internet.herokuapp.com/dynamic_content'
    xpath_avatars = "//div[@class='large-2 columns']/img"
    name_p = 'Punisher'
    url_p = 'https://the-internet.herokuapp.com/img/avatars/Original-Facebook-Geek-Profile-Avatar-3.jpg'
    size_p = 12817 
    punisher = {
        'name': name_p,
        'url' : url_p,
        'size' : size_p
    }

    if os.path.exists("known_avatars.json"):
       known_avatars = json.load(open("known_avatars.json"))
    else:
        known_avatars  = [punisher]
    assign_names = True 

    driver = setup(driver_loc, url)
    
    try:
        test(driver, xpath_avatars, punisher, known_avatars, assign_names)
    except AssertionError as e:
        print(e)
    finally:
        cleanup(driver)