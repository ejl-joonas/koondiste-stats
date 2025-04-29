def calculate_event_momentum_score(row):
    """
    Calculate momentum score for a single event based on the presented scoring system.
    
    Parameters:
    -----------
    row : pd.Series
        A single row from the Dartfish dataframe
        
    Returns:
    --------
    float
        Momentum score for the event
    """
    # Initialize score
    score = 0
    
    # Extract key values
    team = row['Põhimoment'] # AA EESTI ATTACK, DA EESTI ATTACK, DD EESTI DEFENSE, AD EESTI DEFENSE
    outcome = row['Outcome']
    result = row['Result']
    result2 = row['Shot2'] if not pd.isna(row['Shot2']) else ""
    result3 = row['Shot3'] if not pd.isna(row['Shot3']) else ""
    pressing = row['Pressing'] if not pd.isna(row['Pressing']) else ""
    
    # Identify Estonian team (AA/DA) vs opponent (DD/AD)
    is_estonia = team == "AA"
    is_estonia = team == "DA"
    is_opponent = team == "DD"
    is_opponent = team == "AD"
    
    # Goal scored = 20 points (100%)
    if result1 == 'SHOTGOAL':
        score = 20 if is_estonia else -20
    if result2 == 'SHOTGOAL':
        score = 20 if is_estonia else -20
    if result3 == 'SHOTGOAL':
        score = 20 if is_estonia else -20
    
    # Shot on target = 18 points (90%)
    elif result1 == 'SHOTON':
        score = 18 if is_estonia else -18
    elif result2 == 'SHOTON':
        score = 18 if is_estonia else -18
    elif result3 == 'SHOTON':
        score = 18 if is_estonia else -18
    
    # Shot off target = 10 points (50%)
    elif result1 == 'SHOTOFF':
        score = 10 if is_estonia else -10
    elif result2 == 'SHOTOFF':
        score = 10 if is_estonia else -10
    elif result3 == 'SHOTOFF':
        score = 10 if is_estonia else -10
    
    #Shot blocked by outfield player = 6 points (30%)
    elif result1 == 'SHOTBLOCK':
        score =  6 if is_estonia else -6
    elif result2 == 'SHOTBLOCK':
        score =  6 if is_estonia else -6
    elif result3 == 'SHOTBLOCK':
        score =  6 if is_estonia else -6
    
    # Entry into penalty box = 17 points (85%)
    elif result == 'ENTRY':
        score = 17 if is_estonia else -17

   # Earning/conceding a penalty = 14 points (70%)
    elif result == 'WINPENALTY':
         score =  14 if is_estonia else -14
   
   # Earning/conceding a direct set-piece  = 6 points (30%)
    elif result == 'WINSTANDARD':
         score =  6 if is_estonia else -6

    # Positive pressing values based on zone (from pressing momentum values)
    # 1) DD HIGHPRESS
    if outcome == 'POS'
        if pressing == 'HIGHPRESS' and team in ['DD']:
            if result == '-':
                score += 3
        elif pressing == 'HIGHPRESS' and team in ['DD']:
            if result == 'KEEPPOS':
                score += 3
    # 2) DD MIDPRESS
     if outcome == 'POS'
        if pressing == 'MIDPRESS' and team in ['DD']:
            if result == '-':
                score += 2
        elif pressing == 'MIDPRESS' and team in ['DD']:
            if result == 'KEEPPOS':
                score += 2
    # 3) DD LOWPRESS
    if outcome == 'POS'
        if pressing == 'LOWPRESS' and team in ['DD']:
            if result == '-':
                score += 1
        elif pressing == 'LOWPRESS' and team in ['DD']:
            if result == 'KEEPPOS':
                score += 1
  
    # Negative pressing values based on zone (from pressing momentum values)
    # 1) AA HIGHPRESS
    if outcome == 'NEG'
        if pressing == 'HIGHPRESS' and team in ['AA']:
            if result == '-':
                score += -3
        elif pressing == 'HIGHPRESS' and team in ['AA']:
            if result == 'KEEPPOS':
                score += 0
    # 2) AA MIDPRESS
     if outcome == 'NEG'
        if pressing == 'MIDPRESS' and team in ['AA']:
            if result == '-':
                score += -2
        elif pressing == 'MIDPRESS' and team in ['AA']:
            if result == 'KEEPPOS':
                score += 0
    # 3) AA LOWPRESS
    if outcome == 'NEG'
        if pressing == 'LOWPRESS' and team in ['AA']:
            if result == '-':
                score += -1
        elif pressing == 'LOWPRESS' and team in ['AA']:
            if result == 'KEEPPOS':
                score += 0


    
    # Transition possession gains/losses
    # 1) AD POS -
     if team == 'AD' 
        if outcome == 'POS' 
            if result == '-'
               score += 1
    
    # 2) AD POS KEEPPOS
     if team == 'AD' 
        if outcome == 'POS' 
            if result == 'KEEPPOS'
               score += 1
    
    # 3) DA POS -
     if team == 'DA' 
        if outcome == 'POS' 
            if result == '-'
               score += 0

    # 4) DA POS KEEPPOS
     if team == 'DA' 
        if outcome == 'POS' 
            if result == '-'
               score += 0

    # 7) AD NEG - 
     if team == 'AD' 
        if outcome == 'NEG' 
            if result == '-'
               score += -1

    # 8) AD NEG KEEPPOS
     if team == 'AD' 
        if outcome == 'NEG' 
            if result == 'KEEPPOS'
               score += 0

    # 7) DA NEG - 
     if team == 'DA' 
        if outcome == 'NEG' 
            if result == '-'
               score += -1

    # 8) DA NEG KEEPPOS
     if team == 'DA' 
        if outcome == 'NEG' 
            if result == 'KEEPPOS'
               score += 0

    # More detailed transition scoring could be added based on your complete system
    
    return score

def calculate_momentum_by_interval(df):
    """
    Calculate aggregate momentum scores for each 5-minute interval.
    
    Parameters:
    -----------
    df : pd.DataFrame
        Preprocessed Dartfish data
        
    Returns:
    --------
    pd.DataFrame
        Dataframe with momentum scores by interval
    """
    # Calculate momentum score for each event
    df['Momentum_Score'] = df.apply(calculate_event_momentum_score, axis=1)
    
    # Group by interval and sum the momentum scores
    momentum_by_interval = df.groupby(['Interval', 'Interval_Label'])['Momentum_Score'].sum().reset_index()
    
    # Calculate cumulative momentum
    momentum_by_interval['Cumulative_Momentum'] = momentum_by_interval['Momentum_Score'].cumsum()
    
    return momentum_by_interval

def analyze_team_stats(df):
    """
    Calculate team-specific statistics for Estonia and opponent.
    
    Parameters:
    -----------
    df : pd.DataFrame
        Preprocessed Dartfish data
        
    Returns:
    --------
    dict
        Dictionary containing team statistics
    """
    team_stats = {
        'Estonia': {},
        'Opponent': {}
    }
    
    # Goals
    team_stats['Estonia']['goals'] = df[(df['Põhimoment'].str[:2] != 'DD') & (df['Result'] == 'SHOTGOAL')].shape[0]
    team_stats['Opponent']['goals'] = df[(df['Põhimoment'].str[:2] != 'AA') & (df['Result'] == 'SHOTGOAL')].shape[0]
    
    # Shots on target
    team_stats['Estonia']['shots_on_target'] = df[(df['Põhimoment'].str[:2] != 'DD') & (df['Result'] == 'SHOTON')].shape[0]
    team_stats['Opponent']['shots_on_target'] = df[(df['Põhimoment'].str[:2] != 'AA') & (df['Result'] == 'SHOTON')].shape[0]
    
    # Shots off target
    team_stats['Estonia']['shots_off_target'] = df[(df['Põhimoment'].str[:2] != 'DD') & (df['Result'] == 'SHOTOFF')].shape[0]
    team_stats['Opponent']['shots_off_target'] = df[(df['Põhimoment'].str[:2] != 'AA') & (df['Result'] == 'SHOTOFF')].shape[0]
    
    # Entries
    team_stats['Estonia']['entries'] = df[(df['Põhimoment'].str[:2] != 'DD') & (df['Result'] == 'ENTRY')].shape[0]
    team_stats['Opponent']['entries'] = df[(df['Põhimoment'].str[:2] != 'AA') & (df['Result'] == 'ENTRY')].shape[0]
    
    # Possession (simplified - based on event count)
    estonia_events = df[df['Põhimoment'].str[:2] == 'AA'].shape[0]
    opponent_events = df[df['Põhimoment'].str[:2] == 'DD'].shape[0]
    total_events = estonia_events + opponent_events
    
    team_stats['Estonia']['possession_pct'] = round((estonia_events / total_events) * 100, 1) if total_events > 0 else 0
    team_stats['Opponent']['possession_pct'] = round((opponent_events / total_events) * 100, 1) if total_events > 0 else 0
    
    return team_stats