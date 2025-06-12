import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
import os
from collections import Counter
import numpy as np

def plot_sentiment_trends(df, output_folder='task4'):
    """
    Plot sentiment trends over time for each bank.
    """
    # Convert date to datetime
    df['date'] = pd.to_datetime(df['date'])
    
    # Calculate monthly average ratings
    monthly_ratings = df.groupby(['bank', pd.Grouper(key='date', freq='M')])['rating'].mean().reset_index()
    
    plt.figure(figsize=(12, 6))
    for bank in df['bank'].unique():
        bank_data = monthly_ratings[monthly_ratings['bank'] == bank]
        plt.plot(bank_data['date'], bank_data['rating'], label=bank, marker='o')
    
    plt.title('Monthly Average Ratings Trend')
    plt.xlabel('Date')
    plt.ylabel('Average Rating')
    plt.legend()
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    output_path = os.path.join(output_folder, 'sentiment_trends.png')
    plt.savefig(output_path)
    plt.close()

def create_word_cloud(text, title, output_path):
    """
    Create a word cloud from text.
    """
    wordcloud = WordCloud(width=800, height=400,
                         background_color='white',
                         max_words=100,
                         contour_width=3,
                         contour_color='steelblue').generate(text)
    
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.title(title)
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()

def plot_rating_boxplots(df, output_folder='task4'):
    """
    Create box plots of ratings for each bank.
    """
    plt.figure(figsize=(10, 6))
    sns.boxplot(x='bank', y='rating', data=df)
    plt.title('Rating Distribution by Bank')
    plt.xlabel('Bank')
    plt.ylabel('Rating')
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    output_path = os.path.join(output_folder, 'rating_boxplots.png')
    plt.savefig(output_path)
    plt.close()

def create_all_visualizations(input_file='cleaned_reviews.csv'):
    """
    Create all additional visualizations.
    """
    df = pd.read_csv(input_file)
    
    # Create output directory if it doesn't exist
    os.makedirs('task4', exist_ok=True)
    
    # Plot sentiment trends
    plot_sentiment_trends(df)
    
    # Create word clouds for each bank
    for bank in df['bank'].unique():
        # Positive reviews word cloud
        positive_text = ' '.join(df[(df['bank'] == bank) & (df['rating'] >= 4)]['review'])
        create_word_cloud(positive_text, 
                         f'Positive Reviews - {bank}',
                         f'task4/{bank.lower().replace(" ", "_")}_positive_wordcloud.png')
        
        # Negative reviews word cloud
        negative_text = ' '.join(df[(df['bank'] == bank) & (df['rating'] <= 2)]['review'])
        create_word_cloud(negative_text,
                         f'Negative Reviews - {bank}',
                         f'task4/{bank.lower().replace(" ", "_")}_negative_wordcloud.png')
    
    # Create rating box plots
    plot_rating_boxplots(df)

if __name__ == '__main__':
    create_all_visualizations() 