import pandas as pd
import requests
import re
from bs4 import BeautifulSoup

sec_website = "https://www.sec.gov"


def fetch_web_content(url):
    """
    Fetches content from a given URL with custom headers.
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Win64; like Gecko) Chrome/97.0.4692.99 Safari/537.36",
        "Accept-Encoding": "gzip, deflate, br",
        "HOST": "www.sec.gov",
    }
    return requests.get(url, headers=headers)


def construct_edgar_url(cik):
    """
    Constructs a URL to query EDGAR for a given CIK number.
    """
    return f"https://www.sec.gov/cgi-bin/browse-edgar?CIK={cik}&owner=exclude&action=getcompany&type=13F-HR"


def prompt_cik_input():
    """
    Prompts the user to enter a 10-digit CIK number.
    """
    return input("Kindly enter a 10-digit CIK number, please: ")


def harvest_company_data(target_cik):
    """
    Harvests the last two reports of a company from EDGAR based on CIK.
    """
    response = fetch_web_content(construct_edgar_url(target_cik))
    soup = BeautifulSoup(response.text, "html.parser")
    report_links = soup.findAll("a", id="documentsbutton")

    latest_report = sec_website + report_links[0]["href"]
    preceding_report = sec_website + report_links[1]["href"]
    extract_report_data(latest_report, "latest_report")
    extract_report_data(preceding_report, "preceding_report")


def extract_report_data(url, file_label):
    """
    Extracts and converts report data from XML to CSV.
    """
    response = fetch_web_content(url)
    soup = BeautifulSoup(response.text, "html.parser")
    xml_links = soup.findAll("a", attrs={"href": re.compile("xml")})
    xml_report_url = xml_links[3].get("href")

    xml_response = fetch_web_content(sec_website + xml_report_url)
    convert_xml_to_csv(BeautifulSoup(xml_response.content, "lxml"), file_label)


def convert_xml_to_csv(xml_soup, filename):
    """
    Converts XML data into a CSV file.
    """
    column_headers = [
        "Name of Issuer",
        "CUSIP",
        "Value (x$1000)",
        "Shares",
        "Investment Discretion",
        "Voting Sole / Shared / None",
    ]

    data = {
        "Name of Issuer": xml_soup.body.findAll(re.compile("nameofissuer")),
        "CUSIP": xml_soup.body.findAll(re.compile("cusip")),
        "Value (x$1000)": xml_soup.body.findAll(re.compile("value")),
        "Shares": [
            (amt.text + " " + amt_type.text)
            for amt, amt_type in zip(
                xml_soup.body.findAll("sshprnamt"),
                xml_soup.body.findAll(re.compile("sshprnamttype")),
            )
        ],
        "Investment Discretion": xml_soup.body.findAll(
            re.compile("investmentdiscretion")
        ),
        "Voting Sole / Shared / None": [
            f"{sole.text} / {shared.text} / {none.text}"
            for sole, shared, none in zip(
                xml_soup.body.findAll(re.compile("sole")),
                xml_soup.body.findAll(re.compile("shared")),
                xml_soup.body.findAll(re.compile("none")),
            )
        ],
    }

    df = pd.DataFrame(data)
    df.to_csv(f"{filename}.csv", index=False)


if __name__ == "__main__":
    user_cik = prompt_cik_input()
    harvest_company_data(user_cik)
