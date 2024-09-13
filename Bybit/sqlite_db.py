import sqlite3
from utils import unixtime_to_datetime
from settings import app_settings as appset
import traceback
from pybit.unified_trading import HTTP


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
    priceDistanceToMaxPct INTEGER - расстояние между текущей ценой и максимальной ценой в процентах
    """
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS symbols (
        symbol TEXT PRIMARY KEY,
        dateLastCheck INTEGER,
        lastPrice FLOAT,
        volumeUsdt INTEGER,
        maxPrice FLOAT,
        minPrice FLOAT,
        firstLine FLOAT,
        secondLine FLOAT,
        middleLine FLOAT,
        level INTEGER,
        monthsDiff INTEGER,
        priceDistanceToMaxPct INTEGER
    )
    ''')
    # Создание таблицы kline_history с внешним ключом, ссылающимся на symbols
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS kline_history (
        startTime INTEGER,
        symbol TEXT,
        open FLOAT,
        high FLOAT,
        low FLOAT,
        close FLOAT,
        volume FLOAT,
        turnover FLOAT,
        FOREIGN KEY (symbol) REFERENCES symbols(symbol),
        PRIMARY KEY (startTime, symbol)  -- Уникальность на комбинацию startTime и symbol
    );
    ''')
    # Создание таблицы kline_history с внешним ключом, ссылающимся на symbols
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS orders (
        symbol TEXT,
        orderType TEXT,
        orderLinkId TEXT,
        orderId TEXT,
        avgPrice FLOAT,
        cancelType TEXT,
        stopOrderType TEXT,
        lastPriceOnCreated TEXT,
        orderStatus TEXT,
        takeProfit TEXT,
        cumExecValue TEXT,
        smpType TEXT,
        triggerDirection INTEGER,
        blockTradeId TEXT,
        isLeverage TEXT,
        rejectReason TEXT,
        price FLOAT,
        orderIv TEXT,
        createdTime INTEGER,
        tpTriggerBy TEXT,
        positionIdx INTEGER,
        timeInForce TEXT,
        leavesValue TEXT,
        updatedTime INTEGER,
        side TEXT,
        smpGroup INTEGER,
        triggerPrice TEXT,
        cumExecFee TEXT,
        leavesQty TEXT,
        slTriggerBy TEXT,
        closeOnTrigger BOOLEAN,
        cumExecQty TEXT,
        reduceOnly BOOLEAN,
        qty FLOAT,
        stopLoss TEXT,
        smpOrderId TEXT,
        triggerBy TEXT
    );
    ''')
    conn.commit()
    return conn


def update_date_last_check(symbol, date_last_check):
    """
    Обновляет дату последнего обновления цены в базе данных.
    """
    print(f"Обновляем дату последнего обновления цены "
          f"{date_last_check} - {unixtime_to_datetime(date_last_check)} для {symbol}")
    cursor = appset.conn_db.cursor()
    cursor.execute("UPDATE symbols SET dateLastCheck = ? WHERE symbol = ?", (date_last_check, symbol))
    appset.conn_db.commit()
    cursor.close()


def select_recommendations_symbols():
    """
    Получить список рекомендованных пар отобранных по определённым условиям.
    ('SANDUSDT', 1725235200000, 0.23768, 1118543, 8.48992, 0.20807, 2.968686666666667, 5.729303333333334, 4.348995, 1, 34, 3471)
    """
    cursor = appset.conn_db.cursor()
    # SQL-запрос
    query = """
    SELECT *
    FROM symbols
    WHERE monthsDiff > 8
      AND priceDistanceToMaxPct > 200
      AND (level = 1 OR level = 2)
      AND volumeUsdt > 1000000
    ORDER BY volumeUsdt DESC, priceDistanceToMaxPct DESC, level DESC;
    """
    cursor.execute(query)
    results = cursor.fetchall()
    if cursor is not None:
        cursor.close()
    return results


def select_symbol(symbol):
    """
    Получить список рекомендованных пар отобранных по определённым условиям.
    ('SANDUSDT', 1725235200000, 0.23768, 1118543, 8.48992, 0.20807, 2.968686666666667, 5.729303333333334, 4.348995, 1, 34, 3471)
    """
    cursor = appset.conn_db.cursor()
    # SQL-запрос
    query = f"""
    SELECT *
    FROM symbols
    WHERE symbol = '{symbol}';
    """
    cursor.execute(query)
    results = cursor.fetchone()
    if cursor is not None:
        cursor.close()
    return results


def main():
    try:
        appset.bybit_api = HTTP(
            testnet=False,
            api_key=appset.api_key,
            api_secret=appset.api_secret,
        )
        appset.conn_db = create_database()
    except Exception:
        print(traceback.format_exc())
    finally:
        # Гарантированное закрытие соединения
        if appset.conn_db is not None:
            try:
                appset.conn_db.close()
            except Exception as e:
                print("Ошибка при закрытии соединения:", e)


if __name__ == '__main__':
    main()
