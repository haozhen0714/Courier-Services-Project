import requests
import gmplot
import polyline

API_KEY = 'AIzaSyDKQY-dAMpv32uiWSREDRH83FZRcNUhSmw'


def getRoute(origin_lat, origin_long, hub_lat, hub_long, dest_lat, dest_long):
    origin = origin_lat + ', ' + origin_long
    hub = hub_lat + ', ' + hub_long
    dest = dest_lat + ', ' + dest_long

    base_url = 'https://maps.googleapis.com/maps/api/directions/json?'
    response = requests.get(base_url + 'origin=' + origin + '&destination=' + hub + '&key=' + API_KEY)
    direction = response.json()
    step_direction = direction['routes'][0]['legs'][0]['steps']
    lat_origin_hub = []
    long_origin_hub = []
    for i in range(len(step_direction)):
        encoded_polyline = step_direction[i]['polyline']['points']
        decoded_polyline = polyline.decode(encoded_polyline)
        for j in range(len(decoded_polyline)):
            lat_origin_hub.append(decoded_polyline[j][0])
            long_origin_hub.append(decoded_polyline[j][1])
    #print("Customer ", num)
    #print('Origin to Hub')
    #print(direction['routes'][0]['legs'][0])

    base_url = 'https://maps.googleapis.com/maps/api/directions/json?'
    response = requests.get(base_url + 'origin=' + hub + '&destination=' + dest + '&key=' + API_KEY)
    direction = response.json()
    step_direction = direction['routes'][0]['legs'][0]['steps']
    lat_hub_dest = []
    long_hub_dest = []
    for i in range(len(step_direction)):
        encoded_polyline = step_direction[i]['polyline']['points']
        decoded_polyline = polyline.decode(encoded_polyline)
        for j in range(len(decoded_polyline)):
            lat_hub_dest.append(decoded_polyline[j][0])
            long_hub_dest.append(decoded_polyline[j][1])
    #print()
    #print("Hub to Destination")
    #print(direction['routes'][0]['legs'][0])
    #print()
    return lat_origin_hub, long_origin_hub, lat_hub_dest, long_hub_dest


def plotAllRoutes(plotting_list, num):
    origin_name_list, origin_lat_list, origin_long_list = ([] for i in range(3))
    hub_name_list, hub_lat_list, hub_long_list = ([] for i in range(3))
    dest_name_list, dest_lat_list, dest_long_list = ([] for i in range(3))
    lat_origin_hub_list, long_origin_hub_list, lat_hub_dest_list, long_hub_dest_list = ([] for i in range(4))

    for i in range(0, len(plotting_list), 2):
        origin_name_list.append(plotting_list[i][0])
        origin_lat_list.append(plotting_list[i][1]), origin_long_list.append(plotting_list[i][2])
        hub_name_list.append(plotting_list[i][3])
        hub_lat_list.append(plotting_list[i][4]), hub_long_list.append(plotting_list[i][5])
        dest_name_list.append(plotting_list[i][6])
        dest_lat_list.append(plotting_list[i][7]), dest_long_list.append(plotting_list[i][8])
        lat_origin_hub_list.append(plotting_list[i + 1][0]), long_origin_hub_list.append(plotting_list[i + 1][1])
        lat_hub_dest_list.append(plotting_list[i + 1][2]), long_hub_dest_list.append(plotting_list[i + 1][3])

    centre_lat = sum(lat_origin_hub_list[0]) / len(lat_origin_hub_list[0])
    centre_long = sum(long_origin_hub_list[0]) / len(long_origin_hub_list[0])
    gmap = gmplot.GoogleMapPlotter(centre_lat, centre_long, 13)
    gmap.apikey = "AIzaSyDKQY-dAMpv32uiWSREDRH83FZRcNUhSmw"
    for j in range(len(origin_lat_list)):
        gmap.marker(float(origin_lat_list[j]), float(origin_long_list[j]), color='red', title=origin_name_list[j])
        gmap.marker(float(hub_lat_list[j]), float(hub_long_list[j]), color='blue', title=hub_name_list[j])
        gmap.marker(float(dest_lat_list[j]), float(dest_long_list[j]), color='red', title=dest_name_list[j])
        if j == 0:
            gmap.scatter(lat_origin_hub_list[j], long_origin_hub_list[j], 'yellow', size=2, marker=False)
            gmap.plot(lat_origin_hub_list[j], long_origin_hub_list[j], 'yellow', edge_width=15)
            gmap.scatter(lat_hub_dest_list[j], long_hub_dest_list[j], 'yellow', size=2, marker=False)
            gmap.plot(lat_hub_dest_list[j], long_hub_dest_list[j], 'yellow', edge_width=15)
        else:
            gmap.scatter(lat_origin_hub_list[j], long_origin_hub_list[j], 'cornflowerblue', size=2, marker=False)
            gmap.plot(lat_origin_hub_list[j], long_origin_hub_list[j], 'cornflowerblue', edge_width=10)
            gmap.scatter(lat_hub_dest_list[j], long_hub_dest_list[j], 'cornflowerblue', size=2, marker=False)
            gmap.plot(lat_hub_dest_list[j], long_hub_dest_list[j], 'cornflowerblue', edge_width=10)

    gmap.draw('Map for Customer ' + str(num) + '.html')
    print('Draw and Write Map for Customer ' + str(num) + '.html')
