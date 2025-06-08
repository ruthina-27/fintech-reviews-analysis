import pandas as pd
import os

def preprocess_reviews(file_path):
    try:
        # Check if file exists
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Input file '{file_path}' not found")
            
        df = pd.read_csv(file_path)
        
        # Check if DataFrame is empty
        if df.empty:
            print("Warning: The input file is empty")
            return
            
        # Rename columns (assuming original columns are ['content', 'score', 'at', 'bank'])
        df.columns = ['review', 'rating', 'date', 'bank']
        
        # Drop duplicates
        initial_count = len(df)
        df = df.drop_duplicates(subset=['review'])
        removed_count = initial_count - len(df)
        
        # Format date
        df['date'] = pd.to_datetime(df['date']).dt.strftime('%Y-%m-%d')
        
        # Add source column
        df['source'] = 'Google Play'
        
        # Save cleaned data to same directory
        output_path = os.path.join(os.path.dirname(file_path), 'cleaned_reviews.csv')
        df.to_csv(output_path, index=False)
        
        # Print summary
        print(f"Preprocessing complete:")
        print(f"- Removed {removed_count} duplicate reviews")
        print(f"- Final dataset has {len(df)} reviews")
        print(f"- Saved to '{output_path}'")
        
    except Exception as e:
        print(f"Error occurred during preprocessing: {str(e)}")

# Run the function with absolute path
input_path = r'C:\Users\YEADONAY\fintech-reviews-analysis\bank_reviews.csv'
preprocess_reviews(input_path)