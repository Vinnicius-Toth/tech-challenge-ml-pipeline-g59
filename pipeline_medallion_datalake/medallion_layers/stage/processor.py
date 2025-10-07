from .downloader import baixar_csv_stream
from .uploader import subir_csv_para_minio
from minio_client import verificar_objeto_ja_existe
from logger import Logs
from concurrent.futures import ThreadPoolExecutor

log = Logs("processor", emoji="📥")

# def processar_em_lote(anomes):
#     # with ThreadPoolExecutor(max_workers=4) as executor:
#         # executor.map(processar_mes, anomes)
#     processar_mes(anomes)

def processar_mes(anomes: str):
    ano, mes = anomes[:4], anomes[4:]
    object_name = f"bolsa_familia/stage/ano={ano}/mes={mes}/bolsa_familia_{anomes}.csv"

    if verificar_objeto_ja_existe(object_name):
        log.info(f"[{anomes}] - Objeto já existe na STAGE: {object_name}. Pulando camada...")
        return

    try:
        log.info(f"[{anomes}] - Iniciando download...")
        csv_stream = baixar_csv_stream(anomes)
        subir_csv_para_minio(csv_stream, anomes)
    except Exception as e:
        log.error(f"Erro em {anomes}: {str(e)}")