from database.DB_connect import DBConnect


class DAO():
    """con @staticmethod no (self)"""
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

"""stampa di prova output"""
print(DAO.getAllRatings())


