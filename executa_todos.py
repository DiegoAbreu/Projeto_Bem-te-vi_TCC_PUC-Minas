# Projeto: Bem-te-vi
# Autor: Diego Abreu
# Arquivo: executa_todos.py
# Resumo: Este arquivo contém:
#       - Código que abre o navegador na página do dashboard;
#       - Código que atualiza a página do dashboard periodicamente.

# -------------------------------------------------------------------
# Importação de pacotes:
import os
from multiprocessing import Pool
# -------------------------------------------------------------------
# Definir arquivos a serem executados:
processes = ('coleta_tweets.py','dashboard.py', 'atualiza_dashboard.py')
# -------------------------------------------------------------------
# Função para executar os códigos:
def executa(codigo):
    os.system('python {}'.format(codigo))
pool = Pool(processes=3)
pool.map(executa, processes)
