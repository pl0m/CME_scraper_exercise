from scraper_futures_quotes import *
from scraper_futures_settlements import *

def main():
    scrape_futures_quotes()
    scrape_futures_settlements()
    time.sleep(10)
    
if __name__ == '__main__':
    main()