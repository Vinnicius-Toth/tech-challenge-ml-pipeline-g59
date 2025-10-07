from xgboost import XGBRegressor
import joblib
from logger import Logs
from export import salvar_artefato_no_minio

log = Logs("train", emoji="🧠")


def treinar_modelo(df):
    log.info("Iniciando o treinamento do modelo")
    
    df = df.dropna(subset=["valor_parcela", "lag_1m", "media_movel_3m"])
    features = ["lag_1m", "media_movel_3m", "trimestre", "uf_encoded"]
    X = df[features]
    y = df["valor_parcela"]

    model = XGBRegressor(n_estimators=100, max_depth=6)
    model.fit(X, y)

    salvar_artefato_no_minio(model, "bolsa_familia/xgb_model.pkl")
    log.info("Modelo treinado e salvo no MinIO")
    return model
