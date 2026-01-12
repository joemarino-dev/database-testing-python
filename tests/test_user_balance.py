def test_user_balance_calculation(db_connection):
    """Verify total balance across all users"""
    cursor = db_connection.cursor()
    cursor.execute("SELECT SUM(account_balance) as total FROM users")
    result = cursor.fetchone()
    
    assert result['total'] == 3500.00