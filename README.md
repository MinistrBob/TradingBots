# TradingBots
Studying APIs of various exchanges.  

There will be several research projects here, each with its own venv. 

```commandline
pip freeze | Out-File -Encoding UTF8 c:\MyGit\TradingBots\requirements.txt
pip install -r c:\MyGit\TradingBots\requirements.txt
```

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
