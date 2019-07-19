import requests


def get_lat_lon(address):
    api_url = 'https://maps.googleapis.com/maps/api/geocode/json'
    API_key = 'AIzaSyCEE6oOLQ79t5IsEn9SeCE4mirqlFumcOY'
    params = '?address={}&key={}'.format(address, API_key)
    response = requests.get(api_url + params)
    resp_json_payload = response.json()
    lat_lon = None
    try:
        lat_lon = resp_json_payload['results'][0]['geometry']['location']
    finally:
        return lat_lon
