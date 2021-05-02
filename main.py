import Company
import Customer
import DistanceMatrixAPI
import GeocodingAPI
from Company import CompanyClass
from Customer import CustomerClass
from os import path
import time


def read_raw_company_file():
    company_file = open("Company_Raw_Name_Address.txt", "r")
    company_all_list = company_file.readlines()
    company_object_list = []
    c = []
    while len(company_all_list) != 0:
        for i in range(2):
            c.append(company_all_list.pop(0).replace('\n', ''))
        if len(company_all_list) != 0:
            company_all_list.pop(0)
        company_object_list.append(CompanyClass(c[0], c[1]))
        c = []
    company_file.close()
    return company_object_list


def read_raw_customer_file():
    customer_file = open("Customer_Raw_Origin_Destination.txt", "r")
    customer_all_list = customer_file.readlines()
    customer_object_list = []
    c = []
    while len(customer_all_list) != 0:
        for i in range(7):
            c.append(customer_all_list.pop(0).replace('\n', ''))
        if len(customer_all_list) != 0:
            customer_all_list.pop(0)
        customer_object_list.append(CustomerClass(c[0], c[1], c[2], c[3], c[4], c[5], c[6]))
        c = []
    customer_file.close()
    return customer_object_list


def calculate_and_write_location_coordinate(company_lists):
    for company in company_lists:
        location = GeocodingAPI.getGeoCoord(company.address)
        company.latitude = location[0]
        company.longitude = location[1]
    company_file = open("Company_Full_Details.txt", "w")
    for company in company_lists:
        company_file.write(str(company.name) + "\n")
        company_file.write(str(company.address) + "\n")
        company_file.write(str(company.latitude) + "\n")
        company_file.write(str(company.longitude) + "\n\n")


def write_customer_2_point_distance(customer_lists):
    customer_file = open("Customer_Origin_Destination_Including_Distance.txt", 'w')
    for customer in customer_lists:
        customer_file.write(str(customer.customer_name) + "\n")
        customer_file.write(str(customer.ori_name) + "\n")
        customer_file.write(str(customer.ori_lat) + "\n")
        customer_file.write(str(customer.ori_long) + "\n")
        customer_file.write(str(customer.des_name) + "\n")
        customer_file.write(str(customer.des_lat) + "\n")
        customer_file.write(str(customer.des_long) + "\n")
        customer_file.write(str(customer.direct_distance) + "\n\n")


def calc_total_distance(customer, company):
    total_distance = 0
    distance1 = DistanceMatrixAPI.calc_distance_between_2_point(
        Customer.formatted_coordinates(customer.ori_lat, customer.ori_long),
        Company.formatted_coordinates(company.latitude, company.longitude))
    distance2 = DistanceMatrixAPI.calc_distance_between_2_point(
        Company.formatted_coordinates(company.latitude, company.longitude),
        Company.formatted_coordinates(customer.des_lat, customer.des_long))
    total_distance = float(distance1.replace(" km", "")) + float(distance2.replace(" km", ""))
    return total_distance


def generate_file_for_customer_with_each_company(customer_lists, company_lists):
    for customer in customer_lists:
        customer_file = open(customer.customer_name + ".txt", 'w')
        company_ranking_list = []
        for company in company_lists:
            total_distance = calc_total_distance(customer, company)
            company_ranking_list.append([company, total_distance])
        company_ranking_list.sort(key=lambda x: x[1])
        count = 0
        for i in range(len(company_ranking_list)):
            customer_file.write(str(count) + "\n")
            customer_file.write(str(company_ranking_list[i][0].name) + "\n")
            customer_file.write(str(company_ranking_list[i][1]) + " km" + "\n\n")
            if i != len(company_ranking_list) - 1:
                if company_ranking_list[i][1] != company_ranking_list[i + 1][1]:
                    count += 1
        customer_file.close()


def preprocessing_company():
    company_list = read_raw_company_file()
    calculate_and_write_location_coordinate(company_list)


def preprocessing_customer():
    customer_list = read_raw_customer_file()
    write_customer_2_point_distance(customer_list)


def read_company_full_details():
    if path.exists("Company_Full_Details.txt") is False:
        preprocessing_company()
    company_file = open("Company_Full_Details.txt", "r")
    company_all_list = company_file.readlines()
    company_object_list = []
    c = []
    while len(company_all_list) != 0:
        for i in range(4):
            c.append(company_all_list.pop(0).replace('\n', ''))
        if len(company_all_list) != 0:
            company_all_list.pop(0)
        company_object_list.append(CompanyClass(c[0], c[1], c[2], c[3]))
        c = []
    company_file.close()
    return company_object_list


def read_customer_full_details():
    if path.exists("Customer_Origin_Destination_Including_Distance.txt") is False:
        preprocessing_customer()
    customer_file = open("Customer_Origin_Destination_Including_Distance.txt", "r")
    customer_all_list = customer_file.readlines()
    customer_object_list = []
    c = []
    while len(customer_all_list) != 0:
        for i in range(8):
            c.append(customer_all_list.pop(0).replace('\n', ''))
        if len(customer_all_list) != 0:
            customer_all_list.pop(0)
        customer_object_list.append(CustomerClass(c[0], c[1], c[2], c[3], c[4], c[5], c[6], c[7]))
        c = []
    customer_file.close()
    return customer_object_list


initial_time = time.time()
company_list = read_company_full_details()
customer_list = read_customer_full_details()
generate_file_for_customer_with_each_company(customer_list, company_list)  # generate score for problem 1 and save it in file

