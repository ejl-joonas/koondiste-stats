def main():
    """
    Main function to run the momentum analysis.
    """
    # File paths for the CSV data
    first_half_path = "2025.04.14 U17 Eesti - Gruusia (1pa).csv"
    second_half_path = "2025.04.14 U17 Eesti - Gruusia (2pa).csv"
    
    try:
        # Load and preprocess data
        raw_data = load_dartfish_data(first_half_path, second_half_path)
        preprocessed_data = preprocess_data(raw_data)
        
        # Calculate momentum
        momentum_data = calculate_momentum_by_interval(preprocessed_data)
        
        # Calculate team statistics
        team_stats = analyze_team_stats(preprocessed_data)
        
        # Plot the results
        momentum_fig = plot_momentum_chart(momentum_data, team_stats)
        pressing_fig = plot_pressing_effectiveness(preprocessed_data)
        
        # Save the figures if needed
        momentum_fig.savefig("momentum_analysis.png", dpi=300, bbox_inches='tight')
        pressing_fig.savefig("pressing_analysis.png", dpi=300, bbox_inches='tight')
        
        # Print summary statistics
        print("Match Analysis Summary:")
        print(f"Estonia {team_stats['Estonia']['goals']} - {team_stats['Opponent']['goals']} Georgia")
        print(f"Total momentum score: {momentum_data['Momentum_Score'].sum()}")
        print(f"Peak momentum interval: {momentum_data.loc[momentum_data['Momentum_Score'].idxmax(), 'Interval_Label']}")
        print(f"Lowest momentum interval: {momentum_data.loc[momentum_data['Momentum_Score'].idxmin(), 'Interval_Label']}")
        
        # Export detailed results to Excel
        writer = pd.ExcelWriter('match_analysis_results.xlsx', engine='xlsxwriter')
        
        # Momentum by interval
        momentum_data.to_excel(writer, sheet_name='Momentum_Analysis', index=False)
        
        # Event details
        preprocessed_data[['Match_Time_sec', 'Half', 'Põhimoment', 'Result', 'Pressing', 'Momentum_Score']].to_excel(
            writer, sheet_name='Event_Details', index=False
        )
        
        # Team statistics
        pd.DataFrame({
            'Metric': ['Goals', 'Shots on Target', 'Shots off Target', 'Entries', 'Possession %'],
            'Estonia': [
                team_stats['Estonia']['goals'],
                team_stats['Estonia']['shots_on_target'],
                team_stats['Estonia']['shots_off_target'],
                team_stats['Estonia']['entries'],
                team_stats['Estonia']['possession_pct']
            ],
            'Georgia': [
                team_stats['Opponent']['goals'],
                team_stats['Opponent']['shots_on_target'],
                team_stats['Opponent']['shots_off_target'],
                team_stats['Opponent']['entries'],
                team_stats['Opponent']['possession_pct']
            ]
        }).to_excel(writer, sheet_name='Team_Statistics', index=False)
        
        writer.save()
        
        print("Analysis complete! Results saved to Excel and images.")
        
    except Exception as e:
        print(f"Error during analysis: {e}")

if __name__ == "__main__":
    main()