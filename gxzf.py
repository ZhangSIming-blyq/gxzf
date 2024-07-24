import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

base_url = ''

def fetch_page(url, retries=3, backoff_factor=0.3):
    for i in range(retries):
        try:
            print(f'Fetching page: {url}')
            response = requests.get(url, timeout=60)
            response.encoding = 'utf-8'
            return response.content
        except (requests.exceptions.ChunkedEncodingError, requests.exceptions.ConnectionError) as e:
            print(f'Error fetching page {url}: {e}')
            if i < retries - 1:
                sleep_time = backoff_factor * (2 ** i)
                print(f'Retrying in {sleep_time} seconds...')
                time.sleep(sleep_time)
            else:
                print(f'Failed to fetch page {url} after {retries} attempts.')
    return None

def parse_html(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    return soup

def extract_titles(soup, base_path):
    titles = []
    items = soup.find_all('a', href=True)
    for item in items:
        title = item.get_text().strip()
        href = item['href']
        if title and href and href.startswith('./t'):
            if not href.startswith('http'):
                href = base_url.format(base_path + href[1:])
            titles.append((title, href))
    return titles

def get_total_pages(soup):
    pagination_script = soup.find('script', string=lambda x: x and 'createPageHTML' in x)
    if pagination_script:
        pagination_text = pagination_script.get_text()
        total_pages = int(pagination_text.split(',')[0].split('(')[-1])
        return total_pages
    print("No pagination information found.")
    return 1

def scrape_all_pages(base_path, socketio):
    page_url = base_url.format(base_path)
    html_content = fetch_page(page_url)
    soup = parse_html(html_content)
    total_pages = get_total_pages(soup)

    print("Total pages:", total_pages)

    all_titles = []
    for page_num in range(total_pages):
        if page_num == 0:
            page_url = base_url.format(base_path)
        else:
            page_url = base_url.format(f'{base_path}/index_{page_num}.shtml')
        html_content = fetch_page(page_url)
        soup = parse_html(html_content)
        titles = extract_titles(soup, base_path)
        all_titles.extend(titles)

        progress = int((page_num + 1) / total_pages * 100)
        socketio.emit('progress', {'progress': progress})
        socketio.emit('log', {'message': f'Scraping page {page_num + 1}/{total_pages} for section {base_path}'})

    return all_titles

def run(url, socketio):
    global base_url
    base_url = url
    html_content = fetch_page(base_url.format('/'))
    soup = parse_html(html_content)

    sections = soup.select('div.gov-leader ul.more-child-list li a')
    section_links = [(section.get_text().strip(), section['href']) for section in sections if section['href'].startswith('./')]
    section_links = list(set(section_links))
    print(section_links)

    all_data = []
    for i, (section_title, section_href) in enumerate(section_links):
        section_path = section_href.split('/')[-2]
        socketio.emit('log', {'message': f'Fetching section: {section_title}'})
        titles = scrape_all_pages(f'/{section_path}', socketio)
        all_data.append({
            'section': section_title,
            'titles': titles
        })

        progress = int((i + 1) / len(section_links) * 100)
        socketio.emit('progress', {'progress': progress})
        socketio.emit('log', {'message': f'Completed section: {section_title}'})

    with pd.ExcelWriter('gxzf.xlsx') as writer:
        for data in all_data:
            df = pd.DataFrame(data['titles'], columns=['Title', 'URL'])
            df.to_excel(writer, sheet_name=data['section'], index=False)

    socketio.emit('log', {'message': 'Excel file generated successfully.'})
    socketio.emit('task_complete', {'data': 'Task completed'})
