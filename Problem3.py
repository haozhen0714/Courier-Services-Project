def read_p1_p2_ranking_file(customer_list):
    # Process Each Customer P1 Ranking File
    p1p2_dict = {}
    for customer in customer_list:
        customer_p1_ranking_file = open(customer.customer_name + " Problem 1 Ranking.txt", 'r')
        print("Reading " + customer.customer_name + " Problem 1 Ranking.txt")
        p1_result = customer_p1_ranking_file.readlines()
        p1_result = [i.strip() for i in p1_result]
        p1p2_dict[customer.customer_name] = {}
        while len(p1_result) != 0:
            temp_p1_rank = p1_result.pop(0)
            temp_p1_company = p1_result.pop(0)
            temp_route = p1_result.pop(0)
            temp_total_distance = p1_result.pop(0)
            p1p2_dict[customer.customer_name][temp_p1_company] = {'P1 Score': temp_p1_rank,
                                                                  'Route': temp_route,
                                                                  'Total Distance': temp_total_distance}
            if len(p1_result) != 0:
                p1_result.pop(0)  # pop ''
        customer_p1_ranking_file.close()

    # Process P2 Ranking File
    company_p2_ranking_file = open("Problem 2 Ranking.txt", 'r')
    print("Reading Problem 2 Ranking.txt")
    p2_result = company_p2_ranking_file.readlines()
    p2_result = [i.strip() for i in p2_result]
    p2_result.pop()
    p2_result.pop()
    p2_dict = {}
    while len(p2_result) != 0:
        temp_p2_rank = p2_result.pop(0)
        temp_p2_company = p2_result.pop(0)
        temp_positive = p2_result.pop(0)
        temp_negative = p2_result.pop(0)
        temp_positive_percentage = p2_result.pop(0)
        p2_dict[temp_p2_company] = {'P2 Score': 5 - int(temp_p2_rank),
                                    'Positive': temp_positive,
                                    'Negative': temp_negative,
                                    'Positive Percentage': temp_positive_percentage}

        if len(p2_result) != 0:
            p2_result.pop(0)  # pop useless info

    # push p2_dict into p1p2_dict
    for customer_name in p1p2_dict:
        for company_name in p2_dict:
            # Reverse ranking score for probability distribution calculation
            p1p2_dict[customer_name][company_name]['P1 Score'] = len(p2_dict) - int(p1p2_dict[customer_name]
                                                                                    [company_name]['P1 Score'])
            for x in p2_dict[company_name]:
                p1p2_dict[customer_name][company_name][x] = p2_dict[company_name][x]
    return p1p2_dict


def calc_probability_distribution(p1p2_dict):
    n_company = len(p1p2_dict[[i for i in p1p2_dict][0]])
    total_score = (n_company * (n_company + 1)) / 2
    for customer in p1p2_dict:
        print("For " + customer + ":")
        for company in p1p2_dict[customer]:
            p1p2_dict[customer][company]['Probability'] = (((0.6 * p1p2_dict[customer][company]['P1 Score']) +
                                                            (0.4 * p1p2_dict[customer][company][
                                                                'P2 Score'])) / total_score)

            print("Probability for", company, ":", p1p2_dict[customer][company]['Probability'])


def write_final_ranking_file(p1p2_dict):
    n_company = len(p1p2_dict[[i for i in p1p2_dict][0]])
    for customer in p1p2_dict:
        ranking_info = []
        final_ranking_file = open(customer + ' Problem 3 Final Result.txt', 'w')
        print("Writing " + customer + ' Problem 3 Final Result.txt')
        for company in p1p2_dict[customer]:
            ranking_info.append([company, p1p2_dict[customer][company]['Probability']])
        ranking_info.sort(key=lambda x: x[1], reverse=True)
        final_ranking_file.write("Probability Distribution of each Courier Company for " + customer + ":\n")
        for info in ranking_info:
            final_ranking_file.write(info[0] + (": %.4f" % info[1]) + "\n")
        final_ranking_file.write(
            "----------------------------------------------------------------------------------------\n")
        final_ranking_file.write(
            "Conclusion for each company. \"1\" place is the best ranking representation and so on..." + "\n")
        final_ranking_file.write(
            "----------------------------------------------------------------------------------------\n")
        rank_num = 1
        index = 0
        for info in ranking_info:
            final_ranking_file.write("Courier Company: " + info[0] + "\n")
            final_ranking_file.write("Overall Ranking: " + str(rank_num) + " place\n")
            final_ranking_file.write(
                "Distance Ranking based on shortest route: " + str(
                    n_company - p1p2_dict[customer][info[0]]['P1 Score']) + " place\n")
            final_ranking_file.write('Route: ' + str(p1p2_dict[customer][info[0]]['Route']) + "\n")
            final_ranking_file.write(str(p1p2_dict[customer][info[0]]['Total Distance']) + "\n")
            final_ranking_file.write(
                "Sentiment Ranking based on percentage of positive words: " + str(
                    n_company - p1p2_dict[customer][info[0]]['P2 Score']) + " place\n")
            final_ranking_file.write(p1p2_dict[customer][info[0]]['Positive'] + "\n")
            final_ranking_file.write(p1p2_dict[customer][info[0]]['Negative'] + "\n")
            final_ranking_file.write(p1p2_dict[customer][info[0]]['Positive Percentage'] + "\n\n")
            if index != len(ranking_info) - 1:
                if ranking_info[index][1] != ranking_info[index + 1][1]:
                    index += 1
                    rank_num = index + 1
                else:
                    index += 1
            else:
                rank_num = index + 1
        final_ranking_file.close()
