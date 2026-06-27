from database.DB_connect import DBConnect
from model.state import State
from model.sighting import Sighting


class DAO():
    def __init__(self):
        pass


    @staticmethod
    def get_all_states():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select * 
                    from state s"""
            cursor.execute(query)

            for row in cursor:
                result.append(
                    State(**row))

            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def get_all_sightings():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select * 
                    from sighting s 
                    order by `datetime` asc """
            cursor.execute(query)

            for row in cursor:
                result.append(Sighting(**row))
            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def getNodi(v1, v2, shape):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """with giusti as (select UPPER(id) id
from state s
where Lat > %s and Lng > %s), 
peso as (select state, count(distinct id) as peso
from sighting s 
where shape = %s
group by state)

select s.*
from giusti g, state s
where g.id in (select state from peso)
and g.id = UPPER(s.id)"""
            cursor.execute(query, [v1, v2, shape])

            for row in cursor:
                result.append(State(**row))
            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def getArchi(v1, v2, shape):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor()
            query = """with giusti as (select UPPER(id) id
from state s
where Lat > %s and Lng > %s), 
peso as (select state, sum(duration) as peso
from sighting s 
where shape = %s and state in (select id from giusti)
group by state)

select n.state1 primo, n.state2 secondo, max(p1.peso+p2.peso)
from neighbor n, peso p1, peso p2
where n.state1 = p1.state and n.state2 = p2.state
and n.state1>n.state2
group by n.state1, n.state2"""
            cursor.execute(query, [v1, v2, shape])

            for row in cursor:
                result.append(row)
            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def getShape():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor()
            query = """select distinct shape
            from sighting
            where shape != "unknown" and shape != ""
            order by shape DESC"""
            cursor.execute(query)

            for row in cursor:
                result.append(row)
            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def getVal():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor()
            query = """select max(Lng), min(Lng), max(Lat), min(Lat)
                from state"""
            cursor.execute(query)

            for row in cursor:
                result.append(row)
            cursor.close()
            cnx.close()
        return result








