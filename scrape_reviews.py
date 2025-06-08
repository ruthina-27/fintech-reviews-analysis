from google_play_scraper import app, reviews, Sort
import pandas as pd
import sys
import traceback

apps = {
    "CBE": "com.combanketh.mobilebanking",
    "Bank of Abyssinia": "com.boa.boaMobileBanking",
    "Dashen Bank": "com.dashen.dashensuperapp"
}

def scrape_reviews(app_id, bank_name, count=400):
    try:
        print(f"Scraping reviews for {bank_name} (App ID: {app_id})")
        reviews_data, _ = reviews(
            app_id,
            lang='en',        # Language
            country='et',     # Ethiopia
            sort=Sort.NEWEST, # Use Sort enum instead of integer
            count=count       # Number of reviews
        )
        
        if not reviews_data:
            print(f"No reviews found for {bank_name}")
            return pd.DataFrame()
        
        df = pd.DataFrame(reviews_data)
        print(f"Scraped {len(df)} reviews for {bank_name}")
        
        # Flexible column mapping
        column_mapping = {
            'content': 'content',
            'score': 'score',
            'at': 'date'
        }
        
        # Rename columns to match expected format
        df = df.rename(columns={k: v for k, v in column_mapping.items() if k in df.columns})
        
        # Ensure all expected columns exist
        for col in ['content', 'score', 'date']:
            if col not in df.columns:
                df[col] = None
        
        df['bank'] = bank_name
        return df[['content', 'score', 'date', 'bank']]
    
    except Exception as e:
        print(f"Error scraping reviews for {bank_name}: {e}")
        print(traceback.format_exc())
        return pd.DataFrame()

# Scrape all banks
try:
    all_reviews = pd.concat([scrape_reviews(app_id, name) for name, app_id in apps.items()])
    
    if len(all_reviews) > 0:
        # Save to CSV
        all_reviews.to_csv('bank_reviews.csv', index=False)
        print(f"Scraped and saved {len(all_reviews)} total reviews to 'bank_reviews.csv'")
    else:
        print("No reviews were scraped. Please check the app IDs and network connection.")
        sys.exit(1)

except Exception as e:
    print(f"An error occurred during scraping: {e}")
    print(traceback.format_exc())
    sys.exit(1) 