import pandas as pd
from logger import Logs

log = Logs("forecast", emoji="🔮")

def gerar_previsoes(df, model, le_uf, ano_alvo):
    log.info(f"Gerando previsões para o ano {ano_alvo}...")
    municipios = df["nome_municipio"].unique()
    previsoes = []

    for municipio in municipios:
        df_muni = df[df["nome_municipio"] == municipio].sort_values("data")
        if df_muni.empty: continue

        ultimo = df_muni.iloc[-1]
        for mes in range(1, 13):
            nova_data = pd.to_datetime(f"{ano_alvo}-{mes}-01")
            entrada = {
                "nome_municipio": municipio,
                "uf": ultimo["uf"],
                "ano": ano_alvo,
                "mes": mes,
                "trimestre": nova_data.quarter,
                "lag_1m": ultimo["valor_parcela"],
                "media_movel_3m": df_muni["valor_parcela"].tail(3).mean(),
                "uf_encoded": le_uf.transform([ultimo["uf"]])[0]
            }
            X_pred = pd.DataFrame([entrada])[["lag_1m", "media_movel_3m", "trimestre", "uf_encoded"]]
            entrada["valor_previsto"] = model.predict(X_pred)[0]
            previsoes.append(entrada)

    df_previsoes = pd.DataFrame(previsoes)
    log.info(f"Previsões geradas para {ano_alvo}: {df_previsoes.shape[0]} linhas")
    return df_previsoes