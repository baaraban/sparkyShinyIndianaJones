import requests
from config import GOOGLE_MAPS_API_KEY, GOOGLE_MAPS_API_URL

def get_lat_lon(address):
    params = '?address={}&key={}'.format(address, GOOGLE_MAPS_API_KEY)
    response = requests.get(GOOGLE_MAPS_API_URL + params)
    resp_json_payload = response.json()
    lat_lon = None
    try:
        lat_lon = resp_json_payload['results'][0]['geometry']['location']
    finally:
        return lat_lon


#l = get_lat_lon("Lviv")
#print(l)
