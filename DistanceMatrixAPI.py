# importing required libraries
import requests

API_KEY = 'AIzaSyDKQY-dAMpv32uiWSREDRH83FZRcNUhSmw'


def calc_distance_between_2_point(source: str, dest: str):
    # url variable store url
    base_url = 'https://maps.googleapis.com/maps/api/distancematrix/json?'

    # Get method of requests module
    # return response object
    response = requests.get(base_url + 'origins=' + source +
                            '&destinations=' + dest +
                            '&key=' + API_KEY)

    # json method of response object
    # return json format result
    data = response.json()
    '''
    print("Distance Matrix API Data in Dictionary:")
    print(data)
    print()
    '''

    if data['status'] == 'OK':
        result = data['rows'][0]
        distance = result['elements'][0]['distance']['text']
        return distance
    else:
        return None
