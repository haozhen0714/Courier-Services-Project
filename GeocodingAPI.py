import requests

API_KEY = 'AIzaSyDKQY-dAMpv32uiWSREDRH83FZRcNUhSmw'


class GeocodingAPIClass:

    def getGeoCoord(self: str):
        params = {
            'key': API_KEY,
            'address': self.replace(' ', '+')
        }

        base_url = 'https://maps.googleapis.com/maps/api/geocode/json?'
        response = requests.get(base_url, params=params)
        data = response.json()
        print(data)
        if data['status'] == 'OK':
            result = data['results'][0]
            location = result['geometry']['location']
            return location['lat'], location['lng']
        else:
            return None
