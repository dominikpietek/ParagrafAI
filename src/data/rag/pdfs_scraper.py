import requests
from bs4 import BeautifulSoup
import time

HEADERS = {"User-Agent": "Paragram llm projekt edukacyjny"}
DELAY_SECONDS = 1.5
WEB_URL = "https://isap.sejm.gov.pl/isap.nsf/ByYear.xsp"

def fetch_html(url: str) -> str:
    try:
        response = requests.get(url, headers=HEADERS, timeout=120)
        response.raise_for_status()
    except:
        raise Exception("Response exception")
    return response.text

def find_pdf_links():
    html = fetch_html(WEB_URL)
    soup = BeautifulSoup(html, "html.parser")
    print(html)
    u_list = soup.find("ul", class_="categories")
    print(u_list)
    for a in u_list.find_all("a", href=True):
        sub_web = fetch_html(WEB_URL + a["href"])
        u_list_law = sub_web.find("ul", class_="categories")
        time.sleep(DELAY_SECONDS)
        for a_law in u_list_law.find_all("a", href=True):
            sub_sub_web = fetch_html(WEB_URL + a["href"] + a_law["href"])
            u_list_law_positions = sub_sub_web.find("div", id_="view:_id1:_id2:_id59:_id61:callback1:_id93:deedsList")
            time.sleep(DELAY_SECONDS)
            for a_positions in u_list_law_positions.find_all("a", href=True):
                final_sub_web = fetch_html(WEB_URL + a["href"] + a_law["href"] + a_positions["href"])
                final_u_list = final_sub_web.find("a", class_="icon-after doc-link")
                yield final_u_list[0]

for pdf in find_pdf_links():
    print(pdf)

# https://isap.sejm.gov.pl/isap.nsf/ByYear.xsp -> ul categories -> ul categories -> tbody -> td a href -> a pdf