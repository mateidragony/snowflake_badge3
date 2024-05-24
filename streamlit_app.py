# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col, when_matched
import requests
import pandas

# from snowflake.snowpark.context import get_active_session

# option = st.selectbox(
#    "What is your favorite fruit?",
#    ("-- Please select a fruit --", "Banana", "Strawberries", "Peaches"),
# )

# st.write("You selected: ", "None" if option == "-- Please select a fruit --" else option)

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write(
    """Choose the fruits you want in your custom Smoothie!
    """
)

# session = get_active_session()
cnx = st.connection("snowflake")
session = cnx.session()


# option = st.selectbox(
#    "What is your favorite fruit?",
#    ("-- Please select a fruit --", "Banana", "Strawberries", "Peaches"),
# )

# st.write("You selected: ", "None" if option == "-- Please select a fruit --" else option)

my_df = session.table("smoothies.public.fruit_options").select(col("FRUIT_NAME"), col("SEARCH_ON"))

pd_df = my_df.to_pandas()


name = st.text_input("Name on Smoothie", "")



options = st.multiselect(
    "Choose up to 5 ingredients",
    my_df,
    max_selections=5)

# st.write("First selected:", options[0] if options else None)

if options:
    ingredients_string = ''
    for fruit in options:
        ingredients_string += fruit + " "

        search_on=pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
        
        st.subheader(fruit + ' Nutrition Information')
        fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + search_on.lower())
        fv_df = st.dataframe(data=fruityvice_response.json(), use_container_width=True)


    insert_stmt = """
    insert into smoothies.public.orders(ingredients, name_on_order)
    values ('%s', '%s')
    """ % (ingredients_string, name)

    submit_button = st.button("Submit Order")
    
    if submit_button:
        session.sql(insert_stmt).collect()
        st.success('Your smoothie is ordered, %s!' % name, icon="✅")






































