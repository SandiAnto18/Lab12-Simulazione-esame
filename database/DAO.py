from database.DB_connect import DBConnect
from model.Actor import Actor


class DAO():
    """con @staticmethod no (self,,),no (cls,,)"""
    @staticmethod
    def getAllRatings():
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = "SELECT distinct avg_rating  FROM ratings r  ORDER BY avg_rating "

        cursor.execute(query)

        for row in cursor:
            results.append(row["avg_rating"])

        cursor.close()
        conn.close()
        return results

    # stampa di prova output
    # print(DAO.getAllRatings())

    @staticmethod
    def getAllActorsbyRange(rat1, rat2):
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query ="""select distinct rm.name_id as ActorID,n.date_of_birth as date_of_birth,n.name as Name
                  from role_mapping rm ,movie m ,ratings r ,names n 
                   where n.id =rm.name_id 
                    and m.id=rm.movie_id 
                    and n.date_of_birth is not null 
                   and r.movie_id =m.id 
                   and r.avg_rating >= %s
                    and r.avg_rating <= %s"""
        #filtra i film in quel rating
        cursor.execute(query,(rat1,rat2))
        #scorre ogni riga del risultato
        #ogni row ha actor id,name e birth
        for row in cursor:
            #Con results.append CREO UN OGGETTO della classe Actor con i valori id,name e birth
            #E LO AGGIUNGE ALLA LISTA
            results.append(Actor(**row))

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getAllEdges(rat1, rat2):
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """select rm1.name_id as Actor1, rm2.name_id as Actor2, sum( cast(replace(replace(m.worlwide_gross_income, '$', ''),',', '') as unsigned)) as Weight
                    from movie m, role_mapping rm1, role_mapping rm2, ratings r, names n1, names n2
                    where m.id = rm1.movie_id
                    and m.id = rm2.movie_id
                    and m.id = r.movie_id
                    and rm1.name_id = n1.id
                    and rm2.name_id = n2.id
                    and n1.date_of_birth IS NOT NULL
                    and n2.date_of_birth IS NOT NULL
                    and rm1.name_id < rm2.name_id   
                    
                    and r.avg_rating >= %s
                    and r.avg_rating <= %s
                    and m.worlwide_gross_income is not null
                    and m.worlwide_gross_income like '$%'
                    group by rm1.name_id, rm2.name_id"""

#COMMMENTI

#GRAFO NON ORIENTATO 10 -> 20 = 20 -> 10
#and rm1.name_id < rm2.name_id  SERVE PER EVITARE DI AVERE LA STESSA COPPIA DUE VOLTE
#oppure UNA COPPIA DELLO STESSO ATTORE
#and m.worlwide_gross_income like '$%' CONTROLLA CHE L'INCASSO SIA NEL FORMATO DOLLARO
#FUNZIONE SOMMA
#sum( cast(replace(replace(m.worlwide_gross_income, '$', ''),',', '') as unsigned)
#PER FARE UNA SOMMA SQL DEVO TRASFORMARE  $30,0000 IN NUMERO, con 2 REPLACE PRIMA TOLGO '$' E POI ','
#CAST(...AS UNSIGNED) lo trasforma in numero
#SUM() somma gli incassi
        cursor.execute(query, (rat1,rat2))

        for row in cursor:
            results.append((row['Actor1'], row['Actor2'], row['Weight']))

        cursor.close()
        conn.close()
        return results

