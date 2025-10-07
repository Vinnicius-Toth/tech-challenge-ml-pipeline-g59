from minio_client import client
from logger import Logs

log = Logs("uploader", emoji="📥")

def subir_csv_para_minio(csv_stream, anomes: str):
    ano, mes = anomes[:4], anomes[4:]
    object_name = f"bolsa_familia/stage/ano={ano}/mes={mes}/bolsa_familia_{anomes}.csv"
    try:
        log.info(f"[{anomes}] - Enviando {object_name} para o MinIO...")
        client.put_object(
            "datalake",
            object_name,
            data=csv_stream,
            length=-1,
            part_size=10 * 1024 * 1024,
            content_type="application/octet-stream"
        )
        log.info(f"[{anomes}] - Arquivo salvo na STAGE: {object_name}")
        return
    except Exception as e:
        log.error(f"Erro ao enviar {object_name} para o MinIO: {str(e)}")
    
    
