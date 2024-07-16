import pandas as pd
import streamlit as st

# Initial settings 
st.set_page_config(layout="wide", initial_sidebar_state="expanded", page_title="College Earnings", page_icon="🎓")
st.title("College Earnings by Major")

# Load and prepare the data
data = pd.read_csv("data\major_level_data.csv")
earnings_columns = ['1 Year', '4 Years', '5 Years']

# Sidebar filters 
st.sidebar.title("Data Filters")
st.sidebar.markdown("---")
st.sidebar.markdown("## Major")
major = st.sidebar.selectbox("Select a Major", sorted(data["Major"].unique()))
st.sidebar.markdown("---")
st.sidebar.markdown("## Years")
year_selection = st.sidebar.selectbox("Select Earnings By Year After Graduation", ["1 Year", "4 Years", "5 Years"])

st.sidebar.markdown('''
---
Created with ❤️ @ Boston College.
''')

# Filter the data based on selected major
filtered_data = data[data['Major'] == major].copy()
sorted_data = filtered_data.sort_values(by=year_selection, ascending=False)
sorted_data.reset_index(drop=True, inplace=True)
sorted_data.index = sorted_data.index + 1

sorted_data[year_selection] = sorted_data[year_selection].apply(lambda x: f"${x:,.0f}")

st.write(f"Top Earnings For {major} @ {year_selection} Post Graduation")
col1, col2 = st.columns([0.7,0.3])

# Display the table in the left column
with col1:
    st.dataframe(sorted_data[['School Name', year_selection]], use_container_width=True, height=500)

# Calculate mean earnings
mean_earnings = sorted_data.head(10)
mean = mean_earnings[year_selection].replace('[\$,]', '', regex=True).astype(float).mean()
number_of_schools = len(filtered_data)

# Display metrics in the right column with borders
with col2:
    st.markdown("# Metrics")
    st.markdown("---")
    st.metric(label=f"Mean Earnings After {year_selection} For T10 Schools", value=f"${mean:,.0f}")
    st.markdown("---")
    # number emoji
    st.metric(label=f"Number of Schools With a {major} Major", value=number_of_schools,)
