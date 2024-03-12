#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import difflib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.tokenize import RegexpTokenizer


# In[2]:


data = pd.read_excel('Jobs.xlsx')
data.head()


# In[3]:


# removing punctuations from the query of the customer
tokenizer = RegexpTokenizer(r'\w+')
data['Query of the Customer'] = data['Query of the Customer'].apply(lambda x: ' '.join(tokenizer.tokenize(x)))


# In[4]:


# combining all the column's data into a single feature to use it for processing of the queries
combine_feat = data['Query of the Customer'] + ' ' + data['Query Type'] + ' ' + data['Who Can Help']
combine_feat


# In[5]:


# to vectorize the features

vectorizer = TfidfVectorizer()
feature_vectors = vectorizer.fit_transform(combine_feat)


# In[6]:


# similarity scores
similarity  = cosine_similarity(feature_vectors)


# In[7]:


print(similarity)


# In[8]:


# taking user input as query
query = input('Enter your query : ')


# In[9]:


# putting all the queries into one list
list_of_all_queries =data['Query of the Customer'].tolist()
list_of_all_queries


# In[10]:


# finding closest match to user input from the list of all queries

find_close_match = difflib.get_close_matches(query, list_of_all_queries)
find_close_match


# In[11]:


close_match = find_close_match[0]
close_match


# In[12]:


#index of the closest match
index_of_the_query = data[data['Query of the Customer'] == close_match]['index'].values[0]
index_of_the_query


# In[13]:


# checking similarity with every query in the dataset

similarity_score = list(enumerate(similarity[index_of_the_query]))
similarity_score


# In[14]:


len(similarity_score)


# In[15]:


#sorting the similarity score list
sorted_similarity_score = sorted(similarity_score, key = lambda x:x[1], reverse = True) 
print(sorted_similarity_score)


# In[16]:


print('Your query is related to : \n')

i = 1

query_of_the_user = list()

for query1 in sorted_similarity_score:
  index = query1[0]
  query_of_the_user.append(data[data.index==index]['Query Type'].values[0])

print(query_of_the_user)

# for name in query_type:
#   print(name)


# In[17]:


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


# ### Fetching the details from json file to help the user contact the necessary support

# In[18]:


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


# In[20]:


query_1 = query_of_the_user[0]
matching_details = find_details(query_1)

print("USER's Query : ")
print(query)
print("Query related to : ",query_of_the_user[0])
print("="*50)
print("Please contanct the following person for help : ")
print("="*50)
if matching_details:
  # Print employee information
  for employee in matching_details:
    print(f"Employee Name: {employee['Name ']}")
    print(f"Department: {employee['Department ']}")
    print(f"Support: {employee['Support ']}")
    print(f"Phone Number: {employee['Phone Number ']}")
    print(f"Email: {employee['Email Id ']}")
    print("-" * 20)
else:
  print("No matching employees found.")


# In[ ]:




