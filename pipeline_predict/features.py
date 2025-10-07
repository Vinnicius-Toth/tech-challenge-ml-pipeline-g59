from sklearn.preprocessing import LabelEncoder
import pandas as pd
from logger import Logs
from export import salvar_artefato_no_minio

log = Logs("features", emoji="💡")

def criar_features(df):
    log.info("Criando features...")

    df = df.sort_values(["nome_municipio", "ano", "mes"])
    df["data"] = pd.to_datetime(df["ano"].astype(str) + "-" + df["mes"].astype(str) + "-01")

    df["lag_1m"] = df.groupby("nome_municipio")["valor_parcela"].shift(1)
    df["media_movel_3m"] = df.groupby("nome_municipio")["valor_parcela"].rolling(3).mean().shift(1).reset_index(level=0, drop=True)
    df["trimestre"] = df["data"].dt.quarter

    le_uf = LabelEncoder()
    df["uf_encoded"] = le_uf.fit_transform(df["uf"])

    salvar_artefato_no_minio(le_uf, "bolsa_familia/label_encoder_uf.pkl")
    log.info("Features criadas e encoder salvo no MinIO")
    return df, le_uf
