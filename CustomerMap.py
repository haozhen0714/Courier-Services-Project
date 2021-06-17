import requests
import gmplot
import polyline
import GoogleAPIKey

API_KEY = GoogleAPIKey.API_KEY


# Time complexity: O(1)
def read_ranking(customer):
    print("Read " + customer.customer_name + " Problem 1 Ranking.txt")
    customer_file = open("P1/" + customer.customer_name + " Problem 1 Ranking.txt", "r")
    customer_delivery_list = customer_file.readlines()
    company_first_ranking = (customer_delivery_list[1].replace('\n', ''))
    return company_first_ranking


# Time complexity: O(sd)
def get_route(name, customer_lat, customer_long, company_lat, company_long):  # Time complexity: O(sd)
    # get latitude and longitude for customer and company
    hub = company_lat + ', ' + company_long
    dest = customer_lat + ', ' + customer_long

    # get the latitude and longitude of each small step along the route from origin to hub
    base_url = 'https://maps.googleapis.com/maps/api/directions/json?'

    if name == "ori":
        response = requests.get(base_url + 'origin=' + dest + '&destination=' + hub + '&key=' + API_KEY)
    elif name == "des":
        response = requests.get(base_url + 'origin=' + hub + '&destination=' + dest + '&key=' + API_KEY)

    direction = response.json()
    step_direction = direction['routes'][0]['legs'][0]['steps']
    lat_list = []
    long_list = []

    for i in range(len(step_direction)):  # O(s), s = length of each small step along the route
        encoded_polyline = step_direction[i]['polyline']['points']  # the latitude and longitude is in encoded format
        decoded_polyline = polyline.decode(encoded_polyline)  # decode to obtain the numeric format (float

        # separate and store latitude and longitude into respective list
        for j in range(
                len(decoded_polyline)):  # O(d), d = length of decoded coordinates of each small step along the route
            lat_list.append(decoded_polyline[j][0])
            long_list.append(decoded_polyline[j][1])

    return lat_list, long_list


# Time complexity = O(nsd)
def plot_map(customer, company_list):
    gmap = gmplot.GoogleMapPlotter(3.112585695236, 101.6397000538541, 10)
    gmap.apikey = API_KEY

    # the best company based on distance
    first_rank_company = read_ranking(customer)

    # plot red marker for customer's origin and destination
    gmap.marker(float(customer.ori_lat), float(customer.ori_long), color='red', title=customer.ori_name)
    gmap.marker(float(customer.des_lat), float(customer.des_long), color='red', title=customer.des_name)

    for company in company_list:  # O(n), n = length of company list
        # plot blue marker for hub
        gmap.marker(float(company.latitude), float(company.longitude), color='blue', title=company.name)

        # if company is the best company based on distance, plot route in yellow colour
        if company.name == first_rank_company:
            # call method to get the coordinates for the route
            lat_origin_hub, long_origin_hub = get_route("ori", customer.ori_lat, customer.ori_long, company.latitude,
                                                        company.longitude)
            lat_hub_dest, long_hub_dest = get_route("des", customer.des_lat, customer.des_long, company.latitude,
                                                    company.longitude)
            gmap.scatter(lat_origin_hub, long_origin_hub, 'yellow', size=5, marker=False)
            gmap.plot(lat_origin_hub, long_origin_hub, 'yellow', edge_width=10)
            gmap.scatter(lat_hub_dest, long_hub_dest, 'yellow', size=5, marker=False)
            gmap.plot(lat_hub_dest, long_hub_dest, 'yellow', edge_width=10)

        # if not, plot in blue colour
        else:
            lat_origin_hub, long_origin_hub = get_route("ori", customer.ori_lat, customer.ori_long, company.latitude,
                                                        company.longitude)
            lat_hub_dest, long_hub_dest = get_route("des", customer.des_lat, customer.des_long, company.latitude,
                                                    company.longitude)
            gmap.scatter(lat_origin_hub, long_origin_hub, 'cornflowerblue', size=7, marker=False)
            gmap.plot(lat_origin_hub, long_origin_hub, 'cornflowerblue', edge_width=7)
            gmap.scatter(lat_hub_dest, long_hub_dest, 'cornflowerblue', size=7, marker=False)
            gmap.plot(lat_hub_dest, long_hub_dest, 'cornflowerblue', edge_width=7)

    # draw the map for a customer with all routes to each company and save in .html file
    gmap.draw('P1/Map for ' + customer.customer_name + '.html')
    print('Draw and Write Map for ' + customer.customer_name + '.html')
