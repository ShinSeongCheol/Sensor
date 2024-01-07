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
