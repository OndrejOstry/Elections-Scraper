"""
projekt_3.py: třetí projekt do Engeto Online Python Akademie
author: Ondřej Ostrý
email: ondrejostry@gmail.com
discord: ondrejostry
"""

import sys
import requests
from bs4 import BeautifulSoup
import pandas as pd

# FUKNCE PRO STAŽENÍ STRÁNKY
def load_page(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return BeautifulSoup(response.content, "html.parser")
    except requests.exceptions.RequestException as e:
        print(f"Chyba při stahování stránky: {e}")
        sys.exit(1)

# FUNKCE PRO ZISKÁNÍ ODKAZŮ JEDNOTLIVÝCH OBCÍ
def obec_links(soup):
    links = []
    for row in soup.select("tr"): 
        name_cell = row.select_one("td.overflow_name")
        link_cell = row.select_one("td.cislo a")
        if name_cell and link_cell:
            obec_name = name_cell.text.strip()
            obec_url = "https://volby.cz/pls/ps2017nss/" + link_cell["href"]
            obec_code = link_cell.text.strip()
            links.append((obec_name, obec_code, obec_url))
    return links

# FUKCE PRO ZÍSKÁNÍ DETAILŮ OBCE
def obec_details(obec_name, obec_code, obec_url):
    obec_soup = load_page(obec_url)
    try:
        registered = obec_soup.find("td", headers="sa2").text.strip()
        envelopes = obec_soup.find("td", headers="sa3").text.strip()
        valid = obec_soup.find("td", headers="sa6").text.strip()
    except AttributeError as e:
        print(f"Chyba při zpracování dat obce: {e}")
        return None

    obec_data = {
        "code": obec_code,
        "location": obec_name,
        "registered": registered,
        "envelopes": envelopes,
        "valid": valid,
    }

    return obec_data, obec_soup

# FUKCE PRO ZPRACOVÁNÍ HLASŮ
def process_votes(obec_data, obec_soup):
    parties_name = [row.text.strip() for row in obec_soup.find_all("td", headers=["t1sa1 t1sb2", "t2sa1 t2sb2"])]
    parties_votes = [row.text.strip() for row in obec_soup.find_all("td", headers=["t1sa2 t1sb3", "t2sa2 t2sb3"])]

    for party_name, party_vote in zip(parties_name, parties_votes):
        obec_data[party_name] = party_vote

    return obec_data

# FUKCE PRO ULOŽENÍ DAT DO SOUBORU
def save_to_csv(data, filename):
    df = pd.DataFrame(data)
    df.to_csv(filename, index=False)

# MAIN FUNKCE 
def main():
    try:
        url = sys.argv[1]
        output_file = sys.argv[2]
    except IndexError:
        print("Nebyla zadána URL adresa nebo název výstupního souboru")
        sys.exit(1)

    soup = load_page(url)
    obce = []
    for obec_name, obec_code, obec_url in obec_links(soup):
        obec_data, obec_soup = obec_details(obec_name, obec_code, obec_url)
        if obec_data:
            final_data = process_votes(obec_data, obec_soup)
            obce.append(final_data)

    save_to_csv(obce, output_file)
    print(f"Data uložena do {output_file}")

if __name__ == "__main__":
    main()