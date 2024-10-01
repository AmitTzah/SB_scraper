import requests
from bs4 import BeautifulSoup
import csv
import time

def fetch_fictions(base_url, params):
    fictions = []
    page = 1
    
    while True:
        print(f"\nFetching page {page}...")
        url = f"{base_url}/page-{page}?{params}"
        print(f"URL: {url}")
        
        response = requests.get(url)
        if response.status_code != 200:
            print(f"Failed to fetch page {page}. Status code: {response.status_code}")
            break
        
        soup = BeautifulSoup(response.content, 'html.parser')
        threads = soup.find_all('div', class_='structItem--thread')
        
        print(f"Found {len(threads)} thread divs on page {page}")
        
        if not threads:
            print(f"No threads found on page {page}. Ending search.")
            break
        
        for i, thread in enumerate(threads, 1):
            print(f"\nProcessing thread {i} on page {page}")
            
            title_element = thread.find('a', attrs={'data-xf-init': 'preview-tooltip'})
            
            if title_element:
                title = title_element.text.strip()
                print(f"Found title: {title}")
            else:
                print("Couldn't find title for this thread.")
                continue
            
            stats = thread.find('div', class_='structItem-cell--meta')
            if stats:
                print("Found stats div")
                
                # Fetch replies
                replies_dl = stats.find('dl', class_='pairs--justified')
                replies = replies_dl.find('dd').text.strip() if replies_dl else "N/A"
                print(f"Replies: {replies}")
                
                # Fetch views (corrected)
                views_dl = stats.find_all('dl', class_='pairs--justified')[-1]
                views = views_dl.find('dd').text.strip() if views_dl.find('dd') else "N/A"
                print(f"Views: {views}")
                
                # Fetch likes
                likes = stats.get('title', '').split(': ')[-1] if stats.get('title') else "N/A"
                print(f"Likes: {likes}")

                # Fetch tags
                tags = []
                tag_elements = thread.find_all('a', class_='tagItem')
                for tag in tag_elements:
                    tags.append(tag.text.strip())
                print(f"Tags: {', '.join(tags)}")
                
            else:
                print("Couldn't find stats div")
                replies = "N/A"
                views = "N/A"
                likes = "N/A"
            
            fictions.append({
                'title': title,
                'replies': replies,
                'views': views,
                'likes': likes,
                'tags': tags
            })
        print(f"\nProcessed {len(threads)} threads on page {page}")
        page += 1
        time.sleep(2)  # Be nice to the server
    
    return fictions

def save_to_csv(fictions, filename='spacebattles_fictions.csv'):
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['title', 'replies', 'views', 'likes']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for fiction in fictions:
            writer.writerow(fiction)

if __name__ == "__main__":
    base_url = "https://forums.spacebattles.com/forums/original-fiction.48"
    params = "order=view_count&direction=desc&min_word_count=3000&max_word_count=7000"
    fictions = fetch_fictions(base_url, params)
    save_to_csv(fictions)
    print(f"\nScraped {len(fictions)} fictions and saved to spacebattles_fictions.csv")