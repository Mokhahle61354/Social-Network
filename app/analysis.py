def recommed_by_id(id:int):
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
    RETURN sm 
    LIMIT 25
    """

    return cypher


class Movie:
    
    def __init__(self, data):
        self.data = data[0]["sm"].nodes[0]
        pass

