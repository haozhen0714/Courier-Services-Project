import requests
from bs4 import BeautifulSoup
import re
from nltk.tokenize import RegexpTokenizer
import nltk
import plotly.graph_objects as go
from requests.api import request

words = []
words_ns = []
wordfreq = []

# nltk.download('stopwords') # once download ady can comment it :)

# Store 3 urls of online news websites 
# Store 3 urls of online news websites 
#J&T
url1 = 'https://www.malaymail.com/news/malaysia/2021/02/07/courier-company-jt-express-explains-staffs-violent-handling-of-parcels-caug/1947791'
url2 = 'https://www.technobaboy.com/2021/02/03/j-t-express-unlisaya-promo-extended-until-feb-28/'   
url3 = 'https://www.panaynews.net/jt-express-launched-jt-pantry/'
#City-link Express
url4 = 'https://www.nst.com.my/news/nation/2020/05/595858/courier-service-lifeline-time-enforced-isolation'
url5 = 'https://www.truckandbusnews.net/latest-news/posts/2018/november/city-link-express-aims-for-fast-delivery-and-customer-satisfaction-with-isuzu/'
url6 = 'https://www.carsifu.my/news/city-link-express-takes-delivery-of-277-isuzu-vehicles'
#Pos Laju
url7 = 'https://www.prnewswire.com/news-releases/pos-laju-recognized-by-frost--sullivan-for-dominating-the-delivery-service-market-in-malaysia-on-the-strength-of-its-vast-channel-network-301194852.html'
url8 = 'https://soyacincau.com/2020/08/15/pos-malaysia-e-consignment-notes-qr-code-available/'
url9 = 'https://www.digitalnewsasia.com/digital-economy/pos-laju-handles-442mil-parcels-online-purchases-during-1111-sale'
#GDEX
url10 = 'https://www.theedgemarkets.com/article/gdex-top-active-surges-20-stronger-earnings-prospects'
url11 = 'https://www.thestar.com.my/business/business-news/2020/10/21/gdex-express-proposes-1-free-warrant-for-every-8-shares-held'
url12 = 'https://www.theborneopost.com/2020/05/29/gdex-to-still-benefit-from-online-purchasing-if-cmco-is-lifted/'
#DHL
url13 = 'https://www.joc.com/international-logistics/surge-e-commerce-drives-dhl-group-record-profits_20210309.html'
url14 = 'https://www.dw.com/en/dhl-fined-94-million-for-violating-us-sanctions/a-4548974'
url15 = 'https://hrasiamedia.com/top-news/dhl-express-top-employer-in-asia-pacific/'

# get data
# Make the request
r = requests.get(url15)
#r = requests.get(url2)

# Extract HTML from Response object and print
html = r.text

# wrangle the data
# Create a BeautifulSoup object from the HTML
soup = BeautifulSoup(html, "html.parser")

# Get the text out of the soup and print it
text = soup.get_text()
#print(text)

#read positive word txt file 
file = open("positiveWord.txt","r",encoding = 'utf-8')
for line in file:
    line = line.strip() # remove \n
    line = line.replace(" ","") # remove additional space
    line = line.split(",") # convert into list, split by using ,
    my_list = line # mylist now contains a list of words
    #print(my_list)

#read negative word txt file 
file = open("negativeWord.txt","r",encoding = 'utf-8')
for line in file:
    line = line.strip() # remove \n
    line = line.replace(" ","") # remove additional space
    line = line.split(",") # convert into list, split by using ,
    my_list1 = line # mylist now contains a list of words
    #print(my_list1)

#variable to store count 
total_count = 0

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
                    count +=1
                    #print("Pattern occurs with shift:", s)
                    #print(count)
        
            if s < n - m:
                t = (d * (t - ord(T[s]) * h) + ord(T[s + m])) % q
        return count

#loop through the positive list
for x in my_list:
    #print(x)

    text = text 
    pattern = x 
    d = 256 # number of characters
    q = 101  # A prime number
    total_count += rabin_karp(text, pattern, d, q)
print("------------------------------------------------")
print("Total count of positive word is "),
print(total_count)    
print("------------------------------------------------")

#loop through the negative list
for x in my_list1:
    #print(x)

    text = text 
    pattern = x 
    d = 256 # number of characters
    q = 101  # A prime number
    total_count += rabin_karp(text, pattern, d, q)
print("------------------------------------------------")
print("Total count of negative word is "),
print(total_count)    
print("------------------------------------------------")
