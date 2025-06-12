import pandas as pd
import numpy as np
from collections import Counter
import matplotlib.pyplot as plt
import seaborn as sns
import os

def analyze_review_biases(df):
    """
    Analyze potential biases in the review data.
    """
    biases = {
        "rating_distribution": df['rating'].value_counts().sort_index(),
        "bank_ratings": df.groupby('bank')['rating'].agg(['mean', 'std', 'count']),
        "rating_trends": df.groupby('date')['rating'].mean().reset_index()
    }
    return biases

def generate_recommendations(df):
    """
    Generate specific recommendations based on the analysis.
    """
    recommendations = {}
    
    for bank in df['bank'].unique():
        bank_df = df[df['bank'] == bank]
        
        # Get top pain points
        negative_reviews = bank_df[bank_df['rating'] <= 2]
        top_issues = Counter()
        
        for review in negative_reviews['review']:
            words = review.lower().split()
            top_issues.update(words)
        
        # Generate recommendations based on pain points
        bank_recommendations = []
        
        if 'slow' in top_issues or 'lag' in top_issues:
            bank_recommendations.append("Optimize app performance and reduce loading times")
        if 'crash' in top_issues or 'error' in top_issues:
            bank_recommendations.append("Implement better error handling and stability improvements")
        if 'login' in top_issues or 'password' in top_issues:
            bank_recommendations.append("Enhance authentication system and password recovery process")
        if 'transaction' in top_issues or 'payment' in top_issues:
            bank_recommendations.append("Improve transaction processing reliability and add better error messages")
        
        recommendations[bank] = bank_recommendations
    
    return recommendations

def plot_rating_distribution(df, output_folder='task4'):
    """
    Plot rating distribution to visualize potential biases.
    """
    plt.figure(figsize=(12, 6))
    sns.histplot(data=df, x='rating', hue='bank', multiple="dodge", shrink=.8)
    plt.title('Rating Distribution by Bank')
    plt.xlabel('Rating')
    plt.ylabel('Count')
    plt.xticks(range(1, 6))
    plt.tight_layout()
    
    output_path = os.path.join(output_folder, 'rating_distribution.png')
    plt.savefig(output_path)
    plt.close()

def create_ethics_report(df, output_file='task4/ethics_report.txt'):
    """
    Create a comprehensive ethics report.
    """
    biases = analyze_review_biases(df)
    recommendations = generate_recommendations(df)
    
    report = "ETHICS AND RECOMMENDATIONS REPORT\n"
    report += "=" * 40 + "\n\n"
    
    # Rating Distribution Analysis
    report += "1. RATING DISTRIBUTION ANALYSIS\n"
    report += "-" * 30 + "\n"
    for bank, stats in biases['bank_ratings'].iterrows():
        report += f"\n{bank}:\n"
        report += f"- Average Rating: {stats['mean']:.2f}\n"
        report += f"- Standard Deviation: {stats['std']:.2f}\n"
        report += f"- Number of Reviews: {stats['count']}\n"
    
    # Potential Biases
    report += "\n\n2. POTENTIAL BIASES\n"
    report += "-" * 30 + "\n"
    report += "- Rating Distribution: Check if ratings are normally distributed or skewed\n"
    report += "- Time-based Bias: Reviews might be influenced by recent events or updates\n"
    report += "- Selection Bias: Users who had negative experiences might be more likely to leave reviews\n"
    report += "- Language Bias: Analysis might miss nuances in non-English reviews\n"
    
    # Recommendations
    report += "\n\n3. RECOMMENDATIONS\n"
    report += "-" * 30 + "\n"
    for bank, recs in recommendations.items():
        report += f"\n{bank}:\n"
        for i, rec in enumerate(recs, 1):
            report += f"{i}. {rec}\n"
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(report)

if __name__ == '__main__':
    df = pd.read_csv('cleaned_reviews.csv')
    create_ethics_report(df)
    plot_rating_distribution(df) 