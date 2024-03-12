# -*- coding: utf-8 -*-
"""
Created on Thu Feb 29 22:38:35 2024

@author: D VAMIDHAR (dvamsidhar2002@gmail.com)
"""

# Importing necessary libraries


import pandas as pd
import difflib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.tokenize import RegexpTokenizer
import streamlit as st

def intent_recognition(query):
    data = pd.read_excel('Jobs.xlsx')
    
    tokenizer = RegexpTokenizer(r'\w+')
    data['Query of the Customer'] = data['Query of the Customer'].apply(lambda x: ' '.join(tokenizer.tokenize(x)))
    
    combine_feat = data['Query of the Customer'] + ' ' + data['Query Type'] + ' ' + data['Who Can Help']
    
    # to vectorize the features
    
    vectorizer = TfidfVectorizer()
    feature_vectors = vectorizer.fit_transform(combine_feat)
    
    # similarity scores
    similarity  = cosine_similarity(feature_vectors)
    
    
    
    list_of_all_queries =data['Query of the Customer'].tolist()
    find_close_match = list()
    find_close_match = difflib.get_close_matches(query, list_of_all_queries)
    
    close_match = find_close_match[0]
    
    index_of_the_query = data[data['Query of the Customer'] == close_match]['index'].values[0]
    
    similarity_score = list(enumerate(similarity[index_of_the_query]))
    
    sorted_similarity_score = sorted(similarity_score, key = lambda x:x[1], reverse = True) 
    
    query_of_the_user = list()
    
    for query1 in sorted_similarity_score:
      index = query1[0]
      query_of_the_user.append(data[data.index==index]['Query Type'].values[0])
      
      
    print('Your query is related to : ')
    # Set to store unique elements encountered so far
    query_type = set()
    i = 0
    # Iterate over the list and print only those elements that are not in the set
    for word in query_of_the_user:
        if word not in query_type:
            print(word)
            query_type.add(word)
            i+=1
    
            if i>=3:
                break

    import json

    def find_details(query_1):
    
      # Load the JSON data from the file
      with open("Employee Details.json", "r") as f:
        data = json.load(f)
    
      # Find employees with matching support
      matching_details = []
      for details in data:
        if query_1.lower() in details["Support "].lower():
          matching_details.append(details)
    
      return matching_details    
  
    query_1 = query_of_the_user[0]
    matching_details = find_details(query_1)
    
    def format_employee_info(employee):
        info_string = (f"Query related to : {query_type}\n\n"
                       f"\nPLEASE CONTACT THE FOLLOWING PERSON FOR SOLUTION : \n"
                       f"\nEmployee Name: {employee['Name ']}\n"
                       f"\nDepartment: {employee['Department ']}\n"
                       f"\nSupport: {employee['Support ']}\n"
                       f"\nPhone Number: {employee['Phone Number ']}\n"
                       f"\nEmail: {employee['Email Id ']}\n"
                       + "-" * 20 + "\n")
        return info_string

    query_1 = query_of_the_user[0]
    matching_details = find_details(query_1)
    
    print("USER's Query : ")
    print(query)
    print("Query related to : ", query_of_the_user[0])
    print("="*50)
    print("Please contact the following person(s) for help : ")
    print("="*50)
    if matching_details:
        # Print employee information
        for employee in matching_details:
            employee_info_string = format_employee_info(employee)
        return employee_info_string
    else:
        return "No matching employees found."


def main():
    st.title('User Interaction Portal')
    #user input
    query = st.text_input('Enter your query : ')    
    
    if st.button('Post Query'):
        response = intent_recognition(query)
    
    st.success(response)
        

if __name__ == "__main__":
    main()

