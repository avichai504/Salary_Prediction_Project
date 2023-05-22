import re
import spacy
def extract_years_of_experience(job_description):
    pattern = r"\b(at least )?(?!.*years\s+old.*)([0-9]+\+?|(one|two|three|four|five|six|seven|eight|nine|ten))\s+(year|years|years'|ye|ya|Y)\s?(?!old)(\s+of\s+)?\b"

    # Search for the pattern in the job description
    match = re.search(pattern, job_description, re.IGNORECASE)

    if match:
        # Extract the number of years from the match object
        years_of_experience_str = match.group(2).split('+')[0]
        if years_of_experience_str.isdigit():
            years_of_experience = int(years_of_experience_str)
        else:
            # convert word to digit
            words_to_digits = {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5,
                               "six": 6, "seven": 7, "eight": 8, "nine": 9, "ten": 10}

            years_of_experience = words_to_digits[years_of_experience_str]
        if years_of_experience_str < 12:
            return years_of_experience
    else:
        # If no match is found, return -1
        return int(-1)


def extract_education(job_description):  #  { 0:high school, 1:bachelor, 2:m_degree, 3:doctor}

    keywords_high_school = ["high school, highschool, high-school "]

    keywords_bachelor = ["bachelor", "bachelor's", "bs", "b.s.", "b.sc.", "b.sc", "b sc", "bachelor of science",
                         "baccalaureate", "computer science"]
    keywords_master = ["master", "master's", "ms", "m.s.", "m sc", "m.sc.", "m.sc", "master of science", "m.a.", "ma",
                       "master of arts", "m.eng", "meng", "master of engineering", "m.ed", "med", "master of education",
                       "m.b.a", "mba", "master of business administration", "m.f.a.", "mfa", "master of fine arts",
                       "m.j.", "mj", "master of journalism", "m.p.h.", "mph", "master of public health", "m.s.w.",
                       "msw", "master of social work"]
    keywords_doctor = ["doctor", "phd", "ph.d.", "dr", "d.r.", "d.phil.", "doctor of philosophy", "ed.d", "edd",
                       "doctor of education", "j.d.", "jd", "doctor of law", "m.d.", "md", "doctor of medicine",
                       "d.v.m.", "dvm", "doctor of veterinary medicine", "d.d.s.", "dds", "doctor of dental surgery",
                       "d.n.p.", "dnp", "doctor of nursing practice", "d.p.t.", "dpt", "doctor of physical therapy",
                       "psy.d", "psyd", "doctor of psychology"]


    if any(word in job_description.lower() for word in keywords_high_school):
        return int(0)
    if any(word in job_description.lower() for word in keywords_bachelor):
        return int(1)
    if any(word in job_description.lower() for word in keywords_master):
        return int(2)
    if any(word in job_description.lower() for word in keywords_doctor):
        return int(3)
    return int(-1)


def extract_position_level(job_description):  #{junior: 0, senior:1}
    junior_regex = r"\b(Junior|Jr\.|Jnr\.|Entry-level|Assistant|Trainee|Associate|Apprentice|Freshman|Newcomer|Rookie|Junior-level|Junior-level position|Junior role|Junior position|Junior team member|Junior staff member|Junior employee|Junior member|Junior assistant|Junior trainee)\b"
    senior_regex = r"\b(Senior|Sr\.|Snr\.|Lead|Principal|Director|Manager|Executive|Chief|Head|Expert|Specialist|Consultant)\b"

    match_ju = re.search(junior_regex, job_description, re.IGNORECASE)
    match_se = re.search(senior_regex, job_description, re.IGNORECASE)

    if match_ju:
        return int(0)
    if match_se:
        return int(1)
    else:
        return int(-1)




def nlp_for_years_of_experience(job_description):
    # number = -1

    nlp = spacy.load("en_core_web_sm")

    text = job_description
    # perform NER on the text
    doc = nlp(text)
    experience = 0
    # look for entities that might indicate years of experience
    for ent in doc.ents:
        text = ent.text.lower()
        if "year" in text or "yr" in text:
            # see if the entity text contains numbers and/or years of experience patterns
            if any(char.isdigit() for char in text) or "experience" in text or "exp" in text:
                # print(ent.text)
                try:
                    number = ent.text.split()
                    number = number[0]
                    if int(number) > 12:
                        continue
                except:
                    pass

                try:
                    number = ent.text.split("-")
                    number = number[-1]
                except:
                    pass

                try:
                    number = int(''.join(filter(str.isdigit, number)))
                except Exception as e:
                    pass

                if 12 > int(number) > experience:
                    experience = number
    return experience






