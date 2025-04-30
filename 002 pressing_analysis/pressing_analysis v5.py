def analyze_pressing_and_transitions(first_half_path, second_half_path):
    """
    Perform a comprehensive analysis of pressing and transitions.
    
    Parameters:
    -----------
    first_half_path : str
        Path to the first half CSV file
    second_half_path : str
        Path to the second half CSV file
        
    Returns:
    --------
    dict
        Dictionary with analysis results
    """
    # Load and preprocess data
    raw_data = load_dartfish_data(first_half_path, second_half_path)
    preprocessed_data = preprocess_data(raw_data)
    
    # Analyze pressing
    pressing_events = classify_pressing_zones(preprocessed_data)
    pressing_metrics = calculate_pressing_metrics(pressing_events)
    
    # Analyze transitions
    transition_events = identify_transitions(preprocessed_data)
    transition_metrics = calculate_transition_metrics(transition_events)
    
    # Generate visualizations
    pressing_fig, _ = visualize_pressing_statistics(pressing_metrics)
    transition_fig, _ = visualize_transition_statistics(transition_metrics)
    pitch_fig, _ = plot_pitch_with_pressing_zones()
    heatmap_fig, _ = create_pressing_heatmap(pressing_events)
    
    # Save the figures
    pressing_fig.savefig("pressing_statistics.png", dpi=300, bbox_inches='tight')
    transition_fig.savefig("transition_statistics.png", dpi=300, bbox_inches='tight')
    pitch_fig.savefig("pitch_zones.png", dpi=300, bbox_inches='tight')
    heatmap_fig.savefig("pressing_heatmap.png", dpi=300, bbox_inches='tight')
    
    # Export detailed results to Excel
    writer = pd.ExcelWriter('pressing_transition_analysis.xlsx', engine='xlsxwriter')
    
    # Export pressing events
    pressing_events.to_excel(writer, sheet_name='Pressing_Events', index=False)
    
    # Export transition events
    transition_events.to_excel(writer, sheet_name='Transition_Events', index=False)
    
    # Export pressing metrics
    pd.DataFrame({
        'Metric': ['Total Presses', 'Successful Presses', 'Success Rate (%)'],
        'Value': [
            pressing_metrics['total_presses'],
            pressing_metrics['successful_presses'],
            pressing_metrics['success_rate']
        ]
    }).to_excel(writer, sheet_name='Pressing_Metrics', index=False)
    
    # Export pressing by zone
    pressing_metrics['zone_metrics'].reset_index().to_excel(
        writer, sheet_name='Pressing_by_Zone', index=False
    )
    
    # Export transition metrics
    pd.DataFrame({
        'Metric': [
            'Total Transitions',
            'Estonia Gained Possession',
            'Estonia Lost Possession',
            'Transitions to Shots',
            'Shot Rate from Transitions (%)',
            'Average Transition Duration (sec)'
        ],
        'Value': [
            transition_metrics['total_transitions'],
            transition_metrics['estonia_gained_possession'],
            transition_metrics['estonia_lost_possession'],
            transition_metrics['transitions_to_shots'],
            transition_metrics['shot_rate_from_transitions'],
            transition_metrics['avg_transition_duration']
        ]
    }).to_excel(writer, sheet_name='Transition_Metrics', index=False)
    
    # Save Excel file
    writer.save()
    
    # Return all metrics and events for further analysis
    return {
        'pressing_events': pressing_events,
        'pressing_metrics': pressing_metrics,
        'transition_events': transition_events,
        'transition_metrics': transition_metrics
    }

def main():
    """
    Main function to run the pressing analysis.
    """
    # File paths for the CSV data
    first_half_path = "2025.04.14 U17 Eesti - Gruusia (1pa).csv"
    second_half_path = "2025.04.14 U17 Eesti - Gruusia (2pa).csv"
    
    try:
        # Run the comprehensive analysis
        results = analyze_pressing_and_transitions(first_half_path, second_half_path)
        
        # Print summary statistics
        print("Pressing and Transition Analysis Summary:")
        print(f"Total pressing events: {results['pressing_metrics']['total_presses']}")
        print(f"Pressing success rate: {results['pressing_metrics']['success_rate']}%")
        print(f"Total transitions: {results['transition_metrics']['total_transitions']}")
        print(f"Transitions to shots: {results['transition_metrics']['transitions_to_shots']} ({results['transition_metrics']['shot_rate_from_transitions']}%)")
        print(f"Estonia gained possession: {results['transition_metrics']['estonia_gained_possession']} times")
        print(f"Estonia lost possession: {results['transition_metrics']['estonia_lost_possession']} times")
        
        print("\nAnalysis complete! Results saved to Excel and images.")
        
    except Exception as e:
        print(f"Error during analysis: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()