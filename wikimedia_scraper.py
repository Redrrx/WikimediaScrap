import asyncio
import logging
import random
import traceback
from datetime import datetime
from faker import Faker
import requests
import os
from tenacity import retry, stop_after_attempt
import functools
import argparse
import uuid
from termcolor import colored


if not os.path.exists("logs"):
    os.makedirs("logs")

if not os.path.isfile('proxies.txt'):
    with open('proxies.txt', "w") as f:
        pass

logging.basicConfig(filename=os.path.join("logs", datetime.now().strftime("%Y-%m-%d_%H-%M-%S.log")),level=logging.DEBUG)
faker = Faker()


@retry(stop=stop_after_attempt(10))
async def download_image(url, headers, keyword):
    req = functools.partial(requests.get, headers=headers)
    response = await asyncio.get_event_loop().run_in_executor(None, req, url)
    if response.status_code == 200:
        with open(os.path.join(os.getcwd(), f"images/{keyword}", f'{str(uuid.uuid4())}.jpg'), 'wb') as f:
            f.write(response.content)
            print(colored(f'[!] Successfully downloaded and saved {url}', 'green'))
    else:

        print(colored(f'[!] Failed to download image with url {url}, returned response code {response.status_code}',
                      'red'))
        logging.error(f"Failed to download image with url {url}, returned response code {response.status_code} "
                      f"{response.context} "
                      f"{response.headers}")


@retry(stop=stop_after_attempt(10))
async def bake_request(session, url, headers, params):
    try:
        async with session.get(url, params=params, headers=headers) as response:
            return response.json()
    except Exception as e:
        print(colored(f'[!] Failed to fetch {url} due to {e}', 'red'))
        logging.error(f"Error occurred: {e}")
        logging.error(traceback.format_exc())


async def main(keyword, max_offset, batch_size, proxy, proxies_file):
    headers = {
        'authority': 'commons.wikimedia.org',
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'accept-language': 'en-US,en;q=0.9',
        'referer': f'https://commons.wikimedia.org/w/index.php?search={keyword}&title=Special:MediaSearch&go=Go&type=image',
        'sec-ch-ua': '"(Not(A:Brand";v="8", "Chromium";v="101"',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': faker.user_agent(),
        'x-requested-with': 'XMLHttpRequest',
    }
    urls = []
    async with requests.Session() as session:
        if isinstance(proxy, str):
            session.proxies = {"http": proxy, "https": proxy}
        else:
            with open(proxies_file, "r") as f:
                proxies = f.readlines()
            random_proxy = random.choice(proxies).strip()
            session.proxies = {"http": random_proxy, "https": random_proxy}

        tasks = []
        for offset in range(1, max_offset + 1, batch_size):
            params = {
                'action': 'query',
                'format': 'json',
                'uselang': 'en',
                'generator': 'search',
                'gsrsearch': f'filetype:bitmap|drawing -fileres:0 {keyword}',
                'gsrlimit': batch_size,
                'gsrinfo': 'totalhits|suggestion',
                'gsrprop': 'size|wordcount|timestamp|snippet',
                'prop': 'info|imageinfo|entityterms',
                'inprop': 'url',
                'gsrnamespace': '6',
                'iiprop': 'url|size|mime',
                'iiurlheight': '180',
                'wbetterms': 'label',
                'gsroffset': offset
            }
            task = asyncio.create_task(
                bake_request(session, 'https://commons.wikimedia.org/w/api.php', headers, params))
            tasks.append(task)

    for response in asyncio.as_completed(tasks):
        result = await response

        for page_id in result['query']['pages']:
            image_url = result['query']['pages'][page_id]['imageinfo'][0]['url']
            urls.append(image_url)

    download_tasks = []

    for url in urls:
        task = asyncio.create_task(download_image(url))
        download_tasks.append(task)
    await asyncio.gather(*download_tasks)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--keyword', type=str, required=True, help='Keyword to scrap images from Wikimedia Commons')
    parser.add_argument('--maxoffset', type=int, required=True, help='Maximum pages to search for images ')
    parser.add_argument('--batchSize', type=int, required=True, help='Maximum images to search for page')
    parser.add_argument('--proxies_file', type=str, required=False,help='Proxy file to use for scraping images and evade rate limiting')
    parser.add_argument('--reverse_proxy', type=str, required=False,help='Reverse proxy to use for scraping images and evade rate limiting')
    args = parser.parse_args()
    asyncio.run(main(keyword=args.keyword, max_offset=args.maxoffset, batch_size=args.batchSize, proxy=args.reverse_proxy, proxies_file=args.proxies_file))
