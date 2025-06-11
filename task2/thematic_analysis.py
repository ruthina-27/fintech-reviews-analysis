import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize

# One-time downloads for nltk
try:
    stopwords.words('english')
except LookupError:
    nltk.download('stopwords')
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')
try:
    nltk.data.find('corpora/wordnet')
except LookupError:
    nltk.download('wordnet')
try:
    nltk.data.find('tokenizers/punkt_tab')
except LookupError:
    nltk.download('punkt_tab')


# Load data with sentiments
df = pd.read_csv('task2/reviews_with_sentiment.csv')

# Preprocess text: lemmatization + remove stopwords
lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words('english'))

def preprocess(text):
    if not isinstance(text, str):
        return ""
    # tokenization
    tokens = word_tokenize(text.lower())
    # remove punctuation and non-alpha
    tokens = [word for word in tokens if word.isalpha()]
    # remove stopwords and lemmatize
    tokens = [lemmatizer.lemmatize(word) for word in tokens if word not in stop_words]
    return " ".join(tokens)


df['processed_text'] = df['review'].apply(preprocess)

# TF-IDF to extract keywords
tfidf = TfidfVectorizer(max_features=50)  # Top 50 keywords
tfidf_matrix = tfidf.fit_transform(df['processed_text'])
keywords = tfidf.get_feature_names_out()

# Manually group keywords into themes
themes = {
    "UI/UX": ["app", "interface", "design", "slow", "lag", "update", "dark", "mode"],
    "Transactions": ["transfer", "payment", "failed", "transaction", "money", "send", "receive"],
    "Login & Access": ["login", "password", "account", "error", "open", "register", "access", "fingerprint"],
    "Customer Support": ["support", "customer", "service", "help", "issue", "problem"],
    "Features": ["feature", "add", "option", "statement", "limit"]
}

# Assign themes to reviews
def assign_theme(text):
    # use processed_text for matching
    for theme, keywords_list in themes.items():
        if any(keyword in text.split() for keyword in keywords_list):
            return theme
    return "Other"

df['theme'] = df['processed_text'].apply(assign_theme)

# --- New: Get top 2 themes per bank ---
print("\nTop 2 Themes per Bank:")
top_themes = df.groupby('bank')['theme'].apply(lambda x: x.value_counts().nlargest(2).index.tolist())

# Create a DataFrame for the top themes and save to CSV
top_themes_df = top_themes.reset_index()
top_themes_df.columns = ['bank', 'top_themes']
top_themes_df.to_csv('task2/top_themes_per_bank.csv', index=False)

# Print the results in a readable format
for bank, themes_list in top_themes.items():
    print(f"- {bank}: {', '.join(themes_list)}")

# Save final output with individual themes
df.to_csv('task2/reviews_with_themes.csv', index=False)
print("\nThematic analysis complete. Saved to 'task2/reviews_with_themes.csv' and 'task2/top_themes_per_bank.csv'")