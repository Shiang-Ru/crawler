from flask import Flask, render_template, request
from bs4 import BeautifulSoup
import requests

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', movies=[])

@app.route('/scrape', methods=['POST'])
def scrape():
    base_url = 'https://ssr1.scrape.center/page/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36'
    }
    
    movies = []

    # Loop through pages 1 to 10
    for page in range(1, 11):
        url = f"{base_url}{page}"
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        # Parse HTML content for each page
        soup = BeautifulSoup(response.text, 'lxml')

        # Extract movie data
        for item in soup.find_all('div', class_='el-card'):
            title = item.find('h2', class_='m-b-sm').text.strip() if item.find('h2', class_='m-b-sm') else 'N/A'
            categories = ', '.join([cat.text.strip() for cat in item.find_all('button', class_='category')])
            region_duration = item.find_all('div', class_='info')[0].text.strip() if item.find_all('div', class_='info') else 'N/A'
            release_date = item.find_all('div', class_='info')[1].text.strip() if len(item.find_all('div', class_='info')) > 1 else 'N/A'
            rating = item.find('p', class_='score').text.strip() if item.find('p', class_='score') else 'N/A'
            image_url = item.find('img', class_='cover')['src'] if item.find('img', class_='cover') else ''

            # Split region and duration
            region, duration = region_duration.split(' / ') if ' / ' in region_duration else (region_duration, 'N/A')

            movies.append({
                'title': title,
                'categories': categories,
                'region': region,
                'duration': duration,
                'release_date': release_date,
                'rating': rating,
                'image_url': image_url
            })

    # Render the data in index.html
    return render_template('index.html', movies=movies)

if __name__ == '__main__':
    app.run(debug=True)
