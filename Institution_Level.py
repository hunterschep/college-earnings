import streamlit as st
import pandas as pd
import plotly.express as px

# Initial settings
st.set_page_config(layout="wide", initial_sidebar_state="expanded", page_title="College Earnings", page_icon="🎓")
st.title("College Data by Institution")

# Load data
data = pd.read_csv("data/school_level_data.csv")
data = data.sort_values(by='90th Percentile Earnings', ascending=False)

# Sidebar filters 
st.sidebar.title("Earnings Filters")
st.sidebar.markdown("---")
st.sidebar.markdown("## Years")
year_selection = st.sidebar.selectbox("Select Earnings By Year After Graduation", ["1 Year", "4 Years", "5 Years"])

st.sidebar.markdown('''
---
Created with ❤️ @ Boston College.
''')

# Convert 'School Name' to a list of unique values
school_names = data['School Name'].unique()
selected_school = st.selectbox("Search For a School", options=school_names)
filtered_data = data[data['School Name'] == selected_school]

# Check if filtered_data is not empty
if not filtered_data.empty:
    # If any of these values are 0 display 'N/A'
    acceptance_rate = filtered_data['Acceptance Rate'].iloc[0] if filtered_data['Acceptance Rate'].iloc[0] != 0 else "N/A"
    undergrads = filtered_data['Undergraduate Students'].iloc[0] if filtered_data['Undergraduate Students'].iloc[0] != 0 else "N/A"
    sat = filtered_data['Average SAT'].iloc[0] if filtered_data['Average SAT'].iloc[0] != 0 else "N/A"
else:
    acceptance_rate = undergrads = sat = "N/A"

# Display top-level widgets for acceptance rate, num undergrads, and SAT
col1, col2, col3 = st.columns([1, 1, 1])

with col1:
    st.metric("Acceptance Rate", f"{acceptance_rate}%")

with col2:
    st.metric("Number of Undergrads", f"{undergrads:,}")

with col3:
    try:
        sat_value = int(sat)
    except ValueError:
        sat_value = "N/A"
    st.metric("Average SAT Score", f"{sat_value}")

# Insert a blank space to separate the first row of metrics from the second row
st.write("")
st.markdown("---")

# Second row of metrics & majors for the selected school 
col4, col5 = st.columns([0.25, 0.75])

majors = pd.read_csv("data/major_level_data.csv")
majors = majors[majors['School Name'] == selected_school]
majors = majors.sort_values(by=year_selection, ascending=False)
no_majors = majors.empty

with col4:
    earnings = data.copy()
    # Sort and reset index for median earnings
    earnings.sort_values(by='Median Earnings @ 10 Years Post Grad', ascending=False, inplace=True)
    earnings.reset_index(drop=True, inplace=True)
    
    useNinety = st.checkbox("Use 90th Percentile Earnings")

    # Utilize 90th percentile earnings if the checkbox is selected
    if useNinety:
        salary = filtered_data['90th Percentile Earnings'].iloc[0]
        top = earnings.sort_values(by='90th Percentile Earnings', ascending=False)
        top.reset_index(drop=True, inplace=True)
        rank = top[top['School Name'] == selected_school].index[0] + 1
        st.metric("90th Percentile Earnings", f"${salary:,.0f} | #{rank}")

    else:
        salary = filtered_data['Median Earnings @ 10 Years Post Grad'].iloc[0]
        rank = earnings[earnings['School Name'] == selected_school].index[0] + 1
        st.metric("Median Earnings @ 10 Years Post Grad", f"${salary:,.0f} | #{rank}")

    # show median debt @ grad 
    debt = filtered_data['Median Debt @ Graduation'].iloc[0] if pd.notna(filtered_data['Median Debt @ Graduation'].iloc[0]) else "N/A"
    st.metric("Median Debt @ Graduation", f"${debt:,.0f}")
    price = filtered_data['Net Price'].iloc[0] if pd.notna(filtered_data['Net Price'].iloc[0]) else "N/A"
    st.metric("Net Price", f"${price:,.0f}")

with col5:
    if not no_majors:
        earnings_column_name = f'Earnings @ {year_selection}'
        majors[earnings_column_name] = majors[year_selection].apply(lambda x: f"${x:,.0f}")
        st.write(f"Majors @ {selected_school}")
        st.dataframe(majors[['Major', earnings_column_name]], use_container_width=True, hide_index=True)
    else: 
        st.write("No major earnings data available for this school.")

# Third row of metrics 
st.write("")
st.markdown("---")
col6, col7, col8, col9 = st.columns([0.05, 0.25, 0.65, 0.05])

# 4 metrics [First Gen, Women, Family Income, Grad Rate]
with col7:
    st.write("")
    first_gen = filtered_data['First Generation'].iloc[0] if pd.notna(filtered_data['First Generation'].iloc[0]) else "N/A"
    if not first_gen == "N/A":
        first_gen *= 100

    # Special markdown formatting 
    st.markdown(f"""
    <div style='border: 1px solid #ccc; padding: 10px; border-radius: 5px; margin-bottom: 10px; font-size: 20px;'>
        Percent First Gen: {first_gen:.2f}%
    </div>
    """, unsafe_allow_html=True)

    women = filtered_data['Percent Female'].iloc[0] if pd.notna(filtered_data['Percent Female'].iloc[0]) else "N/A"
    if not women == "N/A":
        women *= 100
        
    st.markdown(f"""
    <div style='border: 1px solid #ccc; padding: 10px; border-radius: 5px; margin-bottom: 10px; font-size: 20px;'>
        Percent Women: {women:.2f}%
    </div>
    """, unsafe_allow_html=True)

    grad_rate = filtered_data['4 Year Graduation Rate'].iloc[0] if pd.notna(filtered_data['4 Year Graduation Rate'].iloc[0]) else "N/A"
    if not grad_rate == "N/A":
        grad_rate *= 100
        
    st.markdown(f"""
    <div style='border: 1px solid #ccc; padding: 10px; border-radius: 5px; margin-bottom: 10px; font-size: 20px;'>
        Graduation Rate: {grad_rate:.2f}%
    </div>
    """, unsafe_allow_html=True)

    family = filtered_data['Median Family Income'].iloc[0] if pd.notna(filtered_data['Median Family Income'].iloc[0]) else "N/A"
        
    st.markdown(f"""
    <div style='border: 1px solid #ccc; padding: 10px; border-radius: 5px; margin-bottom: 10px; font-size: 20px;'>
        Median Family Income: ${family:,.0f}
    </div>
    """, unsafe_allow_html=True)

# Demographics pie chart
with col8: 
    # Create a pie chart of the demographics of the selected school
    demographics_cols = ['White', 'Black', 'Hispanic', 'Asian']
    
    # Check if filtered_data is not empty and has the necessary columns
    if not filtered_data.empty and all(col in filtered_data.columns for col in demographics_cols):
        white = filtered_data['White'].iloc[0] if pd.notna(filtered_data['White'].iloc[0]) else 0
        black = filtered_data['Black'].iloc[0] if pd.notna(filtered_data['Black'].iloc[0]) else 0
        hispanic = filtered_data['Hispanic'].iloc[0] if pd.notna(filtered_data['Hispanic'].iloc[0]) else 0
        asian = filtered_data['Asian'].iloc[0] if pd.notna(filtered_data['Asian'].iloc[0]) else 0
        
        other = 1 - (white + black + hispanic + asian)
        
        demographics = {
            'White': white,
            'Black': black,
            'Hispanic': hispanic,
            'Asian': asian,
            'Other / Unknown': other
        }
        
        # Create a pie chart
        pie_chart_data = pd.Series(demographics).reset_index(name='Percentage')
        pie_chart_data.columns = ['Demographic', 'Percentage']
        
        st.markdown(f"<h2 style='font-size:30px; text-align:center;'>Demographics @ {selected_school}</h2>", unsafe_allow_html=True)
        
        fig = px.pie(pie_chart_data, names='Demographic', values='Percentage', 
                     labels={'Percentage': 'Percentage'},
                     hole=0.3)
        
        fig.update_traces(textposition='inside', textinfo='percent+label', textfont_size=12)
        
        st.plotly_chart(fig, use_container_width=True)
    
    else:
        st.write("No demographic data available for this school.")
