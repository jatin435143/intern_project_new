import requests
from bs4 import BeautifulSoup

# Target URL (Ball-by-Ball Commentary)
url = "https://www.espncricinfo.com/series/tn-premier-league-2016-1047323/chepauk-super-gillies-vs-albert-tuti-patriots-1st-match-1047343/ball-by-ball-commentary"

# Mimic a real browser
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
}

# Send GET request
response = requests.get(url, headers=headers)

# Check if request was successful
if response.status_code == 200:
    soup = BeautifulSoup(response.text, "html.parser")

    # Find the div with the specified class
    commentary_div = soup.find("div", class_="ds-w-full ds-bg-fill-content-prime ds-overflow-hidden ds-rounded-xl ds-mb-4 ds-border-y lg:ds-border ds-border-line")

    # Extract and print text
    if commentary_div:
        print(commentary_div.get_text(strip=True))
    else:
        print("No commentary found.")

else:
    print(f"Failed to retrieve data. Status Code: {response.status_code}")
