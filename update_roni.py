import requests
from bs4 import BeautifulSoup
import csv

def scrape_roni_data():
    url = "https://www.cpc.ncep.noaa.gov/products/analysis_monitoring/enso/roni/"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    tables = soup.find_all('table')

    all_data = []
    month_mapping = ['DJF', 'JFM', 'FMA', 'MAM', 'AMJ', 'MJJ', 'JJA', 'JAS', 'ASO', 'SON', 'OND', 'NDJ']

    for table in tables:
        headers = [th.get_text(strip=True) for th in table.find_all('th')]
        if 'Year' not in headers:
            continue

        rows = table.find_all('tr')[1:]
        for row in rows:
            cols = row.find_all('td')
            if len(cols) == 13:
                year_str = cols[0].get_text(strip=True)
                try:
                    year = int(year_str)
                    if year < 1950 or year > 2026:
                        continue
                except ValueError:
                    continue

                for i, value_td in enumerate(cols[1:]):
                    month_index = i + 1
                    value_text = value_td.get_text(strip=True)
                    if value_text and value_text != '-':
                        try:
                            value_float = float(value_text)
                            type_str = 'Neutral'
                            if value_float >= 0.5:
                                type_str = 'El Niño'
                            elif value_float <= -0.5:
                                type_str = 'La Niña'

                            date_str = f"{year}-{month_index:02d}"
                            all_data.append([date_str, value_float, type_str])
                        except ValueError:
                            pass
            
    all_data.sort(key=lambda x: x[0])
    return all_data

def save_data_to_csv(data):
    csv_filename = 'roni_data.csv'
    with open(csv_filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['date', 'roni', 'type'])
        writer.writerows(data)

if __name__ == "__main__":
    roni_data = scrape_roni_data()
    if roni_data:
        save_data_to_csv(roni_data)
