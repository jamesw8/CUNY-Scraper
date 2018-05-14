from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import TimeoutException

def main():
	# set up driver and access webpage
	driver = webdriver.Chrome(executable_path='./chromedriver')
	driver.set_page_load_timeout(5)
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
	# driver.save_screenshot('firstpage.png')

	# select subject
	select_subject = Select(driver.find_element_by_id("subject_ld"))
	print([x.text for x in select_subject.options])
	select_subject.select_by_visible_text("Computer Science")
	Select(driver.find_element_by_id("courseCareerId")).select_by_visible_text("Undergraduate")
	driver.find_element_by_id("open_classId").click()
	# driver.save_screenshot('secondpage.png')
	driver.find_element_by_name("search_btn_search").click()
	# driver.save_screenshot('thirdpage.png')

	# scrape webpage
	d = driver.find_elements_by_xpath('//div[@id="contentDivImg_inst0"]/table')

	course_headers = [	'Class',
						'Section',
						'Days & Times',
						'Room',
						'Instructor',
						'Instruction Mode',
						'Meeting Dates',
						'Status',
						'Institution'
						]
	# load courses
	courses = {}
	course_num = 0
	for table in [t for t in d if t.tag_name == 'table']:
		course = table.find_element_by_xpath("tbody/tr/td/b/span").get_attribute("innerHTML").replace("&nbsp;"," ").replace("&amp;", "&")
		course = course[course.find("</a>") + 4:].strip()
		print(course)
		courses[course] = []
		sections = driver.find_element_by_id('contentDivImg'+str(course_num)).find_element_by_xpath("table/tbody")
		for row in sections.find_elements_by_xpath("*")[1:]:
			row_ = row.find_elements_by_xpath("*")
			for col in row_[1:3]:
				courses[course].append(col.find_element_by_xpath("*").get_attribute("innerHTML").replace("&nbsp;"," ").replace("&amp;", "&").strip())
				print('column_link', col.find_element_by_xpath("*").get_attribute("innerHTML").replace("&nbsp;"," ").replace("&amp;", "&").strip())
			for col in row_[3:8]:
				courses[course].append(col.get_attribute("innerHTML").replace("&nbsp;"," ").replace("&amp;", "&").strip())
				print('column', col.get_attribute("innerHTML").replace("&nbsp;"," ").replace("&amp;", "&").strip())
			courses[course].append(row_[8].find_element_by_xpath("*").get_attribute("title").replace("&nbsp;"," ").replace("&amp;", "&").strip())
			print('column', row_[8].find_element_by_xpath("*").get_attribute("title").replace("&nbsp;"," ").replace("&amp;", "&").strip())
			courses[course].append(row_[9].get_attribute("innerHTML").replace("&nbsp;"," ").replace("&amp;", "&").strip())
			print('column', row_[9].get_attribute("innerHTML").replace("&nbsp;"," ").replace("&amp;", "&").strip())
		course_num += 1
	print(courses)

	# load course sections
	# elem.clear()
	# elem.send_keys("pycon")
	# elem.send_keys(Keys.RETURN)
	# assert "No results found." not in driver.page_source
	# print(driver.page_source)
	driver.close()

if __name__ == '__main__':
	main()