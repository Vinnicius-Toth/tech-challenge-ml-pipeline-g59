import pandas as pd
from minio_client import client, verificar_objeto_ja_existe
from io import BytesIO
from logger import Logs

log = Logs("ingestao_raw", emoji="🥉")

def main(anomes: str):
    ano, mes = anomes[:4], anomes[4:]
    object_csv = f"bolsa_familia/stage/ano={ano}/mes={mes}/bolsa_familia_{anomes}.csv"
    object_parquet = f"bolsa_familia/raw/ano={ano}/mes={mes}/bolsa_familia_{anomes}.parquet"

    if verificar_objeto_ja_existe(object_parquet):
        log.info(f"[{anomes}] - Objeto já existe na RAW: {object_parquet}. Pulando camada...")
        return
    try:
        log.info(f"[{anomes}] - Convertendo {object_csv} para Parquet e salvando como {object_parquet} para camada RAW...")
        response = client.get_object("datalake", object_csv)
        csv_bytes = BytesIO(response.read())  # lê os bytes e prepara para Pandas
        df = pd.read_csv(csv_bytes, sep=";", encoding="windows-1252")

        buffer = BytesIO()
        df.to_parquet(buffer, index=False)
        buffer.seek(0)

        client.put_object(
            "datalake",
            object_parquet,
            data=buffer,
            length=buffer.getbuffer().nbytes,
            content_type="application/octet-stream"
        )

        log.info(f"[{anomes}] - Arquivo salvo na RAW: {object_parquet}")
    except Exception as e:
        log.error(f"Falha ao converter {object_csv}: {str(e)}")

