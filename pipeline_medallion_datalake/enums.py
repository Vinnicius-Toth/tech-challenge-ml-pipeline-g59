from enum import Enum

class MesesDisponiveis(Enum):
    JAN = "01"
    FEV = "02"
    MAR = "03"
    ABR = "04"
    MAI = "05"
    JUN = "06"
    JUL = "07"
    AGO = "08"
    SET = "09"
    OUT = "10"
    NOV = "11"
    DEZ = "12"

ANOS_DISPONIVEIS = [str(ano) for ano in range(2013, 2022)]

url_files = "https://portaldatransparencia.gov.br/download-de-dados/bolsa-familia-saques"