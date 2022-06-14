
import psycopg2
import psycopg2.extras


conn = psycopg2.connect(host='localhost', database='data',
                        user='ghazal', password='qwerty')

cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

cur.execute('SELECT CLOSE_PRICE FROM PRICES')
print(cur.fetchall())


cur.close()

conn.close()