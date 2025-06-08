# Fintech App Reviews Analysis

This project analyzes user reviews for three major Ethiopian banking apps from the Google Play Store. The goal is to understand customer satisfaction, identify key issues, and compare the performance of different banks based on user feedback.

## Methodology

### 1. Data Collection
- Reviews for **CBE**, **Bank of Abyssinia**, and **Dashen Bank** were scraped from the Google Play Store using the `google-play-scraper` library.
- Over 1,200 reviews were collected in total.

### 2. Preprocessing
- The collected data was cleaned to remove duplicate reviews.
- Dates were normalized to a `YYYY-MM-DD` format.
- A `source` column was added to indicate the origin of the data.

### 3. Sentiment and Thematic Analysis
- **Sentiment Analysis**: User sentiment (positive, negative, neutral) was determined for each review using the `TextBlob` library.
- **Thematic Analysis**: Key themes and topics were extracted from the reviews using TF-IDF and NLTK. These themes help categorize feedback into areas like "UI/UX", "Transactions", and "Login Issues".

## Requirements
- Python 3.8+
- Libraries: pandas, google-play-scraper, textblob, nltk, scikit-learn

## How to Run
1. Install dependencies: `pip install -r requirements.txt`
2. Run data scraping: `python scrape_reviews.py`
3. Preprocess data: `python preprocess.py`
4. Perform sentiment analysis: `python task2/sentiment_analysis.py`
5. Perform thematic analysis: `python task2/thematic_analysis.py`