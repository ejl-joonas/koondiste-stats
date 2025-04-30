def analyze_setpieces_and_progressions(first_half_path, second_half_path):
    """
    Perform comprehensive analysis of set pieces and progressions.
    
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
    
    # Analyze set pieces
    set_pieces = identify_set_pieces(preprocessed_data)
    set_piece_metrics = calculate_set_piece_metrics(set_pieces)
    
    # Analyze progressions
    progression_events, progression_sequences = analyze_progressions(preprocessed_data)
    progression_metrics = calculate_progression_metrics(progression_events, progression_sequences)
    
    # Generate visualizations
    sp_fig, _ = visualize_set_pieces(set_pieces, set_piece_metrics)
    sp_dist_fig, _ = visualize_set_piece_distribution(set_pieces)
    prog_fig, _ = visualize_progression_metrics(progression_metrics)
    flow_fig, _ = visualize_progression_flow(progression_sequences)
    
    # Save the figures
    sp_fig.savefig("set_piece_analysis.png", dpi=300, bbox_inches='tight')
    sp_dist_fig.savefig("set_piece_distribution.png", dpi=300, bbox_inches='tight')
    prog_fig.savefig("progression_analysis.png", dpi=300, bbox_inches='tight')
    flow_fig.savefig("progression_flow.png", dpi=300, bbox_inches='tight')
    
    # Export detailed results to Excel
    writer = pd.ExcelWriter('setpiece_progression_analysis.xlsx', engine='xlsxwriter')
    
    # Export set piece data
    set_pieces.to_excel(writer, sheet_name='Set_Pieces', index=False)
    
    # Export set piece metrics
    pd.DataFrame({
        'Metric': [
            'Total Set Pieces',
            'Goals from Set Pieces',
            'Shots from Set Pieces',
            'Shot Rate from Set Pieces (%)',
            'Set Pieces in First Half',
            'Set Pieces in Second Half'
        ],
        'Value': [
            set_piece_metrics['total_set_pieces'],
            set_piece_metrics['goals_from_set_pieces'],
            set_piece_metrics['shots_from_set_pieces'],
            set_piece_metrics['shot_rate_from_set_pieces'],
            set_piece_metrics['set_pieces_first_half'],
            set_piece_metrics['set_pieces_second_half']
        ]
    }).to_excel(writer, sheet_name='SP_Summary', index=False)
    
    # Export set piece metrics by type
    sp_type_data = []
    for sp_type, count in set_piece_metrics['set_pieces_by_type'].items():
        success_rate = set_piece_metrics['success_rate_by_type']['success_rate'].get(sp_type, 0)
        
        # Conversion rates
        shot_rate = goal_rate = 0
        if sp_type in set_piece_metrics['conversion_rates']:
            shot_rate = set_piece_metrics['conversion_rates'][sp_type]['shot_rate']
            goal_rate = set_piece_metrics['conversion_rates'][sp_type]['goal_rate']
        
        sp_type_data.append({
            'Set_Piece_Type': sp_type,
            'Count': count,
            'Success_Rate': success_rate,
            'Shot_Rate': shot_rate,
            'Goal_Rate': goal_rate
        })
    
    pd.DataFrame(sp_type_data).to_excel(writer, sheet_name='SP_By_Type', index=False)
    
    # Export progression events
    progression_events.to_excel(writer, sheet_name='Progression_Events', index=False)
    
    # Export progression sequences
    progression_sequences.to_excel(writer, sheet_name='Progression_Sequences', index=False)
    
    # Export progression metrics
    pd.DataFrame({
        'Metric': [
            'Total Progressions',
            'Successful Progressions',
            'Success Rate (%)',
            'Total Sequences',
            'Sequences with Shots',
            'Sequences with Goals',
            'Shot Rate from Sequences (%)',
            'Goal Rate from Sequences (%)',
            'Average Sequence Duration (sec)',
            'Sequences in First Half',
            'Sequences in Second Half'
        ],
        'Value': [
            progression_metrics['total_progressions'],
            progression_metrics['successful_progressions'],
            progression_metrics['success_rate'],
            progression_metrics['total_sequences'],
            progression_metrics['sequences_with_shots'],
            progression_metrics['sequences_with_goals'],
            progression_metrics['shot_rate_from_sequences'],
            progression_metrics['goal_rate_from_sequences'],
            progression_metrics['avg_sequence_duration'],
            progression_metrics['sequences_first_half'],
            progression_metrics['sequences_second_half']
        ]
    }).to_excel(writer, sheet_name='Progression_Summary', index=False)
    
    # Export efficiency by sequence type
    sequence_type_data = []
    for seq_type in progression_metrics['sequence_types'].keys():
        if seq_type in progression_metrics['efficiency_by_type']['total']:
            total = progression_metrics['efficiency_by_type']['total'][seq_type]
            shots = progression_metrics['efficiency_by_type']['shots'][seq_type]
            goals = progression_metrics['efficiency_by_type']['goals'][seq_type]
            shot_rate = progression_metrics['efficiency_by_type']['shot_rate'][seq_type]
            goal_rate = progression_metrics['efficiency_by_type']['goal_rate'][seq_type]
            
            sequence_type_data.append({
                'Sequence_Type': seq_type,
                'Count': total,
                'Shots': shots,
                'Goals': goals,
                'Shot_Rate': shot_rate,
                'Goal_Rate': goal_rate
            })
    
    pd.DataFrame(sequence_type_data).to_excel(writer, sheet_name='Seq_By_Type', index=False)
    
    # Save Excel file
    writer.save()
    
    # Create a combined report
    generate_combined_report(set_piece_metrics, progression_metrics)
    
    # Return all metrics and events for further analysis
    return {
        'set_pieces': set_pieces,
        'set_piece_metrics': set_piece_metrics,
        'progression_events': progression_events,
        'progression_sequences': progression_sequences,
        'progression_metrics': progression_metrics
    }

def generate_combined_report(set_piece_metrics, progression_metrics):
    """
    Generate a combined report with key metrics.
    
    Parameters:
    -----------
    set_piece_metrics : dict
        Dictionary with set piece metrics
    progression_metrics : dict
        Dictionary with progression metrics
    """
    report = [
        "# Match Analysis Report",
        f"\nDate: {pd.Timestamp.now().strftime('%Y-%m-%d')}",
        "\n## Key Findings",
        "\n### Set Piece Analysis",
        f"\n- Total Set Pieces: {set_piece_metrics['total_set_pieces']}",
        f"- Goals from Set Pieces: {set_piece_metrics['goals_from_set_pieces']}",
        f"- Shot Rate from Set Pieces: {set_piece_metrics['shot_rate_from_set_pieces']}%",
        "\n#### Set Piece Distribution",
    ]
    
    # Add set piece distribution
    for sp_type, count in sorted(set_piece_metrics['set_pieces_by_type'].items(), key=lambda x: x[1], reverse=True):
        report.append(f"- {sp_type}: {count}")
    
    report.extend([
        "\n### Progression Analysis",
        f"\n- Total Progression Sequences: {progression_metrics['total_sequences']}",
        f"- Sequences with Shots: {progression_metrics['sequences_with_shots']} ({progression_metrics['shot_rate_from_sequences']}%)",
        f"- Sequences with Goals: {progression_metrics['sequences_with_goals']} ({progression_metrics['goal_rate_from_sequences']}%)",
        "\n#### Sequence Types",
    ])
    
    # Add sequence types
    for seq_type, count in sorted(progression_metrics['sequence_types'].items(), key=lambda x: x[1], reverse=True):
        report.append(f"- {seq_type}: {count}")
    
    # Add efficiency comparison
    report.extend([
        "\n## Efficiency Analysis",
        "\n### Most Efficient Set Piece Types",
    ])
    
    # Find most efficient set piece types
    if 'conversion_rates' in set_piece_metrics:
        efficient_sp = sorted(
            [(sp_type, data['goal_rate']) 
             for sp_type, data in set_piece_metrics['conversion_rates'].items()
             if data['goal_rate'] > 0],
            key=lambda x: x[1],
            reverse=True
        )
        
        for sp_type, rate in efficient_sp[:3]:
            report.append(f"- {sp_type}: {rate}% goal rate")
    
    report.extend([
        "\n### Most Efficient Progression Sequences",
    ])
    
    # Find most efficient sequence types
    if 'efficiency_by_type' in progression_metrics and 'goal_rate' in progression_metrics['efficiency_by_type']:
        efficient_seq = []
        for seq_type in progression_metrics['efficiency_by_type']['goal_rate'].keys():
            goal_rate = progression_metrics['efficiency_by_type']['goal_rate'][seq_type]
            if goal_rate > 0:
                efficient_seq.append((seq_type, goal_rate))
        
        efficient_seq.sort(key=lambda x: x[1], reverse=True)
        
        for seq_type, rate in efficient_seq[:3]:
            report.append(f"- {seq_type}: {rate}% goal rate")
    
    # Write the report to a file
    with open('match_analysis_report.md', 'w') as f:
        f.write('\n'.join(report))

def main():
    """
    Main function to run the set piece and progression analysis.
    """
    # File paths for the CSV data
    first_half_path = "2025.04.14 U17 Eesti - Gruusia (1pa).csv"
    second_half_path = "2025.04.14 U17 Eesti - Gruusia (2pa).csv"
    
    try:
        # Run the comprehensive analysis
        results = analyze_setpieces_and_progressions(first_half_path, second_half_path)
        
        # Print summary statistics
        print("Set Piece and Progression Analysis Summary:")
        print(f"Total set pieces: {results['set_piece_metrics']['total_set_pieces']}")
        print(f"Goals from set pieces: {results['set_piece_metrics']['goals_from_set_pieces']}")
        
        print(f"\nTotal progression sequences: {results['progression_metrics']['total_sequences']}")
        print(f"Sequences with shots: {results['progression_metrics']['sequences_with_shots']} ({results['progression_metrics']['shot_rate_from_sequences']}%)")
        print(f"Sequences with goals: {results['progression_metrics']['sequences_with_goals']} ({results['progression_metrics']['goal_rate_from_sequences']}%)")
        
        print("\nAnalysis complete! Results saved to Excel and images.")
        print("A combined report has been generated as 'match_analysis_report.md'")
        
    except Exception as e:
        print(f"Error during analysis: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()