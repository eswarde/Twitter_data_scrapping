# importing packages
import snscrape.modules.twitter as sntwitter
import pandas as pd
import streamlit as st
import time
import pymongo
from dotenv import load_dotenv
import os
from datetime import datetime, timedelta

# Load the environment variables from the .env file
load_dotenv()

# Access the environment variables for Twitter API
os.environ['TWITTER_API_KEY'] = 'orosGOAS7p5WhVoSTsFSiboWe'
os.environ['TWITTER_API_SECRET'] = 't1CHilQSNixa9Rbo5UhtwrVv3gXNtZ11NO6LNUp8A0TtNs6p5B'
os.environ['TWITTER_ACCESS_TOKEN'] = '1854579217-7ai2jHbAJvqI7VwcjCd6zoOwxWZNUDftgnmpy5d'
os.environ['TWITTER_ACCESS_TOKEN_SECRET'] = 'rKa5v9TXtzpwc8GzhSmxARLxx1C5KFwW3GPmPelKCXp6c'

# Connect Python with MongoDB
client = pymongo.MongoClient("mongodb://localhost:27017")
db = client["twitter_data"]
collection = db["tweets"]
client.close()

# Creating a empty data frame
tweets_df = pd.DataFrame()
tweets_list = []


# Display a progress bar
def get_progress_text():
    return "Operation in progress. Please wait."


def progress_bar():
    my_bar = st.progress(0)
    for percent_complete in range(100):
        time.sleep(0.1)
        my_bar.progress(percent_complete + 1, text=get_progress_text())


# Streamlit Application to build twitter data scraper.
# Set page title & title
st.set_page_config(page_title="Twitter Data Scraper", page_icon=":bird:")
st.title("Twitter Data Scraper")

# Get user input
input1 = st.selectbox("How you would like to scrape the data", ["Keyword", "Hashtag", "User", "Profile"])
choice = st.text_input(f"Please enter a {input1}")
start_date = st.date_input("Select start date", datetime.now() - timedelta(days=7))
end_date = st.date_input("Select end date", datetime.now())
tweet_c = st.slider("How many tweets you would like to scrape", 0, 1000, 5)

# Define main content
if choice:

    # Display search query and scrape button
    st.write(f"Scraping tweets for '{choice}' from {start_date} to {end_date}")
    if st.button("Scrape"):
        # Call scrape_tweets function and display results
        st.write(f"Scraped {len(tweets_df)} tweets")
        st.write(tweets_df)
        progress_bar()
else:
    st.warning("Please enter a search query")

# Input query by user & scrape data
if choice:
    if input1 == 'Keyword':
        for i, tweet in enumerate(sntwitter.TwitterSearchScraper(f'{input1} + '
                                                                 f'since:{start_date} until:{end_date}').get_items()):
            if i >= tweet_c:
                break
            tweets_list.append([tweet.id, tweet.date, tweet.rawContent, tweet.lang, tweet.user.username,
                                tweet.replyCount, tweet.retweetCount, tweet.likeCount, tweet.hashtags,
                                tweet.sourceUrl, tweet.url, tweet.media])

        tweets_df = pd.DataFrame(tweets_list,
                                 columns=['ID', 'Date', 'Content', 'Language', 'Username', 'ReplyCount', 'RetweetCount',
                                          'LikeCount', 'hashtags', 'Source', 'Url', 'Media'])
    elif input1 == 'Hashtag':
        for i, tweet in enumerate(sntwitter.TwitterHashtagScraper(f'{input1} '
                                                                  f'since:{start_date} until:{end_date}').get_items()):
            if i >= tweet_c:
                break
            tweets_list.append([tweet.id, tweet.date, tweet.rawContent, tweet.lang, tweet.user.username,
                                tweet.replyCount, tweet.retweetCount, tweet.likeCount, tweet.hashtags,
                                tweet.sourceUrl, tweet.url, tweet.media])
        tweets_df = pd.DataFrame(tweets_list,
                                 columns=['ID', 'Date', 'Content', 'Language', 'Username', 'ReplyCount', 'RetweetCount',
                                          'LikeCount', 'hashtags', 'Source', 'Url', 'Media'])
    elif input1 == 'User':
        for i, tweet in enumerate(sntwitter.TwitterUserScraper(f'{input1} '
                                                               f'since:{start_date} until:{end_date}').get_items()):
            if i >= tweet_c:
                break
            tweets_list.append([tweet.id, tweet.date, tweet.rawContent, tweet.lang, tweet.user.username,
                                tweet.replyCount, tweet.retweetCount, tweet.likeCount, tweet.hashtags,
                                tweet.sourceUrl, tweet.url, tweet.media])
        tweets_df = pd.DataFrame(tweets_list,
                                 columns=['ID', 'Date', 'Content', 'Language', 'Username', 'ReplyCount', 'RetweetCount',
                                          'LikeCount', 'hashtags', 'Source', 'Url', 'Media'])
    else:
        for i, tweet in enumerate(sntwitter.TwitterProfileScraper(f'{input1} '
                                                                  f'since:{start_date} until:{end_date}').get_items()):
            if i >= tweet_c:
                break
            tweets_list.append([tweet.id, tweet.date, tweet.rawContent, tweet.lang, tweet.user.username,
                                tweet.replyCount, tweet.retweetCount, tweet.likeCount, tweet.hashtags,
                                tweet.sourceUrl, tweet.url, tweet.media])
        tweets_df = pd.DataFrame(tweets_list,
                                 columns=['ID', 'Date', 'Content', 'Language', 'Username', 'ReplyCount', 'RetweetCount',
                                          'LikeCount', 'hashtags', 'Source', 'Url', 'Media'])
else:
    st.warning("⚠ " + input1 + " can't be empty")
    e = RuntimeError('This is an exception of type RuntimeError')
    st.exception(e)


# DOWNLOAD AS CSV
@st.cache  # IMPORTANT: Cache the conversion to prevent computation on every rerun
def convert_df(df):
    return df.to_csv().encode('utf-8')


if not tweets_df.empty:
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        csv = convert_df(tweets_df)  # CSV
        c = st.download_button(label="Download data as CSV", data=csv, file_name='Twitter_data.csv', mime='text/csv', )
    with col2:  # JSON
        json_string = tweets_df.to_json(orient='records')
        j = st.download_button(label="Download data as JSON", file_name="Twitter_data.json", mime="application/json",
                               data=json_string, )

    with col3:  # SHOW
        y = st.button('Show Filtered Tweets', key=2)

    with col4:
        z = st.button('Upload Tweets to Database', key=3)

if c:
    st.success("The Scraped Data is Downloaded as .CSV file:", icon="✅")
    st.snow()
if j:
    st.success("The Scraped Data is Downloaded as .JSON file", icon="✅")
    st.snow()

if y:  # DISPLAY

    st.success("Tweets Scraped Successfully:", icon="✅")
    st.snow()
    st.write(tweets_df)

if z:  # upload to DB
    # UPLOAD DATA TO DATABASE
    coll = choice
    coll = coll.replace(' ', '_') + '_Tweets'
    mycoll = db[coll]
    dict1 = tweets_df.to_dict('records')
    if dict1:
        mycoll.insert_many(dict1)
        ts = time.time()
        mycoll.update_many({}, {"$set": {"KeyWord_or_Hashtag_or_User_or_Profile": choice + str(ts)}},
                           upsert=False, array_filters=None)
        st.success('Successfully uploaded to database', icon="✅")
        st.snow()
    else:
        st.warning('Cant upload because there are no tweets', icon="⚠️")
        e = RuntimeError('This is an exception of type RuntimeError')
        st.exception(e)
