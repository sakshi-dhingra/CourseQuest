# Import necessary libraries
import streamlit as st
import re
import requests



# Streamlit styling
st.markdown(
    """
    <style>
    body {
        background-color: #F2F3F4;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Add a logo
logo = 'coursequest_image.jpg'
st.image(logo, width=100)

# Streamlit app title
st.title('CourseQuest')
st.write('Redefining Courses searching for you...')

# Welcome message
st.markdown("<h1 style='text-align: center; color: green;'>Welcome to CourseQuest</h2>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center; color: black;'>Find the best suited course for you!</h4>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center; color: black;'>Created by Adaptive System Students (Group Athena)</h4>", unsafe_allow_html=True)

# Multiselect dropdown for selecting tags
selected_tags = st.multiselect("Enter the SkillSet you'd like to acquire...", cleaned_tags)

# Initialize liked_courses and disliked_courses in session state
liked_courses = []
disliked_courses = []
if 'liked_courses' not in st.session_state:
    st.session_state.liked_courses = []
if 'disliked_courses' not in st.session_state:
    st.session_state.disliked_courses = []


# # Multiselect dropdown for selecting difficulty level
# difficulty = []
# for row in courses_all['Difficulty Level']:
#     for entry in row.split(','):
#         difficulty.append(entry.strip())
# difficulty = list(set(difficulty))
# selected_tags = st.multiselect("Enter the Difficulty Level", difficulty)


# Display relevant courses
if selected_tags:
    st.write("Top 5 relevant courses:")
    for tag in selected_tags:
        st.write(f"Selected Tag: {tag}")
    relevant_courses = (" ".join(selected_tags))
    
    # Display courses with like and dislike buttons
    for index, row in relevant_courses.iterrows():
        st.write(f"**{row['Course Name']}**")
        st.write(f"Course URL: {row['Course URL']}")
        
        # Add like and dislike buttons
        col1, col2 = st.columns(2)
        if col1.button(f'Like {row["Course Name"]}'):
            if row['Course Name'] not in st.session_state.liked_courses:
                st.session_state.liked_courses.append(row['Course Name'])
                st.write(f"You liked {row['Course Name']}")
        if col2.button(f'Dislike {row["Course Name"]}'):
            if row['Course Name'] not in st.session_state.disliked_courses:
                st.session_state.disliked_courses.append(row['Course Name'])
                st.write(f"You disliked {row['Course Name']}")
        st.write('---')

# Sidebar to display liked courses
st.sidebar.header("My Courses")
for liked_course in st.session_state.liked_courses:
    if st.sidebar.button(liked_course):
        selected_course_details = courses_all[courses_all['Course Name'] == liked_course]
        if not selected_course_details.empty:
            st.sidebar.subheader(f"Details for {liked_course}:")
            for index, row in selected_course_details.iterrows():
                st.sidebar.write(f"Course Name: **{row['Course Name']}**")
                st.sidebar.write(f"Course URL: {row['Course URL']}")
                st.sidebar.write(f"Difficulty Level: {row['Difficulty Level']}")
                st.sidebar.write(f"Skills: {row['Skills']}")

# Display similar courses
st.sidebar.header("Similar Courses")
for liked_course in st.session_state.liked_courses:
    selected_course_details = courses_all[courses_all['Course Name'] == liked_course]
    if not selected_course_details.empty:
        attributes = selected_course_details.iloc[0]['Attributes']
        similar_courses = map_user_input(attributes)
        similar_courses = similar_courses[~similar_courses['Course Name'].isin(st.session_state.liked_courses)]
        if not similar_courses.empty:
            for index, row in similar_courses.iterrows():
                st.sidebar.write(f"**{row['Course Name']}**")
                st.sidebar.write(f"Course URL: {row['Course URL']}")
                st.sidebar.write('---')
        else:
            st.sidebar.write("No similar courses found.")
