import Problem1 as p1
import Problem2 as p2
import MapForOneCustomer
import CompanyMap
import time

initial_time = time.time()

# moy's code
company_list = p1.read_company_full_details()
customer_list = p1.read_customer_full_details()
print([i.name for i in company_list])

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


# P2
p2.add_company_URL(company_list) # add URL into each company
p2.company_sentiment_analysis(company_list)
p2.plot_positive_negative_graph(company_list)
p2.generate_ranking_file_for_p2(company_list)

print("Execution time:", (time.time()-initial_time), 'seconds')
