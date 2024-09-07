# Import python packages
import streamlit as st
import requests
from snowflake.snowpark.functions import col
# Write directly to the app
st.title(":cup_with_straw: Customize your drinks :cup_with_straw: ")
st.write(
    """choose the fruits you want in your smoothie !
    """
)
name_on_order= st.text_input("Name on smoothie")

cnx= st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'), col('SEARCH_ON'))
pd_df= my_dataframe.to_pandas()

ingredients_list = st.multiselect(
    "Choose up to 5 fruits ",
    my_dataframe , max_selections= 5
)
if ingredients_list and name_on_order:
    # st.write(ingredients_list)
    # st.text(ingredients_list)
    ingredients_string= ""
    for fruit_chosen in ingredients_list:
        ingredients_string+= fruit_chosen + ' '
        search_on=pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
        st.write('The search value for ', fruit_chosen,' is ', search_on, '.')
        st.subheader(fruit_chosen + ' Nutrition Information')
        api_link= "https://fruityvice.com/api/fruit/"+ search_on
        fruityvice_response = requests.get(api_link)
        st.dataframe(fruityvice_response.json())
        
        # fv_df= st.dataframe( data= fruityvice_response.json()  ,use_container_width= true)

        
    # st.write(ingredients_string)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
                values ('""" + ingredients_string +  """','"""+ name_on_order+ """')"""

    # st.write(my_insert_stmt)
    time_toinsert= st.button('submit Order')
    if time_toinsert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")




