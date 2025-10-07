import pandas as pd
import unidecode
from minio_client import client, verificar_objeto_ja_existe
from io import BytesIO
from logger import Logs

log = Logs("ingestao_raw", emoji="🥇")

def main(anomes: str):
    ano, mes = anomes[:4], anomes[4:]
    object_silver = f"bolsa_familia/silver/ano={ano}/mes={mes}/bolsa_familia_{anomes}.parquet"
    object_gold = f"bolsa_familia/gold/ano={ano}/mes={mes}/bolsa_familia_{anomes}.parquet"

    if verificar_objeto_ja_existe(object_gold):
        log.info(f"[{anomes}] - Objeto já existe na GOLD: {object_gold}. Pulando camada...")
        return

    log.info(f"[{anomes}] - Lendo {object_silver} a transformando para camada GOLD...")
    response = client.get_object("datalake", object_silver)
    df = pd.read_parquet(BytesIO(response.read()))

    df_agg = df.groupby(["nome_municipio", "uf"]).agg({
        "valor_parcela": "sum"
    }).reset_index()
    df_agg["ano"] = int(ano)
    df_agg["mes"] = int(mes)


    buffer = BytesIO()
    df_agg.to_parquet(buffer, index=False)
    buffer.seek(0)

    client.put_object("datalake", object_gold, data=buffer, length=buffer.getbuffer().nbytes)
    log.info(f"[{anomes}] - Arquivo salvo na GOLD: {object_gold}")