import requests
from bs4 import BeautifulSoup
import re
import csv

def scrape_game_highlight_links():
    # Set URL
    news_url = 'https://www.arizonacoyotes.com/news'

    # GET and parse the HTML
    try:
        response = requests.get(news_url)
        response.raise_for_status()  # Check for HTTP errors
        soup = BeautifulSoup(response.text, 'html.parser')
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while fetching the webpage: {e}")
        return

    # Currently take all news articles
    news_articles = soup.find_all('a', class_='news__headline')

    # Search for YouTube game highlight links in the articles
    game_highlight_links = []
    for article in news_articles:
        article_url = article['href']
        try:
            article_response = requests.get(article_url)
            article_response.raise_for_status()
            article_soup = BeautifulSoup(article_response.text, 'html.parser')
        except requests.exceptions.RequestException as e:
            print(f"An error occurred while fetching an article: {e}")
            continue

        # Search for YouTube links in the article content
        article_content = article_soup.find('div', class_='content')
        if article_content:
            youtube_links = re.findall(r'(https://www.youtube.com/watch\?v=[\w-]+)', str(article_content))
            game_highlight_links.extend(youtube_links)

    if game_highlight_links:
        # Save the links to a CSV file
        with open("coyotes_links.csv", "w", newline="") as cn_links:
            writer = csv.writer(cn_links)
            for link in game_highlight_links:
                writer.writerow([link])

        print(f"{len(game_highlight_links)} game highlight links saved to coyotes_links.csv")
    else:
        print("No game highlight links found.")

if __name__ == "__main__":
    scrape_game_highlight_links()
