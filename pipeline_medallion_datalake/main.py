from medallion_layers.stage.ingestao_stage import main as ingestao_stage
from medallion_layers.raw.ingestao_raw import main as ingestao_raw
from medallion_layers.silver.ingestao_silver import main as ingestao_silver
from medallion_layers.gold.ingestao_gold import main as ingestao_gold
from minio_client import bucket_exists
from logger import Logs
from enums import MesesDisponiveis, ANOS_DISPONIVEIS
from utils import gerar_lista_anomes
from concurrent.futures import ThreadPoolExecutor

log = Logs("orquestrador", emoji="▶️ ")

def executar_pipeline(anomes_list):
    def executar_etapas(anomes):
        try:
            log.info(f"▶️  Iniciando pipeline para {anomes}")
            ingestao_stage(anomes)         # Baixa e envia CSV para stage
            ingestao_raw(anomes)           # Converte para Parquet na raw
            ingestao_silver(anomes)        # Limpa e estrutura na silver
            ingestao_gold(anomes)          # Agrega e enriquece na gold
            log.info(f"✅ Pipeline finalizado para {anomes}")
        
        except Exception as e:
            log.error(f"❌ Erro em {anomes}: {str(e)}")

    with ThreadPoolExecutor(max_workers=4) as executor:
        executor.map(executar_etapas, anomes_list)

if __name__ == "__main__":
    log.info("🚀 Iniciando orquestrador da pipeline")
    
    # Gera lista de anos e meses disponíveis
    anomes_list = gerar_lista_anomes(ANOS_DISPONIVEIS, MesesDisponiveis)

    # Verificar existência do bucket
    bucket_exists()
      
    # Executa a pipeline para cada ano-mês em paralelo
    executar_pipeline(anomes_list)
    
    log.info("🏁 Orquestrador finalizado")
