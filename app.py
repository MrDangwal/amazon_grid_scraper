import streamlit as st
import requests
import pandas as pd
from bs4 import BeautifulSoup

def scrape_amazon_search(search_url, num_pages):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    product_data = []

    for page in range(1, num_pages + 1):
        url = search_url + '&page=' + str(page)
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')

        products = soup.find_all('div', {'data-component-type': 's-search-result'})

        for product in products:
            product_link = 'https://www.amazon.in' + product.find('a', {'class': 'a-link-normal s-no-outline'})['href']
            product_name = product.find('span', {'class': 'a-text-normal'}).text.strip()

            # Check if review count is available
            review_count_element = product.find('span', {'class': 'a-size-base s-underline-text'})
            review_count = review_count_element.text.strip() if review_count_element else 'N/A'

            # Check if product rating is available
            rating_element = product.select_one('span[aria-label*="out of 5 stars"]')
            rating = rating_element['aria-label'].split()[0] if rating_element else 'N/A'

            product_data.append([product_name, product_link, review_count, rating])

    return product_data

def main():
    st.title("Amazon Scraper with Streamlit UI")

    search_url = st.text_input("Enter Amazon Search URL:")
    num_pages = st.number_input("Enter the number of pages to scrape:", min_value=1, value=10, step=1)

    if st.button("Scrape and Download"):
        if search_url:
            product_data = scrape_amazon_search(search_url, num_pages)

            df = pd.DataFrame(product_data, columns=['Product Name', 'Product Link', 'Review Count', 'Rating'])
            filename = f"{num_pages} RE_Re_Rating_amazon_products.csv"
            df.to_csv(filename, index=False)

            st.success(f'Scraping complete. Data saved to {filename}')
            st.markdown(f'Download your file [here](sandbox:/path/to/{filename})')
        else:
            st.warning("Please enter a valid Amazon search URL.")

if __name__ == '__main__':
    main()
