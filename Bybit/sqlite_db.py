import sqlite3


def create_database():
    """
    Создает базу данных и таблицу, если они не существуют.
    """
    conn = sqlite3.connect('spot_coin_picker_for_portfolio.db')
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS kline_history (
        startTime INTEGER PRIMARY KEY,
        open FLOAT,
        high FLOAT,
        low FLOAT,
        close FLOAT,
        volume FLOAT,
        turnover FLOAT
    )
    ''')
    conn.commit()
    conn.close()
