def assess_randomness(data, target_columns, threshold=0.3):
    """
    Simple assessment: Random or Not Random based on correlations.
    Returns correlation values for each correlated column.
    """
    corr_matrix = data.corr()
    results = {}
    
    for target_col in target_columns:
        correlations = corr_matrix[target_col].drop(target_col)
        correlated = correlations[abs(correlations) >= threshold]
        
        # Create list of tuples: (column_name, correlation_value)
        correlated_list = [(col, corr_val) for col, corr_val in correlated.items()] if len(correlated) > 0 else []
        
        results[target_col] = {
            'correlated_columns': correlated_list,
            'result': 'Random (MCAR)' if len(correlated_list) == 0 else 'Not Random (MAR/MNAR)'
        }
    
    return results