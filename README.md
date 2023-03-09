# WikimediaScrap 
This is a Python script that can be used to scrape images from Wikimedia Commons using a keyword. It was created for educational purposes and can be used as a starting point for building similar scraping projects.

The script accepts several command-line arguments, including the keyword to search for, the maximum number of pages to search, and the maximum number of images to retrieve per page. Additionally, it supports using a list of proxies or a reverse proxy to evade rate limiting.


### Required Arguments

| Argument Name | Description |
|---------------|-------------|
| --keyword      | Keyword to scrap images from Wikimedia Commons |
| --maxoffset    | Maximum pages to search for images |
| --batchSize    | Maximum images to search for page |

### Optional Arguments

| Argument Name | Description |
|---------------|-------------|
| --proxies_file | Proxy file to use for scraping images and evade rate limiting. |
| --reverse_proxy | Reverse proxy to change ip per requests so an entire file of proxies wont be required. |


