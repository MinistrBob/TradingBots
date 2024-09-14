import traceback
from pybit.unified_trading import HTTP
from SETTINGS import app_settings as appset
from sqlite_db import create_database, update_date_last_check, select_symbol
from spot_load_data_to_db import load_data_to_db
from spot_recomendation import get_recommendation, get_graph


def main():
    try:
        # Инициализация API и базы данных
        appset.bybit_api = HTTP(
            testnet=False,
            api_key=appset.api_key,
            api_secret=appset.api_secret,
        )
        appset.conn_db = create_database()
        # list_symbols = ['REEFUSDT', 'HIGHUSDT', 'ARUSDT', 'NOTUSDT', 'SANDUSDT', 'EGLDUSDT', 'RAYUSDT', 'BAKEUSDT', 'CSPRUSDT', 'MINAUSDT', 'QTUMUSDT', 'FLOWUSDT', 'RDNTUSDT', 'KSMUSDT']
        list_symbols = ['1INCHUSDT', '5IREUSDT', 'AAVEUSDT', 'ADAUSDT', 'APEUSDT', 'APTUSDT', 'ARBUSDT', 'ARKMUSDT',
                        'ATOMUSDT',
                        'AVAXUSDT', 'BLURUSDT', 'COREUSDT', 'CRVUSDT', 'DOGEUSDT',
                        'DOTUSDT', 'DYDXUSDT', 'ENSUSDT', 'EOSUSDT', 'FETUSDT', 'FILUSDT', 'FMBUSDT', 'FTMUSDT',
                        'GALAUSDT', 'GMTUSDT',
                        'HBARUSDT', 'HNTUSDT', 'ICPUSDT', 'IMXUSDT', 'INJUSDT',
                        'JASMYUSDT', 'LDOUSDT', 'LINKUSDT', 'LMWRUSDT', 'LTCUSDT', 'MASKUSDT', 'MATICUSDT', 'MEMEUSDT',
                        'NEARUSDT',
                        'OPUSDT', 'ORDIUSDT', 'POLUSDT', 'PPTUSDT', 'PYTHUSDT',
                        'ROOTUSDT', 'RUNEUSDT', 'SEIUSDT', 'SFUNDUSDT', 'SHIBUSDT', 'SNXUSDT', 'SSVUSDT', 'TIAUSDT',
                        'TOKENUSDT',
                        'TOMIUSDT', 'UNIUSDT', 'WLDUSDT', 'WWYUSDT', 'XCADUSDT',
                        'XLMUSDT']
        for symbol in list_symbols:
            result = select_symbol(symbol)
            if result:
                # print(result)
                print(f"{result[0]}\t{result[3]}\t{result[9]}\t{result[10]}\t{result[11]}")
            else:
                print(f"{symbol}\tNone\tNone\tNone\tNone")
    except Exception:
        print(traceback.format_exc())
    finally:
        # Гарантированное закрытие соединения
        if hasattr(appset, 'conn_db') and appset.conn_db is not None:
            try:
                appset.conn_db.close()
            except Exception as e:
                print("Ошибка при закрытии соединения:", e)


if __name__ == "__main__":
    main()
