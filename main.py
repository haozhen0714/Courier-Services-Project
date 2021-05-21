import Problem1 as p1
import MapForOneCustomer
import CompanyMap

# moy's code
company_list = p1.read_company_full_details()
customer_list = p1.read_customer_full_details()
p1.generate_file_for_customer_with_each_company(customer_list,
                                             company_list)  # generate score for problem 1 and save it in file

# added for naim code
CompanyMap.draw_company_map()

# added by jinghui
customers_map = []
for i in range(1, len(customer_list) + 1):
    customers_map.append(p1.read_customer_ranking_details(str(i)))

for i in range(len(customers_map)):
    MapForOneCustomer.plotMap(customers_map[i], i + 1)
