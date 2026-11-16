"""Tiene aggiornati soul.json e pz8.json: prova i domini conosciuti, segue i redirect e mette in testa
quelli che rispondono con il sito giusto. I file contengono SOLO l'elenco degli URL (base, senza barra).
Uso: python3 tools/probe.py   (esce con 0; stampa "changed" se ha riscritto qualcosa)."""
import json, re, sys, urllib.request, urllib.error
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0 Safari/537.36"

# Domini da provare oltre a quelli già nel file (vecchi e nuovi conosciuti): la lista si può allungare qui
APPS = {
    "soul": {
        "extra": ["https://animeunity.cx", "https://www.animeunity.co", "https://www.animeunity.to",
                  "https://www.animeunity.so", "https://www.animeunity.it", "https://www.animeunity.tv"],
        # firma del sito: pagina Inertia della home di AnimeUnity
        "signature": lambda html: "data-page=" in html and "animeunity" in html.lower(),
    },
    "pz8": {
        "extra": ["https://streamingcommunityz.boo", "https://streamingcommunity.boo", "https://streamingunity.to",
                  "https://streamingcommunity.computer", "https://streamingcommunity.spa"],
        # firma: pagina Inertia della home di StreamingCommunity
        "signature": lambda html: "data-page=" in html and ("streamingcommunity" in html.lower() or "Home/Home" in html),
    },
}


def fetch(url):
    """GET con redirect: ritorna (url finale, html) oppure (None, None)."""
    req = urllib.request.Request(url + "/", headers={"User-Agent": UA, "Accept": "text/html,*/*"})
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            return r.geturl(), r.read(400_000).decode("utf-8", "ignore")
    except Exception as e:  # noqa: BLE001
        print(f"  {url}: {e}")
        return None, None


def base_of(url):
    m = re.match(r"^(https?://[^/]+)", url)
    return m.group(1).rstrip("/") if m else None


def update(app, cfg):
    path = ROOT / f"{app}.json"
    current = json.loads(path.read_text()) if path.exists() else []
    candidates = []
    for u in current + cfg["extra"]:
        u = u.rstrip("/")
        if u and u not in candidates:
            candidates.append(u)
    working = []
    for u in candidates:
        fin, html = fetch(u)
        if not fin or not html:
            continue
        b = base_of(fin)
        ok = cfg["signature"](html)
        print(f"  {u} -> {b} {'OK' if ok else 'non è il sito'}")
        if ok and b and b not in working:
            working.append(b)
    if not working:
        print(f"{app}: nessun dominio risponde, file lasciato com'era")
        return False
    # Prima quelli che funzionano, poi gli altri del file (reindirizzano ancora verso il sito, o torneranno)
    new = working + [u for u in current if u not in working]
    if new == current:
        return False
    path.write_text(json.dumps(new, indent=2) + "\n")
    print(f"{app}: aggiornato -> {new}")
    return True


if __name__ == "__main__":
    changed = False
    for app, cfg in APPS.items():
        print(f"== {app}")
        changed = update(app, cfg) or changed
    print("changed" if changed else "unchanged")
    sys.exit(0)
