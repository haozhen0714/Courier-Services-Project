import requests
from bs4 import BeautifulSoup
import re
from nltk.tokenize import RegexpTokenizer
import nltk
import plotly.graph_objects as go
from requests.api import request
from os import name
import plotly
from plotly.offline import plot
import plotly.graph_objs as go
import pandas as pd
from plotly import express

words = []
words_ns = []
wordfreq = []

# nltk.download('stopwords') # once download ady can comment it :)

# Store 3 urls of online news websites 
# Store 3 urls of online news websites 
# J&T
url1 = 'https://www.malaymail.com/news/malaysia/2021/02/07/courier-company-jt-express-explains-staffs-violent-handling-of-parcels-caug/1947791'
url2 = 'https://www.technobaboy.com/2021/02/03/j-t-express-unlisaya-promo-extended-until-feb-28/'
url3 = 'https://www.gmanetwork.com/news/money/companies/745203/j-amp-t-express-shocked-by-viral-video-apologizes/story/'
# City-link Express
url4 = 'https://www.nst.com.my/news/nation/2020/05/595858/courier-service-lifeline-time-enforced-isolation'
url5 = 'https://www.truckandbusnews.net/latest-news/posts/2018/november/city-link-express-aims-for-fast-delivery-and-customer-satisfaction-with-isuzu/'
url6 = 'https://www.bigwheels.my/city-link-buys-isuzu-trucks/'
# Pos Laju
url7 = 'https://www.prnewswire.com/news-releases/pos-laju-recognized-by-frost--sullivan-for-dominating-the-delivery-service-market-in-malaysia-on-the-strength-of-its-vast-channel-network-301194852.html'
url8 = 'https://soyacincau.com/2020/08/15/pos-malaysia-e-consignment-notes-qr-code-available/'
url9 = 'https://www.digitalnewsasia.com/digital-economy/pos-laju-handles-442mil-parcels-online-purchases-during-1111-sale'
# GDEX
url10 = 'https://www.theedgemarkets.com/article/gdex-top-active-surges-20-stronger-earnings-prospects'
url11 = 'https://www.thestar.com.my/business/business-news/2020/10/21/gdex-express-proposes-1-free-warrant-for-every-8-shares-held'
url12 = 'https://www.theborneopost.com/2020/05/29/gdex-to-still-benefit-from-online-purchasing-if-cmco-is-lifted/'
# DHL
url13 = 'https://www.joc.com/international-logistics/surge-e-commerce-drives-dhl-group-record-profits_20210309.html'
url14 = 'https://www.dw.com/en/dhl-fined-94-million-for-violating-us-sanctions/a-4548974'
url15 = 'https://hrasiamedia.com/top-news/dhl-express-top-employer-in-asia-pacific/'

# set url into a list
url_list = [url1, url2, url3, url4, url5, url6, url7, url8, url9, url10, url11, url12, url13, url14, url15]
# url_list = [url1,url2,url3,url4,url5,url6]
# get data
# Make the request
total_positive = 0
total_negative = 0
i = 1
# store into a list for total count of 3 article for each courier company
total_positive_list = []
total_negative_list = []


def positive_graph():
    # plot graph for positive count of each company
    company = ['J&T', 'City-link Express', 'Pos Laju', 'GDEX', 'DHL']
    # df = pd.read_csv("C:/Users/Hp/Documents/Visual Studio 2019/new/test.csv",error_bad_lines=False)
    data = [go.Bar(
        x=company,
        y=total_positive_list
    )]
    fig = go.Figure(data=data)
    plot(fig, filename="Positive Graph.html")


def negative_graph():
    # plot graph for negative count of each company
    company = ['J&T', 'City-link Express', 'Pos Laju', 'GDEX', 'DHL']
    # df = pd.read_csv("C:/Users/Hp/Documents/Visual Studio 2019/new/test.csv",error_bad_lines=False)
    data = [go.Bar(
        x=company,
        y=total_negative_list

    )]
    fig = go.Figure(data=data)
    plot(fig, filename="Negative Graph.html")


def rabin_karp(T, P, d, q):
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


for url in url_list:
    if i % 3 == 0:
        r = requests.get(url)
        print("")
        print("Url of the article:" + url)
        # r = requests.get(url2)

        # Extract HTML from Response object and print
        html = r.text

        # wrangle the data
        # Create a BeautifulSoup object from the HTML
        soup = BeautifulSoup(html, "html.parser")

        # Get the text out of the soup and print it
        text = soup.get_text()
        # print(text)

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

        # variable to store count
        count_positive = 0
        count_negative = 0

        # loop through the positive list
        for x in my_list:
            # print(x)

            text = text
            pattern = x
            d = 256  # number of characters
            q = 101  # A prime number
            count_positive += rabin_karp(text, pattern, d, q)

        print("------------------------------------------------")
        print("Total count of positive word is "),
        print(count_positive)

        # loop through the negative list
        for x in my_list1:
            # print(x)
            text = text
            pattern = x
            d = 256  # number of characters
            q = 101  # A prime number
            count_negative += rabin_karp(text, pattern, d, q)
        print("Total count of negative word is "),
        print(count_negative)
        print("------------------------------------------------")

        # calcualte the total count of positive and negative number(3 url)
        total_positive += count_positive
        # print(total_positive)
        total_positive_list.append(total_positive)
        # print("Total positive number for each courier company: {}".format(total_positive_list)) #print positive total list
        total_negative += count_negative
        # print(total_negative)
        total_negative_list.append(total_negative)
        # print("Total negative number for each courier company: {}".format(total_negative_list)) #print negative total list

        # clear the total count and set to zero after adding 3 url for the same courier company
        total_positive = 0
        total_negative = 0
        i += 1

    else:
        r = requests.get(url)
        print("")
        print("Url of the article:" + url)
        # r = requests.get(url2)

        # Extract HTML from Response object and print
        html = r.text

        # wrangle the data
        # Create a BeautifulSoup object from the HTML
        soup = BeautifulSoup(html, "html.parser")

        # Get the text out of the soup and print it
        text = soup.get_text()
        # print(text)

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

        # variable to store count
        count_positive = 0
        count_negative = 0


        def rabin_karp(T, P, d, q):
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


        # loop through the positive list
        for x in my_list:
            # print(x)

            text = text
            pattern = x
            d = 256  # number of characters
            q = 101  # A prime number
            count_positive += rabin_karp(text, pattern, d, q)

        print("------------------------------------------------")
        print("Total count of positive word is "),
        print(count_positive)

        # loop through the negative list
        for x in my_list1:
            # print(x)
            text = text
            pattern = x
            d = 256  # number of characters
            q = 101  # A prime number
            count_negative += rabin_karp(text, pattern, d, q)
        print("Total count of negative word is "),
        print(count_negative)
        print("------------------------------------------------")

        total_positive += count_positive
        # print(total_positive)
        total_negative += count_negative
        # print(total_negative)
        i += 1

print(total_positive_list)
print(total_negative_list)
positive_graph()
negative_graph()

