from urllib.request import Request, urlopen


# turn html to text
def stripTags(pageContents):
    pageContents = str(pageContents)
    startLoc = pageContents.find("<p>")
    endLoc = pageContents.rfind("<br/>")

    pageContents = pageContents[startLoc:endLoc]

    inside = 0
    text = ''

    for char in pageContents:
        if char == '<':
            inside = 1
        elif inside == 1 and char == '>':
            inside = 0
        elif inside == 1:
            continue
        else:
            text += char

    return text


# remove all non-alphanumeric characters (using Unicode definition of alphanumeric).
def stripNonAlphaNum(text):
    import re
    return re.compile(r'\W+', re.UNICODE).split(text)


def wordListToFreqDict(wordlist):
    wordfreq = [wordlist.count(p) for p in wordlist]
    return dict(list(zip(wordlist, wordfreq)))


def sortFreqDict(freqdict):
    aux = [(freqdict[key], key) for key in freqdict]
    aux.sort()
    aux.reverse()
    return aux


# stop words list
def stopword():
    st = open("stopwords.txt")
    stop = st.read()
    stopwords = stop.split(",")
    return stopwords


def StopWordCount(url):
    print("Executing StopWordCount for URL:", url)
    # file1 = open(readFile, "r", encoding="utf8")
    file1 = Request(url, headers={'User-Agent': 'Mozilla/5.0'})

    pattern = urlopen(file1).read().lower().split()

    text = stopword()

    sw = []
    for i in pattern:
        for j in text:
            found = boyer_goodSuffix(i.decode('utf-8'), j)
            if found:
                sw.append(i.decode('utf-8'))

    return sw


def removeStopWord(url):  # return the list of words without stopwords
    text = stopword()
    # file = open(readFile, "r",encoding="utf8")
    file = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    pattern = urlopen(file).read().lower().split()

    new = []
    for i in pattern:
        for j in text:
            found = boyer_goodSuffix(i.decode('utf-8'), j)
            if found:
                break
        if not found:
            new.append(i.decode('utf-8'))

    return new


def preprocess1(shift, bpos, pat, m):
    # m is the length of pattern
    i = m
    j = m + 1
    bpos[i] = j

    while i > 0:
        while j <= m and pat[i - 1] != pat[j - 1]:
            if shift[j] == 0:
                shift[j] = j - i

            j = bpos[j]  # if mismatch, update the next border

        i -= 1  # if pat[i-1]==pat[j-1], bpos[i-1]=j-1
        j -= 1
        bpos[i] = j


def preprocess2(shift, bpos, m):
    j = bpos[0]
    for i in range(m + 1):

        if shift[i] == 0:
            shift[i] = j  # shift pattern from i to j

        if i == j:
            j = bpos[j]


def boyer_goodSuffix(pat, text):
    # s is shift of the pattern with respect to text
    s = 0
    m = len(pat)
    n = len(text)

    bpos = [0] * (m + 1)

    # initialize all occurrence of shift to 0
    shift = [0] * (m + 1)

    # do preprocessing
    preprocess1(shift, bpos, pat, m)
    preprocess2(shift, bpos, m)

    while s <= n - m:
        j = m - 1

        while j >= 0 and pat[j] == text[s + j]:  # match
            j -= 1

        if j < 0 and n == m and s == 0:
            s += shift[0]  # reset shift position
            return True
        else:
            # mismatch, shift the pattern shift[j+1]
            s += shift[j + 1]

    return False
