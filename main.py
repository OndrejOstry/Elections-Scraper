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

#STÁHNE A ZPRACUJE VÝSLEDKY HLASOVÁNÍ   
def voting_results(url):
#OŠETŘENÍ PŘI CHYBĚ STAHOVÁNÍ STRÁNKY    
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Chyba při stahování stránky: {e}")

    soup = BeautifulSoup(response.content, "html.parser")

    obce = []
    #PROJDE HTML SOUBOR A NAJDE JMÉNA A URL ADRESY
    for row in soup.select("tr"): 
        name_cell = row.select_one("td.overflow_name")
        link_cell = row.select_one("td.cislo a")
        #POKUD NAŠEL JMNÉNA ULOŽÍ DO PROMĚNNÉ, TO STEJNÉ URL OBCE A KÓD OBCE
        if name_cell and link_cell:
            obec_name = name_cell.text.strip()
            obec_url = "https://volby.cz/pls/ps2017nss/" + link_cell["href"]
            obec_code = link_cell.text.strip()

            obec_response = requests.get(obec_url)
            obec_soup = BeautifulSoup(obec_response.content, "html.parser")
            #NAJDE V HTML POČET VALIDNÍCH HLASU A OBÁLEK
            try:
                registered = obec_soup.find("td", headers="sa2").text.strip()
                envelopes = obec_soup.find("td", headers="sa3").text.strip()
                valid = obec_soup.find("td", headers="sa6").text.strip()
            except AttributeError as e:
                print(f"Chyba při zpracování dat obce: {e}")
            #ULOŽÍ DATA DO SLOVNÍKU
            obec_data = {
                "code": obec_code,
                "location" : obec_name,
                "registered" : registered,
                "envelopes" : envelopes,
                "valid" : valid,
            }

            parties_name = [row.text.strip() for row in obec_soup.find_all("td", headers=["t1sa1 t1sb2", "t2sa1 t2sb2"])]
            parties_votes = [row.text.strip() for row in obec_soup.find_all("td", headers=["t1sa2 t1sb3", "t2sa2 t2sb3"])]
            #DATA Z VOLEB SE ULOŽÍ DO SLOVNIKU DAT OBCE
            for party_name, party_vote in zip(parties_name, parties_votes):
                obec_data[party_name] = party_vote

            obce.append(obec_data)

    return obce

#ULOŽÍ DATA DO SOUBORU
def save_to_csv(data, filename):
    df = pd.DataFrame(data)
    df.to_csv(filename, index=False)

def main():
    try:
        url = sys.argv[1]
        output_file = sys.argv[2]
    except IndexError:
        print("Nebyla zadána URL adresa nebo název výstupního souboru")
        sys.exit(1)
    
    try:
        data = voting_results(url)
        save_to_csv(data, output_file)
        print(f"Data uložena do {output_file}")
    
    except Exception as e:
        print(f"Nastala chyba: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
