def analyze_progressions(df):
    """
    Analyze progressions between S1, S2, and S3 zones.
    
    Parameters:
    -----------
    df : pd.DataFrame
        Preprocessed Dartfish data
        
    Returns:
    --------
    tuple
        DataFrame with progression events, DataFrame with progression sequences
    """
    # Create a copy to avoid modifying the original
    progression_df = df.copy()
    
    # Filter rows that contain zone information (S1, S2, S3)
    zone_mask = (
        (progression_df['Tsoon1'].notna() & progression_df['Tsoon1'].isin(['S1', 'S2', 'S3'])) |
        (progression_df['Tsoon2'].notna() & progression_df['Tsoon2'].isin(['S1', 'S2', 'S3'])) |
        (progression_df['Tsoon3'].notna() & progression_df['Tsoon3'].isin(['S1', 'S2', 'S3']))
    )
    
    zone_progressions = progression_df[zone_mask].copy()
    
    # Identify progression types (e.g., S1 to S2, S2 to S3, S1 to S3)
    def identify_progression(row):
        # Get non-NaN zones and sort them (progression is typically from lower to higher zones)
        zones = []
        for zone_col in ['Tsoon1', 'Tsoon2', 'Tsoon3']:
            if pd.notna(row[zone_col]) and row[zone_col] in ['S1', 'S2', 'S3']:
                zones.append(row[zone_col])
        
        if not zones:
            return 'No Zone Progression'
            
        # Sort by zone number
        zones.sort(key=lambda x: int(x[1]))
        
        if len(zones) == 1:
            return f'Static ({zones[0]})'
        else:
            return ' to '.join(zones)
    
    zone_progressions['Progression_Type'] = zone_progressions.apply(identify_progression, axis=1)
    
    # Mark the team
    zone_progressions['Team'] = zone_progressions['Põhimoment'].apply(
        lambda x: 'Estonia' if x.startswith('AA') else 'Georgia' if x.startswith('DD') else 'Transition'
    )
    
    # Mark the outcome of the progression
    zone_progressions['Progression_Outcome'] = zone_progressions['Result'].apply(
        lambda x: 'Goal' if x == 'SHOTGOAL' 
                  else 'Shot on Target' if x == 'SHOTON' 
                  else 'Shot off Target' if x == 'SHOTOFF' 
                  else 'Entry' if x == 'ENTRY'
                  else 'Maintained Possession' if x == 'KEEPPOS' or x == 'WINOPENSTAN'
                  else 'Lost Possession' if x == '-' or pd.isna(x)
                  else 'Other'
    )
    
    # Mark if the progression was successful
    zone_progressions['Progression_Success'] = zone_progressions['Outcome'].apply(
        lambda x: True if x == 'POS' else False
    )
    
    # Mark if the progression resulted in a shot attempt
    shot_results = ['SHOTGOAL', 'SHOTON', 'SHOTOFF', 'SHOTBLOCK']
    zone_progressions['Resulted_In_Shot'] = zone_progressions['Result'].isin(shot_results)
    
    # Identify complete progression sequences (S1 to S2 to S3)
    def identify_sequence_type(row):
        if 'S1' in row['Progression_Type'] and 'S2' in row['Progression_Type'] and 'S3' in row['Progression_Type']:
            return 'Full Progression (S1 to S3)'
        elif 'S1' in row['Progression_Type'] and 'S2' in row['Progression_Type']:
            return 'Partial Progression (S1 to S2)'
        elif 'S2' in row['Progression_Type'] and 'S3' in row['Progression_Type']:
            return 'Partial Progression (S2 to S3)'
        elif 'S1' in row['Progression_Type'] and 'S3' in row['Progression_Type']:
            return 'Skip Progression (S1 to S3)'
        else:
            return 'No Clear Progression'
    
    zone_progressions['Sequence_Type'] = zone_progressions.apply(identify_sequence_type, axis=1)
    
    # Group progressions into sequences based on time proximity
    # This is a simplification - in real implementation, you'd need more sophisticated sequence detection
    sequences = []
    current_sequence = []
    prev_end_time = None
    time_threshold = 10  # seconds
    
    for idx, row in zone_progressions.sort_values('Match_Time_sec').iterrows():
        if prev_end_time is None or (row['Match_Time_sec'] - prev_end_time) > time_threshold:
            # New sequence
            if current_sequence:
                sequences.append(current_sequence)
            current_sequence = [idx]
        else:
            # Continue existing sequence
            current_sequence.append(idx)
        
        prev_end_time = row['Match_Time_sec']
    
    # Add the last sequence
    if current_sequence:
        sequences.append(current_sequence)
    
    # Create a DataFrame for sequences
    sequence_data = []
    
    for seq_idx, seq in enumerate(sequences, 1):
        seq_rows = zone_progressions.loc[seq]
        
        # Extract the start and end times of the sequence
        start_time = seq_rows['Match_Time_sec'].min()
        end_time = seq_rows['Match_Time_sec'].max()
        duration = end_time - start_time
        
        # Determine the team
        team = seq_rows['Team'].iloc[0] if seq_rows['Team'].nunique() == 1 else 'Mixed'
        
        # Get the zones involved
        zones = []
        for _, seq_row in seq_rows.iterrows():
            for zone_col in ['Tsoon1', 'Tsoon2', 'Tsoon3']:
                if pd.notna(seq_row[zone_col]) and seq_row[zone_col] in ['S1', 'S2', 'S3'] and seq_row[zone_col] not in zones:
                    zones.append(seq_row[zone_col])
        
        # Sort zones
        zones.sort(key=lambda x: int(x[1]))
        zones_str = ' to '.join(zones)
        
        # Check outcomes
        final_outcome = seq_rows.iloc[-1]['Progression_Outcome']
        resulted_in_shot = seq_rows['Resulted_In_Shot'].any()
        resulted_in_goal = 'Goal' in seq_rows['Progression_Outcome'].values
        
        # Check sequence completeness
        has_s1 = 'S1' in ''.join(zones)
        has_s2 = 'S2' in ''.join(zones)
        has_s3 = 'S3' in ''.join(zones)
        
        if has_s1 and has_s2 and has_s3:
            sequence_type = 'Full (S1->S2->S3)'
        elif has_s1 and has_s3:
            sequence_type = 'Skip (S1->S3)'
        elif has_s1 and has_s2:
            sequence_type = 'Partial (S1->S2)'
        elif has_s2 and has_s3:
            sequence_type = 'Partial (S2->S3)'
        else:
            sequence_type = 'Incomplete'
        
        # Add to sequence data
        sequence_data.append({
            'Sequence_ID': seq_idx,
            'Team': team,
            'Start_Time_Sec': start_time,
            'Start_Time_Min': round(start_time / 60, 1),
            'Duration_Sec': duration,
            'Zones': zones_str,
            'Sequence_Type': sequence_type,
            'Final_Outcome': final_outcome,
            'Resulted_In_Shot': resulted_in_shot,
            'Resulted_In_Goal': resulted_in_goal,
            'Number_of_Events': len(seq),
            'Half': seq_rows['Half'].iloc[0]
        })
    
    # Create DataFrame from sequence data
    sequences_df = pd.DataFrame(sequence_data)
    
    return zone_progressions, sequences_df

def calculate_progression_metrics(progression_df, sequences_df):
    """
    Calculate efficiency metrics for zone progressions.
    
    Parameters:
    -----------
    progression_df : pd.DataFrame
        DataFrame with progression events
    sequences_df : pd.DataFrame
        DataFrame with progression sequences
        
    Returns:
    --------
    dict
        Dictionary with progression metrics
    """
    metrics = {}
    
    # Overall progression metrics
    metrics['total_progressions'] = progression_df.shape[0]
    metrics['successful_progressions'] = progression_df['Progression_Success'].sum()
    metrics['success_rate'] = round((metrics['successful_progressions'] / metrics['total_progressions']) * 100, 1)
    
    # Progressions by type
    progression_types = progression_df['Progression_Type'].value_counts().to_dict()
    metrics['progression_types'] = progression_types
    
    # Success rate by progression type
    type_success = progression_df.groupby('Progression_Type').agg(
        total=('Progression_Type', 'count'),
        successful=('Progression_Success', 'sum')
    )
    type_success['success_rate'] = (type_success['successful'] / type_success['total'] * 100).round(1)
    metrics['success_rate_by_type'] = type_success.to_dict()
    
    # Sequence metrics
    metrics['total_sequences'] = sequences_df.shape[0]
    metrics['sequences_with_shots'] = sequences_df['Resulted_In_Shot'].sum()
    metrics['sequences_with_goals'] = sequences_df['Resulted_In_Goal'].sum()
    
    # Shot conversion rate from sequences
    metrics['shot_rate_from_sequences'] = round((metrics['sequences_with_shots'] / metrics['total_sequences']) * 100, 1)
    
    # Goal conversion rate from sequences
    metrics['goal_rate_from_sequences'] = round((metrics['sequences_with_goals'] / metrics['total_sequences']) * 100, 1)
    
    # Goal conversion rate from shots in sequences
    if metrics['sequences_with_shots'] > 0:
        metrics['goal_rate_from_shots'] = round((metrics['sequences_with_goals'] / metrics['sequences_with_shots']) * 100, 1)
    else:
        metrics['goal_rate_from_shots'] = 0
    
    # Sequences by type
    sequence_types = sequences_df['Sequence_Type'].value_counts().to_dict()
    metrics['sequence_types'] = sequence_types
    
    # Outcome distribution for sequences
    outcome_dist = sequences_df['Final_Outcome'].value_counts().to_dict()
    metrics['sequence_outcomes'] = outcome_dist
    
    # Efficiency by sequence type
    efficiency_by_type = sequences_df.groupby('Sequence_Type').agg(
        total=('Sequence_Type', 'count'),
        shots=('Resulted_In_Shot', 'sum'),
        goals=('Resulted_In_Goal', 'sum')
    )
    efficiency_by_type['shot_rate'] = (efficiency_by_type['shots'] / efficiency_by_type['total'] * 100).round(1)
    efficiency_by_type['goal_rate'] = (efficiency_by_type['goals'] / efficiency_by_type['total'] * 100).round(1)
    
    metrics['efficiency_by_type'] = efficiency_by_type.to_dict()
    
    # Efficiency by team
    efficiency_by_team = sequences_df.groupby('Team').agg(
        total=('Team', 'count'),
        shots=('Resulted_In_Shot', 'sum'),
        goals=('Resulted_In_Goal', 'sum')
    )
    efficiency_by_team['shot_rate'] = (efficiency_by_team['shots'] / efficiency_by_team['total'] * 100).round(1)
    efficiency_by_team['goal_rate'] = (efficiency_by_team['goals'] / efficiency_by_team['total'] * 100).round(1)
    
    metrics['efficiency_by_team'] = efficiency_by_team.to_dict()
    
    # Average sequence duration
    metrics['avg_sequence_duration'] = round(sequences_df['Duration_Sec'].mean(), 2)
    
    # Sequences by half
    half_sequences = sequences_df.groupby('Half').size()
    metrics['sequences_first_half'] = half_sequences.get(1, 0)
    metrics['sequences_second_half'] = half_sequences.get(2, 0)
    
    return metrics