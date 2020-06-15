import requests
import pandas as pd
import json


def get_ninja_data(latitude=34.125, longitude=39.814, startdate='2015-01-01', enddate='2015-12-31', dataset="merra2",
                   capacity=1.0, systemloss=0.1, tilt=35, azimuth=180):
    """This function gets PV data from renewables.ninja and takes common arguments such as location, dates, dataset,
     capacity, loss, and orientation"""
    token = open("APIToken.txt", "r").readline()

    api_base = 'https://www.renewables.ninja/api/'

    s = requests.session()
    # Send token header with each request
    s.headers = {'Authorization': 'Token ' + token}

    url = api_base + 'data/pv'

    args = {
        'lat': latitude,
        'lon': longitude,
        'date_from': startdate,
        'date_to': enddate,
        'dataset': dataset,
        'capacity': capacity,
        'system_loss': systemloss,
        'tracking': 0,
        'tilt': tilt,
        'azim': azimuth,
        'format': 'json'
    }

    r = s.get(url, params=args)

    # Parse JSON to get a pandas.DataFrame of data and dict of metadata
    parsed_response = json.loads(r.text)

    data = pd.read_json(json.dumps(parsed_response['data']), orient='index')
    return data


data = get_ninja_data()
print(data)