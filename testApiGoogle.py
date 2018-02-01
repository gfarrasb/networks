import urllib.parse
import requests

main_api = 'https://maps.googleapis.com/maps/api/geocode/json?'
key = 'AIzaSyCo4S8TVzIUon5iZiZY-qt-U5Z9oxnlS34'

while True:
    address = input('Address: ')
    if address == 'quit' or address == 'q':
        break
    url = main_api + urllib.parse.urlencode({'address': address}) + '&key=' + key
    print(url)
    json_data = requests.get(url).json()
    print(json_data)
    county=json_data['results'][0]['address_components'][1]['long_name']
    print('aixo vols ' + county)
    json_status = json_data['status']
    print('API Status: ' + json_status)
    if json_status == 'OK':
        for each in json_data['results'][0]['address_components']:
            print(each['long_name'])
            
        formatted_address = json_data['results'][0]['formatted_address']
        lat = json_data['results'][0]['geometry']['location']['lat']
        long = json_data['results'][0]['geometry']['location']['lng']
        print('\n' + formatted_address)
        print('\n' + str(lat) + ' ' + str(long) )
