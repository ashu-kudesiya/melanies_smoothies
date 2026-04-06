# Import python packages.
import streamlit as st
# from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col
import requests  

# Write directly to the app.
st.title(f":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write(
  """Choose the Fruits you want in your custom Smoothie!
  """)

name_on_order = st.text_input("Name on Smoothie: ")
st.write("The name on your smoothie will be: ", name_on_order)

# session = get_active_session()
cnx = st.connection("snowflake")
session = cnx.session()

my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
# st.dataframe(data=my_dataframe, use_container_width=True)

# Convert to pandas → list
fruit_list = my_dataframe.to_pandas()["FRUIT_NAME"].tolist()

# Multiselect
ingredients_list = st.multiselect(
    "Choose up to 5 ingredients:",
    # fruit_list
    my_dataframe,
    max_selections=5
)

# ✅ IF block (only run if something selected)
if ingredients_list:
    
    # st.write(ingredients_list)
    # st.text(ingredients_list)

    # ✅ Step 1: create empty string (IMPORTANT: no space)
    ingredients_string = ''

    # ✅ Step 2: loop through list
    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '
        st.subheader(fruit_chosen + ' Nutrition Information')
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/" + fruit_chosen)  
        sf_df = st.dataframe(data=smoothiefroot_response.json(),use_container_width=True)


    # ✅ Step 3: display string
    st.write(ingredients_string)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
                        values ('""" + ingredients_string + """','""" + name_on_order + """')"""

    # st.write(my_insert_stmt)
    # st.stop()

    # st.write(my_insert_stmt)
    # ✅ Button (important change)
    time_to_insert = st.button('Submit Order')

    # ✅ Insert ONLY when button clicked
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success(f"Your Smoothie is ordered, {name_on_order}! 🎉")
