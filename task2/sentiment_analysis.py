import pandas as pd
from textblob import TextBlob

# Load cleaned data
df = pd.read_csv('cleaned_reviews.csv')

# Use TextBlob for sentiment analysis
def get_sentiment_textblob(text):
    if not isinstance(text, str):
        return "NEUTRAL", 0.0
    analysis = TextBlob(text)
    polarity = analysis.sentiment.polarity
    if polarity > 0.1:
        return "POSITIVE", polarity
    elif polarity < -0.1:
        return "NEGATIVE", polarity
    else:
        return "NEUTRAL", polarity

# Apply sentiment analysis
df[['sentiment_label', 'sentiment_score']] = df['review'].apply(
    lambda x: pd.Series(get_sentiment_textblob(x))
)

# Save results
df.to_csv('task2/reviews_with_sentiment.csv', index=False)
print("Sentiment analysis complete using TextBlob. Saved to 'task2/reviews_with_sentiment.csv'")