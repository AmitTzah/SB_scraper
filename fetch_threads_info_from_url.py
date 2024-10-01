import requests
from bs4 import BeautifulSoup
import csv
import time

def fetch_watcher_count(thread_url):
    try:
        response = requests.get(thread_url)
        if response.status_code != 200:
            print(f"Failed to fetch thread page: {thread_url}")
            return "N/A"
        
        soup = BeautifulSoup(response.content, 'html.parser')
        header_content = soup.find('div', class_='threadmarkListingHeader-stats')
        watcher_count = "N/A"
        
        if header_content:
            pairs = header_content.find_all('dl', class_='pairs pairs--rows')
            for pair in pairs:
                if pair.find('dt') and 'watchers' in pair.find('dt').text.lower():
                    watcher_count = pair.find('dd').text.strip()
                    break

        return watcher_count
    except Exception as e:
        print(f"Error fetching watcher count for {thread_url}: {e}")
        return "N/A"

def fetch_fictions(base_url, params):
    fictions = []
    page = 1

    while True:
        print(f"\nFetching page {page}...")
        
        if page == 1:
            url = f"{base_url}/?{params}"
        else:
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
                thread_url = title_element['href']
                if not thread_url.startswith('http'):
                    thread_url = f"https://forums.spacebattles.com{thread_url}"
                print(f"Found title: {title}")
                print(f"Thread URL: {thread_url}")
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
                
                # Fetch views
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

                # Fetch watcher count from the individual thread page
                watcher_count = fetch_watcher_count(thread_url)
                print(f"Watcher Count: {watcher_count}")

                # Be nice to the server
                time.sleep(2)
                
            else:
                print("Couldn't find stats div")
                replies = "N/A"
                views = "N/A"
                likes = "N/A"
                watcher_count = "N/A"
            
            fictions.append({
                'title': title,
                'replies': replies,
                'views': views,
                'likes': likes,
                'tags': tags,
                'watchers': watcher_count
            })
        
        print(f"\nProcessed {len(threads)} threads on page {page}")

        # Check if there is a "next" link to go to the next page
        next_page_link = soup.find('link', rel='next')
        if next_page_link:
            page += 1
        else:
            print("No 'next' link found. Reached the last page.")
            break
        
        time.sleep(2)  # Be nice to the server

    return fictions

def save_to_csv(fictions, filename='spacebattles_fictions.csv'):
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['title', 'replies', 'views', 'likes', 'tags', 'watchers']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for fiction in fictions:
            writer.writerow(fiction)

if __name__ == "__main__":
    base_url = "https://forums.spacebattles.com/forums/original-fiction.48"
    params = "min_word_count=3000&max_word_count=7000"
    fictions = fetch_fictions(base_url, params)
    save_to_csv(fictions)
    print(f"\nScraped {len(fictions)} fictions and saved to spacebattles_fictions.csv")
