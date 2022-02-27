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




option = st.selectbox(
        'Select ur question?',
        ('1. Number of orders in each Location', '2. Liked Dishes', '3. Number of orders in each hotel in Bangalore',
         '4.Number of votes for each hotel','5. About Menu','6. About table booking and online ordering','7. Number of orders in each hotel in each Area in Bangalore',
         '8. Available cuisines','9. Cost efficient hotels','10. About Rest type','11. Best rated hotels'))

st.header("  ")
st.header("  ")
st.header("  ")


    
st.subheader(option)
st.header("  ")

if(option=="1. Number of orders in each Location"):
    q1_agg_result_1=collection.aggregate([{ "$group": {"_id": "$listed_in(city)", "count": { "$sum": 1 } } },
                                     {"$sort": { "count": -1 } },
                                    {"$limit": 5}])
    
    st.header("  ")
    st.subheader("         i. Top 5 Locations")
    

    
    st.write(list(q1_agg_result_1))


    q1_agg_result_2=collection.aggregate([{ "$group": {"_id": "$listed_in(city)", "count": { "$sum": 1 } } },
                                     {"$sort": { "count": 1 } },
                                       {"$limit": 5}])
    
    
    st.header("  ")
    st.subheader("         ii. Last 5 Locations")
    st.write(list(q1_agg_result_2))


elif(option=='2. Liked Dishes'):
    
    q2=[]
    for rec in collection.find({'dish_liked':{'$ne':None}}):
        q2.append(rec.get('dish_liked'))


    from functools import reduce
    q2flatlist = reduce(lambda a,b:a+b, q2)
    q2flatlist=q2flatlist.split(", ")
    dfq2 = pd.DataFrame({'food':q2flatlist})
    x=(dfq2['food'].value_counts())
    x=x.to_frame()
    x=x.set_axis(['no. of counts'], axis=1, inplace=False)

    x[0:6].plot(kind = 'pie',y = 'no. of counts', figsize=(10, 10))

    
    st.header("  ")
    st.subheader("         i. Top 5 Dishes")
    st.write(x.head(5))

    st.header("  ")
    st.subheader("         ii. Last 5 Dishes")    
    st.write(x.tail(5))


elif(option=='3. Number of orders in each hotel in Bangalore'):
    
    q3_agg_result=collection.aggregate([{ "$group": {"_id": "$name","count": { "$sum": 1 } } },
                                     {"$sort": { "count": -1 }}])

#     st.write(list(q3_agg_result))
    
    
    df = pd.DataFrame(q3_agg_result)
    st.write(df)
    
#     df1=df[0:30]

#     st.image(df1.plot(kind = 'bar',x = '_id', y = 'count'))
#     st.bar_chart(df1.T)
    

    q3_agg_result_1=collection.aggregate([{ "$group": {"_id": "$name","count": { "$sum": 1 } } },
                                     {"$sort": { "count": -1 }},
                                       {"$limit": 5}])

    st.header("  ")
    st.subheader("         i. Top 5 Hotels")
    
    st.write(list(q3_agg_result_1))



    q3_agg_result_2=collection.aggregate([{ "$group": {"_id": "$name","count": { "$sum": 1 } } },
                                     {"$sort": { "count": 1 }},
                                       {"$limit": 5}])
    
    
    st.header("  ")
    st.subheader("         ii. Last 5 Hotels")
    
    st.write(list(q3_agg_result_2))
    
    
    
    
    
    
elif(option=='4.Number of votes for each hotel'):
    
    q4_agg_result=collection.aggregate([{ "$group": {"_id": "$name","votes": { "$sum": "$votes" } } },
                                     {"$sort": { "votes": -1 }}])

    df = pd.DataFrame(q4_agg_result)
    st.write(df)    
    

    q4_agg_result_1=collection.aggregate([{ "$group": {"_id": "$name","votes": { "$sum": "$votes" } } },
                                     {"$sort": { "votes": -1 }},
                                       {"$limit": 5}])
    
    st.header("  ")
    st.subheader("         i. Top 5 highly voted Hotels")
    
    st.write(list(q4_agg_result_1))

    q4_agg_result_2=collection.aggregate([{ "$group": {"_id": "$name","votes": { "$sum": "$votes" } } },
                                     {"$sort": { "votes": 1 }},
                                       {"$limit": 5}])
    
    
    st.header("  ")
    st.subheader("         ii. Last 5 Hotels")
    
    st.write(list(q4_agg_result_2))
    

    
elif(option=='5. About Menu'):
    
    q5_1=[]
    for rec in collection.find({'menu_item':{'$ne':'[]'}}):
        q5_1.append(rec.get('name'))
    
    st.header("  ")
    st.write("         i. Hotels with menu:     ",len(q5_1))
#     st.write((q5_1))


    q5_2=[]
    for rec in collection.find({'menu_item':{'$eq':'[]'}}):
        q5_2.append(rec.get('name'))

    st.header("  ")
    st.write("         ii. Hotels without menu:    ",len(q5_2))
#     st.write((q5_2))
    
    
elif(option=='6. About table booking and online ordering'):
  
    q6_agg_result=collection.aggregate([{ "$group": {"_id": {"booking table": "$book_table","online order": "$online_order"},"count": { "$addToSet": "$name" } }},
                                       {"$sort": { "_id": -1 }}])



    st.header("  ")
    for res in list(q6_agg_result):
        st.write("         "+res.get('_id'),len(res.get('count')))
        
    
    
elif(option=='7. Number of orders in each hotel in each Area in Bangalore'):
    
    q7_agg_result= collection.aggregate([{"$group": {"_id": {"name":"$name" ,"location":"$location" },"count": { "$sum": 1 }}},
                                        {"$sort": { "count": -1 }}])


    st.header("  ")
    st.subheader("         i. Top 5 orders in Hotels w.r.t towns")
    
    q7_agg_result_1= collection.aggregate([{"$group": {"_id": {"name":"$name" ,"location":"$location" },"count": { "$sum": 1 }}},
                                        {"$sort": { "count": -1 }},
                                        {"$limit": 5}])

    st.write(list(q7_agg_result_1))


    st.header("  ")
    st.subheader("         ii. Least 5 orders in Hotels w.r.t towns")
    
    q7_agg_result_2= collection.aggregate([{"$group": {"_id": {"name":"$name" ,"location":"$location" },"count": { "$sum": 1 }}},
                                        {"$sort": { "count": 1 }},
                                        {"$limit": 5}])

    st.write(list(q7_agg_result_2))
    
    
elif(option=='8. Available cuisines'):

    q8_agg_result= collection.aggregate([{"$group": {"_id":"$cuisines"}}])
    q8=[]
    for res in list(q8_agg_result):
        q8.append(res.get('_id'))



    q8=np.array(q8)
    q8_1=np.array([])
    for i in range(len(q8)):
        q8i=q8[i]
        q8_1=np.append(q8_1,(np.array(str(q8i).split(", "))))
    dfq8 = pd.DataFrame({'cusins':q8_1})
    x=(dfq8['cusins'].value_counts())
    x=x.to_frame()
    x=x.set_axis(['no. of counts'], axis=1, inplace=False)

    
    st.write(x)
    
    st.header("  ")
    st.subheader("         i. Top 5 cuisines")
    
    st.write(x.head(5))
    
    
    st.header("  ")
    st.subheader("         ii. Least 5 cuisines")
    
    st.write(x.tail(5))

    
elif(option=='9. Cost efficient hotels'):
    
    q9_agg_result= collection.aggregate([{"$group": {"_id":"$name" ,"rating": { "$addToSet":"$rate" },"approx_cost": { "$avg":"$approx_cost(for two people)"} }},
                                          {"$sort": { "_id": -1 }}])

    val9=[]
    for res in list(q9_agg_result):
        l2=[]
        for i in (list(res.get('rating'))):
    #         print(i)
            if(i!=None):
                if "/" in i:
                    l2.append(float(i.split( "/" )[0]))
        val9.append([res.get('_id'),l2,res.get('approx_cost')])   


    q9_1=[]
    for i in val9:
        if (len(i[1])!=0):
            q9_1.append([i[0],round(np.average(i[1]),2),i[2]])


#     st.subheader("ii. Last 5 Hotels")

    df=pd.DataFrame(q9_1)
    # df.head(5)
    df.columns=['name','rating','cost (two persons)']
    df=df.dropna()
    st.write(df.sort_values(by=['rating','cost (two persons)'],ascending=[False,True], na_position = 'first'))


    #thresolds
    high_rating=4.5
    low_rating =3.5
    high_cost = 500
    low_cost=500

    
    st.header("  ")
    st.subheader("         i. Best hotels    (high rating (> 4.5), low cost (<500))")

    st.write(df[(df['rating'] > high_rating) & (df['cost (two persons)'] <low_cost)])
    
    st.header("  ")
    st.subheader("         ii. Average hotels     (low rating (<3.5), high cost (>500)) & (high rating (>4.5), high cost (>500))")
    
    st.write(df[((df['rating'] < low_rating) & (df['cost (two persons)'] >low_cost))|((df['rating'] > high_rating) & (df['cost (two persons)'] >high_cost))].sort_values(by=['rating','cost (two persons)'],ascending=[False,False], na_position = 'first'))

    st.header("  ")
    st.subheader("         iii. Below Average hotels     (low rating(<3.5), low cost(<500))")
    
    st.write(df[(df['rating'] < low_rating) & (df['cost (two persons)'] <low_cost)])


    
elif(option=='10. About Rest type'):
    
    q10_agg_res = collection.aggregate([{"$group": {"_id":{"name":"$name" },"rest type": { "$addToSet":"$rest_type" }}},
                                       ])

    
elif(option=='11. Best rated hotels'):

    q11_agg_res = collection.aggregate([{"$group": {"_id":"$name","rating": { "$addToSet":"$rate" },"value": { "$sum": "$votes" }}},
                                       {"$sort": { "value":-1}}])


    val11=[]
    for res in list(q11_agg_res):
        l2=[]
        for i in (list(res.get('rating'))):
    #         print(i)
            if(i!=None):
                if "/" in i:
                    l2.append(float(i.split( "/" )[0]))
        val11.append([res.get('_id'),l2,res.get('value')])   


    q111=[]
    for i in val11:
        if (len(i[1])!=0):
            q111.append([i[0],round(np.average(i[1]),2),i[2]])


            
#     st.subheader("ii. Last 5 Hotels")
            
    df=pd.DataFrame(q111)
    df.columns=['name','rating','votes'] 
    df=df.dropna()
    
    st.header("  ")
    st.write(df.sort_values(by=['rating','votes'],ascending=[False,False], na_position = 'first'))

    #thresolds
    high_rating=4.5
    low_rating =3.5
    high_votes = 50000
    low_votes=10000

    st.header("  ")
    st.subheader("         i. more than 4.5 stars and 50k votes")
    
    st.write(df[(df['rating'] > high_rating) & (df['votes'] > high_votes)])

    
    st.header("  ")
    st.subheader("         ii. less than 3. stars and 10k votes")
    
    st.write(df[(df['rating'] < low_rating) & (df['votes'] < low_votes)])


    
 