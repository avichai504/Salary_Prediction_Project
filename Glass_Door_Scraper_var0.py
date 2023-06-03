from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException, TimeoutException
import time
import pandas as pd
from datetime import datetime
from selenium import webdriver
from selenium.webdriver import ActionChains

import Extract_from_text as ets
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException





def get_jobs(keyword, num_jobs, path, slp_time):

    counter_break = 0

    print(f"Entering get_jobs with keyword {keyword}, number of jobs={num_jobs}")

    options = webdriver.ChromeOptions()
    options.add_argument("start-maximized")

    driver = webdriver.Chrome(executable_path=path, options=options)
    url = "https://www.glassdoor.com/Job/jobs.htm?suggestCount=0&suggestChosen=false&clickSource=searchBtn&typedKeyword=" \
          + keyword + "&sc.keyword=" \
          + keyword + "&locT=&locId=&jobType="
    driver.get(url)
    jobs = []

    wait = WebDriverWait(driver, slp_time)  # Wait for a maximum of 3 seconds


    try:
        driver.find_element_by_class_name("selected").click()
        print('#  Process Start Successfully  #')
    except ElementClickInterceptedException:
        pass


    try:
        job_buttons = driver.find_elements_by_css_selector("a.jobLink") #[-1]  # holding 30 'a' tags
        job_buttons[0].click()  # CRUSTAL!!!
        print(job_buttons[0])
        print("Clicked on job button successfully!")
    except Exception as e:
        print(e)


    try:
        close_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[alt="Close"]')))
        close_button.click()  # Clicking the X button
        print('Close button clicked#2\n')  # AGAIN!!
    except TimeoutException:
        print('Close button DID NOT clicked!#2')
        pass


    try:
        total_jobs_locator = (By.XPATH, '//*[@id="MainCol"]/div[1]/div[1]/div/div/h1')
        num_of_total_jobs = wait.until(EC.visibility_of_element_located(total_jobs_locator)).text.replace(f" {keyword.lower()} Jobs", "")
        JOBS = int(num_of_total_jobs)
        if JOBS < num_jobs:
            num_jobs = JOBS
        print(f'Num of total jobs: {num_of_total_jobs}')
    except WebDriverException as e:
        print(e, "e1")
        return "Break"





    num_of_job_in_page = 0  # In every page there has 30 jobs
    currentPage = 0
    # currentPage = 0
    j = int(1)  # for creating a files


    try:
        print(currentPage)
        next_page_locator = (By.CSS_SELECTOR, '[alt="next-icon"]')
        next_page_element = wait.until(EC.element_to_be_clickable(next_page_locator))
        next_page_element.click()
        # print("Next page!")
    except NoSuchElementException:
        df = pd.DataFrame(jobs)
        return df
    except Exception as e:
        pass
        # print("An exception occurred while clicking the next page button:", str(e))

    page_counter = 0
    while num_jobs > len(jobs):
        print("Entering page number:", currentPage + 1)
        page_counter += 1
        if page_counter == 34:
            df = pd.DataFrame(jobs)
            return df

        # Test for the "Sign Up" prompt and get rid of it.
        try:
            driver.find_element_by_class_name("selected").click()
        except ElementClickInterceptedException as e:
            # print(e, "e2")
            pass

        time.sleep(3)
        list_elements = WebDriverWait(driver, 3).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'ul.hover li.react-job-listing')))
        # print(list_elements)


        for i, element in enumerate(list_elements):

            # Check if the number of jobs that collected is below the number we want or below the number of the total jobs
            if len(jobs) >= num_jobs:
                print(f"Progress stop because the number of jobs in the website is over :)"
                      f"\nNumber of jobs in the website:{num_of_total_jobs} Number of jobs scraped:{len(jobs)}")
                break

            if num_of_job_in_page == 30:  # here we will stop and move to the next page
                break

            try:
                div_element = element.find_element(By.TAG_NAME, 'div')
                job_button = div_element.find_element(By.TAG_NAME, 'a')
                job_button.click()
                # print("##job click##")
            except Exception as e:
                pass
                # print(e, 'e2.1')


            if i % 1 == 0:  # because each post has 3 links
                now = datetime.now()  # for testing
                is_remote = False
                num_of_job_in_page += 1  # 1/30

                print(f"\nProgress: {len(jobs) + 1}/{num_jobs} in page number: {currentPage + 1}")


                try:
                    job_button.click()  # Click on the next post in the list
                    # print("--job click--")
                except Exception as e:
                    counter_break += 1
                    # print(f"counter_break = {counter_break}\n"
                    #       f"ERROR = {e}"
                    #       f"ERROR number = e3")
                    if counter_break == 50:
                        print(f"Process stop before reaching the target of jobs {len(jobs)}/{num_jobs}")
                        df = pd.DataFrame(jobs)
                        return df
                    else:
                        pass



                try:
                    show_more_button_locator = (By.XPATH, '//*[@id="JobDescriptionContainer"]/div[2]')
                    show_more_button = wait.until(EC.element_to_be_clickable(show_more_button_locator))
                    show_more_button.click()

                    try:
                        job_description_locator = (By.XPATH, '//*[@id="JobDescriptionContainer"]')
                        job_description = wait.until(EC.visibility_of_element_located(job_description_locator))
                        text = job_description.text

                        years_of_experience = ets.nlp_for_years_of_experience(text)
                        education = ets.extract_education(text)
                        position = ets.extract_position_level(text)

                        doc = False
                        if doc:
                            with open(f"raw text/row_text_{keyword}{j}.txt",
                                      'w') as f:  # for testing the 'extract' functions
                                j += 1
                                f.write(text)
                                f.write(
                                    f"\n\n\nTesting regine:"
                                    f"\nExperience: {years_of_experience}"
                                    f"\nEducation: {education}"
                                    # f"\nPosition Level: {position_level}"
                                    f"\n Time of Scrape: {now}")

                    except Exception as e:
                        years_of_experience = -1
                        education = -1
                        position = -1
                        # print(f"e4 , Attempting to scrape the text did not worked  {str(e)} ")


                except Exception as e:
                    years_of_experience = -1
                    education = -1
                    position = -1
                    # print(f"e5!{str(e)}")



                try:
                    company_name_locator = (By.XPATH, '//div[@class="css-87uc0g e1tk4kwz1"]')
                    company_name_element = wait.until(EC.visibility_of_element_located(company_name_locator))
                    company_name = company_name_element.text

                except:
                    # print("Failed to collect company name!")
                    company_name = int(-1)


                try:
                    job_title_locator = (By.CSS_SELECTOR, "div[data-test='jobTitle']")
                    job_title_element = wait.until(EC.visibility_of_element_located(job_title_locator))
                    job_title = job_title_element.text
                except:
                    # print("Failed to collect job title!")
                    job_title = int(-1)


                try:
                    location_locator = (By.CSS_SELECTOR, "div[data-test='location']")
                    location_element = wait.until(EC.visibility_of_element_located(location_locator))
                    location = location_element.text
                    if "Remote" in location:
                        is_remote = True
                except:
                    # print("Failed to collect location!")
                    location = int(-1)


                try:
                    job_rating_locator = (By.CSS_SELECTOR, "span[data-test='detailRating']")
                    job_rating_element = wait.until(EC.visibility_of_element_located(job_rating_locator))
                    job_rating = job_rating_element.text
                except:
                    # print("Failed to collect job Rating!")
                    job_rating = int(-1)

                try:
                    rating_elements_locator = (By.CSS_SELECTOR, "span.css-a7hxlj.erz4gkm1")
                    rating_elements = wait.until(EC.presence_of_all_elements_located(rating_elements_locator))

                    career_opportunities = rating_elements[1].text
                    comp_and_benefits = rating_elements[3].text
                    culture_and_values = rating_elements[5].text
                    senior_management = rating_elements[7].text
                    work_life_balance = rating_elements[9].text

                except Exception as e:
                    career_opportunities = comp_and_benefits = culture_and_values = senior_management = work_life_balance = int(-1)
                    # print(e, "e6")


                try:
                    salaries_locator = (By.XPATH, '//div[@class="css-1bluz6i e2u4hf13"]')
                    salaries_element = wait.until(EC.visibility_of_element_located(salaries_locator))
                    salaries = salaries_element.text
                except TimeoutException:
                    # print("Failed to collect Salary Estimate!")
                    salaries = int(-1)
                    pass

                try:
                    company_overview_button_locator = (By.CSS_SELECTOR, 'h2.css-1r0ltbv.e9b8rvy0')
                    company_overview_button = wait.until(EC.element_to_be_clickable(company_overview_button_locator))
                    company_overview_button.click()

                    try:
                        size_locator = (By.XPATH, '//div[@class="d-flex justify-content-start css-rmzuhb e1pvx6aw0"]//span[text()="Size"]/following-sibling::span')
                        size_element = wait.until(EC.visibility_of_element_located(size_locator))
                        size = size_element.text
                    except NoSuchElementException:
                        size = -1
                        # print("Failed to collect company size!")

                    try:
                        founded_locator = (By.XPATH, '//span[text()="Founded"]/following-sibling::span')
                        founded_element = wait.until(EC.visibility_of_element_located(founded_locator))
                        founded = founded_element.text
                    except NoSuchElementException:
                        founded = int(-1)
                        # print("Failed to collect founded date!")

                    try:
                        type_of_ownership_locator = (By.XPATH, '//div[@class="d-flex justify-content-start css-rmzuhb e1pvx6aw0"]//span[text()="Type"]/following-sibling::span')
                        type_of_ownership_element = wait.until(EC.visibility_of_element_located(type_of_ownership_locator))
                        type_of_ownership = type_of_ownership_element.text
                    except NoSuchElementException:
                        type_of_ownership = int(-1)
                        # print("Failed to collect type of ownership!")

                    try:
                        industry_locator = (By.XPATH, '//div[@class="d-flex justify-content-start css-rmzuhb e1pvx6aw0"]//span[text()="Industry"]/following-sibling::span')
                        industry_element = wait.until(EC.visibility_of_element_located(industry_locator))
                        industry = industry_element.text
                    except NoSuchElementException:
                        industry = int(-1)
                        # print("Failed to collect industry!")

                    try:
                        sector_locator = (By.XPATH, '//div[@class="d-flex justify-content-start css-rmzuhb e1pvx6aw0"]//span[text()="Sector"]/following-sibling::span')
                        sector_element = wait.until(EC.visibility_of_element_located(sector_locator))
                        sector = sector_element.text
                    except NoSuchElementException:
                        sector = int(-1)
                        # print("Failed to collect sector!")

                    try:
                        revenue_locator = (By.XPATH, '//div[@class="d-flex justify-content-start css-rmzuhb e1pvx6aw0"]//span[text()="Revenue"]/following-sibling::span')
                        revenue_element = wait.until(EC.visibility_of_element_located(revenue_locator))
                        revenue = revenue_element.text
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
                             "Education": education,
                             "Position": position,
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

        # move to the next page
        try:


            # Save the current page URL
            current_url = driver.current_url

            next_page_locator = (By.CSS_SELECTOR, '[alt="next-icon"]')
            next_page_element = wait.until(EC.element_to_be_clickable(next_page_locator))
            next_page_element.click()
            time.sleep(3)

            # Check the new page URL
            new_url = driver.current_url
            if new_url != current_url:
                pass
                # print("Next page!")
            else:
                pass
                # print("Failed to move to the next page")

            # print(curr_page)
            currentPage += 1
            num_of_job_in_page = 0
            time.sleep(1)
        except NoSuchElementException:
            df = pd.DataFrame(jobs)
            return df
        except Exception as e:
            pass
            # print("An exception occurred while clicking the next page button:", str(e))





    df = pd.DataFrame(jobs)
    return df