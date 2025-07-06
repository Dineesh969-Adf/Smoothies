# Import python packages
import streamlit as st
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col 
import requests

# Write directly to the app
st.title(f":cup_with_straw: Customize Your Smoothie! :cup_with_straw: {st.__version__}")
st.write(
  """Choose the fruits you want in your custom Smoothie 
  """
)

name_on_order = st.text_input("Name on Smoothie: ")
st.write("the name on your smoothie will be: ", name_on_order)

session = get_active_session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('fruit_name'),col('search_on'))
#st.dataframe(data=my_dataframe, use_container_width=True)

#Convert the snowpark dataframe to a pandas dataframe so we can use the LOC function
pd_df = my_dataframe.to_pandas()
#st.dataframe(pd_df)
#st.stop()

ingredients_list = st.multiselect(
    "Choose upto 5 Ingrediants?"
    ,my_dataframe
    ,max_selections= 5    
)

if ingredients_list:
    ingredients_string = ''

    for fruit_chosen in ingredients_list:
      ingredients_string += fruit_chosen + ' '

      search_on=pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
      #st.write('The search value for ', fruit_chosen,' is ', search_on, '.')

      st.subheader(fruit_chosen + ' Nutrition information')
      smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/" + search_on)
      #st.text(smoothiefroot_response.json())
      st_df = st.dataframe(data = smoothiefroot_response.json(), use_container_width = true)      
      

    st.write(ingredients_string)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
            values ('""" + ingredients_string + """','""" + name_on_order + """ ')"""

    my_insert_stmt = st.button("Submit order")

#    if ingredients_string:
#        session.sql(my_insert_stmt).collect()
#        st.success('Your Smoothie is ordered!', icon="✅")

smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")
#st.text(smoothiefroot_response.json())
st_df = st.dataframe(data = smoothiefroot_response.json(), use_container_width = true)
