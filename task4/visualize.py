import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os
from task4.analysis import get_top_words
from wordcloud import WordCloud
from textblob import TextBlob
import numpy as np
from collections import Counter
import re

def plot_average_ratings(df, output_folder='task4'):
    """
    Plots the average rating for each bank.
    """
    avg_ratings = df.groupby('bank')['rating'].mean().sort_values(ascending=False)
    
    plt.figure(figsize=(10, 6))
    sns.barplot(x=avg_ratings.index, y=avg_ratings.values, palette='viridis')
    plt.title('Average Bank Ratings')
    plt.xlabel('Bank')
    plt.ylabel('Average Rating')
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    output_path = os.path.join(output_folder, 'average_ratings.png')
    plt.savefig(output_path)
    print(f"Saved average ratings plot to {output_path}")
    plt.close()

def plot_top_words(df, bank_name, sentiment, output_folder='task4'):
    """
    Plots the top words for a given bank and sentiment.
    """
    if sentiment == 'positive':
        reviews = df[(df['bank'] == bank_name) & (df['rating'] >= 4)]['review']
        title = f'Top Positive Keywords for {bank_name}'
        color = 'Greens_d'
    else:
        reviews = df[(df['bank'] == bank_name) & (df['rating'] <= 2)]['review']
        title = f'Top Negative Keywords for {bank_name}'
        color = 'Reds_d'
        
    top_words = get_top_words(reviews)
    words, counts = zip(*top_words)
    
    plt.figure(figsize=(10, 6))
    sns.barplot(x=list(words), y=list(counts), palette=color)
    plt.title(title)
    plt.xlabel('Keywords')
    plt.ylabel('Frequency')
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    output_filename = f"{bank_name.replace(' ', '_').lower()}_{sentiment}_keywords.png"
    output_path = os.path.join(output_folder, output_filename)
    plt.savefig(output_path)
    print(f"Saved top words plot to {output_path}")
    plt.close()

def create_visualizations(input_file='cleaned_reviews.csv'):
    """
    Creates and saves all visualizations.
    """
    df = pd.read_csv(input_file)
    
    # Convert date to datetime
    df['date'] = pd.to_datetime(df['date'])

    # 1. Sentiment Analysis and Trends
    def get_sentiment(text):
        try:
            return TextBlob(str(text)).sentiment.polarity
        except:
            return 0

    df['sentiment'] = df['review'].apply(get_sentiment)

    # Plot 1: Sentiment Trends Over Time
    plt.figure(figsize=(12, 6))
    sentiment_trend = df.groupby('date')['sentiment'].mean().rolling(window=7).mean()
    plt.plot(sentiment_trend.index, sentiment_trend.values)
    plt.title('Sentiment Trends Over Time (7-day Rolling Average)')
    plt.xlabel('Date')
    plt.ylabel('Average Sentiment Score')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('sentiment_trends.png')
    plt.close()

    # 2. Rating Distribution by Bank
    plt.figure(figsize=(10, 6))
    sns.countplot(data=df, x='rating', hue='bank')
    plt.title('Rating Distribution by Bank')
    plt.xlabel('Rating')
    plt.ylabel('Count')
    plt.legend(title='Bank')
    plt.tight_layout()
    plt.savefig('rating_distribution.png')
    plt.close()

    # 3. Word Cloud for Positive Reviews
    positive_reviews = ' '.join(df[df['rating'] >= 4]['review'].astype(str))
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(positive_reviews)
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.title('Word Cloud of Positive Reviews (Rating >= 4)')
    plt.tight_layout()
    plt.savefig('positive_wordcloud.png')
    plt.close()

    # 4. Word Cloud for Negative Reviews
    negative_reviews = ' '.join(df[df['rating'] <= 2]['review'].astype(str))
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(negative_reviews)
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.title('Word Cloud of Negative Reviews (Rating <= 2)')
    plt.tight_layout()
    plt.savefig('negative_wordcloud.png')
    plt.close()

    # 5. Average Rating by Bank
    plt.figure(figsize=(8, 6))
    bank_ratings = df.groupby('bank')['rating'].mean().sort_values(ascending=False)
    sns.barplot(x=bank_ratings.index, y=bank_ratings.values)
    plt.title('Average Rating by Bank')
    plt.xlabel('Bank')
    plt.ylabel('Average Rating')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('bank_ratings.png')
    plt.close()

    print("Visualizations have been generated successfully!")

if __name__ == '__main__':
    create_visualizations() 