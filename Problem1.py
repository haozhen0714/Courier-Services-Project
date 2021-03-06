import Company
import Customer
import DistanceMatrixAPI
import GeocodingAPI
from Company import CompanyClass
from Customer import CustomerClass


def read_raw_company_file():  # O(n) : n company
    print("Read Company_Raw_Name_Address.txt")
    company_file = open("P1/Company_Raw_Name_Address.txt", "r")
    company_all_list = company_file.readlines()
    company_object_list = []
    c = []
    while len(company_all_list) != 0:
        for i in range(2):  # O(2), the time complexity is not significant
            c.append(company_all_list.pop(0).replace('\n', ''))
        if len(company_all_list) != 0:
            company_all_list.pop(0)
        company_object_list.append(CompanyClass(c[0], c[1]))
        c = []
    company_file.close()
    return company_object_list


def read_raw_customer_file():  # O(m): m customer
    print("Read Customer_Raw_Origin_Destination.txt")
    customer_file = open("P1/Customer_Raw_Origin_Destination.txt", "r")
    customer_all_list = customer_file.readlines()
    customer_object_list = []
    c = []
    while len(customer_all_list) != 0:  # O(m): m customer
        for i in range(7):  # O(7), not significant
            c.append(customer_all_list.pop(0).replace('\n', ''))
        if len(customer_all_list) != 0:
            customer_all_list.pop(0)
        customer_object_list.append(CustomerClass(c[0], c[1], c[2], c[3], c[4], c[5], c[6]))
        c = []
    customer_file.close()
    return customer_object_list


def calculate_and_write_company_location_coordinate(company_lists):  # O(n): n company
    for company in company_lists:  # O(n)
        print("Call Geocoding API for address:", company.address, "to get real latitude and longitude")
        location = GeocodingAPI.getGeoCoord(company.address)
        try:
            company.latitude = location[0]
            company.longitude = location[1]
        except TypeError:
            print("Please Provide API KEY in GoogleAPIKey.py")
            exit(0)
    company_file = open("P1/Company_Full_Details.txt", "w")
    print("Write Company_Full_Details.txt")
    for company in company_lists:  # O(n)
        company_file.write(str(company.name) + "\n")
        company_file.write(str(company.address) + "\n")
        company_file.write(str(company.latitude) + "\n")
        company_file.write(str(company.longitude) + "\n\n")


def write_customer_2_point_distance(customer_lists):  # O(m): m customer
    customer_file = open("P1/Customer_Origin_Destination_Including_Distance.txt", 'w')
    print("Write Customer_Origin_Destination_Including_Distance.txt")
    for customer in customer_lists:
        customer_file.write(str(customer.customer_name) + "\n")
        customer_file.write(str(customer.ori_name) + "\n")
        customer_file.write(str(customer.ori_lat) + "\n")
        customer_file.write(str(customer.ori_long) + "\n")
        customer_file.write(str(customer.des_name) + "\n")
        customer_file.write(str(customer.des_lat) + "\n")
        customer_file.write(str(customer.des_long) + "\n")
        customer_file.write(str(customer.direct_distance) + "\n\n")


def calc_total_distance(customer, company):  # O(1)
    print("Call DistanceMatrixAPI to get distance between", customer.ori_name, 'and', company.name)
    print("Call DistanceMatrixAPI to get distance between", company.name, 'and', customer.des_name)
    distance1 = DistanceMatrixAPI.calc_distance_between_2_point(
        Customer.formatted_coordinates(customer.ori_lat, customer.ori_long),
        Company.formatted_coordinates(company.latitude, company.longitude))
    distance2 = DistanceMatrixAPI.calc_distance_between_2_point(
        Company.formatted_coordinates(company.latitude, company.longitude),
        Company.formatted_coordinates(customer.des_lat, customer.des_long))
    total_distance = float(distance1.replace(" km", "")) + float(distance2.replace(" km", ""))
    return distance1, distance2, total_distance


def generate_file_for_customer_with_each_company(customer_lists,
                                                 company_lists):  # O(mn): nested loop for each customer and company
    for customer in customer_lists:  # O(m)
        customer_file_ranking = open("P1/" + customer.customer_name + " Problem 1 Ranking.txt", 'w')
        customer_file_details_route = open("P1/" + customer.customer_name + " Delivery Details.txt", 'w')
        print("Write " + customer.customer_name + " Problem 1 Ranking.txt")
        print("Write " + customer.customer_name + " Delivery Details.txt")
        company_ranking_list = []
        for company in company_lists:  # O(n)
            return_distances = calc_total_distance(customer, company)
            customer_file_details_route.write(str(customer.ori_name) + " --> " + str(company.name) + "\n")
            customer_file_details_route.write(str(return_distances[0]) + "\n")
            customer_file_details_route.write(str(company.name) + " --> " + str(customer.des_name) + "\n")
            customer_file_details_route.write(str(return_distances[1]) + "\n\n")
            total_distance = return_distances[2]
            company_ranking_list.append([company, total_distance])
        company_ranking_list.sort(key=lambda x: x[1])
        count = 0
        for i in range(len(company_ranking_list)):  # O(n) at the end
            customer_file_ranking.write(str(count) + "\n")
            customer_file_ranking.write(str(company_ranking_list[i][0].name) + "\n")  # company object
            customer_file_ranking.write(
                str(customer.ori_name) + " --> " + str(company_ranking_list[i][0].name) + " --> " + str(
                    customer.des_name) + "\n")
            customer_file_ranking.write(
                "Total Distance: " + "{0:.2f}".format(company_ranking_list[i][1]) + " km" + "\n\n")  # distance
            if i != len(company_ranking_list) - 1:
                if company_ranking_list[i][1] != company_ranking_list[i + 1][1]:
                    count = i + 1
            else:
                count = i + 1

        customer_file_ranking.close()
        customer_file_details_route.close()


def preprocessing_company():  # O(1)
    company_list = read_raw_company_file()
    calculate_and_write_company_location_coordinate(company_list)


def preprocessing_customer():  # O(1)
    customer_list = read_raw_customer_file()
    write_customer_2_point_distance(customer_list)


def read_company_full_details():  # O(n): n company
    preprocessing_company()
    company_file = open("P1/Company_Full_Details.txt", "r")
    company_all_list = company_file.readlines()
    company_object_list = []
    c = []
    while len(company_all_list) != 0:  # O(n): n company
        for i in range(4):  # O(4), not significant time complexity
            c.append(company_all_list.pop(0).replace('\n', ''))
        if len(company_all_list) != 0:
            company_all_list.pop(0)
        company_object_list.append(CompanyClass(c[0], c[1], c[2], c[3]))
        c = []
    company_file.close()
    return company_object_list


def read_customer_full_details():  # O(m): m customer
    preprocessing_customer()
    customer_file = open("P1/Customer_Origin_Destination_Including_Distance.txt", "r")
    customer_all_list = customer_file.readlines()
    customer_object_list = []
    c = []
    while len(customer_all_list) != 0:  # O(m): m customer
        for i in range(8):  # O(8), not significant
            c.append(customer_all_list.pop(0).replace('\n', ''))
        if len(customer_all_list) != 0:
            customer_all_list.pop(0)
        customer_object_list.append(CustomerClass(c[0], c[1], c[2], c[3], c[4], c[5], c[6], c[7]))
        c = []
    customer_file.close()
    return customer_object_list


# added by jinghui
def read_customer_ranking_details(c):  # O(m): m customer at the end
    print("Read Customer " + c + " Problem 1 Ranking.txt")
    customer_file = open("P1/Customer " + c + " Problem 1 Ranking.txt", "r")
    customer_delivery_list = customer_file.readlines()
    for i in range(len(customer_delivery_list)):  # O(m) at the end
        customer_delivery_list[i] = customer_delivery_list[i].replace('\n', '')
    details = []
    ranking = []
    while len(customer_delivery_list) != 0:  # O(m): m customer at the end
        for i in range(4):  # O(4)
            details.append(customer_delivery_list.pop(0))
        customer_delivery_list.pop(0)
        ranking.append(details)
        details = []
    customer_file.close()
    return ranking
