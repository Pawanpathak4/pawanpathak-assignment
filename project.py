from tweepy import *
from textblob import TextBlob
import re
from collections import Counter
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import nltk
nltk.download('stopwords')

#### Consumer KEY  ####
Consumer_key = ""

#### Consumer_SECRET ####
Consumer_secret = ""

### Token ###
Token_Key = ""
### Token KEY ###
Token_secret = ""


def retrieve_tweets() :   ####To retrieve the required tweets
    query = input("Enter the keyowords without hashtag :") ###ask for the query to search on twitter
    query = "#"+ query      ####Adding a "#" for better search results
    Tweets = api.search(q=query,  lang="en",count =200) ### Searching the twitter
    return  Tweets


def print_tweets(tweets):   #### For printing the tweets
    for data in tweets:
        tweet = TextBlob(data.text)
        print(tweet)
        print(tweet.sentiment)      ### For analysis of sentiments
        print("Done at :" +str(data.created_at))    ### Print the time for the creation of tweet
        print("Username :"+data.user.name)          ### Print the user name of the twitter user
        print("---------------------------------------------")


def extract_for_user():        ###Extracts tweets for perticular user
    query = input("Enter the onscreen name of the user with an '@' in the front:")
    Tweets = api.user_timeline(screen_name=query, count=200)    ###Search for tweets by the given screen name
    print_tweets(Tweets)



def no_of_followers(Tweet):
    print("Printing no of followers :-\nUSER        No of Followers")
    total = 0
    for data in Tweet:
        print(data.user.name +"     "+str(data.user.followers_count))
        total= total + data.user.followers_count
    print("Total no of persons effected by the Tweets:" + str(total))


def search_for_keywords():      ### search the tweets  for perticular keyword in the tweets by a perticular user
    user = input("Enter the name of the user:")
    query = []      ### Stores the keywords to be searched for
    tweets= []  ### to store the tweets
    tweets2 = []        ### to storre modified tweetss
    shows= True
    while shows :       ### to store the no of keywords till we want
        qw = input("Enter  the keywords ro be searched for :")
        query.append(qw)
        ask= input("Do you want to add more keywords?(Y/N)")
        ask= ask.upper()
        if ask == "Y":
            pass
        elif ask == "N":
            shows = False
        else :
            print("invalid input  \n"
                  "Taking default input as 'No' ")
            shows = False
    result = api.user_timeline(screen_name=user,count = 200) ### searches for the 200 tweets by the perticular user
    for data in result:
        tweets.append(data)
    oldest = tweets[-1].id      ### stores the id of the last tweet retrieved
    oldest_at = tweets[-1].created_at   ### Stores the time and date of the last tweet retrieved
    qu = True
    while qu:       ###to retrieve more older tweets
        qu2 = input("Do you want  more  tweets older than "+str(oldest_at)+"(Y/N)  :")
        qu2 = qu2.upper()
        if qu2 == "Y":
            result2 = api.user_timeline(screen_name=user, count= 200, max_id =oldest)       ###retrieve the tweet older then the given tweet id
            for data in result2:
                tweets.append(data)     ###  appended the new tweets retrived
            oldest = tweets[-1].id
            oldest_at = tweets[-1].created_at
        elif qu2 == "N":
            qu = False
        else:
            print("invalid input  \n"
                  "Taking default input as 'No' ")
            qu = False
    count = -1
    for tweet1 in tweets:
        count = count + 1       ###starts the list from beginning
        tweet = tweet1.text
        tweet = re.sub(r"http\S+", "", tweet)  ##### removes the URL from the text of tweet
        tweets[count].text = tweet
    for keyword in query:
        for data in tweets:
            tex = TextBlob(data.text)
            qw = tex.find(keyword)
            if qw != -1:
                tweets2.append(data)### Appends the modified tweets
            else:
                pass
    if len(tweets2)>0:
        print_tweets(tweets2)
    else :
        print("No tweet found with the related keywords")


def send_message():     ###Sends direct message to a perticular user
    user = input("Enter the user name of the person :")
    message = input("Enter the message to be send :")
    api.send_direct_message(screen_name=user,text=message)


def extract_info():     ### Extract info from the tweets
    tweet= retrieve_tweets()
    location =[]
    for data in tweet:
        tb = TextBlob(data.text)
        print("language of Tweet :"+tb.detect_language()+"\t timezone :" +str(data.user.time_zone))     ###Extract language and timezone for the tweets
        loc = data.user.location    ###Extract location from user info
        location.append(loc)
    word_counts = Counter(location)
    print("location \t No of occurences ")
    common_loc =word_counts.most_common(5) ###passes the 5 most common locaton to the common_loc list
    for data in common_loc:
        print(data)
    print("Blank space indicates no location defined by the user")


def remove_stopwords(): ### rempves the stopwords from the retrieved tweets
    tweet1 = retrieve_tweets()
    stop_words = set(stopwords.words('english'))        ###set the stopwords to be used
    for data in tweet1:
        data.text = data.text.lower()
        word_tokens = word_tokenize(data.text)  ### split the text in different words
        filtered_sentence = []      ###stores the filtered text
        for w in word_tokens:
            if w not in stop_words: ####if the word is not in the stopwords list then it is appended to the filtered_sentance
                filtered_sentence.append(w)
        msg = " ".join(map(str,filtered_sentence))      ### join the different words in a list to for a sentance
        data.text = msg
    data1=[]    ### To Extend the words in the tweets
    for data in tweet1:
        data2 = data.text.split(" ", 30)        ###Spliting the data in different words
        data1.extend(data2) ###extending in data 1
    print_tweets(tweet1)
    word = Counter(data1)
    print("Printing the top 10 words appearing in the tweets:")
    top10 = word.most_common(10)
    for data in top10:
        print(data)


def tweet_on_Twitter():
    text = input("What do you want to tweet")
    api.update_status(text)


def for_narendra_modi():
    print("Retreving tweets")
    Tweets = api.user_timeline(screen_name= "@narendramodi", count=200)  ###Search for tweets by the given screen name
    print_tweets(Tweets)
    query = []  ### Stores the keywords to be searched for
    tweets = []  ### to store the tweets
    tweets2 = []  ### to store modified tweets
    shows = True
    while shows:  ### to store the no of keywords till we want
        qw = input("Enter  the keywords ro be searched for :")
        query.append(qw)
        ask = input("Do you want to add more keywords?(Y/N)")
        ask = ask.upper()
        if ask == "Y":
            pass
        elif ask == "N":
            shows = False
        else:
            print("invalid input  \n"
                  "Taking default input as 'No' ")
            shows = False

    for data in Tweets:
        tweets.append(data)
    oldest = tweets[-1].id  ### stores the id of the last tweet retrieved
    oldest_at = tweets[-1].created_at  ### Stores the time and date of the last tweet retrieved
    qu = True
    while qu:  ###to retrieve more older tweets
        qu2 = input("Do you want  more  tweets older than " + str(oldest_at) + "(Y/N)  :")
        qu2 = qu2.upper()
        if qu2 == "Y":
            result = api.user_timeline(screen_name="@narendramodi", count=200,
                                        max_id=oldest)  ###retrieve the tweet older then the given tweet id
            for data in result:
                tweets.append(data)  ###  appended the new tweets retrived
            oldest = tweets[-1].id
            oldest_at = tweets[-1].created_at
        elif qu2 == "N":
            qu = False
        else:
            print("invalid input  \n"
                  "Taking default input as 'No' ")
            qu = False
    count = -1
    for tweet1 in tweets:
        count = count + 1  ###starts the list from beginning
        tweet = tweet1.text
        tweet = re.sub(r"http\S+", "", tweet)  ##### removes the URL from the text of tweet
        tweets[count].text = tweet
    for keyword in query:
        for data in tweets:
            tex = TextBlob(data.text)
            qw = tex.find(keyword)
            if qw != -1:
                tweets2.append(data)  ### Appends the modified tweets
            else:
                pass
    if len(tweets2) > 0:
        print_tweets(tweets2)
    else:
        print("No tweet found with the related keywords")


def for_donald_trump():
    print("Retreving tweets")
    Tweets = api.user_timeline(screen_name="@realdonaldtrump", count=200)  ###Search for tweets by the given screen name
    print_tweets(Tweets)
    query = []  ### Stores the keywords to be searched for
    tweets = []  ### to store the tweets
    tweets2 = []  ### to store modified tweets
    shows = True
    while shows:  ### to store the no of keywords till we want
        qw = input("Enter  the keywords ro be searched for :")
        query.append(qw)
        ask = input("Do you want to add more keywords?(Y/N)")
        ask = ask.upper()
        if ask == "Y":
            pass
        elif ask == "N":
            shows = False
        else:
            print("invalid input  \n"
                  "Taking default input as 'No' ")
            shows = False

    for data in Tweets:
        tweets.append(data)
    oldest = tweets[-1].id  ### stores the id of the last tweet retrieved
    oldest_at = tweets[-1].created_at  ### Stores the time and date of the last tweet retrieved
    qu = True
    while qu:  ###to retrieve more older tweets
        qu2 = input("Do you want  more  tweets older than " + str(oldest_at) + "(Y/N)  :")
        qu2 = qu2.upper()
        if qu2 == "Y":
            result = api.user_timeline(screen_name="@realdonaldtrump", count=200,
                                        max_id=oldest)  ###retrieve the tweet older then the given tweet id
            for data in result:
                tweets.append(data)  ###  appended the new tweets retrived
            oldest = tweets[-1].id
            oldest_at = tweets[-1].created_at
        elif qu2 == "N":
            qu = False
        else:
            print("invalid input  \n"
                  "Taking default input as 'No' ")
            qu = False
    count = -1
    for tweet1 in tweets:
        count = count + 1  ###starts the list from beginning
        tweet = tweet1.text
        tweet = re.sub(r"http\S+", "", tweet)  ##### removes the URL from the text of tweet
        tweets[count].text = tweet
    for keyword in query:
        for data in tweets:
            tex = TextBlob(data.text)
            qw = tex.find(keyword)
            if qw != -1:
                tweets2.append(data)  ### Appends the modified tweets
            else:
                pass
    if len(tweets2) > 0:
        print_tweets(tweets2)
    else:
        print("No tweet found with the related keywords")



auth = OAuthHandler(Consumer_key, Consumer_secret)      ###authorises the twitter handle
auth.set_access_token(Token_Key, Token_secret)          ###Passes the access tokens and the key

api = API(auth)     ### check for Authorization
menu_display = True
while  menu_display :
    menuchoice = int(input('Choices are: \n1.Extract tweets for the defined keywords and find the total no of persons'
                           'effected by the Tweets  \n'
                           '2.Extract Tweets for a specified user \n'
                           '3.Search for specified words in tweets by the specified users \n'
                           '4.Extract location , language and time zone for the retrieved tweets and print the most'
                           'occurring locations \n'
                           '5.Send a direct message to someone \n'
                           '6.Remove stopWords from retrieved tweets \n'
                           '7.Tweet a message\n'
                           '8.Extract Tweets for donald trump\n'
                           '9.Extract Tweets for narendra modi \n'
                           '10.Exit \n'
                           'Enter your choice :\t '))

    if menuchoice == 1:
        tweet = retrieve_tweets()
        print_tweets(tweet)
    elif menuchoice == 2:
        extract_for_user()
    elif menuchoice == 3:
        search_for_keywords()
    elif menuchoice == 4:
        extract_info()
        pass
    elif menuchoice == 5:
        send_message()
    elif menuchoice == 6:
        remove_stopwords()
    elif menuchoice == 7:
        tweet_on_Twitter()
    elif menuchoice == 8:
        for_donald_trump()
    elif menuchoice == 9:
        for_narendra_modi()
    elif menuchoice == 10:
        menu_display = False
        exit()
    else:
        print("illegal choice, plz retry.")

