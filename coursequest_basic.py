'''
This code performs tasks such as data cleaning, text processing, creating a Streamlit app interface, 
and providing course recommendations based on user preferences. It uses CountVectorizer for text processing, 
KMeans clustering for grouping courses, and Streamlit for building the web application interface. 
Additionally, it provides options for users to like/dislike courses and displays relevant recommendations 
based on their preferences.

Do 'streamlit run coursequest_basic.py' to run the code
'''

# Import necessary libraries
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import streamlit as st
import re
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.cluster import KMeans
from sklearn.metrics.pairwise import cosine_distances
import nltk
from nltk.corpus import stopwords

# Download stopwords from NLTK
nltk.download('stopwords')

# Define stop words
stop_words = set(stopwords.words('english'))

# Read Coursera data from CSV file
coursera_data = pd.read_csv("Coursera.csv")
# Add a new column 'Website' with value 'Coursera'
value_to_add = 'Coursera'
coursera_data['Website'] = value_to_add

# Define function to join words with commas
def join_words(text):
    words = text.split()
    return ', '.join(words)

# Apply join_words function to all cells in the DataFrame
coursera_data = coursera_data.applymap(join_words)

# Combine 'Course Name' and 'Skills' columns and create a new column 'Attributes'
coursera_data['Attributes'] = coursera_data[['Course Name', 'Skills']].apply(lambda row: ', '.join(row), axis=1)

# Define columns to keep
columns_to_keep = ['Course Name', 'Website', 'Course URL', 'Difficulty Level', 'Skills', 'Attributes']

# Drop columns not in the list
columns_to_drop = [col for col in coursera_data.columns if col not in columns_to_keep]
coursera_data.drop(columns=columns_to_drop, inplace=True)

# Define function to remove commas
def remove_commas(row):
    if row.name == 'Course Name' or row.name == 'Skills' :
        return row.str.replace(',', '')
    return row

# Apply remove_commas function to each row
coursera_data = coursera_data.apply(remove_commas)

# Define function to clean attributes
def clean_attributes(text):
    words = text.split(', ')
    cleaned_words = []
    for word in words:
        cleaned_word = ''.join(e for e in word if e.isalnum() or e == ',')
        cleaned_word = cleaned_word.capitalize()
        if cleaned_word.lower() not in stop_words:
            cleaned_words.append(cleaned_word)
    cleaned_text = ', '.join(cleaned_words)
    return cleaned_text

# Apply clean_attributes function to the 'Attributes' column
coursera_data['Attributes'] = coursera_data['Attributes'].apply(clean_attributes)

# Display first 5 rows of Coursera data after cleaning
print(coursera_data.head(5))

# Read EdX data from CSV file
edx_data = pd.read_csv("EdX.csv")
# Add a new column 'Website' with value 'EdX'
value_to_add = 'EdX'
edx_data['Website'] = value_to_add

# Apply join_words function to all cells in the DataFrame
edx_data = edx_data.applymap(join_words)

# Rename columns and create a new column 'Attributes'
edx_data = edx_data.rename(columns={"Name": "Course Name", "Link": "Course URL", "About": "Skills"}).sample(frac=1, random_state=42)
edx_data['Attributes'] = edx_data[['Course Name', 'Skills']].apply(lambda row: ', '.join(row), axis=1)

# Drop columns not in the list
columns_to_drop = [col for col in edx_data.columns if col not in columns_to_keep]
edx_data.drop(columns=columns_to_drop, inplace=True)

# Apply remove_commas function to each row
edx_data = edx_data.apply(remove_commas)

# Apply clean_attributes function to the 'Attributes' column
edx_data['Attributes'] = edx_data['Attributes'].apply(clean_attributes)

# Display first 5 rows of EdX data after cleaning
print(edx_data.head(5))

# Concatenate Coursera and EdX data
courses_all = pd.concat([coursera_data, edx_data], ignore_index=True).sample(frac=1, random_state=42)

# Display first 5 rows of concatenated data
print(courses_all.head(5))

# Extract attributes from 'Attributes' column
attributes = []
for row in courses_all['Attributes']:
    for attribute in row.split(','):
        attributes.append(attribute.strip())

# Initialize CountVectorizer
countv = CountVectorizer(max_features=5000,stop_words='english')

# Transform text data into matrix
X = countv.fit_transform(courses_all['Attributes']).toarray()

# Clean tags
cleaned_tags = []
for tag in attributes:
    cleaned_tag = re.sub(r'[^a-zA-Z\s]', '', tag)
    cleaned_tag = re.sub(r'\s+', ' ', cleaned_tag).strip()
    cleaned_tags.append(cleaned_tag)

# Remove empty tags and deduplicate
cleaned_tags = [tag for tag in cleaned_tags if tag]
cleaned_tags = list(set(cleaned_tags))

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

# Filter course data based on selected tags
filtered_data = courses_all[courses_all['Attributes'].str.contains('|'.join(selected_tags))]

# KMeans clustering
k = 2  # Number of clusters
kmeans = KMeans(n_clusters=k, random_state=42)
kmeans.fit(X)

# Function to map user input
def map_user_input(keyword):
    keyword_vector = countv.transform([keyword])
    distances = cosine_distances(keyword_vector, X)
    closest_indices = distances.argsort()[0][:5]
    relevant_courses = courses_all.iloc[closest_indices][['Course Name', 'Course URL']]
    relevant_courses['Course Name'] = relevant_courses['Course Name'].str.replace(',', ' ')
    return relevant_courses

# Initialize liked_courses and disliked_courses in session state
liked_courses = []
disliked_courses = []
if 'liked_courses' not in st.session_state:
    st.session_state.liked_courses = []
if 'disliked_courses' not in st.session_state:
    st.session_state.disliked_courses = []

# Display relevant courses
if selected_tags:
    st.write("Top 5 relevant courses:")
    for tag in selected_tags:
        st.write(f"Selected Tag: {tag}")
    relevant_courses = map_user_input(" ".join(selected_tags))
    
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

# Multiselect dropdown for selecting difficulty level
difficulty = []
for row in courses_all['Difficulty Level']:
    for entry in row.split(','):
        difficulty.append(entry.strip())
difficulty = list(set(difficulty))
selected_tags = st.multiselect("Enter the Difficulty Level", difficulty)
