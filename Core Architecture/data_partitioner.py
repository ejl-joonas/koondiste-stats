# partitioner.py
class DataPartitioner:
    """Partitions data for parallel processing."""
    
    def partition_by_time(self, events_df, num_partitions):
        """Split events into time-based partitions."""
        max_time = events_df['Position'].max() + events_df['Duration'].max()
        partition_size = max_time / num_partitions
        
        partitions = []
        for i in range(num_partitions):
            start_time = i * partition_size
            end_time = (i + 1) * partition_size
            
            # Get events that fall within this partition
            mask = ((events_df['Position'] >= start_time) & 
                   (events_df['Position'] < end_time)) | \
                   ((events_df['Position'] < start_time) & 
                   (events_df['Position'] + events_df['Duration'] > start_time))
            
            partitions.append(events_df[mask].copy())
        
        return partitions
        
    def process_in_parallel(self, events_df, analyzer_func, num_workers=4):
        """Process data partitions in parallel."""
        partitions = self.partition_by_time(events_df, num_workers)
        
        with concurrent.futures.ProcessPoolExecutor(max_workers=num_workers) as executor:
            results = list(executor.map(analyzer_func, partitions))
            
        # Merge results
        return self._merge_results(results)