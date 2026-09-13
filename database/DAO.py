
from database.DB_connect import DBConnect
from model.Actor import Actor


class DAO():

    # RECUPERA TUTTI I RATING DISPONIBILI
    @staticmethod
    def getAllRatings():
        conn = DBConnect.get_connection()

        results = []

        # USO dictionary=True PER ACCEDERE AI DATI CON IL NOME DELLA COLONNA
        cursor = conn.cursor(dictionary=True)

        query = """
        SELECT DISTINCT avg_rating
        FROM ratings r
        ORDER BY avg_rating
        """

        cursor.execute(query)

        # SCORRO LE RIGHE RESTITUITE DAL DATABASE
        for row in cursor:
            results.append(row["avg_rating"])

        cursor.close()
        conn.close()

        return results


    # RECUPERA GLI ATTORI DEI FILM CON RATING NEL RANGE SCELTO
    @staticmethod
    def getAllActorsbyRange(rat1, rat2):
        conn = DBConnect.get_connection()

        results = []

        # USO dictionary=True PER ACCEDERE AI DATI CON IL NOME DELLA COLONNA
        cursor = conn.cursor(dictionary=True)

        query = """
        SELECT DISTINCT
            rm.name_id AS ActorID,
            n.date_of_birth AS date_of_birth,
            n.name AS Name
        FROM role_mapping rm, movie m, ratings r, names n

        -- COLLEGO L'ATTORE ALLA TABELLA NAMES
        WHERE n.id = rm.name_id

        -- COLLEGO L'ATTORE AL FILM
        AND m.id = rm.movie_id

        -- COLLEGO IL FILM AL RATING
        AND r.movie_id = m.id

        -- LA DATA DI NASCITA DEVE ESISTERE
        AND n.date_of_birth IS NOT NULL

        -- 🔴🔴 EVITO DATE DI NASCITA FUTURE
        AND n.date_of_birth <= CURDATE()

        -- IL RATING DEVE ESSERE COMPRESO NEL RANGE SCELTO
        AND r.avg_rating >= %s
        AND r.avg_rating <= %s
        """

        cursor.execute(query, (rat1, rat2))

        # CREO UN OGGETTO ACTOR PER OGNI RIGA TROVATA
        for row in cursor:
            results.append(Actor(**row))

        cursor.close()
        conn.close()

        return results


    # RECUPERA LE COPPIE DI ATTORI CHE HANNO RECITATO NELLO STESSO FILM
    @staticmethod
    def getAllEdges(rat1, rat2):
        conn = DBConnect.get_connection()

        results = []

        # USO dictionary=True PER ACCEDERE AI DATI CON IL NOME DELLA COLONNA
        cursor = conn.cursor(dictionary=True)

        query = """
        SELECT
            rm1.name_id AS Actor1,
            rm2.name_id AS Actor2,

            -- SOMMO GLI INCASSI DEI FILM IN COMUNE
            SUM(
                CAST(
                    REPLACE(
                        REPLACE(m.worlwide_gross_income, '$', ''),
                        ',',
                        ''
                    ) AS UNSIGNED
                )
            ) AS Weight

        FROM movie m, role_mapping rm1, role_mapping rm2,
             ratings r, names n1, names n2

        -- I DUE ATTORI DEVONO AVER RECITATO NELLO STESSO FILM
        WHERE m.id = rm1.movie_id
        AND m.id = rm2.movie_id

        -- COLLEGO IL FILM AL RATING
        AND m.id = r.movie_id

        -- COLLEGO I DUE ATTORI ALLA TABELLA NAMES
        AND rm1.name_id = n1.id
        AND rm2.name_id = n2.id

        -- LA DATA DI NASCITA DEI DUE ATTORI DEVE ESISTERE
        AND n1.date_of_birth IS NOT NULL
        AND n2.date_of_birth IS NOT NULL

        -- 🔴🔴 EVITO DATE DI NASCITA FUTURE
        AND n1.date_of_birth <= CURDATE()
        AND n2.date_of_birth <= CURDATE()

        -- EVITO DI AVERE LA STESSA COPPIA DUE VOLTE
        -- 10-20 E 20-10 RAPPRESENTANO LO STESSO ARCO
        -- EVITO ANCHE L'ARCO DI UN ATTORE CON SE STESSO
        AND rm1.name_id < rm2.name_id

        -- IL RATING DEVE ESSERE COMPRESO NEL RANGE SCELTO
        AND r.avg_rating >= %s
        AND r.avg_rating <= %s

        -- L'INCASSO DEVE ESISTERE
        AND m.worlwide_gross_income IS NOT NULL

        -- 🔴🔴 CONSIDERO SOLO GLI INCASSI ESPRESSI IN DOLLARI
        AND m.worlwide_gross_income LIKE '$%'

        -- RAGGRUPPO PER COPPIA DI ATTORI
        -- COSI POSSO SOMMARE GLI INCASSI DEI FILM IN COMUNE
        GROUP BY rm1.name_id, rm2.name_id
        """

        cursor.execute(query, (rat1, rat2))

        # SALVO ID DEL PRIMO ATTORE, ID DEL SECONDO ATTORE E PESO
        for row in cursor:
            results.append(
                (row["Actor1"], row["Actor2"], row["Weight"])
            )

        cursor.close()
        conn.close()

        return results

    #COMMENTI EXTRA#
    #SUM(
    #CAST(
    #    REPLACE(
     #       REPLACE(COLONNA, CARATTERE1, ''),
       #     CARATTERE2, '')
      #       AS UNSIGNED
     #    )
    #  )  AS NomeRisultato (wieght)

    #CAST AS UNSIGNED → trasformo il testo in numero PER POTER FARE LA SOMMA


