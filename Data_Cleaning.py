import pandas as pd


def data_cleaning(df1):
    df = df1.copy()

    if 'Salary Estimate' in list(df):
        df = df[df['Salary Estimate'] != -1]
    elif 'Annual Salary' in list(df):
        df = df[df['Annual Salary'] != -1]
    else:
        return None

    def hourly_to_annual(salary):
        return round(float(salary * 2080), 2)  # assuming 40 hours/week and 52 weeks/year

    def monthly_to_annual(salary):
        return round(float(salary * 12), 2)

    def company_size_scale(company_size):
        if company_size == "Unknown" or company_size == -1:
            return -1
        elif company_size == "1 to 50 Employees":
            return 1
        elif company_size == "51 to 200 Employees":
            return 2
        elif company_size == "201 to 500 Employees":
            return 3
        elif company_size == "501 to 1000 Employees":
            return 4
        elif company_size == "1001 to 5000 Employees":
            return 5
        elif company_size == "5001 to 10000 Employees":
            return 6
        elif company_size == "10000+ Employees":
            return 7
        else:
            return -1  # return -1 for any other unknown values

    def revenue_scale(revenue):
        if revenue == "Unknown / Non-Applicable" or revenue == -1:
            return -1
        elif revenue == "Less than $1 million (USD)":
            return 1
        elif revenue == "$1 to $5 million (USD)":
            return 2
        elif revenue == "$5 to $25 million (USD)":
            return 3
        elif revenue == "$25 to $50 million (USD)" or revenue == '$25 to $100 million (USD)':
            return 4
        elif revenue == "$50 to $100 million (USD)":
            return 5
        elif revenue == "$100 to $500 million (USD)":
            return 6
        elif revenue == "$500 million to $1 billion (USD)" or revenue == "$1 to $2 billion (USD)" or revenue == '$1 to $5 billion (USD)':
            return 7
        elif revenue == "$2 to $5 billion (USD)" or revenue == "$5 to $10 billion (USD)":
            return 8
        elif revenue == "$10+ billion (USD)":
            return 9
        else:
            return -1  # return -1 for any other unknown values

    df["Revenue Scale"] = df["Revenue"].apply(revenue_scale)

    # Convert the 'Company Size' to 'Company Size Scal'
    df["Company Size Scale"] = df["Company Size"].apply(company_size_scale)

    # Remove (est.)
    try:
        df["Time Unit"] = df["Salary Estimate"].apply(lambda x: x.split(' ')[1])
    except Exception as e:
        print(e, "e1")

    # Add more columns to calculate the salary
    try:
        df["Time Unit"] = df["Time Unit"].apply(lambda x: x.split('/')[1])
    except Exception as e:
        print(e, "e2")

    # Split the "Salary Estimate" column by the '/' separator and extract the first element
    try:
        df["Salary Estimate"] = df["Salary Estimate"].apply(lambda x: (x.split('/')[0]))
    except Exception as e:
        print(e, "e3")

    # Remove the dollar sign ($) from the "Salary Estimate" column
    try:
        df["Salary Estimate"] = df["Salary Estimate"].apply(lambda x: x.split('$')[1])
    except Exception as e:
        print(e, "e4")

    # Remove any commas from the "Salary Estimate" column
    try:
        df["Salary Estimate"] = df["Salary Estimate"].apply(lambda x: x.replace(',', ''))
    except Exception as e:
        print(e, "e5")

    # Convert the "Salary Estimate" column to float data type
    try:
        df["Salary Estimate"] = df["Salary Estimate"].apply(lambda x: float(x))
    except Exception as e:
        print(e, "e6")

    # Convert hourly salaries to annual salaries
    try:
        df.loc[df['Time Unit'] == 'hr', 'Salary Estimate'] = df.loc[df['Time Unit'] == 'hr', 'Salary Estimate'].apply(
            hourly_to_annual)
    except Exception as e:
        print(e, "e7")

    # Convert monthly salaries to annual salaries
    try:
        df.loc[df['Time Unit'] == 'mo', 'Salary Estimate'] = df.loc[df['Time Unit'] == 'mo', 'Salary Estimate'].apply(
            monthly_to_annual)
    except Exception as e:
        print(e, "e8")

    try:
        df.drop('Time Unit', axis=1, inplace=True)
        df.rename(columns={"Salary Estimate": "Annual Salary"}, inplace=True)
    except Exception as e:
        print(e, "e8")

    # Drop the rating from the company name
    try:
        df['Company Name'] = df['Company Name'].apply(lambda x: x.split('\n')[0])
    except Exception as e:
        print(e, "e9")

    # Convert the 'Founded' to 'Company Old'
    try:
        df['Founded'] = df['Founded'].apply(lambda x: -1 if x == -1 else int(x))
        df['Company Old'] = df['Founded'].apply(lambda x: x if x == -1 else 2023 - x)
        df.insert(9, 'Company Old', df.pop('Company Old'))  # insert it into a specific index
    except Exception as e:
        print(e, "e10")

    # Convert 'Is Remote' to 0/1
    try:
        df['Is Remote'] = df['Is Remote'].astype(int)
    except Exception as e:
        print(e, "e11")

    df = df.reindex(
        columns=['Job Title', 'Annual Salary', 'Experience', 'Education', 'Position', 'Location',
                 'Is Remote', 'Company Size', 'Company Size Scale', 'Founded', 'Company Old', 'Industry', 'Sector',
                 'Revenue', 'Revenue Scale', 'Type of Ownership', 'Rating', 'Career Opportunities', 'Comp & Benefits',
                 'Culture & Values', 'Senior Management', 'Work Life Balance', 'Company Name', 'Time of Scrape'])

    df = pd.DataFrame(df)
    return df


def final_clean(df):
    my_list = list(df)

    print("Entering Final Clean")
    df = pd.DataFrame(df)
    if "Company Name" in my_list:
        df.drop("Company Name", inplace=True, axis=1)
    if "Location" in my_list:
        df.drop("Location", inplace=True, axis=1)
    if "Company Size" in my_list:
        df.drop("Company Size", inplace=True, axis=1)
    if "Founded" in my_list:
        df.drop("Founded", inplace=True, axis=1)
    if "Industry" in my_list:
        df.drop("Industry", inplace=True, axis=1)
    if "Sector" in my_list:
        df.drop("Sector", inplace=True, axis=1)
    if "Revenue" in my_list:
        df.drop("Revenue", inplace=True, axis=1)
    if "Type of Ownership" in my_list:
        df.drop("Type of Ownership", inplace=True, axis=1)
    if "Time of Scrape" in my_list:
        df.drop("Time of Scrape", inplace=True, axis=1)


    df_copy = df.copy()

    df_copy = df_copy[df_copy['Education'] != -1]
    df_copy = df_copy[df_copy['Experience'] != -1]
    df_copy = df_copy[df_copy['Position'] != -1]



    return df_copy
