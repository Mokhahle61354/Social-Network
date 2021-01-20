def recommed_by_id(id: int):
    cypher = f"""
    MATCH
        (hrm:Movie)<-[r:RATED]-(u:User)
    WHERE
        u.userId = "{id}"
        And r.rating>4
    WITH u,hrm LIMIT 25

    MATCH
        (g:Genre)-[:IN_GENRE]-(hrm)
    WITH u,hrm,g

    MATCH
        (su:User)-[r:RATED]-(hrm)
    WHERE
        r.rating>4
    WITH u,su,g

    MATCH
        (sm:Movie)<-[r:RATED]-(su)
    WHERE
        r.rating>4
        AND (sm)-[:IN_GENRE]-(g)
        AND NOT (sm)-[:RATED]-(u)
    RETURN u, g,sm, su
    LIMIT 25
    """

    return cypher


def recommed_by_genre(id: int, genre: str):
    cypher = f"""

    MATCH
        (hrm:Movie)<-[r:RATED]-(u:User)
    WHERE
        u.userId = "{id}"
        And r.rating>4
    WITH u,hrm LIMIT 25

    MATCH
        (g:Genre)-[:IN_GENRE]-(hrm)
    WHERE
        g.name = "{genre}"
    WITH u,hrm,g

    MATCH
        (su:User)-[r:RATED]-(hrm)
    WHERE
        r.rating>4
    WITH u,su,g

    MATCH
        (sm:Movie)<-[r:RATED]-(su)
    WHERE
        r.rating>4
        AND (sm)-[:IN_GENRE]-(g)
        AND NOT (sm)-[:RATED]-(u)
    RETURN u, g,sm, su
    LIMIT 25
    """

    return cypher


def get_user(id: int):
    cypher = f"""
    MATCH 
        (u:User)
    WHERE
        u.userId = "{id}"
    RETURN u.name
    """

    print(cypher)
    pass


from py2neo import Graph

from PIL import Image
import requests
from io import BytesIO
import numpy as np


class Recommend:
    def __init__(self, movies_graph, user_id):
        self.movies_graph = movies_graph
        self.data = self.run_cypher(cypher=recommed_by_id(id=user_id))
        self.user_id = user_id
        self.user_name = self.data[0]["u"].nodes[0].get("name")
        pass

    def byGenre(self, genre):
        self.data = self.run_cypher(
            cypher=recommed_by_genre(id=self.user_id, genre=genre)
        )
        return

    def get_all_genres(self):
        cyp = "MATCH (n:Genre) RETURN n LIMIT 25"
        genres = self.run_cypher(cypher=cyp)
        lst_genres = [
            gnr["name"] for idx in range(len(genres)) for gnr in genres[idx]["n"].nodes
        ]
        return lst_genres

    def run_cypher(self, cypher):
        results = self.movies_graph.run(cypher=cypher)
        data = results.data().copy()
        return data

    def SimilarUsers(self):
        similar_users = []
        id_set = []
        for index in range(len(self.data)):
            # name = self.data[index]["su"].nodes[0].get("name")
            user = self.data[index]["su"].nodes[0]
            similar_users.append(user)
            pass
        # get unique users from list
        similar_users = list({p["userId"]: p for p in similar_users}.values())
        return similar_users  # np.unique(similar_users)

    # @st.cache
    def getMovieInfo(self, index=0):
        released = self.data[index]["sm"].nodes[0].get("released")
        runtime = self.data[index]["sm"].nodes[0].get("runtime")
        movieId = self.data[index]["sm"].nodes[0].get("movieID")
        rating = self.data[index]["sm"].nodes[0].get("imbdRating")
        year = self.data[index]["sm"].nodes[0].get("year")
        title = self.data[index]["sm"].nodes[0].get("title")
        # Image
        url = self.data[index]["sm"].nodes[0].get("poster")
        response = requests.get(url)
        poster = Image.open(BytesIO(response.content))
        su_id = self.data[index]["su"].nodes[0].get("userId")
        genre = self.data[index]["g"].nodes[0].get("name")

        return dict(
            movieId=movieId,
            title=title,
            poster=poster,
            rating=rating,
            year=year,
            runtime=runtime,
            released=released,
            su_id=su_id,  # similar user ID
            genre=genre,
        )


class User:
    def __init__(self, user_id):
        self.user_id = user_id
        pass
