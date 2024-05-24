# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col, when_matched


# from snowflake.snowpark.context import get_active_session

# Write directly to the app
st.title(":cup_with_straw: Pending Smoothie Orders :cup_with_straw:")
st.write(
    """Orders that need to be filled.
    """
)

# option = st.selectbox(
#    "What is your favorite fruit?",
#    ("-- Please select a fruit --", "Banana", "Strawberries", "Peaches"),
# )

# st.write("You selected: ", "None" if option == "-- Please select a fruit --" else option)


# session = get_active_session()
cnx = st.connection("Snowflake")
session = cnx.session()

my_df = session.table("smoothies.public.orders").filter(col("ORDER_FILLED")==0).collect()

if not my_df:
    st.write("Looks like there's nothing here...")
else:
    e_df = st.data_editor(my_df)
    
    submitted = st.button("Submit")
    
    if submitted:
        with st.spinner('Updating Dataset..'):
            original = session.table("smoothies.public.orders")
            edited = session.create_dataframe(e_df)
            try:
                original.merge(edited, 
                           (original['order_uid'] == edited['order_uid']),
                          [when_matched().update({'ORDER_FILLED' : edited['ORDER_FILLED']})])
                st.success("Dataset Updated.")
            except:
                st.error("Something went wrong.")
























