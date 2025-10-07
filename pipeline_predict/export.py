import joblib
from io import BytesIO
from minio_client import client
from logger import Logs

log = Logs("export", emoji="📥")

def exportar_previsoes(df_previsoes, ano):
    object_path = f"bolsa_familia/predictions/ano={ano}/previsoes_{ano}.parquet"
    buffer = BytesIO()
    df_previsoes.to_parquet(buffer, index=False)
    buffer.seek(0)

    client.put_object("datalake", object_path, data=buffer, length=buffer.getbuffer().nbytes)
    log.info(f"Previsões salvas em {object_path}")

def salvar_artefato_no_minio(objeto, caminho_minio):
    buffer = BytesIO()
    joblib.dump(objeto, buffer)
    buffer.seek(0)

    client.put_object(
        bucket_name="artefatos",
        object_name=caminho_minio,
        data=buffer,
        length=buffer.getbuffer().nbytes
    )
    log.info(f"Artefato salvo em: {caminho_minio}")
