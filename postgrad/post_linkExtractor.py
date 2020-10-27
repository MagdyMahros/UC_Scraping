"""Description:
    * author: Magdy Abdelkader
    * company: Fresh Futures/Seeka Technology
    * position: IT Intern
    * date: 26-10-20
    * description:This script extracts all the courses links and save it in txt file.
"""
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import os


option = webdriver.ChromeOptions()
option.add_argument(" - incognito")
option.add_argument("headless")
exec_path = Path(os.getcwd().replace('\\', '/'))
exec_path = exec_path.parent.__str__() + '/Libraries/Google/v86/chromedriver.exe'
browser = webdriver.Chrome(executable_path=exec_path, options=option) #

# MAIN ROUTINE
courses_page_url = 'https://search.canberra.edu.au/s/search.html?collection=courses&form=course-search&profile=_default&query=!padre&course-search-widget__submit=&meta_C_and=COURSE&sort=metaH&f.Type|B=postgraduate'
list_of_links = []
browser.get(courses_page_url)
the_url = browser.page_source
delay_ = 5  # seconds
# KEEP CLICKING NEXT UNTIL THERE IS NO BUTTON COLLECT THE LINKS
condition = True
while condition:
    result_elements = browser.find_element_by_xpath('/html/body/div/main/div[2]/div[4]/div/table')\
        .find_element_by_tag_name('tbody').find_elements_by_tag_name('tr')
    for i, element in enumerate(result_elements):
        print(i, element.text)
        url = element.get_attribute('data-fb-result')
        list_of_links.append(url)
    try:
        browser.execute_script("arguments[0].click();", WebDriverWait(browser, delay_).until(
            EC.element_to_be_clickable((By.LINK_TEXT, 'Next'))))
    except TimeoutException:
        print('timeout')
        condition = False
# SAVE TO FILE
course_links_file_path = os.getcwd().replace('\\', '/') + '/UC_postgrad_links.txt'
course_links_file = open(course_links_file_path, 'w')
for link in list_of_links:
    if link is not None and link != "" and link != "\n":
        if link == list_of_links[-1]:
            course_links_file.write(link.strip())
        else:
            course_links_file.write(link.strip() + '\n')
course_links_file.close()
