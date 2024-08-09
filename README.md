# Elections-Scraper
Tento projekt je součástí Engeto Python Akademie. Je to python skript, který stahuje volební výsledky z webové stránky a následně je ukládá do CSV souboru.

Autor:
Jméno: Ondřej Ostrý
Email: ondrejostry@gmail.com
Discord: ondrejostry

Requirements:
K provozování tohoto projektu potřebujete nainstalovat potřebné python knihovny. Tyto knihovny nainstalujete pomocí souboru "requirements.txt"

Instalace:
Naklonování repositáře
git clone https://github.com/OndrejOstry/Elections-Scraper.git
cd Elections-Scraper

Vytvoření virtualního prostředí
MacOS:
python3 -m venv .venv
source .venv/bin/activate

Windows:
python -m venv .venv
source .venv/bin/activate

Instalace knihoven:
pip install -r requirements.txt



Skript spustíte pomocí následujícího příkazu v příkazovém řádku odkazující do složky kde je skript uložený:
MacOS:
python3 main.py "URL" "output_file.csv"

Windows:
python main.py "URL" "output_file.csv"

