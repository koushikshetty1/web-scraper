# web-scraper
Investing News Fetcher
A Python-based application to fetch and save the latest financial news from Investing.com using their RSS feed. This tool extracts, processes, and stores the news data in JSON and CSV formats for further analysis or use.

Features
RSS Feed Parsing: Fetches the latest financial news articles from the Investing.com RSS feed.
Data Storage: Saves the fetched data in both JSON and CSV formats.
Error Handling: Implements robust error handling with retry logic and logging for better reliability.
Data Parsing: Cleans and formats the news articles, including titles, summaries, publication dates, authors, and categories.
Exponential Backoff: Handles connection errors with retry logic to ensure data fetching reliability.

Usage
Run the script:

bash
Copy code
python investing_news_fetcher.py
View the output:

CSV: investing_news.csv
JSON: investing_news.json
Analyze the data: Use tools like pandas to analyze the news data:

python
Copy code
import pandas as pd
df = pd.read_csv('investing_news.csv')
print(df.head())
Example Output
CSV File
Title	URL	Date	Summary	Author	Categories
Example News Title	https://example.com/news1	2024-12-23 12:34:56	News summary goes here	John Doe	[Category1]
JSON File
json
Copy code
[
    {
        "title": "Example News Title",
        "url": "https://example.com/news1",
        "date": "2024-12-23 12:34:56",
        "summary": "News summary goes here",
        "author": "John Doe",
        "categories": ["Category1"]
    }
]
Logging
The script logs its progress and errors to the console, including:

Fetching status
Parsing errors
Retry attempts
Requirements
Python 3.7+
Packages:
requests
beautifulsoup4
pandas
logging
Install all dependencies using:

bash
Copy code
pip install -r requirements.txt
Future Enhancements
Add more RSS feed sources for broader news coverage.
Support for saving data into a database.
Advanced data visualization using libraries like matplotlib or seaborn.
Contributing
Contributions are welcome! Please fork this repository, make your changes, and open a pull request.

License
This project is licensed under the MIT License. See the LICENSE file for details.

Acknowledgments
Investing.com for providing the RSS feed.
Python libraries like requests, BeautifulSoup, and pandas for enabling this functionality.
Feel free to customize this content further to suit your preferences or repository needs!
