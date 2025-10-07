import pandas as pd
from io import BytesIO
from minio_client import client
from logger import Logs

log = Logs("ingest", emoji="🥇")

def carregar_dados_gold():
    prefix = "bolsa_familia/gold/"
    objects = client.list_objects("datalake", prefix=prefix, recursive=True)

    log.info(f"Carregando dados da camada GOLD: {prefix}")
    dfs = []
    for obj in objects:
        if obj.object_name.endswith(".parquet"):
            response = client.get_object("datalake", obj.object_name)
            df = pd.read_parquet(BytesIO(response.read()))
            dfs.append(df)

    if dfs:
        df_final = pd.concat(dfs, ignore_index=True)
        log.info(f"Total de linhas carregadas da GOLD: {df_final.shape[0]}")
        return df_final
    else:
        log.warning("Nenhum arquivo Parquet encontrado na camada gold.")
        return pd.DataFrame()