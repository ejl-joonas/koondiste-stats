# optimized_analyzer.py
def calculate_momentum_timeline(events_df, interval_seconds=300):
    """Calculate momentum timeline using vectorized operations."""
    # Convert to numpy arrays for faster computation
    timestamps = events_df['Position'].values
    durations = events_df['Duration'].values
    event_types = events_df['Result'].values
    
    # Pre-allocate result array
    max_time = np.max(timestamps + durations)
    num_intervals = int(np.ceil(max_time / interval_seconds))
    momentum_timeline = np.zeros(num_intervals)
    
    # Vectorized mapping of event types to points
    point_values = {
        'SHOTGOAL': 20,
        'SHOTON': 4,
        'SHOTOFF': 2,
        # etc.
    }
    
    # Vectorized calculation
    for i in range(num_intervals):
        start_time = i * interval_seconds
        end_time = (i + 1) * interval_seconds
        
        # Find events in this interval
        mask = ((timestamps >= start_time) & (timestamps < end_time)) | \
               ((timestamps < start_time) & (timestamps + durations > start_time))
        
        interval_events = events_df[mask]
        
        # Calculate momentum for interval
        momentum_timeline[i] = sum(point_values.get(et, 0) for et in interval_events['Result'])
    
    return momentum_timeline