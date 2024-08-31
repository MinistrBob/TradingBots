import sqlite3
from utils import unixtime_to_datetime


def create_database():
    """
    Создает базу данных и таблицы, если они не существуют.
    """
    conn = sqlite3.connect('spot_coin_picker_for_portfolio.db')
    cursor = conn.cursor()

    # Создание таблицы symbols
    """
    symbol TEXT PRIMARY KEY - уникальный идентификатор символа (например, BTCUSDT)
    dateLastCheck INTEGER - дата последнего обновления цены (unixtime)
    lastPrice FLOAT - текущая цена
    volumeUsdt INTEGER - оборот в USDT за 24часа
    maxPrice FLOAT - максимальная цена за всё время торгов этой пары
    minPrice FLOAT - минимальная цена за всё время торгов этой пары
    -- Эти значения вычисляются
    firstLine FLOAT - линия цены отделяющая первую треть от второй трети
    secondLine FLOAT - линия цены отделяющая вторую треть от третьей трети 
    middleLine FLOAT - серединная линия цены 
    level INTEGER - диапазон цены [1-4]
    monthsDiff INTEGER - сколько месяцев торгуется монета
    """
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS symbols (
        symbol TEXT PRIMARY KEY,
        dateLastCheck INTEGER,
        lastPrice FLOAT,
        volumeUsdt INTEGER
        maxPrice FLOAT,
        minPrice FLOAT,
        firstLine FLOAT,
        secondLine FLOAT,
        middleLine FLOAT,
        level INTEGER,
        monthsDiff INTEGER
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
    return conn


def update_date_last_check(appset, symbol, date_last_check):
    """
    Обновляет дату последнего обновления цены в базе данных.
    """
    print(f"Обновляем дату последнего обновления цены "
          f"{date_last_check} - {unixtime_to_datetime(date_last_check)} для {symbol}")
    cursor = appset.conn_db.cursor()
    cursor.execute("UPDATE symbols SET dateLastCheck = ? WHERE symbol = ?", (date_last_check, symbol))
    appset.conn_db.commit()
    cursor.close()
