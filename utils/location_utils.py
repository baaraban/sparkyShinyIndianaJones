import requests
import pickle

GOOGLE_MAPS_API_KEY = 'AIzaSyCEE6oOLQ79t5IsEn9SeCE4mirqlFumcOY'
GOOGLE_MAPS_API_URL = 'https://maps.googleapis.com/maps/api/geocode/json'
LOCATION_CASH_FILE = "location_cash"

def getCashedAddress(address):
    infile = open(LOCATION_CASH_FILE, 'rb')
    cashed_data = pickle.load(infile)
    lat_lon_cashed = cashed_data[address]
    return lat_lon_cashed

def cashAddress(addresses):
    outfile = open(LOCATION_CASH_FILE, 'wb')
    pickle.dump(addresses, outfile)
    outfile.close()
    return


def get_lat_lon(address):
    lat_lon_cashed = getCashedAddress(address)
    if lat_lon_cashed:
        return lat_lon_cashed

    params = '?address={}&key={}'.format(address, GOOGLE_MAPS_API_KEY)
    response = requests.get(GOOGLE_MAPS_API_URL + params)
    resp_json_payload = response.json()
    lat_lon = None
    try:
        lat_lon = resp_json_payload['results'][0]['geometry']['location']
    finally:
        if lat_lon:
            cashed_data[address] = lat_lon
            cashAddresses(cashed_data)
        return lat_lon

#l = get_lat_lon("Lviv")
#print(l)
