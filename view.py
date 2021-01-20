# Aura queries use an encrypted connection using the "neo4j+s" URI scheme
bolt_url = "bolt://34.229.69.148:33078"  # "%%BOLT_URL_PLACEHOLDER%%"
user = "neo4j"  # "<Username for Neo4j Aura database>"
password = "metal-technicians-morale"  # "<Password for Neo4j Aura database>"

import pandas as pd
from py2neo import Graph
import streamlit as st
from PIL import Image
from app.analysis import Recommend, get_user, recommed_by_id

from PIL import Image
import requests
from io import BytesIO

st.title("Movie Recommender System")
"""
Thabo Mokhahle 1738085\n
Tools used:\n
- Neo4j with py2neo\n
- UI : streamlit
- Dataset : https://sandbox.neo4j.com/?ref=hcard  -> new project -> "Recommendation"
    - For new bolt password and ip


```
Dependecies:
    pip install neo4j
    pip install -U pylint --user
    pip install neo4j-driver
    pip install streamlit
    pip install --upgrade py2neo
    pandas

Run App:
 - streamlit run view.py

user provided env:


```
"""

chbx_recommend = st.sidebar.checkbox("Recommender system")


if chbx_recommend:
    """
    #### _Connect to Neo4j_
    """
    col_bolt_ip, col_password = st.beta_columns(2)
    txt_bolt_ip = col_bolt_ip.text_input("Neo4j bolt ip:", value="100.25.182.248:33004")
    txt_bolt_password = col_password.text_input(
        "Neo4j bolt Password :", value="dawns-decoders-pull"
    )
    str_url = f"bolt://neo4j:{txt_bolt_password}@{txt_bolt_ip}"
    movies_index = 0
    movies_graph = Graph(str_url)

    """
    #### _User and filter inputs_
    """
    user_id = st.text_input("User Id:", 2)
    obj_recommend = Recommend(movies_graph=movies_graph, user_id=user_id)
    all_genres = obj_recommend.get_all_genres()

    col_genre, col_slt_genre = st.beta_columns(2)
    # is_by_genre = False
    with col_genre:
        slt_genre = st.selectbox(label="Genre: ", options=all_genres)
        is_by_genre = col_slt_genre.checkbox("Activate genre")
        if is_by_genre:
            obj_recommend.byGenre(genre=slt_genre)
            col_slt_genre.write("Will filter by selected genre!!!")

    f"""
    ### __Desplay recommended movies__
    ```
    User Name: {obj_recommend.user_name}
    User ID: {obj_recommend.user_id}
    ```
    """

    count = -3  # reson for -3 is to make sure slide corrolate with cols
    for _ in obj_recommend.data:
        count = count + 1
    # Pan through.
    page = st.slider(
        "Page: ", min_value=0, max_value=count, value=0, step=1, format=None, key=None
    )
    movies_index = page

    col1, col2, col3 = st.beta_columns(3)
    with col1:
        idx = movies_index
        rcm_movie = obj_recommend.getMovieInfo(index=idx)
        st.header(f"""{rcm_movie["title"]}""")
        st.image(rcm_movie["poster"], use_column_width=True)
        # st.write(f"""Similar userID: {rcm_movie["su_id"]}""")
        {
            key: rcm_movie.get(key)
            for key in ["genre", "year", "runtime", "released", "su_id"]
        }

    with col2:
        idx = movies_index + 1
        rcm_movie = obj_recommend.getMovieInfo(index=idx)
        st.header(f"""{rcm_movie["title"]}""")
        st.image(rcm_movie["poster"], use_column_width=True)
        # st.write(f"""Similar userID: {rcm_movie["su_id"]}""")
        {
            key: rcm_movie.get(key)
            for key in ["genre", "year", "runtime", "released", "su_id"]
        }

    with col3:
        idx = movies_index + 2
        rcm_movie = obj_recommend.getMovieInfo(index=idx)
        st.header(f"""{rcm_movie["title"]}""")
        st.image(rcm_movie["poster"], use_column_width=True)
        # st.write(f"""Similar userID: {rcm_movie["su_id"]}""")
        {
            key: rcm_movie.get(key)
            for key in ["genre", "year", "runtime", "released", "su_id"]
        }
        movies_index = movies_index + 2
        pass

    col_sm_users, col_sm_info = st.beta_columns(2)

    with col_sm_users:
        # change col_sm_info here
        pass

st.markdown(
    """
    ==========================================================================
    # Improvement plan:

    ### Future Milestones
    - :computer: GraphQl server
        - separate app from GUI
        - Access neo4j server
        
        Using https://tartiflette.io/ or https://ariadnegraphql.org/ :
        - tartiflette  -> _async
        - ariadnegraphql

    - :fire: :fire: Neo4j
        - Node and Graph management
        - 

    - :confused: Intergration of the algorithms from:
        - Graph Data Science in neo4j
        - https://neo4j.com/docs/graph-data-science/1.4/management-ops/
    """
)


