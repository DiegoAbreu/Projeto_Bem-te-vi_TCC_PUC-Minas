# Projeto: Bem-te-vi
# Autor: Diego Abreu
# Arquivo: dashboard.py
# Resumo: Este arquivo contém:
#       - Códigos de cálculos e análises;
#       - Código de criação do dashboard.
# -------------------------------------------------------------------
# -------------------------------------------------------------------
# Importação de pacotes Dash:
import dash
import dash_core_components as dcc
import dash_html_components as html
# Dash
app = dash.Dash(__name__)
# Pacotes e bibliotecas para análise
import pandas as pd
from unidecode import unidecode
import json
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from pymongo import MongoClient
import time
import datetime
import emoji
import chaves
import modelo_analise_de_sentimentos
from sklearn.feature_extraction.text import CountVectorizer
import dicionario_brasil
# -------------------------------------------------------------------
# Não mostra avisos e alertas sobre versões desatualizadas e processos etc.
import sys
if not sys.warnoptions:
    import warnings
    warnings.simplefilter("ignore")
# -------------------------------------------------------------------
# Banco de dados
# Criação da conexão ao MongoDB
client = MongoClient('localhost', 27017)
# Criação do banco de dados
db = client[chaves.banco]
# Criação da collection
col = db[chaves.banco]
# -------------------------------------------------------------------
# Layout do dashboard
def serve_layout():
    # criação de um dataset com dados retornados do MongoDB
    dataset = [{"created_at": item["created_at"],
                "cp_screen_name": item["cp_screen_name"],
                "verified": item["verified"],
                "text": item["text"],
                "location": item["location"],
               } for item in col.find()]
    # Criação do dataframe
    df = pd.DataFrame(dataset)
    # -------------------------------------------------------------------
    # Tratamento da váriavel created_at:
    # Função para formatar data/hora:
    def format_datetime(dt_series):
        def get_split_date(strdt):
            split_date = strdt.split()
            str_date = split_date[1] + ' ' + split_date[2] + ' ' + split_date[5] + ' ' + split_date[3]+ ' ' + split_date[4]
            return str_date
        dt_series = pd.to_datetime(dt_series.apply(lambda x: get_split_date(x)), format = '%b %d %Y %H:%M:%S %z')
        return dt_series
    # Cria nova variável para o horário correto:
    df['data_hora'] = format_datetime(df['created_at'])
    # Converte para o nosso fuso horário:
    df['data_hora'] = df['data_hora'].dt.tz_convert('America/Sao_Paulo')
    # -------------------------------------------------------------------
    # Quantidade total de tweets:
    total_tweets = len(df)
    # Cria uma variavél chamada "retweeted" que armazena se o conteúdo do tweet começa com RT ou não:
    df['retweeted'] = df['text'].str.startswith('RT')
    # Contagem dos retweets:
    retweets = len(df[df['retweeted'] == True])
    # Contagem dos originais:
    originais = len(df[df['retweeted'] == False])
    # Total tweets título:
    total_tt_st = str(total_tweets) + "  Tweets"
    # -------------------------------------------------------------------
    # Contagem de usuários únicos:
    qtd_usuarios_unicos = df['cp_screen_name'].nunique()
    # Contagem de usuários verificados:
    usuarios_verificados = df[df['verified'] == True]
    total_tt_verificados = len(usuarios_verificados)
    qtd_usuarios_verificados = usuarios_verificados['cp_screen_name'].nunique()
    # Contagem de usuários não verificados:
    usuarios_nao_verificados = df[df['verified'] == False]
    total_tt_nao_verificados = len(usuarios_nao_verificados)
    qtd_usuarios_nao_verificados = usuarios_nao_verificados['cp_screen_name'].nunique()
    # Total usuários título:
    total_us_st = str(qtd_usuarios_unicos) + " Usuários"
    # -------------------------------------------------------------------
    # Cria um dataframe com a quantidade de tweets por horário:
    tw_x_pd = df['data_hora'].value_counts().to_frame().reset_index()
    tw_x_pd.columns = ['data_hora', 'qtd_tweets']
    # Ordenar pelo horário:
    tw_x_pd = tw_x_pd.sort_values(by=['data_hora'])
    # -------------------------------------------------------------------
    # Aplicação da função de tratamento de texto:
    analise_sent_tweets = modelo_analise_de_sentimentos.tf_vectorizer.transform(df['text'])
    # Aplicação do modelo
    predicao_MNB = pd.Series(modelo_analise_de_sentimentos.classificador_MNB.predict(analise_sent_tweets))
    # Armazenamento dos resultados em uma nova variável chamada "analise_sentimento":
    df['analise_sentimento'] = predicao_MNB
    # Análise de emojis:
    # Função de extração:
    def extracao_de_emojis(str):
      return ' '.join(c for c in str if c in emoji.UNICODE_EMOJI)
    # Criação da nova variável contendo os emojis:
    df['emojis_extraidos'] = df['text'].apply(lambda x: extracao_de_emojis(x))
    # Aplicação do modelo Vader
    df['analise_sent_emoji'] = df['emojis_extraidos'].apply(lambda x: modelo_analise_de_sentimentos.vader(x))
    # Substituição das análises dos tweets com emojis
    df.loc[df['analise_sent_emoji'] == 'Positivo', 'analise_sentimento'] = 'Positivo'
    df.loc[df['analise_sent_emoji'] == 'Negativo', 'analise_sentimento'] = 'Negativo'
    # Contagem de sentimentos
    polaridade_sentimentos = pd.DataFrame(df['analise_sentimento'].value_counts()).reset_index()
    polaridade_sentimentos.columns = ['sentimento', 'num_de_tweets']
    # -------------------------------------------------------------------
    # Contagem de sentimentos por horário:
    # Criação de um dataframe para essa  análise:
    total_sents = pd.DataFrame()
    total_sents['horario'] = df['data_hora']
    total_sents['sentimento'] = df['analise_sentimento']
    # Contagem dos tweets positivos:
    total_sents_pos = total_sents[total_sents['sentimento'] == 'Positivo']
    total_sents_pos = total_sents_pos['horario'].value_counts().to_frame().reset_index()
    total_sents_pos.columns = ['data_hora', 'qtd_tweets']
    total_sents_pos = total_sents_pos.sort_values(by=['data_hora'])
    # Contagem dos tweets neutros:
    total_sents_neu = total_sents[total_sents['sentimento'] == 'Neutro']
    total_sents_neu = total_sents_neu['horario'].value_counts().to_frame().reset_index()
    total_sents_neu.columns = ['data_hora', 'qtd_tweets']
    total_sents_neu = total_sents_neu.sort_values(by=['data_hora'])
    # Contagem dos tweets negativos:
    total_sents_neg = total_sents[total_sents['sentimento'] == 'Negativo']
    total_sents_neg = total_sents_neg['horario'].value_counts().to_frame().reset_index()
    total_sents_neg.columns = ['data_hora', 'qtd_tweets']
    total_sents_neg = total_sents_neg.sort_values(by=['data_hora'])
    # -------------------------------------------------------------------
    # Contagem de hashtags e palavras mais presentes:
    verifica_hash = pd.DataFrame()
    verifica_hash['text'] = df['text']
    # Substituição dos caracteres # e @ antes do tratamento para que não sejam excluídos no processo:
    verifica_hash['text'] = verifica_hash['text'].str.replace('#', 'hashtag_vl', regex=True)
    verifica_hash['text'] = verifica_hash['text'].str.replace('@', 'arroba_vl', regex=True)
    # Utilização do método CountVectorizer para criar uma matriz de documentos:
    cv = CountVectorizer(strip_accents = None)
    count_matrix = cv.fit_transform(verifica_hash['text'])
    # Criação de um dataframe com o número de ocorrências das principais palavras em nosso dataset:
    contagem_palavras = pd.DataFrame(cv.get_feature_names(), columns=["palavra"])
    contagem_palavras["count"] = count_matrix.sum(axis=0).tolist()[0]
    contagem_palavras = contagem_palavras.sort_values("count", ascending=False).reset_index(drop=True)
    # Retorno do caracteres # e @:
    contagem_palavras['palavra'] = contagem_palavras['palavra'].str.replace('hashtag_vl','#', regex=True)
    contagem_palavras['palavra'] = contagem_palavras['palavra'].str.replace('arroba_vl','@', regex=True)
    # Contagem de Hashtags:
    hashtags = contagem_palavras[contagem_palavras['palavra'].str.startswith('#')]
    # Separação e exibição das 5 mais presentes:
    top5_hashtags = hashtags.head()
    # Arrobas de usuários citadas nos tweets:
    arrobas_citadas = contagem_palavras[contagem_palavras['palavra'].str.startswith('@')]
    # Remoção hashtags e arrobas
    contagem_palavras_relevantes = contagem_palavras[(contagem_palavras['palavra'].isin(hashtags['palavra'])==False)]
    contagem_palavras_relevantes = contagem_palavras_relevantes[(contagem_palavras_relevantes['palavra'].isin(arrobas_citadas['palavra'])==False)]
    # Remoção de termos irrelevantes:
    contagem_palavras_relevantes = contagem_palavras_relevantes[contagem_palavras_relevantes['palavra'] != 'rt']
    contagem_palavras_relevantes = contagem_palavras_relevantes[contagem_palavras_relevantes['palavra'] != 'https']
    contagem_palavras_relevantes = contagem_palavras_relevantes[contagem_palavras_relevantes['palavra'] != 'http']
    contagem_palavras_relevantes = contagem_palavras_relevantes[contagem_palavras_relevantes['palavra'] != 'co']
    contagem_palavras_relevantes = contagem_palavras_relevantes[contagem_palavras_relevantes['palavra'] != '#']
    # Remoção de stop words:
    contagem_palavras_relevantes = contagem_palavras_relevantes[(contagem_palavras_relevantes['palavra'].isin(modelo_analise_de_sentimentos.portugues_stops)==False)]
    # Separação e exibição das 5 mais presentes:
    top5_contagem_palavras_relevantes = contagem_palavras_relevantes.head()
    # -------------------------------------------------------------------
    ## Contagem de estados:
    df['localizacao'] = df['location']
    df['localizacao'] = df['localizacao'].str.upper()
    df['localizacao'] = df['localizacao'].fillna('NULO')
    df['localizacao'] = df['localizacao'].apply(unidecode)
    df['localizacao'] = df['localizacao'].str.replace('BRASIL', 'NULO', regex=True)
    df['localizacao'] = df['localizacao'].str.replace('-', ',', regex=True)
    df['localizacao'] = df['localizacao'].str.replace('/', ',', regex=True)
    df['localizacao'] = df['localizacao'].str.replace('|', ',', regex=True)
    df['localizacao'] = df['localizacao'].str.replace(' ', '', regex=True)
    # Divisão dos dois primeiros termos presentes:
    df['loc_01'] = df['localizacao'].str.split(',').str[0]
    df['loc_02'] = df['localizacao'].str.split(',').str[1]
    # Mapeamento com dicionário para a criação da variável "estado":
    df['estado'] = df['loc_01'].map(dicionario_brasil.dic)
    df['estado_02'] = df['loc_02'].map(dicionario_brasil.dic)
    df['estado'] = df['estado'].fillna(df['estado_02'])
    # Verificação da quantidade de localizações estaduais obtidas:
    tweets_localizados = sum(df['estado'].value_counts())
    pct_tweets_localizados = round((tweets_localizados*100)/len(df),2)
    # Dataframe com a contagem dos estados:
    tweets_estados = df['estado'].value_counts().to_frame().reset_index()
    tweets_estados.columns = ['estado', 'qtd_tweets']
    # Separação e exibição dos 5 mais presentes:
    top5_estados = tweets_estados.head()
    # -------------------------------------------------------------------
    # Cálculo de taxas de tweets:
    # Criação de um dataframe para a análise:
    data_hora_coleta = pd.DataFrame()
    # Separação de data e hora:
    data_hora_coleta['data'] = [d.date() for d in df['data_hora']]
    data_hora_coleta['hora'] = [d.time() for d in df['data_hora']]
    # Coletando o último e o primeiro horário:
    fim = data_hora_coleta['hora'].iloc[-1]
    inicio = data_hora_coleta['hora'].iloc[0]
    # Transformação dos dados:
    horario_fim = datetime.datetime.combine(datetime.date.today(), fim)
    horario_inicio = datetime.datetime.combine(datetime.date.today(), inicio)
    # Cálculo do período de coleta:
    periodo = horario_fim - horario_inicio
    # Taxa média de tweets por usuário:
    if qtd_usuarios_unicos > 0:
        media_tweets_por_usuario = round((total_tweets/ qtd_usuarios_unicos),2)
    else:
        media_tweets_por_usuario = 0
    # Taxa média de tweets por usuário verificado:
    if qtd_usuarios_verificados > 0:
        media_tweets_por_usuario_verificado = round((total_tt_verificados/ qtd_usuarios_verificados),2)
    else:
        media_tweets_por_usuario_verificado = 0
    # Taxa média de tweets por usuário não verificado:
    if qtd_usuarios_nao_verificados > 0:
        media_tweets_por_usuario_nao_verificado = round((total_tt_nao_verificados/ qtd_usuarios_nao_verificados),2)
    else:
        media_tweets_por_usuario_nao_verificado = 0
    # Taxa média de tweets por minuto:
    tweets_por_minuto = round((total_tweets/(periodo.seconds/60)),2)
    # Taxa média de tweets por segundo:
    tweets_por_segundo = round(tweets_por_minuto/60,2)
    # -------------------------------------------------------------------
    # Gráficos do dashboard:
    # Estrutura:
    fig = make_subplots(
        rows=3, cols=4, start_cell="top-left",
        specs=[[{"colspan": 2},None, {"type": "domain"}, {"type": "domain"}],[{"colspan": 2},None, {},
        {"rowspan": 2, "type": "table"}],[{},{},{},None]],
        subplot_titles=("Tweets ao longo do período", total_tt_st, total_us_st, "Sentimento ao longo do período",
                        "Polaridade","","Top 5 hashtags", "Top 5 palavras", "Top 5 estados"))
    # Tweets ao longo do período
    fig.add_trace(go.Scatter(x=tw_x_pd['data_hora'], y=tw_x_pd['qtd_tweets'], fill='tozeroy', mode= 'lines',
                            line=dict(color='gold', width=1),name=""),row=1, col=1)
    # Quantidade de tweets e retweets
    fig.add_trace(go.Pie(labels = ['Originais', 'Retweets'], values = [originais, retweets], hole = .7,
                         marker_colors=['gold', 'darkgoldenrod'], textinfo='label+percent',hoverinfo='value'),row=1, col=3)
    # Quantidade de usuários
    fig.add_trace(go.Pie(labels = ['Verificados', 'Não verificados'],values = [qtd_usuarios_verificados,
                        qtd_usuarios_nao_verificados], hole = .5, marker_colors=['darkgoldenrod','gold'],
                        textinfo='label+percent', hoverinfo='value',rotation=90),row=1, col=4)
    # Sentimento ao longo do período
    fig.add_trace(go.Scatter(x=total_sents_pos['data_hora'], y=total_sents_pos['qtd_tweets'], line=dict(color='gold', width=1),name="Positivo"),row=2, col=1)
    fig.add_trace(go.Scatter(x=total_sents_neu['data_hora'], y=total_sents_neu['qtd_tweets'], line=dict(color='white', width=1),name="Neutro"),row=2, col=1)
    fig.add_trace(go.Scatter(x=total_sents_neg['data_hora'], y=total_sents_neg['qtd_tweets'], line=dict(color='darkgoldenrod', width=1),name="Negativo"),row=2, col=1)
    # Polaridade de sentimento
    cores_dic = {'Positivo': 'gold', 'Neutro': 'white', 'Negativo': 'darkgoldenrod'}
    cores= polaridade_sentimentos['sentimento'].map(cores_dic)
    fig.add_trace(go.Bar( x=polaridade_sentimentos['num_de_tweets'],y=polaridade_sentimentos['sentimento'],orientation='h',
                         marker_color = cores, name=""),row=2, col=3).update_yaxes(categoryorder="total ascending")
    # Tabela de taxas
    values_tx = [['','','','Tweets','Por usuário', 'Por usuário verificado', 'Por usuário não verificado', 'Por minuto', 'Por segundo'],
              ['','','','Taxa média',media_tweets_por_usuario, media_tweets_por_usuario_verificado,
               media_tweets_por_usuario_nao_verificado, tweets_por_minuto, tweets_por_segundo ]]
    palavras_chaves = str(chaves.keywords).strip('[]')
    fig.add_trace(go.Table(columnorder = [1,2],columnwidth = [5,5], header = dict(values = [['Tweets'],['Taxa média']],
        line_color='rgb(122, 94, 8)',fill_color='black', align=['center','center'],font=dict(color='gold', size=11),
        height=25),cells=dict( values=values_tx,
        line_color=[['rgb(122, 94, 8)'if (val != '') else 'rgb(17, 17, 17)' for val in values_tx[0]],
                   ['rgb(122, 94, 8)'if (val != '') else 'rgb(17, 17, 17)' for val in values_tx[1]]],
        fill_color='rgb(17, 17, 17)', align=['center', 'center'],
        font = dict(color =[['gold'if (val == 'Tweets') else 'white' for val in values_tx[0]],
                   ['gold'if (val == 'Taxa média') else 'white' for val in values_tx[1]]], size = 11),height=25)),row=2, col=4)

    fig.add_trace(go.Table(header=dict(values=['Termos monitorados'],line_color='rgb(122, 94, 8)',fill_color='rgb(17, 17, 17)',
                                align=['center','center'],font=dict(color='gold', size=12),height=30),
                                cells=dict(values=[[palavras_chaves,]],line_color='rgb(122, 94, 8)',
                                fill=dict(color=['rgb(17, 17, 17)', 'rgb(17, 17, 17)']),
                                align=['center', 'center'],font_size=12,height=30)),row=2, col=4)
    # Top 5 Hashtags
    fig.add_trace(go.Bar(y = top5_hashtags['count'], x = top5_hashtags['palavra'],
                        marker_color='gold',name=""),row=3, col=1)
    # Top 5 Palavras
    fig.add_trace(go.Bar(y = top5_contagem_palavras_relevantes['palavra'],x = top5_contagem_palavras_relevantes['count'],
                        marker_color='darkgoldenrod',orientation='h',name=""),row=3, col=2)
    # Top 5 Estados
    fig.add_trace(go.Bar(x = top5_estados['estado'].head(5), y=top5_estados['qtd_tweets'].head(5),
                     marker_color='gold',name=""),row=3, col=3)
    # Configura Tema
    fig.update_layout(showlegend=False, title=go.layout.Title(text="Bem-te-vi Dashboard",xref="paper",x=0.5),
                      template="plotly_dark").update_xaxes(showgrid=False).update_yaxes(showgrid=False)
    # Desenha o dashboard
    return html.Div([dcc.Graph(figure=fig, id='Dashboard')])
# -------------------------------------------------------------------
# Roda o dashboard em http://127.0.0.1:8050/
app.layout = serve_layout
if __name__ == '__main__':
    app.run_server(debug=True)
