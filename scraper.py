from selenium import webdriver
from bs4 import BeautifulSoup
import json

#Variable setup
SCHOOL = "school"
USERNAME = "username"
PASSWORD = "password"
MAIN_URL = "https://sms.schoolsoft.se/{}/sso".format(SCHOOL)
###############################################################

#Logging in to the website
driver = webdriver.PhantomJS()
driver.get(MAIN_URL)

btn = driver.find_elements_by_xpath("//*[@id='username']")[0]
btn.send_keys(USERNAME)
btn = driver.find_elements_by_xpath("//*[@id='password']")[0]
btn.send_keys(PASSWORD)
btn = driver.find_elements_by_xpath("//*[@class='form__button form__button--primary']")[0]
btn.click()

#Fetch schedule
driver.get("https://sms.schoolsoft.se/{}/jsp/student/right_student_schedule.jsp?menu=schedule".format(SCHOOL))
html = driver.page_source
schedule = BeautifulSoup(html)

theSchedule = []

for a in schedule.find_all("a", {"class": "schedule"}):
    info = a.find("span")
    i = info.get_text()
    theSchedule.append(i)

#Fetch messages
driver.get("https://sms.schoolsoft.se/{}/jsp/student/right_student_message.jsp?menu=message".format(SCHOOL))
html = driver.page_source
msg = BeautifulSoup(html)

messages = []
senders = []

for a in msg.find_all("div", {"class": "accordion_inner_left"}):
    info = a.find("span")
    i = info.get_text()
    messages.append(i)

for a in msg.find_all("div", {"class": "accordion_inner_right"}):
    info = a.find("span")
    i = info.get_text()
    senders.append(i)

#Parse to a json file
data = open('a.json').read()
count = data.count('message')
count2 = data.count('schema')

n = 0
i = 0
if messages.__len__() > count:
    with open('a.json', 'w') as f:
        while i < messages.__len__():
            if theSchedule.__len__() > count2 and n < theSchedule.__len__():
                json.dump({
                'schema' : theSchedule[n]},
                f, sort_keys=True, indent=4, 
                ensure_ascii=False)
            n += 1
            if messages.__len__() > count:
                json.dump({
                'sender' : senders[i],
                'message' : messages[i]},
                f, sort_keys=True, indent=4, 
                ensure_ascii=False)
            i += 1
