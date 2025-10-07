from ingest import carregar_dados_gold
from features import criar_features
from train import treinar_modelo
from forecast import gerar_previsoes
from export import exportar_previsoes, salvar_artefato_no_minio
from minio_client import bucket_exists
from logger import Logs

log = Logs("ingest", emoji="▶️ ")


def main(ano_alvo_list):
    bucket_exists()

    log.info("🚀 Iniciando pipeline de predição")
    
    df = carregar_dados_gold()

    for ano_alvo in ano_alvo_list:
        df_feat, le_uf = criar_features(df)
        model = treinar_modelo(df_feat)
        df_previsoes = gerar_previsoes(df_feat, model, le_uf, ano_alvo)
        exportar_previsoes(df_previsoes, ano_alvo)

    log.info("🏁 Pipeline de predição finalizada")

if __name__ == "__main__":
    ano_alvo_list = [2025]
    main(ano_alvo_list)