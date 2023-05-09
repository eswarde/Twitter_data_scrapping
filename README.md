**Twitter_data_scrapping**
This is a simple web application built with Streamlit and Python that allows you to scrape Twitter data using various search criteria, such as keywords, hashtags, users, and profiles. The app uses the snscrape library to access the Twitter API and retrieve tweets matching your search query.

Requirements
To run this application, you need to have the following software installed:
Python 3
pip package manager
MongoDB
You will also need to create a Twitter Developer account and obtain API keys, tokens, and secrets. Please refer to the Twitter Developer documentation for more information.

Installation
Clone the repository to your local machine:
git clone https://github.com/eswargc/twitter_data_scrapping.git

Change into the project directory:
cd twitter-data-scraper

Install the required Python packages:
pip install -r requirements.txt

Create a .env file in the root directory of the project and add your Twitter API credentials:
TWITTER_API_KEY=<your_api_key>
TWITTER_API_SECRET=<your_api_secret>
TWITTER_ACCESS_TOKEN=<your_access_token>
TWITTER_ACCESS_TOKEN_SECRET=<your_access_token_secret>

Start a MongoDB server on your local machine (e.g., by running mongod in a terminal window).

**Usage**
To start the application, run the following command in your terminal:
streamlit run Twitter_data_scraping.py
This will launch the app in your default web browser. You can then enter your search query, select your search criteria, and set your date range and tweet limit. When you click the "Scrape" button, the app will retrieve the tweets matching your query and display them in a table.

You can also store the scraped data in a MongoDB database by uncommenting the code that connects to the database and inserts the tweets into a collection. You will need to have a running MongoDB server and create a database and a collection before you can store the data.

**Credits**
This application was created by Vadiveeswaran. The code is based on the snscrape library and the Streamlit framework.

