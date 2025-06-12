import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from collections import Counter
import re

# Download nltk data if not already downloaded
try:
    stopwords.words('english')
except LookupError:
    nltk.download('stopwords')
    nltk.download('punkt')

def get_top_words(reviews, n=10):
    """
    Get the most common words from a series of reviews.
    """
    # Combine all reviews into a single string
    all_reviews = ' '.join(reviews.astype(str))
    # Remove non-alphabetic characters and convert to lowercase
    all_reviews = re.sub('[^a-zA-Z]', ' ', all_reviews).lower()
    
    # Tokenize the text
    words = word_tokenize(all_reviews)
    
    # Remove stopwords
    stop_words = set(stopwords.words('english'))
    filtered_words = [word for word in words if word not in stop_words and len(word) > 2]
    
    # Get the most common words
    word_counts = Counter(filtered_words)
    return word_counts.most_common(n)

def analyze_reviews(input_file='cleaned_reviews.csv', output_file='task4/analysis_summary.txt'):
    """
    Analyzes bank reviews to identify drivers and pain points.
    """
    df = pd.read_csv(input_file)

    # Get unique bank names
    banks = df['bank'].unique()
    
    analysis_summary = ""

    for bank in banks:
        analysis_summary += f"--- Analysis for {bank} ---\n"
        bank_df = df[df['bank'] == bank]

        # Overall sentiment
        avg_rating = bank_df['rating'].mean()
        analysis_summary += f"Average Rating: {avg_rating:.2f}\n"

        # Separate reviews by sentiment based on rating
        positive_reviews = bank_df[bank_df['rating'] >= 4]['review']
        negative_reviews = bank_df[bank_df['rating'] <= 2]['review']

        # Get top words for positive reviews (drivers)
        top_positive_words = get_top_words(positive_reviews)
        analysis_summary += "Top Drivers (Positive Keywords):\n"
        for word, count in top_positive_words:
            analysis_summary += f"- {word}: {count}\n"

        # Get top words for negative reviews (pain points)
        top_negative_words = get_top_words(negative_reviews)
        analysis_summary += "\nTop Pain Points (Negative Keywords):\n"
        for word, count in top_negative_words:
            analysis_summary += f"- {word}: {count}\n"
        
        analysis_summary += "\n\n"

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(analysis_summary)
    
    print(f"Analysis summary saved to {output_file}")

if __name__ == '__main__':
    analyze_reviews() 