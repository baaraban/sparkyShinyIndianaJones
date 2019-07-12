import requests
from dateutil.parser import parse

def getLatLonFromAddress(address = ""):
    api_url = 'https://maps.googleapis.com/maps/api/geocode/json'
    API_key = 'AIzaSyCEE6oOLQ79t5IsEn9SeCE4mirqlFumcOY'
    params = '?address={}&key={}'.format(address, API_key)
    response = requests.get(api_url + params)
    resp_json_payload = response.json()
    lat_lon = resp_json_payload['results'][0]['geometry']['location']
    #print(lat_lon)
    return lat_lon

#getLatLonFromAddress("Lviv")

def parseRandomDate(date_str):
    parsed_date = parse(date_str)
    #print(parsed_date)
    return parsed_date

#parseRandomDate("2017 Jan 03")
