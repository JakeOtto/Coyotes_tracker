import requests
from bs4 import BeautifulSoup
import re

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

# Step 5: Post the links to a location of your choice
if game_highlight_links:
    # You can print the links or save them to a file, database, etc.
    for link in game_highlight_links:
        print(link)
else:
    print("No game highlight links found.")

