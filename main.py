from fastapi import FastAPI
import pandas as pd
import random
import os
from datetime import datetime, timedelta

app = FastAPI(title="API Logs de Energia")

def gerar_logs():
    status_list = [
        'NORMAL',
        'ALERTA: SOBRECARGA',
        'ERRO: QUEDA DE TENSAO',
        'ALERTA: ALTA TEMPERATURA'
    ]

    dispositivos = [
        'Transformador_01',
        'Disjuntor_Principal',
        'Rele_Protecao_A3',
        'Banco_Capacitores'
    ]

    data_inicial = datetime.now() - timedelta(days=7)
    logs = []

    for i in range(100):
        data = data_inicial + timedelta(hours=i)
        dispositivo = random.choice(dispositivos)
        status = random.choice(status_list)
        tensao = round(random.uniform(12.0, 14.0), 2)

        logs.append([
            data.strftime('%Y-%m-%d %H:%M:%S'),
            dispositivo,
            status,
            tensao
        ])

    df = pd.DataFrame(logs, columns=[
        'Timestamp', 'Dispositivo', 'Status', 'Tensao_kV'
    ])

    df.to_csv('logs_clp_energia.csv', index=False)

def analisar_logs():
    if not os.path.exists('logs_clp_energia.csv'):
        return {"erro": "Arquivo não encontrado"}

    df = pd.read_csv('logs_clp_energia.csv')

    df['Status'] = df['Status'].fillna('').astype(str).str.upper()

    total = len(df)
    erros = df['Status'].str.contains('ERRO', na=False).sum()
    alertas = df['Status'].str.contains('ALERTA', na=False).sum()

    falhas = df[df['Status'] != 'NORMAL']['Dispositivo'].value_counts().to_dict()

    return {
        "total": total,
        "erros": int(erros),
        "alertas": int(alertas),
        "falhas": falhas
    }

@app.get("/")
def home():
    return {"status": "API online"}

@app.get("/gerar")
def gerar():
    gerar_logs()
    return {"msg": "Logs gerados"}

@app.get("/analisar")
def analisar():
    return analisar_logs()
