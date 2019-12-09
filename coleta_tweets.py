# Projeto: Bem-te-vi
# Autor: Diego Abreu
# Arquivo: coleta_tweets.py
# Resumo: Este arquivo contém:
#       - Algoritmo para coleta de tweets;
#       - Algoritmo de criptografia usado para camuflar a identificação dos usuários.
# -------------------------------------------------------------------
# -------------------------------------------------------------------
# Importação de pacotes:
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import json
from unidecode import unidecode
from itsdangerous import URLSafeSerializer
from pymongo import MongoClient
import time
# -------------------------------------------------------------------
# Importação do arquivo chaves.py:
import chaves
# -------------------------------------------------------------------
# Autenticação com API do twitter:
auth = OAuthHandler(chaves.consumer_key, chaves.consumer_secret)
auth.set_access_token(chaves.access_token, chaves.access_token_secret)
# Função de criptografia:
cripto = URLSafeSerializer(chaves.cripto_key)
# -------------------------------------------------------------------
# Função de filtragem de tweets:
class Filtratweets(StreamListener):
    def on_data(self, dados):
        tweet = json.loads(dados)
        created_at = tweet["created_at"]
        cp_screen_name = cripto.dumps(tweet["user"]["screen_name"])
        verified = tweet["user"]["verified"]
        text = tweet["text"]
        location = tweet["user"]["location"]

        obj = {"created_at":created_at,
               "cp_screen_name": cp_screen_name,
               "verified":verified,
               "text":text,
               "location":location}

        tweetind = col.insert_one(obj).inserted_id
        print (obj)
        return True

    def on_error(self, status_code):
        if status_code == 420:
            return True
# Objeto filtragem de tweets
filtratweets = Filtratweets()
# Objeto captura de tweets, faz a conexão via API do Twitter
capturatweets = Stream(auth, listener = filtratweets, wait_on_rate_limit=True)
# -------------------------------------------------------------------
# Criação da conexão ao MongoDB
client = MongoClient('localhost', 27017)
# Criação do banco de dados
db = client[chaves.banco]
# Criação da collection
col = db[chaves.banco]
# -------------------------------------------------------------------
# Função que inicia a coleta de tweets:
def inicia_coleta():
    while True:
        try:
            capturatweets.filter(languages=["pt"], track=chaves.keywords)
        except:
            time.sleep(10)
            continue
# -------------------------------------------------------------------
# Inicia a coleta dos tweets
inicia_coleta()
