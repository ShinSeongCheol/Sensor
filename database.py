import pymysql

host = "127.0.0.1"
user = "seongcheol"
password = "seongcheol"
db = "Sensors"
charset='utf8'
port = 13306

def insertDht11Log(*args):
    con = pymysql.connect(host=host, user=user, password=password, db=db, charset=charset, port=port)

    cursor = con.cursor()
    query = "INSERT INTO dht11_log VALUES(CURRENT_TIMESTAMP(), %s, %s)"
    cursor.execute(query, args)
    
    con.commit()
    con.close()
