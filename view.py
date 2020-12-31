# Aura queries use an encrypted connection using the "neo4j+s" URI scheme
bolt_url = "bolt://34.229.69.148:33078" #"%%BOLT_URL_PLACEHOLDER%%"
user = "neo4j" #"<Username for Neo4j Aura database>"
password = "metal-technicians-morale" #"<Password for Neo4j Aura database>"

from py2neo import Graph
import streamlit as st
from PIL import Image
from app.analysis import recommed_by_id

from PIL import Image
import requests
from io import BytesIO

recommend = st.sidebar.checkbox("Recommender system")


if recommend:
    st.title('Movie Recommender System')
    str_url = "bolt://neo4j:switch-shortage-shell@34.229.69.148:33108"
    movies_index = 0
    movies_graph = Graph(str_url)


    user_input = st.text_input("User Id:", 0)
    cypher = recommed_by_id(id=user_input)
    # f"""
    # user id {user_input}

    # {cypher}
    # """
    movies_recommended = movies_graph.run(cypher=cypher)
    data = movies_recommended.data().copy()
    @st.cache
    def getTitle(index=0):
        global data
        return data[index]["sm"].nodes[0].get("title")

    @st.cache
    def getImage(index=0):
        global data
        url = data[index]["sm"].nodes[0].get("poster")
        response = requests.get(url)
        img = Image.open(BytesIO(response.content))
        return img
    #st.write(movies_recommended)
    count = -3 # reson for -3 is to make sure slide corrolate with cols
    for _ in data:
        count=count+1
    # Pan through.
    page = st.slider("Page: ", min_value=0, max_value=count, value=0, step=1, format=None, key=None)
    movies_index = page
    # col_back, col_page, col_forward = st.beta_columns(3)

    # goback = col_back.button("Back")
    # gofoward = col_forward.button("Next")

    # @st.cache
    # def pan():
    #     global movies_index
    #     if goback:
    #         movies_index = movies_index-1
    #         print(movies_index)
    #     elif gofoward:
    #         movies_index = movies_index+1
    #         print(movies_index)

    # num_page = col_page.write(movies_index)

    # pan()
    """
    ## __Desplay recommended movies__
    """
    col1, col2, col3 = st.beta_columns(3)

    with col1:
        idx = movies_index
        st.header(f"""{getTitle(index=idx)}""")
        st.image(getImage(index=idx), use_column_width=True)

    with col2:
        idx = movies_index + 1
        st.header(f"""{getTitle(index=idx)}""")
        st.image(getImage(index=idx), use_column_width=True)

    with col3:
        idx = movies_index + 2
        st.header(f"""{getTitle(index=idx)}""")
        st.image(getImage(index=idx), use_column_width=True)
        movies_index = movies_index + 2


    st.write(f"""
    {data}
    """
    )


