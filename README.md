# 🚀 tech-challenge-ml-pipeline-g59

Projeto Tech Challenge - Fase 3 - Engenharia de Machine Learning  
Pipeline de Predição de Valores do Bolsa Família

---

## 📚 Visão Geral

Este projeto implementa um pipeline completo de Machine Learning para prever os valores mensais do programa Bolsa Família por município, utilizando dados históricos, engenharia de features, treinamento de modelo XGBoost e exportação de previsões e artefatos para o MinIO. Os resultados podem ser integrados ao Power BI para visualização.

---

## 🗂️ Estrutura do Projeto

```
tech-challenge-ml-pipeline-g59/
├── pipeline_medallion_datalake/   # Pipeline ETL Medallion (Stage, Raw, Silver, Gold)
│   ├── medallion_layers/
│   │   ├── stage/
│   │   ├── raw/
│   │   ├── silver/
│   │   └── gold/
│   ├── enums.py
│   ├── logger.py
│   ├── main.py
│   ├── minio_client.py
│   └── utils.py
├── pipeline_predict/              # Pipeline de predição ML
│   ├── ingest.py
│   ├── features.py
│   ├── train.py
│   ├── forecast.py
│   ├── export.py
│   ├── minio_client.py
│   ├── logger.py
│   └── main.py
├── data/                          # Dados auxiliares e arquivos consolidados
│   ├── Coordenadas_Municipios_IBGE.json   # Coordenadas geográficas dos municípios
│   ├── Coordenadas_UF_IBGE.json           # Coordenadas geográficas dos estados
│   └── *.parquet                          # Arquivos Parquet consolidados para análise local
├── artefatos/                     # Arquivo PowerBI
└── README.md
```

---

## 🔗 Pipeline de Dados Datalake

### pipeline_medallion_datalake

O pipeline `pipeline_medallion_datalake` é responsável por toda a ingestão, limpeza, transformação e organização dos dados em múltiplas camadas no MinIO, seguindo o padrão Medallion Architecture:

- **Stage:** Recebe os dados brutos, exatamente como foram extraídos da fonte do [Bolsa Familia](https://portaldatransparencia.gov.br/download-de-dados/bolsa-familia-saques).
- **Raw:** Realiza pequenas limpezas e padronizações, mantendo a granularidade original, convertendo em parquet.
- **Silver:** Aplica transformações, normalizações e enriquecimentos, tornando os dados prontos para análise.
- **Gold:** Dados agregados e otimizados para consumo analítico e modelagem, particionados por ano/mês.

O processo é orquestrado pelo script [`main.py`](pipeline_medallion_datalake/main.py), que executa cada etapa sequencialmente e salva os arquivos Parquet em buckets e pastas específicas do MinIO.

---

## 🔗 Pipeline de Predição

### pipeline_predict

O pipeline `pipeline_predict` é responsável por todo o processo de previsão utilizando Machine Learning:

1. **Ingestão dos Dados Gold:**  
   O script [`ingest.py`](pipeline_predict/ingest.py) lê todos os arquivos Parquet da camada gold do MinIO e concatena em um único DataFrame para modelagem.

2. **Engenharia de Features:**  
   O script [`features.py`](pipeline_predict/features.py) cria variáveis históricas (lags, médias móveis, trimestre, etc.) e codifica variáveis categóricas, salvando o encoder no MinIO.

3. **Treinamento do Modelo:**  
   O script [`train.py`](pipeline_predict/train.py) treina um modelo XGBoost para prever o valor da parcela do Bolsa Família, salvando o modelo treinado no bucket de artefatos.

4. **Geração de Previsões:**  
   O script [`forecast.py`](pipeline_predict/forecast.py) utiliza o modelo treinado para gerar previsões mês a mês para cada município, considerando os últimos valores históricos.

5. **Exportação de Resultados:**  
   O script [`export.py`](pipeline_predict/export.py) salva as previsões e artefatos (modelo, encoder) no MinIO, organizando por ano de previsão.

6. **Integração com Power BI:**  
   Os arquivos Parquet de previsões podem ser baixados do MinIO e utilizados diretamente no Power BI para análise e visualização.

---

## 🐳 Como subir o MinIO com Docker

Para executar o MinIO localmente utilizando Docker, siga os passos abaixo:

```sh
docker run -d -p 9000:9000 -p 9001:9001 \
  --name minio \
  -e "MINIO_ROOT_USER=admin" \
  -e "MINIO_ROOT_PASSWORD=admin123" \
  minio/minio server /data --console-address ":9001"
```

- O MinIO estará disponível em: [http://localhost:9000](http://localhost:9000)
- O painel de administração estará em: [http://localhost:9001](http://localhost:9001)
- Usuário: `admin`
- Senha: `admin123`

> **Observação:** Não é necessário criar os buckets manualmente, pois as pipelines já realizam essa tarefa automaticamente.

---

## ⚙️ Arquitetura

> ![Exemplo de arquitetura](docs/arquitetura_pipeline_bolsa_familia.png)  
> *(Adicione um desenho da arquitetura do seu pipeline aqui, se desejar)*

---

## 🔎 Como Executar

### 1. Requisitos

- Python 3.10+
- MinIO rodando localmente (`localhost:9000`)
- Bibliotecas: pandas, xgboost, scikit-learn, joblib, minio, pyarrow

Instale as dependências:

```sh
pip install -r requirements.txt
```

### 2. Execute o Pipeline Medallion

```sh
cd pipeline_medallion_datalake
python main.py
```

### 3. Execute o Pipeline de Predição

```sh
cd pipeline_predict
python main.py
```

### 4. Visualize no Power BI

- Baixe os arquivos Parquet de previsões do MinIO para uma pasta local.
- No Power BI: Obter Dados → Pasta → Selecione a pasta com os arquivos.

---

## 📝 Variáveis e Configurações

- Buckets MinIO: `datalake` (dados), `artefatos` (modelos/encoders)
- Dados auxiliares: [`data/Coordenadas_UF_IBGE.json`](data/Coordenadas_UF_IBGE.json)

---

## 🔄 CI/CD

Este projeto pode ser facilmente integrado a pipelines de CI/CD e orquestradores como Airflow ou Task Scheduler para automação.

---

## 🧰 Tecnologias Utilizadas

- Python 3.10+
- Pandas
- XGBoost
- Scikit-learn
- MinIO
- Power BI

---

## 👨‍💻 Desenvolvedores

- Vinnicius Toth – Engenheiro de Dados e Machine Learning  
- G59 Team – FIAP Tech Challenge 3

---