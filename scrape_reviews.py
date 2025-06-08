from google_play_scraper import app, reviews, Sort
import pandas as pd

apps = {
    "CBE": "com.combanketh.mobilebanking",
    "Bank of Abyssinia": "com.boa.boaMobileBanking",
    "Dashen Bank": "com.dashen.dashensuperapp"
}

def scrape_reviews(app_id, bank_name, count=400):
    reviews_data, _ = reviews(
        app_id,
        lang='en',        # Language
        country='et',     # Ethiopia
        sort=Sort.NEWEST, # Use Sort enum instead of integer
        count=count       # Number of reviews
    )
    df = pd.DataFrame(reviews_data)
    df['bank'] = bank_name
    return df[['content', 'score', 'at', 'bank']]

# Scrape all banks
all_reviews = pd.concat([scrape_reviews(app_id, name) for name, app_id in apps.items()])

# Save to CSV
all_reviews.to_csv('bank_reviews.csv', index=False)
print("Scraped and saved reviews to 'bank_reviews.csv'")