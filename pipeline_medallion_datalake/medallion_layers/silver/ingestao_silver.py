import pandas as pd
import unidecode
from minio_client import client, verificar_objeto_ja_existe
from io import BytesIO
from logger import Logs

log = Logs("ingestao_raw", emoji="🥈")

def transformar_valor_parcela(df):
    if "valor_parcela" in df.columns:
            df["valor_parcela"] = (
            df["valor_parcela"]
            .astype(str)
            .str.replace(",", ".", regex=False)
            .str.replace(r"[^\d\.]", "", regex=True)
            .str.strip()
            )
            df["valor_parcela"] = pd.to_numeric(df["valor_parcela"], errors="coerce")

def normalizar_coluna(col):
    col = unidecode.unidecode(col)  # remove acentos
    col = col.lower().strip()
    col = col.replace(" ", "_").replace("-", "_")
    col = col.replace("__", "_")
    return col

def main(anomes: str):
    ano, mes = anomes[:4], anomes[4:]
    object_raw = f"bolsa_familia/raw/ano={ano}/mes={mes}/bolsa_familia_{anomes}.parquet"
    object_silver = f"bolsa_familia/silver/ano={ano}/mes={mes}/bolsa_familia_{anomes}.parquet"

    if verificar_objeto_ja_existe(object_silver):
        log.info(f"[{anomes}] - Objeto já existe na SILVER: {object_silver}. Pulando camada...")
        return

    try:
        log.info(f"[{anomes}] - Lendo {object_raw} e transformando para camada SILVER...")
        response = client.get_object("datalake", object_raw)
        df = pd.read_parquet(BytesIO(response.read()))

        # Corrige e padroniza os nomes das colunas
        df.columns = [normalizar_coluna(col) for col in df.columns]

        transformar_valor_parcela(df)

        df.dropna(subset=["nome_municipio", "valor_parcela"], inplace=True)

        buffer = BytesIO()
        df.to_parquet(buffer, index=False)
        buffer.seek(0)

        client.put_object("datalake", object_silver, data=buffer, length=buffer.getbuffer().nbytes)
        log.info(f"[{anomes}] - Arquivo salvo na SILVER: {object_silver}")
    except Exception as e:
        log.error(f"Erro ao processar {anomes}: {str(e)}")