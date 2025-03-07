# import pandas as  pd
# import requests
# import re
# from bs4 import BeautifulSoup


# url = input('Enter the URL seperated by comma: ').strip().split(',')

# data = []

# for urls in url:
#     urls = urls.strip()
#     headers = {
#     'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
#     'sec-ch-ua' : 'Chromium";v="134", "Not:A-Brand";v="24", "Google Chrome";v="134"',
#     'sec-ch-ua-mobile':'?0',
#     'sec-ch-ua-platform':'"Windows"'}
#     try:
#         response = requests.get(urls, headers= headers)
#         print(f'Fetching emails from: {url}')
#         soup = BeautifulSoup(response.text,'html.parser')
#         text_content = soup.get_text()
#         email_pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
#         emails = re.findall(email_pattern, text_content)
#         email = list(set(emails))
#         for emai in email:
#             data.append({"URL": urls, 'Email':emai})
#     except:
#         print('Request Denied Try again')


# if data:
#     df = pd.DataFrame(data)
#     df.to_excel("scraped_emails.xlsx", index=False)
#     print("Emails saved in 'scraped_emails'")
# else:
#     print("No emails found on the given URLs.")


import streamlit as st
import pandas as pd
import requests
import re
from bs4 import BeautifulSoup
from streamlit_autorefresh import st_autorefresh

# App title
st.title("Email Scraper")

# Auto-refresh to prevent app from becoming inactive
st_autorefresh(interval=14 * 60 * 1000, key="refresh")

# Function to fetch emails
@st.cache_data
def fetch_emails(url_list):
    data = []
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
        'sec-ch-ua': 'Chromium";v="134", "Not:A-Brand";v="24", "Google Chrome";v="134"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"'
    }
    for url in url_list:
        url = url.strip()
        try:
            response = requests.get(url, headers=headers)
            soup = BeautifulSoup(response.text, 'html.parser')
            text_content = soup.get_text()
            email_pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
            emails = list(set(re.findall(email_pattern, text_content)))
            for email in emails:
                data.append({"URL": url, "Email": email})
        except:
            st.warning(f"Request Denied for {url}. Try again.")
    return pd.DataFrame(data) if data else None

# Input field
urls = st.text_area("Enter URLs (comma-separated):")

if st.button("Scrape Emails"):
    if urls:
        url_list = urls.split(',')
        df = fetch_emails(url_list)
        if df is not None:
            st.write("### Scraped Emails")
            st.dataframe(df)

            # Download button
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button("Download CSV", csv, "scraped_emails.csv", "text/csv", key="download-csv")
        else:
            st.error("No emails found on the given URLs.")
    else:
        st.warning("Please enter at least one URL.")
