from GeocodingAPI import GeocodingAPIClass
from Company import CompanyClass
import json


def read_company_file(file_name):
    company_file = open(file_name, "r")
    company_all_list = company_file.readlines()
    company_object_list = []
    c = []
    while len(company_all_list) != 0:
        for i in range(2):
            c.append(company_all_list.pop(0).replace('\n', ''))
        if len(company_all_list) == 0:
            break
        else:
            company_all_list.pop(0)
        company_object_list.append(CompanyClass(c[0], c[1]))
        c = []
    company_file.close()
    return company_object_list


def calculate_and_write_location_coordinate(company_lists):
    for company in company_lists:
        location = GeocodingAPIClass.getGeoCoord(company.address)
        company.latitude = location[0]
        company.longitude = location[1]
    company_file = open("Company_Full_Details.txt", "w")
    for company in company_lists:
        company_file.write(str(company.name) + "\n")
        company_file.write(str(company.address) + "\n")
        company_file.write(str(company.latitude) + "\n")
        company_file.write(str(company.longitude) + "\n")
        company_file.write("\n")


company_list = read_company_file("Company_Name_Address.txt")
#calculate_and_write_location_coordinate(company_list)

