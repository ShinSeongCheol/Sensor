# 개요
집을 정리하는 도중 라즈베리파이 관련 장비를 모아둔 박스를 한번 들여다 보게 되었다.
여러가지 센서가 있었는데 dht11 센서가 눈에 띄었다.

dht11센서는 온도, 습도를 측정할 수 있는 센서인데 이 센서를 이용하여 방안의 온도를 측정할 수 있는 프로그램을 만들면 좋을꺼 같아 만들게 되었다.

 

# 프로그램
방안의 온도, 습도를 1분마다 측정하는 프로그램

## 언어
- python
## 데이터베이스
- mysql
## 라이브러리
- adafruit-dht
- pymysql
- apscheduler
- python-dotenv
## 데이터베이스 테이블 구조
데이터베이스 테이블의 속성으로 측정시간(measurement_time), 온도(temperature), 습도(humidity)를 설정하였다.
측정시간은 제약조건을  PRIMARY KEY로 설정하였다.


## 라즈베리파이 회로도
라즈베리 파이의 5V, GND, GPIO17 핀을 이용해 dht11 센서와 연결을 구성하였다.


## dht11.py
온도, 습도를 측정하는 코드이다.
Adafruit_DHT 라이브러리를 사용하여 dht11 센서의 값을 읽어오도록 하였다.
apscheduler 라이브러리를 사용하여 매 분마다 dht11 센서에서 값을 읽고 dht11_log 테이블에 값을 저장하도록 하였다.

```
import Adafruit_DHT      # 라이브러리 불러오기
import database
from apscheduler.schedulers.blocking import BlockingScheduler

sensor = Adafruit_DHT.DHT11     #  sensor 객체 생성

pin = 17                        # Data핀의 GPIO핀 넘버

scheduler = BlockingScheduler()

@scheduler.scheduled_job(trigger='cron', minute='*')
def read():
    """
    온도 습도 측정
    """

    humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)

    if humidity is not None and temperature is not None:
        temp = "{0:0.1f}".format(temperature)
        hum = "{0:0.1f}".format(humidity)

        database.insertDht11Log(temp,hum)


scheduler.start()
```

## database.py
데이터베이스의 연결하고 값을 삽입할 수 있는 코드다.
python-dotenv 라이브러리를 사용해 DB 정보를 읽고 데이터베이스에 연결해 insertDht11Log 함수의 인자로 온도, 습도 값을 받아 데이터베이스에 삽입할 수 있도록 구현하였다.

```
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
```
