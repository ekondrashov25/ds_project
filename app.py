import streamlit as st
import pandas as pd
import plotly.express as px
import pycountry
import numpy as np

# Loading data
@st.cache_data
def load_data():
    df = pd.read_csv('ds_salaries.csv', sep=';')
    return df

df = load_data()

# Descriptive statistics
st.title("Data Science Salaries Analysis")

st.subheader("Dataset Structure")
st.write(df.head())

st.subheader("NaN Data Check")
st.write(df.isna().sum())

st.subheader("Dataset Info")
st.write(df.info())

st.subheader("Descriptive Statistics")
st.write(df.describe())

st.subheader("Salary in USD Description")
st.write(df['salary_in_usd'].describe())

# Transforming data
st.subheader("Data Transformation")

# Drop redundant columns
df.drop(columns=['salary_currency', 'salary'], inplace=True)
st.write("Columns dropped successfully.")

# Convert country name to ISO-3 format
def convert_country_name(country_name: str) -> str:
    return pycountry.countries.get(alpha_2=country_name).alpha_3

df['employee_residence_iso_3'] = df['employee_residence'].apply(convert_country_name)
st.write("Country names converted to ISO-3 format.")

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
st.write("Experience level and employment type converted to understandable names.")

# Simple Plots
st.subheader("Simple Plots")

# Salary Distribution
salaries_dist = px.box(
    df,
    x='salary_in_usd',
    title='Salary Distribution',
    labels={'remote_ratio': 'Salary (USD)'}
)

salaries_dist.update_traces(
    marker_color='blue',
    line_color='black'
)

salaries_dist.update_layout(
    title_font_size=16,
    xaxis_title='Salary (USD)'
)

st.plotly_chart(salaries_dist)

# Most Popular Positions
experience_level = df['experience_level'].value_counts()
popular_positions = px.pie(
    values=experience_level,
    names=experience_level.index.to_list()
)

popular_positions.update_layout(
    title='The most popular positions',
    width=600
)

st.plotly_chart(popular_positions)

# Most Popular Countries
country_counts = df['employee_residence_iso_3'].value_counts()
low_count_countries = country_counts[country_counts < 5].index
df['employee_residence_grouped'] = df['employee_residence_iso_3'].apply(lambda x: 'Less than 5 employees per country' if x in low_count_countries else x)

employee_residence = df['employee_residence_grouped'].value_counts()
top_countries = px.pie(
    values=employee_residence,
    names=employee_residence.index.to_list()
)

top_countries.update_layout(
    title='Residence of work',
    width=600
)

st.plotly_chart(top_countries)

# Salaries in Residence of Work Countries
aggregated_salaries = df.groupby('employee_residence_grouped')['salary_in_usd'].mean().reset_index()
salaries = px.bar(
    aggregated_salaries,
    x='employee_residence_grouped',
    y='salary_in_usd'
)

st.plotly_chart(salaries)

# Salary Change from 2020 to 2022
salary_by_year = df.groupby('work_year')['salary_in_usd'].mean().reset_index()
salaries = px.line(
    salary_by_year,
    x='work_year',
    y='salary_in_usd',
    title='Average Salary Change from 2020 to 2022',
    labels={'work_year': 'Year', 'salary_in_usd': 'Average Salary (USD)'},
    markers=True,
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

# Salary Distribution by Company Size
filtered_companies_by_size = df.groupby('company_size')['salary_in_usd'].median()
salaries_dist_violin = px.violin(
    df,
    x='company_size',
    y='salary_in_usd',
    title="Salary Distribution by Company Size",
    labels={'company_size': 'Company Size', 'salary_in_usd': 'Salary (USD)'},
    box=True,
    points="all"
)

salaries_dist_violin.update_layout(
    xaxis=dict(
        categoryorder='array',
        categoryarray=['S', 'M', 'L']
    )
)

st.plotly_chart(salaries_dist_violin)

# Detailed Overview via Complex Plots
st.subheader("Detailed Overview via Complex Plots")

# Sunburst Plot
sunburst_plot = px.sunburst(
    df,
    path=['experience_level', 'employment_type', 'job_title'],
    values='salary_in_usd',
    color='salary_in_usd',
    color_continuous_scale='RdBu',
    title='Salaries by Experience, Employment Type, and Job Title',
    width=1000,
    height=800
)

st.plotly_chart(sunburst_plot)

# Salary Distribution by Experience Level and Remote Ratio
salaries_dist_2 = px.box(
    df,
    x='experience_level',
    y='salary_in_usd',
    color='employment_type',
    facet_col='remote_ratio',
    title='Salary Distribution by Experience Level and Remote Ratio',
    labels={'experience_level': 'Experience Level', 'salary_in_usd': 'Salary (USD)', 'employment_type': 'Employment Type'}
)

salaries_dist_2.update_layout(
    xaxis=dict(
        categoryorder='array',
        categoryarray=['Junior', 'Middle', 'Senior', 'Director']
    )
)

st.plotly_chart(salaries_dist_2)

# 3D Scatter Plot
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
    height=800
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
)

st.plotly_chart(distribution_map)

# Hypothesis Statement
st.subheader("Hypothesis Statement")
st.write("Seniors and Directors working remotely in large companies (remote_ratio = 100) earn significantly higher salaries than employees with similar experience in smaller companies and it is also works for Juniors and Middles employees.")

# Hypothesis Check
st.subheader("Hypothesis Check")

# Fully Remote Employees
fully_remote = df[df['remote_ratio'] == 100]

# Seniors and Directors
seniors_and_directors = fully_remote[((fully_remote['experience_level'] == 'Senior') | (fully_remote['experience_level'] == 'Director'))]

# Juniors and Middles
juniors_and_middles = fully_remote[(fully_remote['experience_level'] == 'Junior') | (fully_remote['experience_level'] == 'Middle')]

# Salary Distribution among Seniors and Directors
filter_seniors_and_directors_by_company = seniors_and_directors[seniors_and_directors['company_size'] != 'M']
seniors_and_directors_plot = px.box(
    filter_seniors_and_directors_by_company,
    x='experience_level',
    y='salary_in_usd',
    color='employment_type',
    facet_col='company_size',
    title='Salary Distribution by Experience Level and Company Size among Fully-Remote Seniors and Directors',
    labels={'experience_level': 'Experience Level', 'salary_in_usd': 'Salary (USD)', 'employment_type': 'Employment Type'},
    category_orders={"company_size": ["S", "L"]}
)

seniors_and_directors_plot.update_layout(
    xaxis=dict(
        categoryorder='array',
        categoryarray=['Senior', 'Director']
    )
)

st.plotly_chart(seniors_and_directors_plot)

# Mean Salary Comparison: Seniors and Directors
large_companies_dir_and_sen = seniors_and_directors[seniors_and_directors['company_size'] == 'L']
small_and_medium_companies_dir_and_sen = seniors_and_directors[(seniors_and_directors['company_size'] == 'S')]

companies_df_dir_and_sen = pd.DataFrame({'company_size': ['L', 'S'], 'mean_salary': [large_companies_dir_and_sen['salary_in_usd'].mean(), small_and_medium_companies_dir_and_sen['salary_in_usd'].mean()]})

salaries_comparison_seniors_and_directors = px.bar(
    companies_df_dir_and_sen,
    x='company_size',
    y='mean_salary',
    title='Mean Salary Comparison: Seniors and Directors',
    labels={'Mean Salary (USD)': 'Mean Salary (USD)', 'Company Type': 'Company Type'},
    color='company_size'
)

salaries_comparison_seniors_and_directors.update_layout(
    width=700,
)

st.plotly_chart(salaries_comparison_seniors_and_directors)

# Salary Distribution among Juniors and Middles
filter_juniors_and_middles_by_company = juniors_and_middles[juniors_and_middles['company_size'] != 'M']
juniors_and_middles_plot = px.box(
    filter_juniors_and_middles_by_company,
    x='experience_level',
    y='salary_in_usd',
    color='employment_type',
    facet_col='company_size',
    title='Salary Distribution by Experience Level and Company Size among Fully-Remote Juniors and Middles',
    labels={'experience_level': 'Experience Level', 'salary_in_usd': 'Salary (USD)', 'employment_type': 'Employment Type'},
    category_orders={"company_size": ["S", "L"]}
)

juniors_and_middles_plot.update_layout(
    xaxis=dict(
        categoryorder='array',
        categoryarray=['Junior', 'Middle']
    )
)

st.plotly_chart(juniors_and_middles_plot)

# Mean Salary Comparison: Juniors and Middles
large_companies_mid_and_jun = juniors_and_middles[juniors_and_middles['company_size'] == 'L']
small_and_medium_companies_mid_and_jun = juniors_and_middles[(juniors_and_middles['company_size'] == 'S')]

companies_df_mid_and_jun = pd.DataFrame({'company_size': ['L', 'S'], 'mean_salary': [large_companies_mid_and_jun['salary_in_usd'].mean(), small_and_medium_companies_mid_and_jun['salary_in_usd'].mean()]})

salaries_comparison_juniors_and_middles = px.bar(
    companies_df_mid_and_jun,
    x='company_size',
    y='mean_salary',
    title='Mean Salary Comparison: Juniors and Middles',
    labels={'Mean Salary (USD)': 'Mean Salary (USD)', 'Company Type': 'Company Type'},
    color='company_size'
)

salaries_comparison_juniors_and_middles.update_layout(
    width=700,
)

st.plotly_chart(salaries_comparison_juniors_and_middles)

# Percentage Difference in Salaries
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