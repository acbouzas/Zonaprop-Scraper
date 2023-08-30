from playwright.sync_api import sync_playwright
from playwright_stealth import stealth_sync
from ipdb import set_trace
from bs4 import BeautifulSoup
import pandas as pd
from tqdm import tqdm


def parse_item(div):
    
    href = div.find('div', attrs={'data-qa': 'posting PROPERTY'}).get("data-to-posting")    
    
    # Extracting price
    price = div.find('div', attrs={'data-qa': 'POSTING_CARD_PRICE'}).text
    price = price.split('USD ')[1]

    # Extracting location
    location = div.find('div', attrs={'data-qa': 'POSTING_CARD_LOCATION'}).text

    # Extracting features
    features_element = div.find('div', attrs={'data-qa': 'POSTING_CARD_FEATURES'})
    features = [x.text for x in features_element.find_all('span') if x.find("img")]
    
    item = {
        "href": href,
        "price": price,
        "location": location,
    }
    
    for i,feature in enumerate(features):
        item[i] = feature

    return item


def extract_data(soup):
    # Find the first div with class="postings-container"
    container_div = soup.find('div', class_='postings-container')

    # Find all divs within the container div
    # divs = container_div.find_all('div')
    
    # List to store the extracted data
    results = []    
    # Iterate over the divs and extract the relevant information
    for i,div in enumerate(container_div.contents):
        try:
            if div:
                item = parse_item(div)
                # print(item)
                results.append(item)
        except Exception as e:
            print(e)
            pass
    
    return pd.DataFrame(results)


page_links = [f'https://www.zonaprop.com.ar/casas-venta-capital-federal-pagina-{i}.html' for i in range(2, 309)]
page_links.append('https://www.zonaprop.com.ar/casas-venta-capital-federal.html')

with sync_playwright() as p:
#    for browser_type in [p.chromium, p.firefox]:
    browser = p.chromium.launch(headless=False)
    context = browser.new_context(
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36",
    )
    page = context.new_page()
    # stealth_sync(page)
    
    headers = {
        'authority': 'www.zonaprop.com.ar',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8,es;q=0.7,pt;q=0.6',
        'cache-control': 'max-age=0',
        'cookie': 'g_state={"i_l":0}; usuarioLogeado=m4rbel@gmail.com; usuarioFormNombre=Martin; usuarioFormEmail=m4rbel%40gmail.com; usuarioFormTelefono=; usuarioFormId=48770308; usuarioFormNombre=Martin; usuarioFormApellido=Bel; usuarioFormEmail=m4rbel@gmail.com; usuarioFormId=48770308; usuarioSeeker=true; sessionId=083712bd-8eda-442a-8546-a62aa9237c6b; idUltimoAvisoVisto=49539678; hashKey=4Ypb4i178NeNGjgDajK21GdpUaoYpMO63cS5qt3U2c7zAfyJxpOUsaJrcQqDwYJORGYcG6pBna3NhUoRii3m3CTWhGZixpY4Z0rN; JSESSIONID=A50B2F92BC5B848D2EFACA377D5586DA; __cf_bm=qcFZHp0EUwu610zs_j6AMcxfqJM6pqUUBigUm_cdRXA-1686337911-0-AZC1IOeOc3y18KJthOkS0kQ0UTWSVpaQXgYiixDrWjArCdE0nFvoT7LRbHN4gIXNwDPXKRrZWR4zymzzCTcP5xqXnbUc9O/47nv3isZD1CaS',
        'sec-ch-ua': '"Google Chrome";v="113", "Chromium";v="113", "Not-A.Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Linux"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'none',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36'
    }

    page.set_extra_http_headers(headers)
    
    #timeout_ms = 100
    #page.set_default_timeout(timeout_ms)
    
    data = []
    for page_link in tqdm(page_links):
        print(page_link)
        try:
            page.goto(page_link)
        except:
            page.goto(page_link)
            pass

        # get HTML
        html = page.content()
        soup = BeautifulSoup(html, 'lxml')
    
        # parse content
        df_page = extract_data(soup)
        data.append(df_page)
        
    # set_trace()
        
    df = pd.concat(data)
    df.to_csv("results/scraped.csv", index=False)
    
    browser.close()
        

