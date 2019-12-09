# Projeto: Bem-te-vi
# Autor: Diego Abreu
# Arquivo: modelo_analise_de_sentimentos.py
# Resumo: Este arquivo contém:
#       - Algoritmo MultinomialNB utilizado para classificar sentimentos dos tweets;
#       - Algoritmo Vader utilizado para classificar sentimentos de emojis extraídos dos tweets.
# -------------------------------------------------------------------
# Importação de pacotes:
import pandas as pd
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import TfidfVectorizer
import nltk
from nltk.corpus import stopwords
import emoji
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
# Não mostra avisos e alertas sobre versões desatualizadas e etc.
import sys
if not sys.warnoptions:
    import warnings
    warnings.simplefilter("ignore")
# -------------------------------------------------------------------
# Criação do Algoritmo de análise de sentimentos:
# Leitura dos dados de treino:
df_treino = pd.read_csv("dados_base_analise_de_sentimentos/df_treino.csv")
# Importação de stop words em português do pacote NLTK:
portugues_stops = set(stopwords.words('portuguese'))
# Adição de novas stop words identificadas como faltantes em análises anteriores:
novas_stopwords = ['tá', 'ta', 'pra','pro']
portugues_stops = portugues_stops.union(novas_stopwords)
# Função de tratamento do texto:
tf_vectorizer = TfidfVectorizer(stop_words = portugues_stops,analyzer='word', ngram_range=(1, 1),
                                lowercase=True, use_idf=True, strip_accents='unicode')
# Definição de variáveis de treinamento e aplicação da função de tratamento de texto:
treino_x = tf_vectorizer.fit_transform(df_treino['tweets'])
treino_y = df_treino['sentimento']
# Criação do modelo de análise:
classificador_MNB = MultinomialNB()
# Treinamento do modelo:
classificador_MNB.fit(treino_x, treino_y)
# -------------------------------------------------------------------
# Criação do modelo Vader:
analyser = SentimentIntensityAnalyzer()
def vader(text):
    score = analyser.polarity_scores(text)
    lb = score['compound']
    if lb >= 0.05:
        return 'Positivo'
    elif (lb > -0.05) and (lb < 0.05):
        return 'Neutro'
    else:
        return 'Negativo'
