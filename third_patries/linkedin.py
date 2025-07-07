import os
import requests
from dotenv import load_dotenv

load_dotenv()


def scrape_linkedin_profile(linkedin_profile_url: str, mock: bool = False):
    """Scrape information from LinkedIn profiles,
    Manually scrape information from LinkedIn profile"""

    if mock:
        linkedin_profile_url = "https://gist.githubusercontent.com/K-u-r-c/145869099986ff96eede9cf4f2a2e8dd/raw/fbd567b5241223915f66a5828b4a638ea0e9f847/gistfile1.txt"
        response = requests.get(linkedin_profile_url, timeout=10)
    else:
        api_endpoint = "https://api.scrapin.io/v1/enrichment/profile"
        params = {
            "apikey": os.environ["SCRAPIN_API_KEY"],
            "linkedInUrl": linkedin_profile_url,
        }
        response = requests.get(api_endpoint, params=params, timeout=10)

    data = response.json().get("person")
    data = {
        k: v
        for k, v in data.items()
        if v not in ([], "", None) and k not in ["certifications"]
    }

    return data


if __name__ == "__main__":
    print(
        scrape_linkedin_profile(
            linkedin_profile_url="https://www.linkedin.com/in/jakub-kurc-3565ab287/",
            mock=True,
        )
    )
