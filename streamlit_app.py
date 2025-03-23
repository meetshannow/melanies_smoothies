# Import python packages
import streamlit as st
import pandas as pd
import requests
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write("Choose the fruits you want in your custom Smoothie!")
 
Name_on_order = st.text_input("Name on Smoothie")
st.write("The Name on your smoothie will be ", Name_on_order)

cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select (col('FRUIT_NAME'),col('SEARCH_ON'))
pd_df=my_dataframe.to_pandas()

#st.dataframe(data=my_dataframe, use_container_width=True)

ingredients_list = st.multiselect(
    'Choose upto 5 Ingredients:',
   my_dataframe,
    max_selections=5
)
if ingredients_list :
   # st.write(ingredients_list)
   # st.text(ingredients_list)
    
    ingredients_string = ''
    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' ' 
        search_on=pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen,'SEARCH_ON'].iloc[0]
        st.subheader(fruit_chosen + ' Nutrition Information')
        # smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/"+search_on)
        #sf_df=st.dataframe(data=smoothiefroot_response.json(),use_container_width=True)
        fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + str(search_on))
        fv_df = st.dataframe(data=fruityvice_response.json(),use_container_width=True)
        #st.write(ingredients_string)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
            values ('""" + ingredients_string + """','""" + Name_on_order + """')"""
    time_to_insert = st.button('Submit Order')
    st.write(my_insert_stmt)
    
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered,'+ Name_on_order, icon="✅")


 
