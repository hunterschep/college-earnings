import streamlit as st

st.set_page_config(layout="wide", initial_sidebar_state="expanded", page_title="College Earnings", page_icon="🎓")
st.title("About This App")
st.markdown("---")

# Using Markdown for formatted text with a link to the College Scorecard dataset
st.markdown(
    """
    This app was created to showcase the metrics of colleges and their graduates. 
    The data was collected from the [College Scorecard dataset](https://collegescorecard.ed.gov/data/).
    """
)

st.markdown("---")

# Contact and GitHub information with logos
st.markdown(
    """
    If there are issues with this application, please make a PR on the [GitHub repo](https://github.com/yourusername/college-earnings)
    or reach out to me directly. Thank you for using this app! - Hunter
    """,
    unsafe_allow_html=True
)

# Adding logos for GitHub and LinkedIn with links
col1, col2 = st.columns(2)

with col1:
    st.markdown("![GitHub](https://img.icons8.com/nolan/64/github.png)")
    st.markdown("[GitHub Repository](https://github.com/yourusername/college-earnings)")

with col2:
    st.markdown("![LinkedIn](https://img.icons8.com/nolan/64/linkedin.png)")
    st.markdown("[Connect on LinkedIn](https://www.linkedin.com/in/hunterscheppat/)")

