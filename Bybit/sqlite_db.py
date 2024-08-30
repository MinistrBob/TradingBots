import sqlite3


def create_database():
    """
    Создает базу данных и таблицы, если они не существуют.
    """
    conn = sqlite3.connect('spot_coin_picker_for_portfolio.db')
    cursor = conn.cursor()

    # Создание таблицы symbols
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS symbols (
        symbol TEXT PRIMARY KEY,
        maxPrice FLOAT,
        minPrice FLOAT,
        dateLastCheck INTEGER
    )
    ''')

    # Создание таблицы kline_history с внешним ключом, ссылающимся на symbols
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS kline_history (
        startTime INTEGER PRIMARY KEY,
        symbol TEXT,
        open FLOAT,
        high FLOAT,
        low FLOAT,
        close FLOAT,
        volume FLOAT,
        turnover FLOAT,
        FOREIGN KEY (symbol) REFERENCES symbols(symbol)
    )
    ''')

    conn.commit()
    conn.close()

