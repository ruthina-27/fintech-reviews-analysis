import os
from analysis import analyze_reviews
from visualize import create_visualizations
from additional_visualizations import create_all_visualizations

def main():
    """
    Run all Task 4 analysis components.
    """
    # Create task4 directory if it doesn't exist
    os.makedirs('task4', exist_ok=True)
    
    # Run sentiment and thematic analysis
    print("Running sentiment and thematic analysis...")
    analyze_reviews()
    
    # Create basic visualizations
    print("Creating basic visualizations...")
    create_visualizations()
    
    # Create additional visualizations
    print("Creating additional visualizations...")
    create_all_visualizations()
    
    print("\nTask 4 analysis complete!")
    print("Generated files:")
    print("1. task4/analysis_summary.txt - Detailed analysis results")
    print("2. task4/final_report.md - Comprehensive report")
    print("3. Various visualization files in task4/ directory")
    print("\nPlease review the final_report.md for complete findings and recommendations.")

if __name__ == '__main__':
    main() 