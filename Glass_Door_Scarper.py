from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
import time
import pandas as pd
from datetime import datetime
from selenium import webdriver
import Extract_from_text as et

#Chaning your life to be expert


def get_jobs(keyword, num_jobs, path, slp_time):

    print(f"Entering get_jobs with keyword {keyword}, number of jobs={num_jobs}")

    options = webdriver.ChromeOptions()
    options.add_argument("start-maximized")

    driver = webdriver.Chrome(executable_path=path, options=options)
    url = "https://www.glassdoor.com/Job/jobs.htm?suggestCount=0&suggestChosen=false&clickSource=searchBtn&typedKeyword=" \
          + keyword + "&sc.keyword=" \
          + keyword + "&locT=&locId=&jobType="
    driver.get(url)

    time.sleep(3)
    jobs = []

    try:
        driver.find_element_by_class_name("selected").click()
        print('#  Process Start Successfully  #')
    except ElementClickInterceptedException:
        pass

    try:
        driver.find_element_by_css_selector('[alt="Close"]').click()  # clicking to the X.
        print('Close button clicked\n')
    except NoSuchElementException:
        pass

    try:
        job_buttons = driver.find_elements_by_css_selector("a.jobLink")  # holding 30 'a' tags
        time.sleep(3)
        job_buttons[0].click()  # CRUSTAL!!!
        time.sleep(slp_time)
        print("Clicked on job button successfully!")

    except Exception as e:
        print(e)


    try:
        driver.find_element_by_css_selector('[alt="Close"]').click()  # clicking to the X. AGAIN
        print('Close button clicked\n')
    except NoSuchElementException:
        pass

    try:
        # Get the total number of jobs in this keyword
        num_of_total_jobs = driver.find_element_by_xpath('//*[@id="MainCol"]/div[1]/div[1]/div/div/h1').text.replace(f" {keyword.lower()} Jobs", "")
        print(f'Num of total jobs: {num_of_total_jobs}')
    except ElementClickInterceptedException:
        return "Brake!"

    num_of_job_in_page = 0  # In every page there has 30 jobs
    currentPage = 0
    j = int(1)  # for creating a files

    while num_jobs > len(jobs):
        print("Entering page number:", currentPage + 1)
        time.sleep(slp_time)

        # Test for the "Sign Up" prompt and get rid of it.
        try:
            driver.find_element_by_class_name("selected").click()
        except ElementClickInterceptedException:
            pass
        time.sleep(2)

        job_buttons = driver.find_elements_by_css_selector("a.jobLink")  # list of links to the current page

        for i, job_button in enumerate(job_buttons):

            if len(jobs) >= num_jobs or len(jobs) >= int(num_of_total_jobs):  # Check if the number of jobs that collected is below the number we want or below the number of the total jobs
                print(f"Progress stop because the number of jobs in the website is over :)\nNumber of jobs in the website:{num_of_total_jobs} Number of jobs scraped:{len(jobs)}")
                break

            if num_of_job_in_page == 30:  # here we will stop and move to the next page
                break

            if i % 3 == 0:  # because each post has 3 links
                now = datetime.now()  # for testing
                is_remote = False
                num_of_job_in_page += 1  # 1/30

                print(f"\nProgress: {len(jobs) + 1}/{num_jobs} in page number: {currentPage + 1}")

                try:
                    job_button.click()  # Click on the next post in the list
                    time.sleep(1)  # Waiting for the element to create
                except:
                    print(
                        "Scraping terminated before reaching target number of jobs. Needed {}, got {}.".format(num_jobs,
                                                                                                               len(jobs)))
                    df = pd.DataFrame(jobs)
                    return df


                try:
                    show_more_button = driver.find_element_by_xpath('//*[@id="JobDescriptionContainer"]/div[2]')
                    show_more_button.click()
                    try:
                        text = driver.find_element_by_xpath('//*[@id="JobDescriptionContainer"]').text

                        years_of_experience = et.extract_years_of_experience(text)
                        # years_of_experience = -1 if et.extract_years_of_experience(text) > 11 else et.extract_years_of_experience(text)
                        education = et.extract_education(text)
                        position_level = et.extract_position_level(text)

                        doc = 0
                        if doc:
                            with open(f"row text2/row_text_{keyword}{j}.txt",
                                      'w') as f:  # for testing the 'extract' functions
                                j += 1
                                f.write(text)
                                f.write(
                                    f"\n\n\nTesting regine:"
                                    f"\nExperience: {years_of_experience}"
                                    f"\nEducation: {education}"
                                    f"\nPosition Level: {position_level}"
                                    f"\n Time of Scrape: {now}")

                    except Exception as e:
                        years_of_experience = education = position_level = int(-1)
                        print(f"Attempting to scrape the text did not worked  {str(e)} ")


                except Exception as e:
                    years_of_experience = education = position_level = int(-1)
                    print(f"e2!{str(e)}")



                try:
                    company_name = driver.find_element_by_xpath(
                        '//div[@class="css-87uc0g e1tk4kwz1"]').text  # It's working!
                except:
                    # print("Failed to collect company name!")
                    company_name = int(-1)


                try:
                    job_title = driver.find_element_by_css_selector("div[data-test='jobTitle']").text
                except:
                    # print("Failed to collect job title!")
                    job_title = int(-1)


                try:
                    location = driver.find_element_by_css_selector("div[data-test='location']").text
                    if "Remote" in location:
                        is_remote = True
                except:
                    # print("Failed to collect location!")
                    location = int(-1)


                try:
                    job_rating = driver.find_element_by_css_selector("span[data-test='detailRating']").text
                except:
                    # print("Failed to collect job Rating!")
                    job_rating = int(-1)

                try:
                    rating_elements = driver.find_elements_by_css_selector("span.css-a7hxlj.erz4gkm1")

                    career_opportunities = rating_elements[1].text
                    comp_and_benefits = rating_elements[3].text
                    culture_and_values = rating_elements[5].text
                    senior_management = rating_elements[7].text
                    work_life_balance = rating_elements[9].text

                    # career_opportunities = driver.find_element_by_class_name(r'css-a7hxlj.erz4gkm1').text
                    # comp_and_benefits = driver.find_element_by_xpath(r'//*[@id="JDCol"]/div/article/div/div[2]/div[1]/div[3]/div/ul/span[6]')
                    # culture_and_values = driver.find_element_by_xpath(r'//*[@id="JDCol"]/div/article/div/div[2]/div[1]/div[3]/div/ul/span[9]')
                    # senior_management = driver.find_element_by_xpath(r'//*[@id="JDCol"]/div/article/div/div[2]/div[1]/div[3]/div/ul/span[12]')
                    # work_life_balance = driver.find_element_by_xpath(r'//*[@id="JDCol"]/div/article/div/div[2]/div[1]/div[3]/div/ul/span[15]')
                    # print(career_opportunities," ", comp_and_benefits)

                except Exception as e:
                    career_opportunities = comp_and_benefits = culture_and_values = senior_management = work_life_balance = int(-1)
                    print(e)

                try:
                    salaries = driver.find_element_by_xpath('//div[@class="css-1bluz6i e2u4hf13"]').text
                except NoSuchElementException:
                    # print("Failed to collect Salary Estimate!")
                    salaries = int(-1)

                try:
                    company_overview_button = driver.find_element_by_css_selector('h2.css-1r0ltbv.e9b8rvy0')
                    company_overview_button.click()

                    try:
                        size = driver.find_element_by_xpath(
                            '//div[@class="d-flex justify-content-start css-rmzuhb e1pvx6aw0"]//span[text()="Size"]/following-sibling::span').text
                    except NoSuchElementException:
                        size = -1
                        # print("Failed to collect company size!")

                    try:
                        founded = driver.find_element_by_xpath('//span[text()="Founded"]/following-sibling::span').text
                    except NoSuchElementException:
                        founded = int(-1)
                        # print("Failed to collect founded date!")

                    try:
                        type_of_ownership = driver.find_element_by_xpath(
                            '//div[@class="d-flex justify-content-start css-rmzuhb e1pvx6aw0"]//span[text()="Type"]/following-sibling::span').text
                    except NoSuchElementException:
                        type_of_ownership = int(-1)
                        # print("Failed to collect type of ownership!")

                    try:
                        industry = driver.find_element_by_xpath(
                            '//div[@class="d-flex justify-content-start css-rmzuhb e1pvx6aw0"]//span[text()="Industry"]/following-sibling::span').text
                    except NoSuchElementException:
                        industry = int(-1)
                        # print("Failed to collect industry!")

                    try:
                        sector = driver.find_element_by_xpath(
                            '//div[@class="d-flex justify-content-start css-rmzuhb e1pvx6aw0"]//span[text()="Sector"]/following-sibling::span').text
                    except NoSuchElementException:
                        sector = int(-1)
                        # print("Failed to collect sector!")

                    try:
                        revenue = driver.find_element_by_xpath(
                            '//div[@class="d-flex justify-content-start css-rmzuhb e1pvx6aw0"]//span[text()="Revenue"]/following-sibling::span').text
                    except NoSuchElementException:
                        revenue = int(-1)
                        # print("Failed to collect revenue!")

                except:
                    size = int(-1)
                    founded = int(-1)
                    type_of_ownership = int(-1)
                    industry = int(-1)
                    sector = int(-1)
                    revenue = int(-1)

                    # print("Failed to click the Company Overview button!")

                jobs.append({"Job Title": job_title,
                             "Experience": years_of_experience,
                             "Position": position_level,
                             "Education": education,
                             "Company Name": company_name,
                             "Salary Estimate": salaries,
                             "Location": location,
                             "Rating": job_rating,
                             "Is Remote": is_remote,
                             "Company Size": size,
                             "Founded": founded,
                             "Type of Ownership": type_of_ownership,
                             "Industry": industry,
                             "Sector": sector,
                             "Revenue": revenue,
                             "Career Opportunities": career_opportunities,
                             "Comp & Benefits": comp_and_benefits,
                             "Culture & Values": culture_and_values,
                             "Senior Management": senior_management,
                             "Work Life Balance": work_life_balance,
                             "Time of Scrape": now})

        # END FOR LOOP

        currentPage += 1
        num_of_job_in_page = 0

        # move to the next page
        try:
            next_page = driver.find_element_by_css_selector('[alt="next-icon"]')
            time.sleep(3)
            next_page.click()
            time.sleep(3)
        except NoSuchElementException:
            df = pd.DataFrame(jobs)
            return df

    df = pd.DataFrame(jobs)
    return df



