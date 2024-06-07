import requests
from bs4 import BeautifulSoup

def scrape_gewobag():
    items = []
    request_url = 'https://www.gewobag.de/fuer-mieter-und-mietinteressenten/mietangebote/?bezirke%5B%5D=friedrichshain-kreuzberg&bezirke%5B%5D=friedrichshain-kreuzberg-friedrichshain&bezirke%5B%5D=friedrichshain-kreuzberg-kreuzberg&bezirke%5B%5D=mitte&bezirke%5B%5D=mitte-gesundbrunnen&bezirke%5B%5D=mitte-wedding&bezirke%5B%5D=neukoelln&bezirke%5B%5D=pankow-prenzlauer-berg&bezirke%5B%5D=tempelhof-schoeneberg-schoeneberg&nutzungsarten%5B%5D=wohnung&gesamtmiete_von=&gesamtmiete_bis=700&gesamtflaeche_von=50&gesamtflaeche_bis=&zimmer_von=2&zimmer_bis=&keinwbs=1&sort-by=recent'
    response = requests.get(request_url, verify=False)
    parser = BeautifulSoup(response.content, 'html.parser')
    content = parser.find(class_='filtered-mietangebote')
    if content:
        items_website = content.find_all(class_='angebot-content')
        for item in items_website:
            address = item.find('address').get_text().strip() if item.find('address') else None
            area = item.find(class_='angebot-area').find('td').get_text().strip() if item.find(class_='angebot-area') else None
            rent = item.find(class_='angebot-kosten').find('td').get_text().strip() if item.find(class_='angebot-kosten') else None
            if address:
                items.append(f"{address} ({area}, {rent})")
    return items

if __name__ == "__main__":
    print(', '.join(scrape_gewobag()))