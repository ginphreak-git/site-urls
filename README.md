# site-urls

Elenchi dei domini dei siti usati dalle app Soul e PZ8, letti dalle app all'avvio:

- `soul.json`: AnimeUnity
- `pz8.json`: StreamingCommunity

Ogni file è solo un elenco di URL base in ordine di preferenza. Il workflow `Aggiorna i domini` li verifica
ogni 6 ore (`tools/probe.py`): segue i redirect, controlla che la pagina sia davvero il sito e mette in testa
i domini che rispondono. Per aggiungere domini nuovi da provare basta allungare la lista `extra` nello script.

URL letti dalle app:

- https://raw.githubusercontent.com/ginphreak-git/site-urls/main/soul.json
- https://raw.githubusercontent.com/ginphreak-git/site-urls/main/pz8.json

## App Android

- Soul: https://github.com/ginphreak-git/site-urls/raw/main/apps/Soul-Android-0.1.0.apk
- PZ8: https://github.com/ginphreak-git/site-urls/raw/main/apps/PZ8-Android-0.1.0.apk
