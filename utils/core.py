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


class Engine:
    def _remove_commas(self, row):
        if row.name == 'Course Name' or row.name == 'Skills' :
            return row.str.replace(',', '')
        return row

    # Define function to clean attributes
    def _clean_attributes(self, text):
        words = text.split(', ')
        cleaned_words = []
        for word in words:
            cleaned_word = ''.join(e for e in word if e.isalnum() or e == ',')
            cleaned_word = cleaned_word.capitalize()
            if cleaned_word.lower() not in self.stop_words:
                cleaned_words.append(cleaned_word)
        cleaned_text = ', '.join(cleaned_words)
        return cleaned_text

    def __init__(self):
        # Download stopwords from NLTK
        nltk.download('stopwords')

        # Define stop words
        self.stop_words = set(stopwords.words('english'))

        # ---------------------------- # Coursera Cleaning # ---------------------------- #
        print("Setup coursera dataset")
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

        # Apply self._remove_commas function to each row
        coursera_data = coursera_data.apply(self._remove_commas)

        # Apply self._clean_attributes function to the 'Attributes' column
        coursera_data['Attributes'] = coursera_data['Attributes'].apply(self._clean_attributes)

        # ---------------------------- # EDX Cleaning # ---------------------------- #

        print("Setup EDX dataset")
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

        # Apply self._remove_commas function to each row
        edx_data = edx_data.apply(self._remove_commas)

        # Apply self._clean_attributes function to the 'Attributes' column
        edx_data['Attributes'] = edx_data['Attributes'].apply(self._clean_attributes)

        # ---------------------------- # Combine # ---------------------------- #
        print("Combine datasets and extract attributes")
        # Concatenate Coursera and EdX data
        self.courses_all = pd.concat([coursera_data, edx_data], ignore_index=True).sample(frac=1, random_state=42)

        attributes = []
        for row in self.courses_all['Attributes']:
            for attribute in row.split(','):
                attributes.append(attribute.strip())

        print("Setup CountVectorizer for recommendations")
        # Initialize CountVectorizer
        self.countv = CountVectorizer(max_features=5000,stop_words='english')

        # Transform text data into matrix
        self.X = self.countv.fit_transform(self.courses_all['Attributes']).toarray()

        # Clean tags
        cleaned_tags = []
        for tag in attributes:
            cleaned_tag = re.sub(r'[^a-zA-Z\s]', '', tag)
            cleaned_tag = re.sub(r'\s+', ' ', cleaned_tag).strip()
            cleaned_tags.append(cleaned_tag)

        # Remove empty tags and deduplicate
        cleaned_tags = [tag for tag in cleaned_tags if tag]
        self.cleaned_tags = list(set(cleaned_tags))

        difficulty = []
        for row in self.courses_all['Difficulty Level']:
            for entry in row.split(','):
                difficulty.append(entry.strip())
        self.difficulty = list(set(difficulty))

    # Function to map user input
    def get_recommendations(self, keyword):
        print(f"Getting recommendations for '{keyword}'")
        keyword_vector = self.countv.transform([keyword])
        distances = cosine_distances(keyword_vector, self.X)
        closest_indices = distances.argsort()[0][:5]
        relevant_courses = self.courses_all.iloc[closest_indices][['Course Name', 'Course URL']]
        relevant_courses['Course Name'] = relevant_courses['Course Name'].str.replace(',', ' ')
        return relevant_courses
