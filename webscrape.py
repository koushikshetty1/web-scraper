import requests
from bs4 import BeautifulSoup
import csv
from typing import List, Dict
import logging
from datetime import datetime
import time

class InvestingNewsFetcher:
    def __init__(self):
        self.rss_url = "https://www.investing.com/rss/news_25.rss"

        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)

    def parse_date(self, date_str: str) -> str:
        """
        Parse date string with fallback options
        """
        try:
            return datetime.strptime(date_str, "%a, %d %b %Y %H:%M:%S %z").strftime("%Y-%m-%d %H:%M:%S")
        except:
            try:
                return datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%d %H:%M:%S")
            except:
                self.logger.warning(f"Could not parse date: {date_str}")
                return date_str

    def fetch_news(self) -> List[Dict]:
        """
        Fetch news articles from the RSS feed using BeautifulSoup
        """
        self.logger.info("Fetching news from RSS feed")
        articles = []

        try:
            response = requests.get(self.rss_url)
            if response.status_code != 200:
                self.logger.error(f"Error fetching RSS feed: Status {response.status_code}")
                return articles

            soup = BeautifulSoup(response.content, 'xml')

            items = soup.find_all('item')
            self.logger.info(f"Found {len(items)} entries in feed")

            for entry in items:
                try:
                    title = entry.find('title').text if entry.find('title') else 'No title'
                    link = entry.find('link').text if entry.find('link') else ''
                    pub_date = entry.find('pubDate').text if entry.find('pubDate') else ''
                    summary = entry.find('description').text if entry.find('description') else 'No summary available'
                    author = entry.find('dc:creator').text if entry.find('dc:creator') else 'Not specified'
                    categories = [category.text for category in entry.find_all('category')]

                    article = {
                        "title": title,
                        "url": link,
                        "date": self.parse_date(pub_date),
                        "summary": summary,
                        "author": author,
                        "categories": categories
                    }

                    articles.append(article)

                except Exception as e:
                    self.logger.error(f"Error processing entry: {str(e)}")
                    continue

            self.logger.info(f"Successfully processed {len(articles)} articles")

        except Exception as e:
            self.logger.error(f"Error processing RSS feed: {str(e)}")

        return articles

    def save_to_json(self, articles: List[Dict], filename: str = 'investing_news.json'):
        """
        Save fetched data to JSON file
        """
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(articles, f, indent=4, ensure_ascii=False)
            self.logger.info(f"Successfully saved data to {filename}")
        except Exception as e:
            self.logger.error(f"Error saving to JSON: {str(e)}")

    def save_to_csv(self, articles: List[Dict], filename: str = 'investing_news.csv'):
        """
        Save fetched data to CSV file
        """
        try:
            if not articles:
                return

            fields = articles[0].keys()
            with open(filename, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=fields)
                writer.writeheader()
                writer.writerows(articles)
            self.logger.info(f"Successfully saved data to {filename}")
        except Exception as e:
            self.logger.error(f"Error saving to CSV: {str(e)}")

def main():
    fetcher = InvestingNewsFetcher()

    # Add retry logic
    max_retries = 3
    for attempt in range(max_retries):
        try:
            articles = fetcher.fetch_news()
            if articles:
                break
            time.sleep(2 ** attempt)  # Exponential backoff
        except Exception as e:
            if attempt == max_retries - 1:
                fetcher.logger.error(f"Failed after {max_retries} attempts")
                articles = []
            else:
                fetcher.logger.warning(f"Attempt {attempt + 1} failed, retrying...")
                time.sleep(2 ** attempt)

    fetcher.save_to_csv(articles)

if __name__ == "__main__":  # Corrected line
    main()

import pandas as pd
df = pd.read_csv('investing_news.csv')
print(df)
