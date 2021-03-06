import streamlit as st
import pymongo
from pymongo import MongoClient 
    
# Connect with the portnumber and host  
client = MongoClient("mongodb://localhost:27017/")  

import pandas as pd
import json
import numpy as np

data= pd.read_csv("zomato.csv")
data.head()

json_data = json.loads(data.to_json(orient='records'))


dblist=client.list_database_names()

# Access database  
mydb = client['bdmszomo'] 
collection = mydb['zomo']

collection.remove()
collection.insert_many(json_data)

# preprocessing some values
collection.update_many({},[{"$set": {"approx_cost(for two people)": {"$convert":{"input" : "$approx_cost(for two people)", "to":"int", "onError":"$approx_cost(for two people)", "onNull": None}}}}])

q0_agg_result=collection.aggregate([{ "$group": {"_id": "$listed_in(city)", "count": { "$sum": 1 } } },
                                 {"$sort": { "count": -1 } }])



st.header("19AIE304")
st.header("BDMS PROJECT")
st.header("ANALYSIS ZOMATO DATASET")
st.header("  ")
st.header("  ")


st.write('Total number of hotels:     ',len(list(q0_agg_result)))

   
    
import numpy as np
import pandas as pd
import warnings
warnings.filterwarnings('always')
warnings.filterwarnings('ignore')
import re
from nltk.corpus import stopwords
from sklearn.metrics.pairwise import linear_kernel
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer

zomato_real= collection.aggregate([{"$project": {"name":"$name" ,"approx_cost(for two people)":"$approx_cost(for two people)",
                                            "rate":"$rate","reviews_list":"$reviews_list","cuisines":"$cuisines"}}])


zomato_real=pd.DataFrame(zomato_real)


# st.write(zomato_real.head())



#Deleting Unnnecessary Columns
zomato=zomato_real.drop(['_id'],axis=1) #Dropping the column "dish_liked", "phone", "url" and saving the new dataset as "zomato"
# zomato=zomato_real[['name','approx_cost(for two people)','rate','reviews_list','cuisines']]
#Removing the Duplicates
zomato.duplicated().sum()
zomato.drop_duplicates(inplace=True)

#Remove the NaN values from the dataset
zomato.isnull().sum()
zomato.dropna(how='any',inplace=True)


# st.write(zomato)

#Changing the column names
zomato = zomato.rename(columns={'approx_cost(for two people)':'cost'})

#Some Transformations
zomato['cost'] = zomato['cost'].astype(str) #Changing the cost to string
zomato['cost'] = zomato['cost'].apply(lambda x: x.replace(',','.')) #Using lambda function to replace ',' from cost
zomato['cost'] = zomato['cost'].astype(float)

#Removing '/5' from Rates
zomato = zomato.loc[zomato.rate !='NEW']
zomato = zomato.loc[zomato.rate !='-'].reset_index(drop=True)
remove_slash = lambda x: x.replace('/5', '') if type(x) == np.str else x
zomato.rate = zomato.rate.apply(remove_slash).str.strip().astype('float')

# Adjust the column names
zomato.name = zomato.name.apply(lambda x:x.title())
# zomato.online_order.replace(('Yes','No'),(True, False),inplace=True)
# zomato.book_table.replace(('Yes','No'),(True, False),inplace=True)

## Computing Mean Rating
restaurants = list(zomato['name'].unique())
zomato['Mean Rating'] = 0

for i in range(len(restaurants)):
    zomato['Mean Rating'][zomato['name'] == restaurants[i]] = zomato['rate'][zomato['name'] == restaurants[i]].mean()
    
from sklearn.preprocessing import MinMaxScaler
scaler = MinMaxScaler(feature_range = (1,5))
zomato[['Mean Rating']] = scaler.fit_transform(zomato[['Mean Rating']]).round(2)


# st.write(zomato.head())


zomato["reviews_list"] = zomato["reviews_list"].str.lower()

## Removal of Puctuations
import string
PUNCT_TO_REMOVE = string.punctuation
def remove_punctuation(text):
    """custom function to remove the punctuation"""
    return text.translate(str.maketrans('', '', PUNCT_TO_REMOVE))

zomato["reviews_list"] = zomato["reviews_list"].apply(lambda text: remove_punctuation(text))

## Removal of Stopwords
from nltk.corpus import stopwords
STOPWORDS = set(stopwords.words('english'))
def remove_stopwords(text):
    """custom function to remove the stopwords"""
    return " ".join([word for word in str(text).split() if word not in STOPWORDS])

zomato["reviews_list"] = zomato["reviews_list"].apply(lambda text: remove_stopwords(text))

## Removal of URLS
def remove_urls(text):
    url_pattern = re.compile(r'https?://\S+|www\.\S+')
    return url_pattern.sub(r'', text)

zomato["reviews_list"] = zomato["reviews_list"].apply(lambda text: remove_urls(text))

zomato[['reviews_list', 'cuisines']].sample(5)


# st.write(zomato.head())


# RESTAURANT NAMES:
restaurant_names = list(zomato['name'].unique())
def get_top_words(column, top_nu_of_words, nu_of_word):
    vec = CountVectorizer(ngram_range= nu_of_word, stop_words='english')
    bag_of_words = vec.fit_transform(column)
    sum_words = bag_of_words.sum(axis=0)
    words_freq = [(word, sum_words[0, idx]) for word, idx in vec.vocabulary_.items()]
    words_freq =sorted(words_freq, key = lambda x: x[1], reverse=True)
    return words_freq[:top_nu_of_words]
    

import pandas

# Randomly sample 60% of your dataframe
df_percent = zomato.sample(frac=0.5)


df_percent.set_index('name', inplace=True)
indices = pd.Series(df_percent.index)

# Creating tf-idf matrix
tfidf = TfidfVectorizer(analyzer='word', ngram_range=(1, 2), min_df=0, stop_words='english')
tfidf_matrix = tfidf.fit_transform(df_percent['reviews_list'])

cosine_similarities = linear_kernel(tfidf_matrix, tfidf_matrix)


# st.write(df_percent.head())


def recommend(name, cosine_similarities = cosine_similarities):
    
    # Create a list to put top restaurants
    recommend_restaurant = []
    
    # Find the index of the hotel entered
    idx = indices[indices == name].index[0]
    
    # Find the restaurants with a similar cosine-sim value and order them from bigges number
    score_series = pd.Series(cosine_similarities[idx]).sort_values(ascending=False)
    
    # Extract top 30 restaurant indexes with a similar cosine-sim value
    top30_indexes = list(score_series.iloc[0:31].index)
    
    # Names of the top 30 restaurants
    for each in top30_indexes:
        recommend_restaurant.append(list(df_percent.index)[each])
    
    # Creating the new data set to show similar restaurants
    df_new = pd.DataFrame(columns=['cuisines', 'Mean Rating', 'cost'])
    
    # Create the top 30 similar restaurants with some of their columns
    for each in recommend_restaurant:
        df_new = df_new.append(pd.DataFrame(df_percent[['cuisines','Mean Rating', 'cost']][df_percent.index == each].sample()))
    
    # Drop the same named restaurants and sort only the top 10 by the highest rating
    df_new = df_new.drop_duplicates(subset=['cuisines','Mean Rating', 'cost'], keep=False)
    df_new = df_new.sort_values(by='cost', ascending=False).head(10)
    
    st.write('TOP %s RESTAURANTS LIKE %s WITH SIMILAR REVIEWS: ' % (str(len(df_new)), name))
    
    return df_new



# shop_name = st.text_input('Hotel Name', "Sultan'S Biryani")

shop_name = st.selectbox("Selct ur restaruent:    ",restaurant_names)

xx=recommend(str(shop_name))     

st.write(xx)







    
    
    
    
    
    