# app.py

# Step 1: Import Libraries
import streamlit as st
import pandas as pd
import plotly.express as px

# --- Page Configuration ---
# This command sets the title that appears in your browser tab and the layout.
# "wide" layout uses the full width of the screen.
st.set_page_config(
    page_title="Credit Risk EDA Dashboard",
    page_icon="📊",
    layout="wide"
)


# Step 2: Load the Data
# The decorator @st.cache_data tells Streamlit to run this function only once
# and store the result in a cache. This prevents reloading the data every time
# a user interacts with the dashboard.
@st.cache_data
def load_data():
    # 'pd.read_csv' is the pandas function to read a CSV file.
    # 'index_col=0' sets the first column of the CSV as the index of the DataFrame.
    data = pd.read_csv('german_credit_data.csv', index_col=0)
    
    # '.fillna()' is used to fill missing (NaN) values. Here we replace them
    # with the string 'no_info'.
    data['Saving accounts'] = data['Saving accounts'].fillna('no_info')
    data['Checking account'] = data['Checking account'].fillna('no_info')
    job_mapping = {
        0: 'Unskilled',
        1: 'Skilled',
        2: 'Highly Skilled',
        3: 'Executive'
    }
    data['Job'] = data['Job'].map(job_mapping)
    return data

# Call the function to load the data into a variable named 'data'.
data = load_data()


# Step 3: Create Title and Sidebar
st.title("📊 Exploratory Data Analysis for Credit Risk")

# 'st.sidebar.header' adds a title to the sidebar.
st.sidebar.header("Dashboard Filters")


# Step 4: Create Interactive Filters

# Filter for Job Type. '.unique()' gets all unique values from the 'Job' column.
job_options = sorted(data['Job'].unique())
# 'default=job_options' makes all job types selected by default.
selected_job = st.sidebar.multiselect("Filter by Job Type", job_options, default=job_options)

# Filter for Housing Type.
housing_options = sorted(data['Housing'].unique())
selected_housing = st.sidebar.selectbox("Filter by Housing Type", housing_options, index=0)

# Filter for Age using a slider.
min_age, max_age = int(data['Age'].min()), int(data['Age'].max())
selected_age_range = st.sidebar.slider(
    "Filter by Age Range",
    min_value=min_age,
    max_value=max_age,
    value=(min_age, max_age) # 'value' sets the default selected range.
)



# Step 5: Apply Filters to the DataFrame
# This is the logic that connects the filters to the data.
# It uses boolean indexing from Pandas.
filtered_data = data[
    (data['Job'].isin(selected_job)) &
    (data['Housing'] == selected_housing) &
    (data['Age'] >= selected_age_range[0]) &
    (data['Age'] <= selected_age_range[1])
]


# Step 6: Display KPIs and Visualizations

# --- KPIs ---
st.subheader("High-Level Metrics")
total_applicants = len(filtered_data)
avg_credit_amount = int(filtered_data['Credit amount'].mean())

# Create three columns for our KPIs.
kpi1, kpi2 = st.columns(2)
kpi1.metric(label="Total Applicants 👥", value=total_applicants)
kpi2.metric(label="Average Credit Amount 💵", value=f"$ {avg_credit_amount:,.0f}")

# --- Visualizations ---
st.subheader("Interactive Visualizations")
col1, col2 = st.columns(2)
with col1:
    st.markdown("##### Distribution of Credit Amount")
    # This text guides the user on what to look for in the chart.
    st.write("This histogram shows how many applicants fall into different credit amount brackets.")
    fig1 = px.histogram(filtered_data, x="Credit amount")
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    st.markdown("##### Count of Loans by Purpose")
    st.write("This bar chart shows the most common reasons applicants request loans.")
    purpose_counts = filtered_data['Purpose'].value_counts().reset_index()
    fig2 = px.bar(purpose_counts, x="Purpose", y="count", title="Loan Purpose Counts")
    st.plotly_chart(fig2, use_container_width=True)


# Step 8: Add a Scatter Plot to Explore Relationships

st.subheader("Relationship between Credit Amount and Loan Duration")
st.write("This scatter plot helps us see if there is a correlation between the loan duration and the amount borrowed, segmented by housing type.")
fig3 = px.scatter(
    filtered_data,
    x="Duration",
    y="Credit amount",
    color="Housing",
    title="Credit Amount vs. Loan Duration by Housing Type"
)
st.plotly_chart(fig3, use_container_width=True)


# Step 9: Add a Box Plot and Summary Statistics

# --- Box Plot ---
st.subheader("Distribution of Credit Amount by Housing Type")

# We create the box plot using the filtered_data DataFrame.
# x='Housing' puts the categories on the horizontal axis.
# y='Credit amount' sets the numerical variable for the vertical axis.
fig4 = px.box(
    filtered_data,
    x="Housing",
    y="Credit amount",
    color="Housing", # Colors the boxes to match the legend
    title="Credit Amount Distribution by Housing Type"
)
st.plotly_chart(fig4, use_container_width=True)


# --- Summary Statistics in an Expander ---
# st.expander creates a collapsible section.
with st.expander("View Detailed Summary Statistics"):
    # .describe() is a powerful pandas function that generates descriptive statistics.
    st.write(filtered_data.describe())


# Place this right after st.title(...)

st.markdown("""
This interactive dashboard is designed for Exploratory Data Analysis (EDA) of the German Credit Risk dataset.
You can use the filters on the left to dynamically explore the relationships between different applicant attributes and see how they affect key metrics.
""")

# Place this before st.subheader("High-Level Metrics")

st.markdown("---") # This adds a horizontal line for separation



