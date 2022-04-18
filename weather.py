import requests
import ssl
from speak import espeak_chinese
ssl._create_default_https_context = ssl._create_unverified_context
def report_weather():
    myurl = "http://t.weather.sojson.com/api/weather/city/101070101"


    response = requests.get(myurl)

    print(response)
    json = response.json()
    print(json)
    data = json.get("data")
    temperature = data.get("wendu")
    pm25 = data.get("pm25")
    print("temperature:{},pm25:{}".format(temperature,pm25))
    espeak_chinese("明天的温度是{}，度,明天的pm25污染指数是{}".format(temperature,pm25))