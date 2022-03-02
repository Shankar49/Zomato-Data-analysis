# Zomato-Data-analysis

In this project We have performed exploratory data analysis on zomato data set and drawn some meaningful visualizations and information using MongoDb, a recomendation system for hotel suggestion deployed on Streamlit platform

## About Dataset


* url : contains the url of the restaurant in the zomato website
    
* address : contains the address of the restaurant in Bengaluru
    
* name : contains the name of the restaurant
* online_order : whether online ordering is available in the restaurant or not
* book_table : table book option available or not
* rate : contains the overall rating of the restaurant out of 5
* votes : contains total number of rating for the restaurant as of the above mentioned date
* phone : contains the phone number of the restaurant
* location : contains the neighborhood in which the restaurant is located
* rest_type : restaurant type
* dish_liked : dishes people liked in the restaurant
* cuisines : food styles, separated by comma
* approx_cost(for two people) : contains the approximate cost for meal for two people
* reviews_list : list of tuples containing reviews for the restaurant, each tuple consists of two values, rating and review by the customer
* menu_item : contains list of menus available in the restaurant
* listed_in(type) : type of meal
* listed_in(city) : contains the neighborhood in which the restaurant is listed

## Analysed Questions

1. Number of hotels in Bangalore
2. Number of orders in each Location
3. Liked Dishes
4. Number of orders in each hotel in Bangalore
5. Number of votes for each hotel
6. Hotels with Menu
7. About table booking and online ordering
8. Number of orders in each hotel in each Area in Bangalore
9. Cuisines available in each hotel
10. Cost effcient and quality hotels (Based on Rating and Cost)
11. Types of hotels
12. Best rated hotels

## Recomendation system 
we also build a recommentation system to give the list of hotels that ate similar to out input. For example, if a user need to find a hotel in the Bangaluru location similar to hotel Sultan's Briyani, the system recommond hotels like Ambur Briyani Classic, Pot Biryani, Pallavi Restaurent, etc.. Along with the hotel rating and cost per two peoples. 

This recomendation was based upon Available cuisines, Mean Rating, Cost and Customer reviews.
