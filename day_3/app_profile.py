import streamlit as st
import pandas as pd

# Title of the app
st.title("Researcher Profile Page")

# Collect basic information
name = "Kyle Solomons"
field = "Astrophysics"
institution = "University of Cape Town; SAAO"

# Display basic profile information
st.header("Researcher Overview")
st.write(f"**Name:** {name}")
st.write(f"**Field of Research:** {field}")
st.write(f"**Institution:** {institution}")

# Add a section for publications
# st.header("Publications")
# uploaded_file = st.file_uploader("Upload a CSV of Publications", type="csv")

# if uploaded_file:
#     publications = pd.read_csv(uploaded_file)
#     st.dataframe(publications)
#
#     # Add filtering for year or keyword
#     keyword = st.text_input("Filter by keyword", "")
#     if keyword:
#         filtered = publications[
#             publications.apply(lambda row: keyword.lower() in row.astype(str).str.lower().values, axis=1)
#         ]
#         st.write(f"Filtered Results for '{keyword}':")
#         st.dataframe(filtered)
#     else:
#         st.write("Showing all publications")
#
# # Add a section for visualizing publication trends
# st.header("Publication Trends")
# if uploaded_file:
#     if "Year" in publications.columns:
#         year_counts = publications["Year"].value_counts().sort_index()
#         st.bar_chart(year_counts)
#     else:
#         st.write("The CSV does not have a 'Year' column to visualize trends.")


#Education Section
st.header("Education")
st.write("Bsc in Mathematics and Astronomy (2017-2020), UCT")
st.write("Honours in Astrophysics (2021-2021), UCT")
st.write("Msc in Astrophysics (2022-2024), UCT")
st.write("PhD in Astrophysics (2024-current), UCT")
# Add a contact section
st.header("Contact Information")
email = "SLMKYL003@myuct.ac.za"
st.write(f"You can reach {name} at {email}.")

# if st.button("Click for a surprise!"):
#     st.markdown("[Click here to view the surprise!](https://www.youtube.com/watch?v=dQw4w9WgXcQ)")

st.link_button(f"click for surprise!", "https://www.youtube.com/watch?v=dQw4w9WgXcQ")