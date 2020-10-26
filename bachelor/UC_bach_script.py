import csv
import re
import time
from pathlib import Path
from selenium import webdriver
import bs4 as bs4
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import os
import copy
from CustomMethods import TemplateData

option = webdriver.ChromeOptions()
option.add_argument(" - incognito")
option.add_argument("headless")
exec_path = Path(os.getcwd().replace('\\', '/'))
exec_path = exec_path.parent.__str__() + '/Libraries/Google/v86/chromedriver.exe'
browser = webdriver.Chrome(executable_path=exec_path, options=option)

# read the url from each file into a list
course_links_file_path = Path(os.getcwd().replace('\\', '/'))
course_links_file_path = course_links_file_path.__str__() + '/UC_Bachelor_links.txt'
course_links_file = open(course_links_file_path, 'r')

# the csv file we'll be saving the courses to
csv_file_path = Path(os.getcwd().replace('\\', '/'))
csv_file = csv_file_path.__str__() + '/UC_bachelors.csv'

course_data = {'Level_Code': '', 'University': 'Australian Catholic University', 'City': '', 'Country': 'Australia',
               'Course': '', 'Int_Fees': '', 'Local_Fees': '', 'Currency': 'AUD', 'Currency_Time': 'year',
               'Duration': '', 'Duration_Time': '', 'Full_Time': '', 'Part_Time': '', 'Prerequisite_1': '',
               'Prerequisite_2': 'IELTS', 'Prerequisite_3': '', 'Prerequisite_1_grade': '', 'Prerequisite_2_grade': '',
               'Prerequisite_3_grade': '', 'Website': '', 'Course_Lang': '', 'Availability': '', 'Description': '',
               'Career_Outcomes': '', 'Online': 'no', 'Offline': 'yes', 'Distance': 'no', 'Face_to_Face': 'yes',
               'Blended': '', 'Remarks': ''}

possible_cities = {'canberra': 'Canberra', 'bruce': 'Bruce', 'mumbai': 'Mumbai', 'melbourne': 'Melbourne',
                   'brisbane': 'Brisbane', 'sydney': 'Sydney'}

course_data_all = []
level_key = TemplateData.level_key  # dictionary of course levels
faculty_key = TemplateData.faculty_key  # dictionary of course levels

# GET EACH COURSE LINK
for each_url in course_links_file:
    actual_cities = []
    browser.get(each_url)
    pure_url = each_url.strip()
    each_url = browser.page_source

    soup = bs4.BeautifulSoup(each_url, 'lxml')
    time.sleep(1)

    # SAVE COURSE URL
    course_data['Website'] = pure_url

    # SAVE COURSE TITLE
    course_title = soup.find('h1', class_='course_title').text
    print('COURSE TITLE: ', course_title)
    course_data['Course'] = course_title.strip()



