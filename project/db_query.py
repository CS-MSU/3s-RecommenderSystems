import yaml
import psycopg2


with open("project/config.yml", "r") as f:
    config = yaml.load(f, yaml.Loader)


DB = config.get('database').get('db')
USER = config.get('database').get('user')
PSWD = config.get('database').get('password')


def get_db_connection():
    conn = psycopg2.connect(
        host='localhost',
        database=DB,
        user=USER,
        password=PSWD
        )
    return conn


def execute_query(query):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(query)
    info = cur.fetchall()
    cur.close()
    conn.close()
    return info


def get_recommendations(user_id):
    q = f"""
SELECT  m.movie_title, m.release_date, m.url
FROM ratings r
INNER JOIN movies m
ON r.movie_id = m.movie_id
WHERE r.watched is false AND r.user_id = {user_id}
ORDER BY r.rating DESC
LIMIT 15;    
    """
    info = execute_query(q)
    return info


def get_watched(user_id):
    q = f"""
SELECT  m.movie_title, m.release_date, m.url, r.rating
FROM ratings r
INNER JOIN movies m
ON r.movie_id = m.movie_id
WHERE r.watched is true AND r.user_id = {user_id};
    """
    info = execute_query(q)
    return info


def get_user_info(user_id):
    q = f"""
SELECT * 
FROM users 
WHERE user_id = {user_id};
    """
    info = execute_query(q)
    return info
