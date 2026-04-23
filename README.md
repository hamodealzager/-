# Forex Intellect (Starter)

مشروع أولي لمنصة **Forex Intellect** للتحليل والتداول الذكي.

## تشغيل سريع

```bash
python3 src/forex_intellect.py --symbol EUR/USD --price 1.0842 --plan day
```

## المزايا الحالية

- تغطية فئات الأسواق: majors / minors / exotics / commodities.
- محرك تحليل أولي يدمج RSI + MACD + Bollinger + Trend + News Impact + Sentiment.
- مولّد صفقات يضمن حدًا أدنى لنسبة المخاطرة/العائد **1:2** على الهدف الأول.
- 3 خطط تداول: scalping / day / swing.

## الاختبارات

```bash
python3 -m unittest discover -s tests -p "test_*.py"
```
