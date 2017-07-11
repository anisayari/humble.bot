# coding=utf-8
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import string
import csv
import random
from tools import sleep
from config import path_to_chrome_driver , path_to_phantom_driver , my_username

domains = [ "hotmail.com", "gmail.com", "aol.com", "mail.com" , "mail.kz", "yahoo.com"]
letters = string.ascii_lowercase[:12]


def get_random_domain(domains):
    return random.choice(domains)

def get_random_name(letters, length):
    return ''.join(random.choice(letters) for i in range(length))

def generate_random_emails(length):
    prime = get_random_name(letters, length)
    return prime + '@' + get_random_domain(domains),prime


def save_info(dict,prime):
    with open('data.csv', 'a') as f:
        w = csv.writer(f, delimiter=',',lineterminator='\n')
        w.writerow([str(prime)+str(dict['username']), dict['password'], dict['email'] ,dict['full_name']])

def generate_password(size = 6, chars = string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def info_generation():
    info_generate={}
    info_generate['password'] = generate_password(size=10)
    info_generate['email'],prime = generate_random_emails(7)
    same_1 = prime
    same_2 = str(get_random_name(letters, 7))
    info_generate['username'] ='.'+same_2 #because instagram autocomplete username info from email and full_name....
    info_generate['full_name'] = same_1+' '+same_2
    return info_generate,prime

def main():
    count = 0
    for i in range(0,3000):
        driver = webdriver.Chrome(path_to_chrome_driver)
        #driver = webdriver.PhantomJS(path_to_phantom_driver)
        driver.get("https://instagram.com")
        email = driver.find_element_by_xpath("//input[@aria-label='Mobile Number or Email']")
        full_name = driver.find_element_by_xpath("//input[@aria-label='Full Name']")
        username = driver.find_element_by_xpath("//input[@aria-label='Username']")
        password = driver.find_element_by_xpath("//input[@aria-label='Password']")

        info_generate,prime = info_generation()

        email.send_keys(info_generate['email'])
        sleep(3)
        full_name.send_keys(info_generate['full_name'])
        sleep(3)
        username.send_keys(info_generate['username'])
        sleep(3)
        password.send_keys(info_generate['password'])

        #driver.find_element_by_link_text("Sign up").click()
        test = driver.find_element_by_xpath("//button[contains(text(), 'Sign up')]")
        sleep(3)
        test.click()
        sleep(4)
        try:
            driver.find_element_by_id('ssfErrorAlert')
            error = True
            print 'click error'
        except:
            error = False
        sleep(4)
        count_error = 0
        while error:
            count_error += 1
            sleep(3)
            test.click()
            sleep(int(count_error))
            try:
                driver.find_element_by_id('ssfErrorAlert')
                error = True
                print 'click error'
            except:
                error = False
                print 'click ok'
                sleep(4)
                button_close = driver.find_element_by_xpath("//button[contains(text(), 'Close')]")
                button_close.click()
                sleep(2)
                button_search = driver.find_element_by_xpath("//span[contains(text(), 'search')]")
                button_search.click()
                sleep(2)
                search_bar= driver.find_element_by_xpath("//input[@placeholder='Search']")
                search_bar.send_keys(my_username)

        count += 1
        print str(count)+' account created'
        save_info(info_generate,prime)
        driver.close()
        sleep(2)

main()

if __name__ == '__main__':
    main()