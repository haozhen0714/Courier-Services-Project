import requests
from bs4 import BeautifulSoup
import plotly.graph_objects as go
from plotly.offline import plot
import plotly.graph_objs as go
from urllib.request import Request, urlopen
import obo
import matplotlib.pyplot as plt


def add_company_URL(company_list):
    read_URL = open('All Company URL.txt', 'r')
    company_URL = read_URL.readlines()
    company_URL = [i.strip() for i in company_URL]
    for company in company_list:
        for i in range(len(company_URL)):
            if company.name == company_URL[i]:
                company_URL.pop(i)  # pop useless company name
                while company_URL[i] != 'end':
                    company.url_list.append(company_URL.pop(i))
                company_URL.pop(i)  # pop end
                break
    read_URL.close()


def generate_ranking_file_for_p2(company_list):
    company_list = company_list.copy()
    for company in company_list:
        company.calc_positive_percentage()  # compute positive percentage for each company
    company_list.sort(key=lambda x: x.positive_percentage, reverse=True)
    p2_ranking_file = open('Problem 2 Ranking.txt', 'w')
    text = ""
    conclusion = ""
    last_place = len(company_list) - 1
    i = 0
    j = 0
    for company in company_list:
        # construct conclusion
        conclusion += company.name + " is ranked number " + str(i + 1) + " out of " + str(
            last_place + 1) + " companies. "
        if i == 0:
            conclusion += company.name + (
                    " is the highest ranking courier company. It has the highest percentage of positive " +
                    "word count. ")
        elif i == last_place:
            conclusion += company.name + " is the lowest ranking courier company."
        text += str(i) + "\n"  # write ranking
        text += company.name + "\n" + "Positive Word Count: " + str(company.positive) + "\n"
        text += "Negative Word Count: " + str(company.negative) + "\n"
        text += "Positive Percentage: " + str("{0:.2f}".format(company.positive_percentage)) + "%\n\n"
        if j != len(company_list) - 1:
            if company_list[j].positive_percentage != company_list[j + 1].positive_percentage:  # avoid same ranking
                j += 1
                i = j
            else:
                j += 1
        else:
            i = j

    text += "Conclusion: \n" + conclusion
    print(text)
    # write to file
    p2_ranking_file.write(text)
    p2_ranking_file.close()


def plot_positive_negative_graph(company_list):
    company = [i.name for i in company_list]
    total_positive_list = [i.positive for i in company_list]
    total_negative_list = [i.negative for i in company_list]
    graph_type = [["Company's Positive Sentiment Analysis Graph.html", total_positive_list],
                  ["Company's Negative Sentiment Analysis Graph.html", total_negative_list]]
    for graph in graph_type:
        data = [go.Bar(
            x=company,
            y=graph[1]
        )]
        fig = go.Figure(data=data)
        plot(fig, filename=graph[0])


def rabin_karp(T, P, d=256, q=101):  # time complexity:O(n)
    n = len(T)  # length of text string
    m = len(P)  # length of pattern string
    h = 1

    """
    The value of h would be "(d ** (m - 1)) % q"
    To make sure h would not be overflowed if the values too
    large by using the formula, use loop for each power term 
    rather than powered h instantly
    """
    for i in range(m - 1):
        h = (h * d) % q

    p = 0
    t = 0
    count = 0

    for i in range(m):  # preprocessing, initial hash value for both string
        p = (d * p + ord(P[i])) % q  # hash for pattern string
        t = (d * t + ord(T[i])) % q  # hash for text string

    for s in range(n - m + 1):

        if p == t:  # hash value matched
            j = 0

            while j < m:  # Naive String Matcher Algorithm
                if T[s + j] != P[j]:
                    break
                j += 1
            if j == m:
                count += 1
                # print("Pattern occurs with shift:", s)
                # print(count)

        if s < n - m:
            t = (d * (t - ord(T[s]) * h) + ord(T[s + m])) % q
    return count


def company_sentiment_analysis(company_list):
    url_count = 1
    for company in company_list:
        i = 1
        for url in company.url_list:  # time complexity:O(n^2)
            r = requests.get(url)
            print("")
            print("URL", url_count, ": Url of the article: " + url)
            # r = requests.get(url2)

            # Extract HTML from Response object and print
            html = r.text

            # wrangle the data
            # Create a BeautifulSoup object from the HTML
            soup = BeautifulSoup(html, "html.parser")

            # Get the text out of the soup and print it
            text = soup.get_text()
            # print(text)

            response = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            html = urlopen(response).read()
            # text = obo.stripTags(html).lower()
            # text = text.replace('&amp;amp;', '&')
            wordlist = obo.stripNonAlphaNum(text)
            dictionary = obo.wordListToFreqDict(wordlist)
            sorteddict = obo.sortFreqDict(dictionary)

            x_wordcount = []
            y_wordcount = []

            for w in range(len(sorteddict)):
                x_wordcount.append(sorteddict[w][1])
                y_wordcount.append(sorteddict[w][0])
            print(x_wordcount, "\n", y_wordcount)

            textfile = open("Words Frequency for " + company.name + " URL " + str(i) + ".txt", "w",
                            errors="ignore")
            for element in str(sorteddict):
                line = str(element).replace(")", ")\n")
                textfile.writelines(str(line))
            textfile.close()
            print("Write txt file into: " + "Words Frequency for " + company.name + " URL " + str(i) + ".txt")

            plt.bar(x_wordcount[:30], y_wordcount[:30])
            plt.xticks(x_wordcount[:30], rotation='vertical')
            plt.title("Top 30 Words for " + company.name + " URL " + str(i))
            # plt.show()
            plt.tight_layout()
            plt.savefig("Top 30 Words for " + company.name + " URL " + str(i) + ".png")
            print("Save Figure into: Top 30 Words for " + company.name + " URL " + str(i) + ".png")
            plt.clf()

            stopwords = obo.StopWordCount(url)
            print("Total word counts for stopwords: ", stopwords)
            # read positive word txt file

            file = open("positiveWord.txt", "r", encoding='utf-8')
            for line in file:
                line = line.strip()  # remove \n
                line = line.replace(" ", "")  # remove additional space
                line = line.split(",")  # convert into list, split by using ,
                my_list = line  # mylist now contains a list of words
                # print(my_list)

            # read negative word txt file

            file = open("negativeWord.txt", "r", encoding='utf-8')
            for line in file:
                line = line.strip()  # remove \n
                line = line.replace(" ", "")  # remove additional space
                line = line.split(",")  # convert into list, split by using ,
                my_list1 = line  # mylist now contains a list of words
                # print(my_list1)

            current_positive_count = 0
            current_negative_count = 0
            print("------------------------------------------------")
            print("Executing Rabin-Karp for comparing positive word with positiveWord.txt")
            # loop through the positive list
            for x in my_list:
                # print(x)
                text = text
                pattern = x
                current_positive_count += rabin_karp(text, pattern)

            print("Total count of positive words in this article are: " + str(current_positive_count)),
            print("------------------------------------------------")
            print("Executing Rabin-Karp for comparing negative word with negativeWord.txt")
            # loop through the negative list
            for x in my_list1:
                # print(x)
                text = text
                pattern = x
                current_negative_count += rabin_karp(text, pattern)
            print("Total count of negative words in this article are: " + str(current_negative_count)),
            print("------------------------------------------------")
            company.positive += current_positive_count
            company.negative += current_negative_count
            print("Cumulative positive words for " + str(company.name) + ": " + str(company.positive))
            print("Cumulative negative words for " + str(company.name) + ": " + str(company.negative))
            print("------------------------------------------------")
            i += 1
            url_count += 1
