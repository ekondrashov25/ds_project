import streamlit as st
import pandas as pd
import plotly.express as px
import pycountry
import numpy as np

# Set Streamlit page config for light theme
st.set_page_config(page_title="Data Science Salaries Analysis")

# Loading data
@st.cache_data
def load_data():
    df = pd.read_csv('ds_salaries.csv', sep=';')
    return df

df = load_data()

# Descriptive statistics
st.title("Data Science Salaries Analysis")

st.subheader('Importing libraries')
st.code('''
import pandas as pd
import plotly.express as px
import pycountry
''')

st.subheader('Data')
st.text('Loading data')
st.code('''
df = pd.read_csv('ds_salaries.csv', sep=';')
''')

st.subheader("Dataset Structure")
st.text('Let us have a look at dataset structure:')
st.code('''df.head()''')
st.write(df.head())

st.text("Looking for NaN data")
st.code('df.isna().sum()')
st.write(df.isna().sum())
st.write("From the results above we can see, that dataset does not have none cells which means that it is already **cleaned up**.")

st.subheader("Descriptive Statistics")
st.write("Checking the description of dataset and numeric columns:")
st.write(df.describe())

st.subheader("Salary in USD Description")
st.write("Checking the description of column `salary_in_usd`:")
st.write(df['salary_in_usd'].describe())
st.write("We got mean salary value in USD which ≈ $112 297")


st.write("Checking the description of col `job_title`:")
st.write("To get information about job titles I have to add numeric column for it:")

def convert_job_titles(title: str) -> int:
    job_titles_dict = {title: idx + 1 for idx, title in enumerate(df['job_title'].unique().tolist())}
    return job_titles_dict[title]

df['job_title_numeric'] = df['job_title'].apply(convert_job_titles)

st.code('''
def convert_job_titles(title: str) -> int:
    job_titles_dict = {title: idx + 1 for idx, title in enumerate(df['job_title'].unique().tolist())}
    return job_titles_dict[title]

df['job_title_numeric'] = df['job_title'].apply(convert_job_titles)
''')

st.code('''df.head()''')
st.write(df.head())


st.code('''
median_job_title = df['job_title_numeric'].median()
median_job_title
''')
median_job_title = df['job_title_numeric'].median()
st.write(median_job_title)

st.text('Let us create a  function to convert numeric value back:')

st.code('''
def convert_job_titles_to_text(title: int) -> str:
    job_titles_dict = {idx + 1: title for idx, title in enumerate(df['job_title'].unique().tolist())}
    return job_titles_dict[title]''')

def convert_job_titles_to_text(title: int) -> str:
    job_titles_dict = {idx + 1: title for idx, title in enumerate(df['job_title'].unique().tolist())}
    return job_titles_dict[title]



st.code('convert_job_titles_to_text(median_job_title)')
st.write(convert_job_titles_to_text(median_job_title))

st.write('It can be seen that on average the position of programmers in dataset is `Business Data Analyst`.')
st.code("df['employee_residence'].describe()")
st.write(df['employee_residence'].describe())
st.text('Now we know that the most popular residence for work is United States ')


st.write('Checking the description of column `remote_ratio:`')
st.write('''
- 0 No remote work 
- 50 Partially remote 
- 100 Fully remote
         ''')

st.code("df['remote_ratio'].value_counts()")
st.write(df['remote_ratio'].value_counts())
st.text('We can conclude that most of employees works remotely')


# Transforming data
st.subheader("Data Transformation")

st.write("Let us drop the column `salary_currency`. This information is redundant because it is more convenient to evaluate the salary in USD (which already exists in the dataset as a separate column `salary_in_usd`).")
st.code("df.drop(columns='salary_currency', inplace=True)")
df.drop(columns='salary_currency', inplace=True)

st.code('df.head()')
st.write(df.head())


st.write("Also let us drop the coloumn `salary`. As it was mentioned before I will evaluate the salary in USD.")
st.code("df.drop(columns='salary', inplace=True)")
df.drop(columns='salary', inplace=True)

st.code('df.head()')
st.write(df.head())

st.text('As you can see columns dropped successfully.')

st.write("In my dataset I have a column `employee_residence` which contains country name in ISO-3166 format. It will be used for the country plot which takes ISO-3 format of the country name. So I need to convert it to the desired format for proper handling.")


def convert_country_name(country_name: str) -> str:
    return pycountry.countries.get(alpha_2=country_name).alpha_3

st.code('''
def convert_country_name(country_name: str) -> str:
    return pycountry.countries.get(alpha_2=country_name).alpha_3
''')

st.code("df['employee_residence_iso_3'] = df['employee_residence'].apply(convert_country_name)")
df['employee_residence_iso_3'] = df['employee_residence'].apply(convert_country_name)
st.code('df.head()')
st.write(df.head())


st.write("We can see that there is a new column `employee_residence_iso_3` with the correct format.")


st.write("Let us convert columns `experience_level` and `employment_type` to more convenient to understand names.")


st.write('''`experience_level:`
- EN Junior 
- MI Intermediate 
- SE Expert 
- EX Director
''')
st.code("df['experience_level'].value_counts()")
st.write(df['experience_level'].value_counts())


st.write('''
`employment_type:`
- PT Part-time
- FT Full-time
- CT Contract
- FL Freelance
''')

st.code("df['employment_type'].value_counts()")
st.write(df['employment_type'].value_counts())

st.code('''

experience_level_mapping = {
    'EN': 'Junior',
    'MI': 'Middle',
    'SE': 'Senior',
    'EX': 'Director'
}

employment_type_mapping = {
    'PT': 'Part-time',
    'FT': 'Full-time',
    'CT': 'Contract',
    'FL': 'Freelance'
}


df['experience_level'] = df['experience_level'].replace(experience_level_mapping)
df['employment_type'] = df['employment_type'].replace(employment_type_mapping)
''')

# Convert experience_level and employment_type to more understandable names
experience_level_mapping = {
    'EN': 'Junior',
    'MI': 'Middle',
    'SE': 'Senior',
    'EX': 'Director'
}

employment_type_mapping = {
    'PT': 'Part-time',
    'FT': 'Full-time',
    'CT': 'Contract',
    'FL': 'Freelance'
}

df['experience_level'] = df['experience_level'].replace(experience_level_mapping)
df['employment_type'] = df['employment_type'].replace(employment_type_mapping)

st.code('df.head()')
st.write(df.head())
st.write("We can see that now we have all the modifications done correctly.")





# Simple Plots
st.subheader("Simple Plots")

# Salary Distribution
st.text("Distribution of employees' salary")
st.code('''
salaries_dist = px.box(
    df,
    x='salary_in_usd',
    title='Salary Distribution',
    labels={'remote_ratio': 'Salary (USD)'},
    template='plotly_white'
)

salaries_dist.update_traces(
    marker_color='blue',
)

salaries_dist.update_layout(
    title_font_size=16,
    xaxis_title='Salary (USD)',
    xaxis=dict(
        showgrid=True,  
        gridcolor='lightgray'  
    ),
    yaxis=dict(
        showgrid=True,  
        gridcolor='lightgray' 
    )
)
''')

salaries_dist = px.box(
    df,
    x='salary_in_usd',
    title='Salary Distribution',
    labels={'remote_ratio': 'Salary (USD)'},
    template='plotly_white'
)

salaries_dist.update_traces(
    marker_color='blue',
)

salaries_dist.update_layout(
    title_font_size=16,
    xaxis_title='Salary (USD)',
    xaxis=dict(
        showgrid=True,  
        gridcolor='lightgray'  
    ),
    yaxis=dict(
        showgrid=True,  
        gridcolor='lightgray' 
    )
)

st.plotly_chart(salaries_dist)

# Most Popular Positions
st.text("Now let's check the most popular positions of programmers in this dataset:")
st.code('''
experience_level = df['experience_level'].value_counts()
popular_positions = px.pie(
    values=experience_level,
    names=experience_level.index.to_list(),
    template='plotly_white'
)

popular_positions.update_layout(
    title='The most popular positions',
    width=600
)
''')

experience_level = df['experience_level'].value_counts()
popular_positions = px.pie(
    values=experience_level,
    names=experience_level.index.to_list(),
    template='plotly_white'
)

popular_positions.update_layout(
    title='The most popular positions',
    width=600
)

st.plotly_chart(popular_positions)

# Most Popular Countries
st.text("Now look for the most popular countries among programmers for work:")
st.code("df['employee_residence'].value_counts()")
st.write(df['employee_residence'].value_counts())

st.write("Since I have a lot of countries in which there are less than 5 programmers I will create a separate field for them called: `Other`")
st.code('''
country_counts = df['employee_residence_iso_3'].value_counts()
low_count_countries = country_counts[country_counts < 5].index
df['employee_residence_grouped'] = df['employee_residence_iso_3'].apply(lambda x: 'Less than 5 employees per country' if x in low_count_countries else x)

employee_residence = df['employee_residence_grouped'].value_counts()
top_countries = px.pie(
    values=employee_residence,
    names=employee_residence.index.to_list(),
    template='plotly_white'
)

top_countries.update_layout(
    title='Residence of work',
    width=600
)
''')

country_counts = df['employee_residence_iso_3'].value_counts()
low_count_countries = country_counts[country_counts < 5].index
df['employee_residence_grouped'] = df['employee_residence_iso_3'].apply(lambda x: 'Less than 5 employees per country' if x in low_count_countries else x)

employee_residence = df['employee_residence_grouped'].value_counts()
top_countries = px.pie(
    values=employee_residence,
    names=employee_residence.index.to_list(),
    template='plotly_white'
)

top_countries.update_layout(
    title='Residence of work',
    width=600
)

st.plotly_chart(top_countries)

# Salaries in Residence of Work Countries
st.text("Plot salaries in residence of work countries:")
st.code('''
aggregated_salaries = df.groupby('employee_residence_grouped')['salary_in_usd'].mean().reset_index()
salaries = px.bar(
    aggregated_salaries,
    x='employee_residence_grouped',
    y='salary_in_usd',
    template='plotly_white'
)
''')

aggregated_salaries = df.groupby('employee_residence_grouped')['salary_in_usd'].mean().reset_index()
salaries = px.bar(
    aggregated_salaries,
    x='employee_residence_grouped',
    y='salary_in_usd',
    template='plotly_white'
)

st.plotly_chart(salaries)

# Salary Change from 2020 to 2022
st.text("Plot salary change from 2020 to 2022:")
st.code('''
salary_by_year = df.groupby('work_year')['salary_in_usd'].mean().reset_index()
salaries = px.line(
    salary_by_year,
    x='work_year',
    y='salary_in_usd',
    title='Average Salary Change from 2020 to 2022',
    labels={'work_year': 'Year', 'salary_in_usd': 'Average Salary (USD)'},
    markers=True,
    template='plotly_white'
)

salaries.update_layout(
    title_font_size=18,
    xaxis_title='Year',
    yaxis_title='Average Salary (USD)',
    xaxis=dict(
        tickmode='linear',
        dtick=1
    ),
)
''')

salary_by_year = df.groupby('work_year')['salary_in_usd'].mean().reset_index()
salaries = px.line(
    salary_by_year,
    x='work_year',
    y='salary_in_usd',
    title='Average Salary Change from 2020 to 2022',
    labels={'work_year': 'Year', 'salary_in_usd': 'Average Salary (USD)'},
    markers=True,
    template='plotly_white'
)

salaries.update_layout(
    title_font_size=18,
    xaxis_title='Year',
    yaxis_title='Average Salary (USD)',
    xaxis=dict(
        tickmode='linear',
        dtick=1
    ),
)

st.plotly_chart(salaries)
st.write("On the graph we can see a **slight increase** in salaries during the years.")

# Salary Distribution by Company Size
st.subheader("Salary distribution by company size")
st.write("We have 3 types of companies:")
st.write("* **L** - large company (more than 250 employees)")
st.write("* **M** - medium company (from 50 to 250 employees)")
st.write("* **S** - small company (up to 50 employees)")
st.code('''
filtered_companies_by_size = df.groupby('company_size')['salary_in_usd'].median()
salaries_dist_violin = px.violin(
    df,
    x='company_size',
    y='salary_in_usd',
    title="Salary Distribution by Company Size",
    labels={'company_size': 'Company Size', 'salary_in_usd': 'Salary (USD)'},
    box=True,
    points="all",
    template='plotly_white'
)

salaries_dist_violin.update_layout(
    xaxis=dict(
        categoryorder='array',
        categoryarray=['S', 'M', 'L']
    )
)
''')

filtered_companies_by_size = df.groupby('company_size')['salary_in_usd'].median()
salaries_dist_violin = px.violin(
    df,
    x='company_size',
    y='salary_in_usd',
    title="Salary Distribution by Company Size",
    labels={'company_size': 'Company Size', 'salary_in_usd': 'Salary (USD)'},
    box=True,
    points="all",
    template='plotly_white'
)

salaries_dist_violin.update_layout(
    xaxis=dict(
        categoryorder='array',
        categoryarray=['S', 'M', 'L']
    )
)

st.plotly_chart(salaries_dist_violin)
st.write("- Maximum median of salary is in M companies")
st.write("- Maximum of salary reached in L companies")
st.write("- Maximum people with median salary in S companies")

# Detailed Overview via Complex Plots
st.subheader("Detailed Overview via Complex Plots")
st.write("More informative plot of distribution of programmers by `experience_level`, `employment_type` and `job_title`:")

# Sunburst Plot
st.subheader("Sunburst Plot")
st.code('''
sunburst_plot = px.sunburst(
    df,
    path=['experience_level', 'employment_type', 'job_title'],
    values='salary_in_usd',
    color='salary_in_usd',
    color_continuous_scale='RdBu',
    title='Salaries by Experience, Employment Type, and Job Title',
    width=1000,
    height=800,
    template='plotly_white'
)
''')

sunburst_plot = px.sunburst(
    df,
    path=['experience_level', 'employment_type', 'job_title'],
    values='salary_in_usd',
    color='salary_in_usd',
    color_continuous_scale='RdBu',
    title='Salaries by Experience, Employment Type, and Job Title',
    width=1000,
    height=800,
    template='plotly_white'
)

st.plotly_chart(sunburst_plot)

# Salary Distribution by Experience Level and Remote Ratio
st.subheader("Salary Distribution by Experience Level and Remote Ratio")
st.code('''
salaries_dist_2 = px.box(
    df,
    x='experience_level',
    y='salary_in_usd',
    color='employment_type',
    facet_col='remote_ratio',
    title='Salary Distribution by Experience Level and Remote Ratio',
    labels={'experience_level': 'Experience Level', 'salary_in_usd': 'Salary (USD)', 'employment_type': 'Employment Type'},
    template='plotly_white'
)

salaries_dist_2.update_layout(
    xaxis=dict(
        categoryorder='array',
        categoryarray=['Junior', 'Middle', 'Senior', 'Director']
    )
)
''')

salaries_dist_2 = px.box(
    df,
    x='experience_level',
    y='salary_in_usd',
    color='employment_type',
    facet_col='remote_ratio',
    title='Salary Distribution by Experience Level and Remote Ratio',
    labels={'experience_level': 'Experience Level', 'salary_in_usd': 'Salary (USD)', 'employment_type': 'Employment Type'},
    template='plotly_white'
)

salaries_dist_2.update_layout(
    xaxis=dict(
        categoryorder='array',
        categoryarray=['Junior', 'Middle', 'Senior', 'Director']
    )
)

st.plotly_chart(salaries_dist_2)
st.write("Employees who have `remote_ratio = 0` (work from office) mostly work Full-Time.")

# 3D Scatter Plot
st.text("Let us view this graphs in 3D")
st.code('''
salaries_dist_2_cube = px.scatter_3d(
    df,
    x='remote_ratio',
    y='salary_in_usd',
    z='experience_level',
    color='experience_level',
    size='salary_in_usd',
    title='Salary vs Remote Ratio and Experience Level',
    labels={'remote_ratio': 'Remote Ratio (%)', 'salary_in_usd': 'Salary (USD)', 'experience_level': 'Experience Level'},
    width=1200,
    height=800,
    template='plotly_white'
)

salaries_dist_2_cube.update_layout(
    scene=dict(
        zaxis=dict(
            categoryorder='array',
            categoryarray=['Junior', 'Middle', 'Senior', 'Director']
        )
    )
)
''')

salaries_dist_2_cube = px.scatter_3d(
    df,
    x='remote_ratio',
    y='salary_in_usd',
    z='experience_level',
    color='experience_level',
    size='salary_in_usd',
    title='Salary vs Remote Ratio and Experience Level',
    labels={'remote_ratio': 'Remote Ratio (%)', 'salary_in_usd': 'Salary (USD)', 'experience_level': 'Experience Level'},
    width=1200,
    height=800,
    template='plotly_white'
)

salaries_dist_2_cube.update_layout(
    scene=dict(
        zaxis=dict(
            categoryorder='array',
            categoryarray=['Junior', 'Middle', 'Senior', 'Director']
        )
    )
)

st.plotly_chart(salaries_dist_2_cube)

# Distribution of Employees Residence on Heat-map
st.text("Distribution of Employees Residence on Heat-map")
st.code('''
employee_residence = df[df['employee_residence_grouped'] != 'Less than 5 employees per country']['employee_residence_grouped'].value_counts()
employee_residence_filtered = pd.DataFrame({"residence": employee_residence.index.to_list(), 'number_of_programmers': employee_residence.values.tolist()})

distribution_map = px.choropleth(
    employee_residence_filtered,
    locations="residence",
    locationmode="ISO-3",
    color="number_of_programmers",
    hover_name="residence",
    color_continuous_scale="Viridis",
    title="Distribution of Programmers by Country",
    width=1000,
    height=800,
    template='plotly_white'
)
''')

employee_residence = df[df['employee_residence_grouped'] != 'Less than 5 employees per country']['employee_residence_grouped'].value_counts()
employee_residence_filtered = pd.DataFrame({"residence": employee_residence.index.to_list(), 'number_of_programmers': employee_residence.values.tolist()})

distribution_map = px.choropleth(
    employee_residence_filtered,
    locations="residence",
    locationmode="ISO-3",
    color="number_of_programmers",
    hover_name="residence",
    color_continuous_scale="Viridis",
    title="Distribution of Programmers by Country",
    width=1000,
    height=800,
    template='plotly_white'
)

st.plotly_chart(distribution_map)
st.write("The most popular country for employees is the United States as I mention in Descriptive Statistics, but now we can see this result on the map.")

# Hypothesis Statement
st.subheader("Hypothesis Statement")
st.write("- Seniors and Directors working remotely in large companies (remote_ratio = 100) earn significantly higher salaries than employees with similar experience in smaller companies and it is also works for Juniors and Middles employees.")

# Hypothesis Check
st.subheader("Hypothesis Check")
st.write("We are interested in only remote employees, so I will take employees with `remote_ratio` = 100 and create a subdataframe:")

# Fully Remote Employees
st.code("fully_remote = df[df['remote_ratio'] == 100]")
fully_remote = df[df['remote_ratio'] == 100]

st.write('''
Now, we create two dataframes:
- With Seniors and Directors
- With Juniors and Middles
''')
st.code('''
seniors_and_directors = fully_remote[((fully_remote['experience_level'] == 'Senior') | (fully_remote['experience_level'] == 'Director'))]
juniors_and_middles = fully_remote[(fully_remote['experience_level'] == 'Junior') | (fully_remote['experience_level'] == 'Middle')]
        ''')

# Seniors and Directors
seniors_and_directors = fully_remote[((fully_remote['experience_level'] == 'Senior') | (fully_remote['experience_level'] == 'Director'))]

# Juniors and Middles
juniors_and_middles = fully_remote[(fully_remote['experience_level'] == 'Junior') | (fully_remote['experience_level'] == 'Middle')]

# Salary Distribution among Seniors and Directors
st.text("Let us check distribution of salaries among Seniors and Directors in companies with different sizes:")
st.code('''
filter_seniors_and_directors_by_company = seniors_and_directors[seniors_and_directors['company_size'] != 'M']
seniors_and_directors_plot = px.box(
    filter_seniors_and_directors_by_company,
    x='experience_level',
    y='salary_in_usd',
    color='employment_type',
    facet_col='company_size',
    title='Salary Distribution by Experience Level and Company Size among Fully-Remote Seniors and Directors',
    labels={'experience_level': 'Experience Level', 'salary_in_usd': 'Salary (USD)', 'employment_type': 'Employment Type'},
    category_orders={"company_size": ["S", "L"]},
    template='plotly_white'
)

seniors_and_directors_plot.update_layout(
    xaxis=dict(
        categoryorder='array',
        categoryarray=['Senior', 'Director']
    )
)
''')


filter_seniors_and_directors_by_company = seniors_and_directors[seniors_and_directors['company_size'] != 'M']
seniors_and_directors_plot = px.box(
    filter_seniors_and_directors_by_company,
    x='experience_level',
    y='salary_in_usd',
    color='employment_type',
    facet_col='company_size',
    title='Salary Distribution by Experience Level and Company Size among Fully-Remote Seniors and Directors',
    labels={'experience_level': 'Experience Level', 'salary_in_usd': 'Salary (USD)', 'employment_type': 'Employment Type'},
    category_orders={"company_size": ["S", "L"]},
    template='plotly_white'
)

seniors_and_directors_plot.update_layout(
    xaxis=dict(
        categoryorder='array',
        categoryarray=['Senior', 'Director']
    )
)

st.plotly_chart(seniors_and_directors_plot)
st.write("Here we consider only remote workers. We can mention that salaries of such employees are bigger in large companies, but still it does not fully clear.")

# Mean Salary Comparison: Seniors and Directors
st.text("Let us plot mean value of salary among Seniors and Directors in Large companies and mean in Small companies together to have more detailed view:")
st.code('''
large_companies_dir_and_sen = seniors_and_directors[seniors_and_directors['company_size'] == 'L']
small_and_medium_companies_dir_and_sen = seniors_and_directors[(seniors_and_directors['company_size'] == 'S')]

companies_df_dir_and_sen = pd.DataFrame({'company_size': ['L', 'S'], 'mean_salary': [large_companies_dir_and_sen['salary_in_usd'].mean(), small_and_medium_companies_dir_and_sen['salary_in_usd'].mean()]})

salaries_comparison_seniors_and_directors = px.bar(
    companies_df_dir_and_sen,
    x='company_size',
    y='mean_salary',
    title='Mean Salary Comparison: Seniors and Directors',
    labels={'Mean Salary (USD)': 'Mean Salary (USD)', 'Company Type': 'Company Type'},
    color='company_size',
    template='plotly_white'
)

salaries_comparison_seniors_and_directors.update_layout(
    width=700
)
''')

large_companies_dir_and_sen = seniors_and_directors[seniors_and_directors['company_size'] == 'L']
small_and_medium_companies_dir_and_sen = seniors_and_directors[(seniors_and_directors['company_size'] == 'S')]

companies_df_dir_and_sen = pd.DataFrame({'company_size': ['L', 'S'], 'mean_salary': [large_companies_dir_and_sen['salary_in_usd'].mean(), small_and_medium_companies_dir_and_sen['salary_in_usd'].mean()]})

salaries_comparison_seniors_and_directors = px.bar(
    companies_df_dir_and_sen,
    x='company_size',
    y='mean_salary',
    title='Mean Salary Comparison: Seniors and Directors',
    labels={'Mean Salary (USD)': 'Mean Salary (USD)', 'Company Type': 'Company Type'},
    color='company_size',
    template='plotly_white'
)

salaries_comparison_seniors_and_directors.update_layout(
    width=700
)

st.plotly_chart(salaries_comparison_seniors_and_directors)
st.write("Indeed, now we can easily see that salaries of Seniors and Directors in Large companies are bigger than salaries of similar employees but in small companies.")

# Salary Distribution among Juniors and Middles
st.text("Now let us check the same thing among Juniors and Middles:")
st.code('''
filter_juniors_and_middles_by_company = juniors_and_middles[juniors_and_middles['company_size'] != 'M']
juniors_and_middles_plot = px.box(
    filter_juniors_and_middles_by_company,
    x='experience_level',
    y='salary_in_usd',
    color='employment_type',
    facet_col='company_size',
    title='Salary Distribution by Experience Level and Company Size among Fully-Remote Juniors and Middles',
    labels={'experience_level': 'Experience Level', 'salary_in_usd': 'Salary (USD)', 'employment_type': 'Employment Type'},
    category_orders={"company_size": ["S", "L"]},
    template='plotly_white'
)

juniors_and_middles_plot.update_layout(
    xaxis=dict(
        categoryorder='array',
        categoryarray=['Junior', 'Middle']
    )
)
''')

filter_juniors_and_middles_by_company = juniors_and_middles[juniors_and_middles['company_size'] != 'M']
juniors_and_middles_plot = px.box(
    filter_juniors_and_middles_by_company,
    x='experience_level',
    y='salary_in_usd',
    color='employment_type',
    facet_col='company_size',
    title='Salary Distribution by Experience Level and Company Size among Fully-Remote Juniors and Middles',
    labels={'experience_level': 'Experience Level', 'salary_in_usd': 'Salary (USD)', 'employment_type': 'Employment Type'},
    category_orders={"company_size": ["S", "L"]},
    template='plotly_white'
)

juniors_and_middles_plot.update_layout(
    xaxis=dict(
        categoryorder='array',
        categoryarray=['Junior', 'Middle']
    )
)

st.plotly_chart(juniors_and_middles_plot)
st.write("Here, situation is a little bit interesting, we cannot see that salary is really bigger in Large companies. So, let us go deeply to understand it:")

# Mean Salary Comparison: Juniors and Middles
st.code('''
large_companies_mid_and_jun = juniors_and_middles[juniors_and_middles['company_size'] == 'L']
small_and_medium_companies_mid_and_jun = juniors_and_middles[(juniors_and_middles['company_size'] == 'S')]

companies_df_mid_and_jun = pd.DataFrame({'company_size': ['L', 'S'], 'mean_salary': [large_companies_mid_and_jun['salary_in_usd'].mean(), small_and_medium_companies_mid_and_jun['salary_in_usd'].mean()]})

salaries_comparison_juniors_and_middles = px.bar(
    companies_df_mid_and_jun,
    x='company_size',
    y='mean_salary',
    title='Mean Salary Comparison: Juniors and Middles',
    labels={'Mean Salary (USD)': 'Mean Salary (USD)', 'Company Type': 'Company Type'},
    color='company_size',
    template='plotly_white'
)

salaries_comparison_juniors_and_middles.update_layout(
    width=700
)
''')

large_companies_mid_and_jun = juniors_and_middles[juniors_and_middles['company_size'] == 'L']
small_and_medium_companies_mid_and_jun = juniors_and_middles[(juniors_and_middles['company_size'] == 'S')]

companies_df_mid_and_jun = pd.DataFrame({'company_size': ['L', 'S'], 'mean_salary': [large_companies_mid_and_jun['salary_in_usd'].mean(), small_and_medium_companies_mid_and_jun['salary_in_usd'].mean()]})

salaries_comparison_juniors_and_middles = px.bar(
    companies_df_mid_and_jun,
    x='company_size',
    y='mean_salary',
    title='Mean Salary Comparison: Juniors and Middles',
    labels={'Mean Salary (USD)': 'Mean Salary (USD)', 'Company Type': 'Company Type'},
    color='company_size',
    template='plotly_white'
)

salaries_comparison_juniors_and_middles.update_layout(
    width=700
)

st.plotly_chart(salaries_comparison_juniors_and_middles)
st.write("Now it can be seen that salaries of Juniors and Middles quite bigger in Large companies.")

# Percentage Difference in Salaries
st.text("Then let us calculate the difference between salaries in persentage for each of type of employees:")
st.code('''
def percentage(a, b):
    if a > b:
        return round(a / b * 100 - 100)
    else:
        return round(b / a * 100 - 100)

change_sen_dir = percentage(large_companies_dir_and_sen['salary_in_usd'].mean(), small_and_medium_companies_dir_and_sen['salary_in_usd'].mean())
change_jun_mid = percentage(large_companies_mid_and_jun['salary_in_usd'].mean(), small_and_medium_companies_mid_and_jun['salary_in_usd'].mean())
''')

def percentage(a, b):
    if a > b:
        return round(a / b * 100 - 100)
    else:
        return round(b / a * 100 - 100)

change_sen_dir = percentage(large_companies_dir_and_sen['salary_in_usd'].mean(), small_and_medium_companies_dir_and_sen['salary_in_usd'].mean())
change_jun_mid = percentage(large_companies_mid_and_jun['salary_in_usd'].mean(), small_and_medium_companies_mid_and_jun['salary_in_usd'].mean())

st.write(f'The difference in the percentage of salaries between Seniors and Directors in Large and Small companies is: {change_sen_dir} %')
st.write(f'The difference in the percentage of salaries between Juniors and Middles in Large and Small companies is: {change_jun_mid} %')

# Discussion
st.subheader("Discussion")
st.write("In conclusion, my hypothesis was proved and I was right. Salaries for Seniors and Directors in large companies are significantly higher than those in small companies, with a 47% difference. Similarly, Juniors and Middles in large companies earn 68% more on average compared to employees in the same positions at small companies.")
