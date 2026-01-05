def test_account_balance_integrity(db_connection):
    """Property-based test: Validate transaction data integrity
    
    This test demonstrates scalable validation - it works regardless of
    how many users or transactions exist. Instead of hardcoding expected
    values, it validates mathematical relationships that must always hold.
    
    Business rules tested:
    - Deposits are never negative
    - Withdrawals are never negative  
    - If transactions exist, totals must be greater than zero
    - Aggregate calculations match manual verification
    """
    cursor = db_connection.cursor()
    
    # Get all users
    cursor.execute("SELECT id, name FROM users")
    users = cursor.fetchall()
    
    # For each user, validate their balance
    for user in users:
        # Calculate deposits and withdrawals using SQL aggregation
        cursor.execute("""
                    SELECT
                        SUM(CASE WHEN transaction_type='deposit' THEN amount ELSE 0 END) as deposits,
                        SUM(CASE WHEN transaction_type='withdrawal' THEN amount ELSE 0 END) as withdrawals,
                        COUNT(*) as transaction_count
                    FROM transactions
                    WHERE user_id = ? AND status = 'completed'
                    """, (user['id'],))
                    
        result = cursor.fetchone()
        
        # Handle case where user has no transactions
        deposits = result['deposits'] or 0
        withdrawals = result['withdrawals'] or 0
        txn_count = result['transaction_count'] or 0
        
        # Business Rule 1: Deposits must be non-negative
        assert deposits >= 0, \
            f"User {user['id']} (user['name']) has negative deposits: {deposits}"
            
        # Business Rule 2: Withdrawals must be non-negative
        assert withdrawals >= 0, \
            f"User {user['id']} (user['name']) has negative withdrawals: {withdrawals}"
            
        # Business Rule 3: If user has transactions, totals must be > 0
        if txn_count > 0:
            assert (deposits + withdrawals) > 0, \
                f"User {user['id']} ({user['name']}) has {txn_count} transactions but zero total amount"
                
        # Verify aggregate calculation matches manual calculation
        cursor.execute("""
            SELECT transaction_type, amount
            FROM transactions
            WHERE user_id = ? and status = 'completed'
        """, (user['id'],))
        
        transactions = cursor.fetchall()
        
        # Manually calculate to verify aggregation is correct
        manual_deposits = sum(t['amount'] for t in transactions if t['transaction_type'] == 'deposit')
        manual_withdrawals = sum(t['amount'] for t in transactions if t['transaction_type'] == 'withdrawal')
        
        # Business Rule 4: Aggregate queries must match manual calculation
        assert abs(deposits - manual_deposits) < 0.01, \
            f"Deposit aggregation mismatch for user {user['id']} (user['name'])"
        assert abs(withdrawals - manual_withdrawals) < 0.01, \
            f"Withdrawal aggregation mismatch for user {user['id']} (user['name'])"
                    
                    
                        