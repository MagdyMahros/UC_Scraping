import csv
import re
import time
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import bs4 as bs4
import os
import copy
from CustomMethods import TemplateData
from CustomMethods import DurationConverter

option = webdriver.ChromeOptions()
option.add_argument(" - incognito")
option.add_argument("headless")
exec_path = Path(os.getcwd().replace('\\', '/'))
exec_path = exec_path.parent.__str__() + '/Libraries/Google/v86/chromedriver.exe'
browser = webdriver.Chrome(executable_path=exec_path, options=option)

# read the url from each file into a list
course_links_file_path = Path(os.getcwd().replace('\\', '/'))
course_links_file_path = course_links_file_path.__str__() + '/UC_postgrad_links.txt'
course_links_file = open(course_links_file_path, 'r')

# the csv file we'll be saving the courses to
csv_file_path = Path(os.getcwd().replace('\\', '/'))
csv_file = csv_file_path.__str__() + '/UC_postgrad.csv'

course_data = {'Level_Code': '', 'University': 'University of Canberra', 'City': '', 'Country': '',
               'Course': '', 'Int_Fees': '', 'Local_Fees': '', 'Currency': 'AUD', 'Currency_Time': 'year',
               'Duration': '', 'Duration_Time': '', 'Full_Time': 'yes', 'Part_Time': 'yes', 'Prerequisite_1': 'IELTS',
               'Prerequisite_2': '', 'Prerequisite_3': '', 'Prerequisite_1_grade': '6.5', 'Prerequisite_2_grade': '',
               'Prerequisite_3_grade': '', 'Website': '', 'Course_Lang': '', 'Availability': '', 'Description': '',
               'Career_Outcomes': '', 'Online': '', 'Offline': '', 'Distance': '', 'Face_to_Face': '',
               'Blended': '', 'Remarks': ''}

possible_cities = {'canberra': 'Canberra', 'bruce': 'Bruce', 'mumbai': 'Mumbai', 'melbourne': 'Melbourne',
                   'brisbane': 'Brisbane', 'sydney': 'Sydney', 'queensland': 'Queensland', 'ningbo': 'Ningbo',
                   'shanghai': 'Shanghai', 'bhutan': 'Bhutan', 'online': 'Online', 'hangzhou': 'Hangzhou',
                   'hanoi': 'Hanoi'}
possible_countries = {'canberra': 'Australia', 'mumbai': 'India', 'melbourne': 'Australia',
                      'brisbane': 'Australia', 'sydney': 'Australia', 'queensland': 'Australia', 'ningbo': 'China',
                      'shanghai': 'China', 'bhutan': 'Bhutan', 'online': 'Online', 'hangzhou': 'China',
                      'hanoi': 'Vietnam'}

possible_languages = {'Japanese': 'Japanese', 'French': 'French', 'Italian': 'Italian', 'Korean': 'Korean',
                      'Indonesian': 'Indonesian', 'Chinese': 'Chinese', 'Spanish': 'Spanish'}

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

    # DECIDE THE LEVEL CODE
    for i in level_key:
        for j in level_key[i]:
            if j in course_data['Course']:
                course_data['Level_Code'] = i
    print('COURSE LEVEL CODE: ', course_data['Level_Code'])

    # DECIDE THE FACULTY
    for i in faculty_key:
        for j in faculty_key[i]:
            if j.lower() in course_data['Course'].lower():
                course_data['Faculty'] = i
    print('COURSE FACULTY: ', course_data['Faculty'])

    # COURSE DESCRIPTION
    d_title = soup.find('div', id='introduction')
    if d_title:
        description = d_title.find('p')
        if description:
            print('COURSE DESCRIPTION: ', description.get_text())
            course_data['Description'] = description.get_text()
        elif description is None:
            description_1 = d_title.find('div')
            print('COURSE DESCRIPTION: ', description_1.get_text())
            course_data['Description'] = description_1.get_text()

    # COURSE LANGUAGE
    for language in possible_languages:
        if language in course_data['Course']:
            course_data['Course_Lang'] = language
        else:
            course_data['Course_Lang'] = 'English'
    print('COURSE LANGUAGE: ', course_data['Course_Lang'])

    # CITY
    location_head = soup.find('th', class_='course-details-table__th', text=re.compile('Location', re.IGNORECASE))
    temp_city = []
    if location_head:
        cities = location_head.find_next('td', class_='course-details-table__td').text
        temp_city = re.findall(r"[\w']+", cities.__str__().strip().lower())
        if 'canberra' in temp_city:
            actual_cities.append('canberra')
            course_data['Availability'] = 'A'
        if 'mumbai' in temp_city:
            actual_cities.append('mumbai')
            course_data['Availability'] = 'I'
        if 'melbourne' in temp_city:
            actual_cities.append('melbourne')
        if 'brisbane' in temp_city or 'south' in temp_city:
            actual_cities.append('brisbane')
            course_data['Availability'] = 'A'
        if 'sydney' in temp_city:
            actual_cities.append('sydney')
            course_data['Availability'] = 'A'
        if 'queensland' in temp_city:
            actual_cities.append('queensland')
            course_data['Availability'] = 'A'
        if 'ningbo' in temp_city:
            actual_cities.append('ningbo')
            course_data['Availability'] = 'I'
        if 'shanghai' in temp_city:
            actual_cities.append('shanghai')
            course_data['Availability'] = 'I'
        if 'bhutan' in temp_city:
            actual_cities.append('bhutan')
            course_data['Availability'] = 'I'
        if 'online' in temp_city:
            actual_cities.append('online')
            course_data['Availability'] = 'A'
        if 'hangzhou' in temp_city:
            actual_cities.append('hangzhou')
            course_data['Availability'] = 'I'
        if 'hanoi' in temp_city:
            actual_cities.append('hanoi')
            course_data['Availability'] = 'I'
    else:
        actual_cities.append('canberra')
        course_data['Availability'] = 'A'
    print('CITY: ', actual_cities)

    # CAREER OPPORTUNITIES
    career_title = soup.find('h2', text=re.compile('Career opportunities', re.IGNORECASE))
    if career_title:
        career_list = career_title.find_next('ul')
        if career_list:
            career_list = career_list.get_text().__str__().strip().replace('\n', ' / ')
            course_data['Career_Outcomes'] = career_list
    print('CAREER OUTCOMES: ', course_data['Career_Outcomes'])

    # FEES
    # navigate to fees tab
    try:
        browser.execute_script("arguments[0].click();", WebDriverWait(browser, 5).until(
            EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, 'Fees'))))
    except TimeoutException:
        print('Timeout Exception')
        pass
    # grab the data
    year_table = soup.find('div', id='fees').find_next('table', class_='short-table grey')
    if year_table:
        year_table_row = year_table.find_all('tr')
        for x in year_table_row:
            fees = x.find('td', text=re.compile('2021', re.IGNORECASE))
            if fees:
                for index, fee in enumerate(fees.find_next_siblings('td')):
                    if index == 0:
                        course_data['Local_Fees'] = fee.get_text().__str__().strip().replace('$', '')
                    if index == 1:
                        course_data['Int_Fees'] = fee.get_text().__str__().strip().replace('$', '')
        print('LOCAL FEES: ', course_data['Local_Fees'])
        print('INTERNATIONAL FEES: ', course_data['Int_Fees'])

        # DURATION & DURATION TIME
        # navigate to "important to know" tab
        try:
            browser.execute_script("arguments[0].click();", WebDriverWait(browser, 5).until(
                EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, 'Important to know'))))
        except TimeoutException:
            print('Timeout Exception')
            pass
        # grab the data
        duration_title = soup.find('h2', class_='h4 blue', text=re.compile('Course Duration', re.IGNORECASE))
        if duration_title:
            duration_text = duration_title.find_next('p')
            if duration_text:
                first_part = duration_text.get_text().__str__().split('.')[0]
                if first_part is not None:
                    if DurationConverter.convert_duration(first_part) is not None:
                        converted_first_part = list(DurationConverter.convert_duration(first_part))
                        course_data['Duration'] = converted_first_part[0]
                        if converted_first_part[0] == 1 and 'Years' in converted_first_part[1]:
                            converted_first_part[1] = 'Year'
                            course_data['Duration_Time'] = converted_first_part[1]
                        elif converted_first_part[0] == 1 and 'Months' in converted_first_part[1]:
                            converted_first_part[1] = 'Month'
                            course_data['Duration_Time'] = converted_first_part[1]
                        else:
                            course_data['Duration_Time'] = converted_first_part[1]
                    else:
                        course_data['Duration'] = 'not specified'
                        course_data['Duration_Time'] = 'not specified'
        print('DURATION: ', course_data['Duration'])
        print('DURATION TIME: ', course_data['Duration_Time'])

    # DELIVERY (online, offline, face-to-face, blended, distance)
    # navigate to "Unit Delivery Modes" tab
    try:
        browser.execute_script("arguments[0].click();", WebDriverWait(browser, 5).until(
            EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, 'Unit Delivery Modes'))))
    except TimeoutException:
        print('Timeout Exception')
        pass
    # grab the data
    delivery_tag = soup.find('div', id='unit_delivery_modes')
    delivery_list = []
    if delivery_tag:
        delivery_tag2 = delivery_tag.find_next('div', class_='collapsible-section__details')
        if delivery_tag2:
            delivery_table = delivery_tag2.find('table', class_='unit-delivery-mode')
            if delivery_table:
                table_rows = delivery_table.find_all('tr')
                if table_rows:
                    for column in table_rows:
                        table_columns = column.find_all('td')
                        for index, element in enumerate(table_columns):
                            if index == 0:
                                delivery_unit = element.get_text().__str__().strip().lower().replace(':', '')
                                delivery_list.append(delivery_unit)
                                if 'flexible' in delivery_list:
                                    course_data['Blended'] = 'yes'
                                    course_data['Face_to_Face'] = 'yes'
                                else:
                                    course_data['Blended'] = 'no'
                                if 'online' in delivery_list:
                                    course_data['Online'] = 'yes'
                                else:
                                    course_data['Online'] = 'no'
                                if 'on campus' in delivery_list:
                                    course_data['Offline'] = 'yes'
                                    course_data['Face_to_Face'] = 'yes'
                                else:
                                    course_data['Offline'] = 'no'
                                    course_data['Face_to_Face'] = 'no'
                                if 'distance' in delivery_list:
                                    course_data['Distance'] = 'yes'
                                else:
                                    course_data['Distance'] = 'no'
    print('DELIVERY: online: ' + course_data['Online'] + ' offline: ' + course_data['Offline'] + ' face to face: ' +
          course_data['Face_to_Face'] + ' blended: ' + course_data['Blended'] + ' distance: ' + course_data[
              'Distance'])

    # duplicating entries with multiple cities for each city and mapping the corresponding country
    for i in actual_cities:
        course_data['City'] = possible_cities[i]
        course_data['Country'] = possible_countries[i]
        course_data_all.append(copy.deepcopy(course_data))
    del actual_cities

    # TABULATE THE DATA
    desired_order_list = ['Level_Code', 'University', 'City', 'Course', 'Faculty', 'Int_Fees', 'Local_Fees',
                          'Currency', 'Currency_Time', 'Duration', 'Duration_Time', 'Full_Time', 'Part_Time',
                          'Prerequisite_1', 'Prerequisite_2', 'Prerequisite_3', 'Prerequisite_1_grade',
                          'Prerequisite_2_grade', 'Prerequisite_3_grade', 'Website', 'Course_Lang', 'Availability',
                          'Description', 'Career_Outcomes', 'Country', 'Online', 'Offline', 'Distance', 'Face_to_Face',
                          'Blended', 'Remarks']

    course_dict_keys = set().union(*(d.keys() for d in course_data_all))

    with open(csv_file, 'w', encoding='utf-8', newline='') as output_file:
        dict_writer = csv.DictWriter(output_file, course_dict_keys)
        dict_writer.writeheader()
        dict_writer.writerows(course_data_all)

    with open(csv_file, 'r', encoding='utf-8') as infile, open('UC_postgrad_ordered.csv', 'w', encoding='utf-8',
                                                               newline='') as outfile:
        writer = csv.DictWriter(outfile, fieldnames=desired_order_list)
        # reorder the header first
        writer.writeheader()
        for row in csv.DictReader(infile):
            # writes the reordered rows to the new file
            writer.writerow(row)

