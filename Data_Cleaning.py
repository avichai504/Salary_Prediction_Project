import pandas as pd

from sklearn.preprocessing import StandardScaler


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


def data_cleaning(df1):
    df = df1.copy()
    df = df[df['Salary Estimate'] != -1].copy()

    # Remove (est.)
    try:
        df["Time Unit"] = df["Salary Estimate"].apply(lambda x: x.split(' ')[1])
    except Exception as e:
        pass
        # print(e, "e1")

    # Add more columns to calculate the salary
    try:
        df["Time Unit"] = df["Time Unit"].apply(lambda x: x.split('/')[1])
    except Exception as e:
        pass
        # print(e, "e2")

    # Split the "Salary Estimate" column by the '/' separator and extract the first element
    try:
        df["Annual Salary"] = df["Salary Estimate"].apply(lambda x: (x.split('/')[0]))
    except Exception as e:
        pass
        # print(e, "e3")

    # Remove the dollar sign ($) from the "Salary Estimate" column
    try:
        df["Annual Salary"] = df["Annual Salary"].apply(lambda x: x.split('$')[1])
    except Exception as e:
        pass
        # print(e, "e4")

    # Remove any commas from the "Salary Estimate" column
    try:
        df["Annual Salary"] = df["Annual Salary"].apply(lambda x: x.replace(',', ''))
    except Exception as e:
        pass
        # print(e, "e5")

    # Convert the "Salary Estimate" column to a float data type
    try:
        df["Annual Salary"] = df["Annual Salary"].apply(lambda x: float(x))
    except Exception as e:
        pass
        # print(e, "e6")

    # Convert hourly salaries to annual salaries
    try:
        df.loc[df['Time Unit'] == 'hr', 'Annual Salary'] = df.loc[df['Time Unit'] == 'hr', 'Annual Salary'].apply(
            hourly_to_annual)
    except Exception as e:
        pass
        # print(e, "e7")

    # Convert monthly salaries to annual salaries
    try:
        df.loc[df['Time Unit'] == 'mo', 'Annual Salary'] = df.loc[df['Time Unit'] == 'mo', 'Annual Salary'].apply(
            monthly_to_annual)
    except Exception as e:
        pass
        # print(e, "e8")

    try:
        df['Company Name'] = df['Company Name'].apply(lambda x: x.split('\n')[0])
    except Exception as e:
        pass
        # print(e, "e9")

    # Convert the 'Founded' to 'Company Old'
    try:
        df['Founded'] = df['Founded'].apply(lambda x: -1 if x == -1 else int(x))
        df['Company Old'] = df['Founded'].apply(lambda x: x if x == -1 else 2023 - x)
        df.insert(9, 'Company Old', df.pop('Company Old'))  # insert it into a specific index
    except Exception as e:
        pass
        # print(e, "e10")

    # Convert 'Is Remote' to 0/1
    try:
        df['Is Remote'] = df['Is Remote'].astype(int)
    except Exception as e:
        pass
        # print(e, "e11")

    desired_columns = ['Salary Estimate', 'Annual Salary']
    df = df.reindex(columns=desired_columns + [col for col in df.columns if col not in desired_columns])

    # make location only two characters or Remote
    try:
        # print(df.dtypes)
        df['Location'] = df['Location'].fillna('')
        df['Location'] = df['Location'].apply(lambda x: x.split(',')[-1])
    except Exception as e:
        print(e, 'e location')

    df = pd.DataFrame(df)
    return df


def preprocess_scaling(df):  # Not fit for the ML model!!!
    # Preprocess the 'Type of Ownership' column
    ownership_mapping = {
        'Company - Private': int(1),
        '-1': None,  # Missing value
        'Company - Public': int(2),
        'Private Practice / Firm': int(3),
        'Unknown': None,  # Missing value
        'Subsidiary or Business Segment': int(4),
        'Nonprofit Organization': int(5)
    }
    df['Type of Ownership Scale'] = df['Type of Ownership'].map(ownership_mapping)

    # Preprocess the 'Sector' column
    sector_mapping = {
        "Unknown / Non-Applicable / -1": None,
        'Information Technology': 1,
        'Media & Communication': 2,
        'Financial Services': 3,
        'Aerospace & Defense': 4,
        'Manufacturing': 5,
        'Management & Consulting': 6,
        'Agriculture': 7,
        'Pharmaceutical & Biotechnology': 8,
        'Human Resources & Staffing': 9,
        'Insurance': 10,
        'Education': 11,
        'Retail & Wholesale': 12,
        'Transportation & Logistics': 13,
        'Healthcare': 14,
        'Personal Consumer Services': 15,
        'Construction, Repair & Maintenance Services': 16,
        'Energy, Mining & Utilities': 17,
        'Telecommunications': 18,
        'Real Estate': 19,
        'Nonprofit & NGO': 20,
        'Government & Public Administration': 21,

    }
    df['Sector Scale'] = df['Sector'].map(sector_mapping)

    # Preprocess the 'Company Size' column
    company_size_mapping = {
        "Unknown / Non-Applicable": None,
        "-1": None,
        "1 to 50 Employees": int(1),
        "51 to 200 Employees": int(2),
        "201 to 500 Employees": int(3),
        "501 to 1000 Employees": int(4),
        "1001 to 5000 Employees": int(5),
        "5001 to 10000 Employees": int(6),
        "10000+ Employees": int(7)
    }
    df["Company Size Scale"] = df["Company Size"].map(company_size_mapping)

    # Preprocess the 'Revenue' column
    revenue_mapping = {
        "Unknown / Non-Applicable / -1": None,
        "Less than $1 million (USD)": 1,
        "$1 to $5 million (USD)": 2,
        "$5 to $25 million (USD)": 3,
        "$25 to $50 million (USD)": 4,
        "$50 to $100 million (USD)": 5,
        "$100 to $500 million (USD)": 6,
        "$500 million to $1 billion (USD)": 7,
        "$1 to $2 billion (USD)": 7,
        "$1 to $5 billion (USD)": 7,
        "$2 to $5 billion (USD)": 8,
        "$5 to $10 billion (USD)": 8,
        "$10+ billion (USD)": 9
    }
    df["Revenue Scale"] = df["Revenue"].map(revenue_mapping)

    industry_mapping = {
        "Unknown / Non-Applicable / -1": None,
        'Internet & Web Services': 1,
        'HR Consulting': 2,
        'Information Technology Support Services': 3,
        'Municipal Agencies': 4,
        'Machinery Manufacturing': 5,
        'Architectural & Engineering Services': 6,
        'Enterprise Software & Network Solutions': 7,
        'Home Furniture & Housewares Stores': 8,
        'Advertising & Public Relations': 9,
        'Construction': 10,
        'Car & Truck Rental': 11,
        'Computer Hardware Development': 12,
        'Financial Transaction Processing': 13,
        'Banking & Lending': 14,
        'Biotech & Pharmaceuticals': 15,
        'Business Consulting': 16,
        'Airlines, Airports & Air Transportation': 17,
        'Transportation Equipment Manufacturing': 18,
        'Software Development': 19,
        'Stock Exchanges': 20,
        'Aerospace & Defense': 21,
        'Video Game Publishing': 22,
        'Insurance Carriers': 23,
        'Taxi & Car Services': 24,
        'Health Care Services & Hospitals': 25,
        'Energy & Utilities': 26,
        'Electronics Manufacturing': 27,
        'Film Production': 28,
        'Shipping & Trucking': 29,
        'Telecommunications Services': 30,
        'Accounting & Tax': 31,
        'Consumer Product Manufacturing': 32,
        'Staffing & Subcontracting': 33,
        'Real Estate': 34,
        'Education & Training Services': 35,
        'Investment & Asset Management': 36,
        'Grantmaking & Charitable Foundations': 37,
        'Animal Production': 38,
        'Colleges & Universities': 39,
        'Food & Beverage Stores': 40,
        'Insurance Agencies & Brokerages': 41,
        'State & Regional Agencies': 42,
        'Beauty & Wellness': 43
    }
    df["Industry Sector"] = df["Industry"].map(industry_mapping)

    # df["Revenue Scale"] = df["Revenue"].apply(revenue_scale)
    # df["Company Size Scale"] = df["Company Size"].apply(company_size_scale)

    return df


def column_unique_values(df1, df2, df3, df4, df5, column_name, keyword):
    concatenated_column = pd.concat(
        [df1[column_name], df2[column_name], df3[column_name], df4[column_name], df5[column_name]])

    unique_values = concatenated_column.unique()
    str_unique = ''
    for i, unique in enumerate(unique_values):
        str_unique += unique
        if i % 5 == 0:
            str_unique += '\n'
        else:
            str_unique += ','

    with open(f"unique_values_'{column_name}'_in_'{keyword}'.txt", 'w') as f:
        f.write(str_unique)
        f.write(f"\n\nThe number of unique values is {len(unique_values)}")


def one_hot_encoding(df, column_names):
    df_encoded = pd.get_dummies(df, columns=column_names)
    # df_encoded.to_csv(f"one_hot_encoding{0}.csv")
    return df_encoded


def final_clean(df):  # call this function after one-hot encoding!
    columns = list(df)

    if 'Salary Estimate' in columns:
        df.drop('Salary Estimate', axis=1, inplace=True)
    if 'Company Name' in columns:
        df.drop('Company Name', axis=1, inplace=True)
    if '<null>' in columns:
        df.drop('<null>', axis=1, inplace=True)
    if 'null' in columns:
        df.drop('null', axis=1, inplace=True)
    if 'Company Size' in columns:
        df.drop('Company Size', axis=1, inplace=True)
    if 'Revenue' in columns:
        df.drop('Revenue', axis=1, inplace=True)
    if 'Time Unit' in columns:
        df.drop('Time Unit', axis=1, inplace=True)
    if 'Industry' in columns:
        df.drop('Industry', axis=1, inplace=True)
    if 'Sector' in columns:
        df.drop('Sector', axis=1, inplace=True)
    if 'Type of Ownership' in columns:
        df.drop('Type of Ownership', axis=1, inplace=True)
    if 'Time of Scrape' in columns:
        df.drop('Time of Scrape', axis=1, inplace=True)
    if 'Location' in columns:
        df.drop('Location', axis=1, inplace=True)
    if 'Unnamed: 0' in columns:
        df.drop('Unnamed: 0', axis=1, inplace=True)
    if 'Unnamed: 0.1' in columns:
        df.drop('Unnamed: 0.1', axis=1, inplace=True)
    if 'Founded' in columns:
        df.drop('Founded', axis=1, inplace=True)
    if 'Job Title' in columns:
        df.drop('Job Title', axis=1, inplace=True)
    if 'anonymous' in columns:
        df.drop('anonymous', axis=1, inplace=True)
    # df = df.loc[:, ~df.columns.str.contains('^anonymous')]

    print(f"The number of Duplicated = {df.duplicated().sum()}")
    df.drop_duplicates(keep='first', inplace=True)
    print(f"The final files = {df.shape} ")


    df = pd.DataFrame(df)
    return df

