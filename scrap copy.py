from distutils.log import error
from itertools import count
from numpy import NAN
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import pickle
import datetime
import pandas as pd
from openpyxl import load_workbook
import re
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd

#Load essentials:
driver_path = "geckodriver.exe"
driver = webdriver.Firefox(executable_path=driver_path)

#Get the website:
#with location:
#driver.get("https://www.naukri.com/financial-planning-and-analysis-jobs-in-bangalore?k=financial%20planning%20and%20analysis&nignbevent_src=jobsearchDeskGNB&")
#without location
driver.get("https://www.naukri.com/financial-planning-and-analysis-jobs?k=financial%20planning%20and%20analysis&nignbevent_src=jobsearchDeskGNB&")

time.sleep(5)


# Press the got it button to avoid errors
for data in driver.find_elements_by_tag_name('button'):
    if data.text == "Got it":
        data.click()

#Select the Finance and accounting filter
num_ = 0
for element in driver.find_elements_by_xpath("//span[@class='ellipsis fleft filterLabel']"):#("//i[@class='fleft naukicon naukicon-checkbox']"):
    if element.text == "Finance & Accounting":
        index = num_
        break
    num_+=1
driver.find_elements_by_xpath("//i[@class='fleft naukicon naukicon-checkbox']")[index].click()

#Beginning of While loop
n = 0
designation = [] #0
company_name = [] #1
location = [] #4
skills_all = []
while n<13:
    try:
        print(len(driver.find_elements_by_xpath("//span[@class='ellipsis fleft filterLabel']")), "***********************", len(driver.find_elements_by_xpath("//i[@class='fleft naukicon naukicon-checkbox']")))

        # Setup wait for later
        wait = WebDriverWait(driver, 10)

        # Press the got it button to avoid errors
        for data in driver.find_elements_by_tag_name('button'):
            if data.text == "Got it":
                data.click()

        time.sleep(2)
        page_num = n+1
        #Page Looper:
        for page_element in range(0, len(driver.find_elements_by_class_name("jobTuple"))):
            try:
                max_page_len = len(driver.find_elements_by_class_name("jobTuple"))
                
                driver.find_elements_by_class_name("jobTuple")[page_element].click()#Company location, key skills, title #Financial Planning and analysis - All cities for captives in Aon List - Clustering of skills
                time.sleep(7)
                # Wait for the new window or tab
                #wait.until(EC.number_of_windows_to_be(2))

                # Store the ID of the original window
                original_window = driver.current_window_handle
                # Loop through until we find a new window handle
                for window_handle in driver.window_handles:
                    if window_handle != original_window:
                        driver.switch_to.window(window_handle)
                        break

                basic_info = driver.find_elements_by_class_name("jd-header")[0].text.splitlines() #Array containing basic info
                #print(driver.find_element_by_class_name("chip clickable"))#[0].text)
                print(f"On Page {page_num}, Company Name - {basic_info[1]}")
                print("Basic Details : ", [dp for dp in basic_info])
                designation.append(basic_info[0])
                company_name.append(basic_info[1])
                location.append(basic_info[4])
                skills = driver.find_elements_by_xpath("//a[@class='chip clickable']")
                temp = []
                for i in skills:
                    temp.append(i.text+",")

                skills_all.append(temp)
                #print("##############\n\n\n\n\n",driver.find_elements_by_class_name("job-desc")[0].text)
                #time.sleep(3)

                driver.close()
                time.sleep(1)

                #Switch to current window
                driver.switch_to.window(driver.window_handles[0])
                time.sleep(2)#5

            except Exception as e:
                print("*****ALERT***** - An error has occured: \n", e)
                #time.sleep(3)

                driver.close()
                time.sleep(1)

                #Switch to current window
                driver.switch_to.window(driver.window_handles[0])
                time.sleep(2)
                continue

        #Go to next page
        print(f"Going to page {n+2}")
        driver.find_elements_by_xpath("//a[@class='fright fs14 btn-secondary br2']")[0].click()
        time.sleep(5)
        n += 1
    except:
        n += 1
        continue


df = pd.DataFrame(list(zip(designation, company_name, location, skills_all)), columns = ['Designation', 'Company Name', 'Location', 'Skills'])
df.to_excel("Master.xlsx")
