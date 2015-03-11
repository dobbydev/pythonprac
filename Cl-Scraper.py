import requests
from bs4 import BeautifulSoup
import sys
import pprint
import csv

def fetch_search_results(query=None, minAsk=None, maxAsk=None, bedrooms=None):
    search_params = { key: val for key, val in locals().items() if val is not None    }
    if not search_params:
        raise ValueError("No valid keywords")

    base = 'http://seattle.craigslist.org/search/apa'
    resp = requests.get(base, params=search_params, timeout=3)
    resp.raise_for_status()  # <- no-op if status==200
    return resp.content, resp.encoding
    
def parse_source(html, encoding='utf-8'):
    parsed = BeautifulSoup(html, from_encoding=encoding)
    return parsed
    
def extract_listings(parsed):
    location_attrs = {'data-latitude': True, 'data-longitude': True}
    listings = parsed.find_all('p', class_='row')
    extracted = []
    for listing in listings:
        location = {key: listing.attrs.get(key, '') for key in location_attrs}
        link = listing.find('span', class_='pl').find('a')
        price_span = listing.find('span', class_='price')   # add me
        this_listing = {
            'location': location,
            'link': link.attrs['href'],
            'description': link.string.strip(),
            'price': price_span.string.strip(),             # and me
            'size': price_span.next_sibling.strip(' \n-/')  # me too
        }
        #extracted.append(this_listing)
        extracted.append({
             'link': link.attrs['href'],
             'price': price_span.string.strip(),             # and me
             'description': link.string.strip(),
            'location': location,
            'size': price_span.next_sibling.strip(' \n-/')  # me too
        })
    return extracted
    
def write_results(results,econd):
    """Writes list of dictionaries to file."""
    fields = results[0].keys()
    print(fields)
    with open('results.csv', 'w',encoding ='utf-8') as f:
        dw = csv.DictWriter(f, fieldnames=fields, delimiter=',')
        print(dw.fieldnames)
        dw.writeheader()
        #dw.writer.writerow(dw.fieldnames)
        dw.writerows(results)
        
if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'test':
        html, encoding = fetch_search_results()
    else:
        html, encoding = fetch_search_results(
            minAsk=500, maxAsk=1000, bedrooms=2
        )
    doc = parse_source(html, encoding)
    listings = extract_listings(doc) # add this line
    write_results(listings,'utf-8')
    print (len(listings) )             # and this one
    pprint.pprint(listings[0])   