def identify_transitions(df):
    """
    Identify transition moments in the match data.
    
    Parameters:
    -----------
    df : pd.DataFrame
        Preprocessed Dartfish data
        
    Returns:
    --------
    pd.DataFrame
        DataFrame with identified transition moments
    """
    # Create a copy to avoid modifying the original
    transition_df = df.copy()
    
    # Identify explicit transitions (AD, DA)
    explicit_transitions = transition_df[transition_df['Põhimoment'].isin(['AD', 'DA'])].copy()
    
    # Mark transition types
    explicit_transitions['Transition_Type'] = explicit_transitions['Põhimoment'].map({
        'AD': 'EST AD',  # Estonia lost possession
        'DA': 'EST DA'   # Estonia gained possession
    })
    
    # Identify outcome of transition
    explicit_transitions['Transition_Result'] = explicit_transitions['Result'].fillna('Unknown')
    
    # Identify zones involved in transitions
    # Starting zone
    explicit_transitions['Transition_Starting_Zone'] = explicit_transitions['Tsoon1'].fillna('Unknown')
    
    # Ending zone (if available)
    mask = explicit_transitions['Tsoon3'].notna()
    explicit_transitions.loc[mask, 'Transition_Ending_Zone'] = explicit_transitions.loc[mask, 'Tsoon3']
    
    mask = (explicit_transitions['Tsoon3'].isna()) & (explicit_transitions['Tsoon2'].notna())
    explicit_transitions.loc[mask, 'Transition_Ending_Zone'] = explicit_transitions.loc[mask, 'Tsoon2']
    
    explicit_transitions['Transition_Ending_Zone'] = explicit_transitions['Transition_Ending_Zone'].fillna('Unknown')
    
    # Calculate field progress during transition (if field position data available)
    if 'Field Position' in explicit_transitions.columns:
        # This would require more detailed field position tracking
        # Placeholder for future implementation
        pass
    
    # Identify if transition led to dangerous attack
    explicit_transitions['Resulted_In_Shot'] = explicit_transitions['Result'].isin(['SHOTGOAL', 'SHOTON', 'SHOTOFF', 'SHOTBLOCK'])
    explicit_transitions['Resulted_In_Entry'] = explicit_transitions['Result'] == 'ENTRY'
    
    return explicit_transitions

def calculate_transition_metrics(transitions_df):
    """
    Calculate metrics for transitions.
    
    Parameters:
    -----------
    transitions_df : pd.DataFrame
        DataFrame with identified transitions
        
    Returns:
    --------
    dict
        Dictionary with transition metrics
    """
    metrics = {}
    
    # Total transitions
    metrics['total_transitions'] = transitions_df.shape[0]
    
    # Transitions by type
    type_counts = transitions_df['Transition_Type'].value_counts()
    metrics['estonia_lost_possession'] = type_counts.get('EST AD', 0)
    metrics['estonia_gained_possession'] = type_counts.get('EST DA', 0)
    
    # Transition outcomes
    metrics['transitions_to_shots'] = transitions_df['Resulted_In_Shot'].sum()
    metrics['transitions_to_entries'] = transitions_df['Resulted_In_Entry'].sum()
    
    # Shot rate from transitions
    metrics['shot_rate_from_transitions'] = round((metrics['transitions_to_shots'] / metrics['total_transitions']) * 100, 1) if metrics['total_transitions'] > 0 else 0
    
    # Transitions by starting zone
    metrics['transitions_by_starting_zone'] = transitions_df['Transition_Starting_Zone'].value_counts().to_dict()
    
    # Transitions by ending zone
    metrics['transitions_by_ending_zone'] = transitions_df['Transition_Ending_Zone'].value_counts().to_dict()
    
    # Transitions by half
    half_transitions = transitions_df.groupby('Poolaeg').size()
    metrics['transitions_first_half'] = half_transitions.get(1, 0)
    metrics['transitions_second_half'] = half_transitions.get(2, 0)
    
    # Transition effectiveness by type
    effectiveness = transitions_df.groupby('Transition_Type').agg(
        total=('Transition_Type', 'count'),
        to_shots=('Resulted_In_Shot', 'sum'),
        to_entries=('Resulted_In_Entry', 'sum')
    )
    effectiveness['shot_rate'] = (effectiveness['to_shots'] / effectiveness['total'] * 100).round(1)
    effectiveness['entry_rate'] = (effectiveness['to_entries'] / effectiveness['total'] * 100).round(1)
    
    metrics['transition_effectiveness'] = effectiveness
    
    return metrics