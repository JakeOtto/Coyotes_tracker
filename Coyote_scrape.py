import requests
from bs4 import BeautifulSoup
import re
import csv

# want to help or improve, please us readme for scope and intentions. 

# set url
news_url = 'https://www.arizonacoyotes.com/news'

# GET and parse the HTML
response = requests.get(news_url)
soup = BeautifulSoup(response.text, 'html.parser')

# currently take all news articles
news_articles = soup.find_all('a', class_='news__headline')

# Step 4: Search for YouTube game highlight links in the articles
game_highlight_links = []
for article in news_articles:
    article_url = article['href']
    article_response = requests.get(article_url)
    article_soup = BeautifulSoup(article_response.text, 'html.parser')
    
    # Search for YouTube links in the article content
    article_content = article_soup.find('div', class_='content')
    if article_content:
        youtube_links = re.findall(r'(https://www.youtube.com/watch\?v=[\w-]+)', str(article_content))
        game_highlight_links.extend(youtube_links)

# post the links to the csv file - can change this to wherever
if game_highlight_links:

    
    # i could have done this as - writer.writerows(game_highlight_links) -

    # opening the file
    with open("coyotes_links.csv", "w", newline="") as cn_links:
        for link in game_highlight_links:
            # creating the writer
            writer = csv.writer(cn_links)
            # using writerow to write individual record one by one
            writer.writerow([link])
        # close the writer and file 
        cn_links.close()

else:
    print("No game highlight links found.")

