import MapsPlotting

API_KEY = 'AIzaSyDKQY-dAMpv32uiWSREDRH83FZRcNUhSmw'


def plotMap(customer, num):
    route = getAllRoute(customer)
    company = read_company_full_details()
    customer_distance = read_customer_origin_destination_including_distance()
    customer_name = 'Customer ' + str(num)
    origin_lat, origin_long, hub_lat, hub_long, dest_lat, dest_long = '', '', '', '', '', ''
    plot_list = []
    plot_marker = []
    for i in range(len(route)):
        for j in range(len(customer_distance)):
            if customer_name == customer_distance[j]:
                for k in range(len(customer_distance)):
                    if route[i][0] == customer_distance[k]:
                        origin_lat = customer_distance[k + 1]
                        origin_long = customer_distance[k + 2]
                    if route[i][2] == customer_distance[k]:
                        dest_lat = customer_distance[k + 1]
                        dest_long = customer_distance[k + 2]
        for a in range(len(company)):
            if route[i][1] == company[a]:
                hub_lat = company[a + 2]
                hub_long = company[a + 3]
        plot_marker.append(route[i][0])
        plot_marker.append(origin_lat)
        plot_marker.append(origin_long)
        plot_marker.append(route[i][1])
        plot_marker.append(hub_lat)
        plot_marker.append(hub_long)
        plot_marker.append(route[i][2])
        plot_marker.append(dest_lat)
        plot_marker.append(dest_long)
        plot_list.append(plot_marker)
        plot_marker = []
        plotting = MapsPlotting.getRoute(origin_lat, origin_long, hub_lat, hub_long, dest_lat, dest_long)
        plot_list.append(plotting)

    MapsPlotting.plotAllRoutes(plot_list, num)


def getAllRoute(customer):
    route_all_list = []
    for i in range(len(customer)):
        route_all_list.append(customer[i][2].split(" --> "))
    return route_all_list


def read_company_full_details():
    print("Reading Company_Full_Details.txt")
    company_file = open("Company_Full_Details.txt", "r")
    company_list = company_file.readlines()
    for i in range(len(company_list)):
        company_list[i] = company_list[i].replace('\n', '')
    company_file.close()
    return company_list


def read_customer_origin_destination_including_distance():
    print("Reading Customer_Origin_Destination_Including_Distance.txt")
    customer_origin_dest_distance_file = open("Customer_Origin_Destination_Including_Distance.txt", "r")
    customer_origin_dest_distance_list = customer_origin_dest_distance_file.readlines()
    for i in range(len(customer_origin_dest_distance_list)):
        customer_origin_dest_distance_list[i] = customer_origin_dest_distance_list[i].replace('\n', '')
    customer_origin_dest_distance_file.close()
    return customer_origin_dest_distance_list
