import requests
from sqlalchemy import create_engine, Column, String, Float, Integer, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime
from time import sleep
from dotenv import load_dotenv
import os
load_dotenv()   

#configurações do banco de dados
DATABASE_URL = os.getenv('DATABASE_KEY')


#criação engine e sessão
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
Base = declarative_base()

#Definição do modelo de dados
class BitcoinDados(Base):
    __tablename__ = 'bitcoin_dados'

    id = Column(Integer, primary_key=True)
    valor = Column(Float)
    criptomoeda = Column(String(10))
    moeda = Column(String(10))
    timestamp = Column(DateTime)
    
# Criação das tabelas no banco de dados
Base.metadata.create_all(engine)

def extrair():
    url = 'https://api.coinbase.com/v2/prices/spot'
    response = requests.get(url)
    return response.json()

def transformar(dados_json):
    valor = float(dados_json['data']['amount'])
    criptomoeda = dados_json['data']['base']
    moeda = dados_json['data']['currency']

    dados_tratados = BitcoinDados(
        valor= valor,
        criptomoeda= criptomoeda,
        moeda= moeda,
        timestamp= datetime.now()
    )
    return dados_tratados

def salvar_dentro_sqlalchemy(dados):
    """"Salva os dados tratados no banco de dados usando SQLAlchemy."""
    with Session() as session:
        session.add(dados)
        session.commit()
        print("Dados inseridos no banco de dados com sucesso!")



if __name__ == '__main__':
    while True:
        dados_json = extrair()
        dados_tratados = transformar(dados_json)
    
        print("Dados extraídos e transformados com sucesso!")
        salvar_dentro_sqlalchemy(dados_tratados)
        print('Aguardando 15 segundos antes de repetir...')
        sleep(15)  # Aguarda 15 segundos antes de repetir