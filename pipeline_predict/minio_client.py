from minio import Minio
from minio.error import S3Error
from logger import Logs

log = Logs("minio_client", emoji="📥")


client = Minio(
    "localhost:9000",
    access_key="admin",
    secret_key="admin123",
    secure=False
)

def bucket_exists(bucket="artefatos"):
    if not client.bucket_exists(bucket):
        log.info(f'Criando bucket {bucket}')
        client.make_bucket(bucket)
        return 
    
    log.info(f'Bucket: {bucket} já exitente. Iniciando processamento.')

    
def verificar_objeto_ja_existe(object_name: str) -> bool:
    try:
        client.stat_object("artefatos", object_name)
        return True
    except S3Error:
        return False
