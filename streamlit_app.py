# # Import python packages.
# import streamlit as st
# # from snowflake.snowpark.context import get_active_session
# from snowflake.snowpark.functions import col
# import requests  

# # Write directly to the app.
# st.title(f":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
# st.write(
#   """Choose the Fruits you want in your custom Smoothie!
#   """)

# name_on_order = st.text_input("Name on Smoothie: ")
# st.write("The name on your smoothie will be: ", name_on_order)

# # session = get_active_session()
# cnx = st.connection("snowflake")
# session = cnx.session()

# my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'), col('SEARCH_ON'))
# # st.dataframe(data=my_dataframe, use_container_width=True)
# # st.stop()

# #Convert the Snowpark Dataframe to a Pandas Dataframe so we can use the LOC function
# pd_df=my_dataframe.to_pandas()
# # st.dataframe(pd_df)
# # st.stop()

# # Convert to pandas → list
# fruit_list = my_dataframe.to_pandas()["FRUIT_NAME"].tolist()

# # Multiselect
# ingredients_list = st.multiselect(
#     "Choose up to 5 ingredients:",
#     # fruit_list
#     my_dataframe,
#     max_selections=5
# )

# # ✅ IF block (only run if something selected)
# if ingredients_list:
    
#     # st.write(ingredients_list)
#     # st.text(ingredients_list)

#     # ✅ Step 1: create empty string (IMPORTANT: no space)
#     ingredients_string = ''

#     # ✅ Step 2: loop through list
#     for fruit_chosen in ingredients_list:
#         ingredients_string += fruit_chosen + ' '

#         search_on = pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
#         st.write('The search value for ', fruit_chosen, ' is ', search_on, '.')


      
#         st.subheader(fruit_chosen + ' Nutrition Information')
#         smoothiefroot_response = requests.get(f"https://my.smoothiefroot.com/api/fruit/{search_on}")  
#         sf_df = st.dataframe(data=smoothiefroot_response.json(),use_container_width=True)


#     # ✅ Step 3: display string
#     st.write(ingredients_string)

#     my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
#                         values ('""" + ingredients_string + """','""" + name_on_order + """')"""

#     # st.write(my_insert_stmt)
#     # st.stop()

#     # st.write(my_insert_stmt)
#     # ✅ Button (important change)
#     time_to_insert = st.button('Submit Order')

#     # ✅ Insert ONLY when button clicked
#     if time_to_insert:
#         session.sql(my_insert_stmt).collect()
#         st.success(f"Your Smoothie is ordered, {name_on_order}! 🎉")




# Import python packages
import streamlit as st
import pandas as pd
from snowflake.snowpark.functions import col
import requests  

# -------------------------------
# Title
# -------------------------------
st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write("Choose the Fruits you want in your custom Smoothie!")

# -------------------------------
# Name Input
# -------------------------------
name_on_order = st.text_input("Name on Smoothie:")
st.write("The name on your smoothie will be:", name_on_order)

# -------------------------------
# Snowflake Connection
# -------------------------------
cnx = st.connection("snowflake")
session = cnx.session()

# -------------------------------
# Get Data from Snowflake
# -------------------------------
my_dataframe = session.table("smoothies.public.fruit_options") \
    .select(col('FRUIT_NAME'), col('SEARCH_ON'))

# Convert to Pandas
pd_df = my_dataframe.to_pandas()

# Optional: Display table (for debugging)
# st.dataframe(pd_df)

# -------------------------------
# Multi-select
# -------------------------------
ingredients_list = st.multiselect(
    "Choose up to 5 ingredients:",
    pd_df['FRUIT_NAME'].tolist(),
    max_selections=5
)

# -------------------------------
# Process Selection
# -------------------------------
if ingredients_list:

    ingredients_string = ''

    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '

        # ✅ Get SEARCH_ON value
        search_on = pd_df.loc[
            pd_df['FRUIT_NAME'] == fruit_chosen,
            'SEARCH_ON'
        ].iloc[0]

        # ✅ Debug message (as per lab)
        st.write('The search value for', fruit_chosen, 'is', search_on)

        # -------------------------------
        # API Call
        # -------------------------------
        st.subheader(fruit_chosen + " Nutrition Information")

        response = requests.get(
            "https://my.smoothiefroot.com/api/fruit/" + search_on
        )

        if response.status_code == 200:
            st.dataframe(response.json(), use_container_width=True)
        else:
            st.error(f"Failed to fetch data for {fruit_chosen}")

    # -------------------------------
    # Show Selected Ingredients
    # -------------------------------
    st.write("Your Smoothie Ingredients:", ingredients_string)

    # -------------------------------
    # Insert into Snowflake
    # -------------------------------
    my_insert_stmt = f"""
        insert into smoothies.public.orders(ingredients, name_on_order)
        values ('{ingredients_string}', '{name_on_order}')
    """

    # -------------------------------
    # Submit Button
    # -------------------------------
    if st.button("Submit Order"):
        session.sql(my_insert_stmt).collect()
        st.success(f"Your Smoothie is ordered, {name_on_order}! 🎉")
