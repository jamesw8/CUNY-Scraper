from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select

# set up driver and access webpage
driver = webdriver.PhantomJS(executable_path="C:/phantomjs-2.1.1-windows/bin/phantomjs.exe")
driver.set_window_size(1024, 768)
driver.get("https://globalsearch.cuny.edu/CFGlobalSearchTool/search.jsp")
assert "Global Class Search" in driver.title

# fill in forms and submit
select_school = driver.find_element_by_id("CTY01")
select_school.click()
select_semester = Select(driver.find_element_by_id("t_pd"))
select_semester.select_by_visible_text("2018 Fall Term")
submit = driver.find_element_by_name("next_btn")
submit.click()
driver.save_screenshot('firstpage.png')

# select subject
select_subject = Select(driver.find_element_by_id("subject_ld"))
print([x.text for x in select_subject.options])
select_subject.select_by_visible_text("Computer Science")
Select(driver.find_element_by_id("courseCareerId")).select_by_visible_text("Undergraduate")
driver.find_element_by_id("open_classId").click()
driver.save_screenshot('secondpage.png')
driver.find_element_by_name("search_btn_search").click()
driver.save_screenshot('thirdpage.png')
# print(driver.find_elements_by_class_name("cunylite_LABEL")[0].get_attribute("innerHTML"))

# scrape webpage
print([o.get_attribute("innerHTML") for o in driver.find_element_by_id("contentDivImg_inst0").find_elements_by_css_selector("*")])
# elem.clear()
# elem.send_keys("pycon")
# elem.send_keys(Keys.RETURN)
# assert "No results found." not in driver.page_source
# print(driver.page_source)
driver.close()