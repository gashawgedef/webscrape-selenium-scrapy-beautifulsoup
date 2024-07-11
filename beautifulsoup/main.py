import os
import requests
from bs4 import BeautifulSoup

# Root URL
root = "https://subslikescript.com"
website = f'{root}/movies_letter-A'

# Headers to include a User-Agent
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
}

# Fetch the initial page to get pagination details
res = requests.get(website, headers=headers)
content = res.text
soup = BeautifulSoup(content, "lxml")

pagination = soup.find('ul', class_='pagination')
pages = pagination.find_all('li', class_='page-item')
last_page = int(pages[-2].text)
# Iterate through each page
for page in range(1, last_page + 1)[:2]:
    paginated_url = f'{website}?page={page}'
    res = requests.get(paginated_url, headers=headers)
    content = res.text
    soup = BeautifulSoup(content, "lxml")
    box = soup.find("article", class_="main-article")
    a_elements = box.find_all('a', href=True)
    links = [link['href'] for link in a_elements]
    for link in links: 
        try:
            res = requests.get(f'{root}{link}', headers=headers)
            content = res.text
            soup = BeautifulSoup(content, "lxml")
            box = soup.find("article", class_="main-article")
            title = box.find('h1').get_text(strip=True)
            transcript = box.find('div', class_='full-script').get_text(strip=True, separator=' ')
            
            # Ensure the title is valid for a filename
            valid_title = "".join([c if c.isalnum() else "_" for c in title])
            
            with open(f'{valid_title}.txt', "w", encoding="utf-8") as file:
                file.write(transcript)
                
        except Exception as e:
            print(f"Failed to process link {link}: {e}")
