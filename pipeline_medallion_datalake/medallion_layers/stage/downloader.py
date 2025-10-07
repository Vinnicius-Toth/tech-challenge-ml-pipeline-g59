import requests, zipfile, io
from logger import Logs
from enums import url_files

log = Logs("downloader", emoji="📥")

def baixar_csv_stream(anomes: str) -> io.BytesIO:
    url = f"{url_files}/{anomes}"
    headers = {"User-Agent": "Mozilla/5.0"}
    log.info(f"[{anomes}] - Baixando de {url}")
    response = requests.get(url, headers=headers, stream=True)
    if response.status_code != 200:
        log.error(f"[{anomes}] - Erro ao baixar {anomes}: {response.status_code}")
    zip_buffer = io.BytesIO(response.content)
    with zipfile.ZipFile(zip_buffer) as z:
        log.info(f"[{anomes}] - Extraindo CSV...")
        csv_name = [f for f in z.namelist() if f.endswith(".csv")][0]
        return z.open(csv_name)
