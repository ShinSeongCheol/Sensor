import pymysql
from dotenv import load_dotenv
import os

load_dotenv()

host = os.environ.get("host")
user = os.environ.get("user")
password = os.environ.get("password")
db = os.environ.get("db")
charset = os.environ.get("charset")
port = int(os.environ.get("port"))

def insertDht11Log(*args):
    con = pymysql.connect(host=host, user=user, password=password, db=db, charset=charset, port=port)

    cursor = con.cursor()
    query = "INSERT INTO dht11_log VALUES(CURRENT_TIMESTAMP(), %s, %s)"
    cursor.execute(query, args)
    
    con.commit()
    con.close()
