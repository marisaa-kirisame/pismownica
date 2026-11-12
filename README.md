# Pismownica

**Pismownica** to skrypt, który przyjmuje listę słówek po japońsku i generuje plik .csv gotowy do użycia jako zestaw fiszek w Anki czy Quizlet. Fiszki zawierają słowo w kanji, czytanie (kun'yomi w katakanie, on'yomi lub ateji w hiraganie) oraz znaczenie.

## Przykład działania

Obecnie program przyjmuje słowa jako argumenty konsolowe. Gdy wywołamy:
```
uv run main.py 鴎 烏 雀
```
otrzymamy plik `out.csv` o treści:
```
鴎;かもめ;mewa siwa, mewa pospolita
烏;からす;kruk, wrona
雀;すずめ;wróbel, wróbel mazurek
```
