# Bybit

https://github.com/bybit-exchange/pybit

```commandline
pip install pybit
pip install matplotlib mplfinance
```


Статья - [Bybit OpenAPI Services: Transition from Legacy Version to New V5 API](https://announcements.bybit.com/en/article/bybit-openapi-services-transition-from-legacy-version-to-new-v5-api-blt25b43a5738c00765/)
Офф.док - [V5 API Documentation](https://bybit-exchange.github.io/docs/v5/intro)
Отсюда можно скачать исторические данные - https://www.bybit.com/derivatives/en/history-data

## SQL запросы

```sql
-- На Bybit капитализация (объёмы) меньше поэтому порог 4млн. нужно снижать.
SELECT *
FROM symbols
WHERE monthsDiff > 8
  AND priceDistanceToMaxPct > 200
  AND (level = 1 OR level = 2)
  AND volumeUsdt > 1000000
ORDER BY volumeUsdt DESC, priceDistanceToMaxPct DESC, level DESC;

```