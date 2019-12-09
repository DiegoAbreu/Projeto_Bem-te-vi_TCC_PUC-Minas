# Projeto: Bem-te-vi
# Autor: Diego Abreu
# Arquivo: atualiza_dashboard.py
# Resumo: Este arquivo contém:
#       - Código que abre o navegador na página do dashboard;
#       - Código que atualiza a página do dashboard periodicamente.
# -------------------------------------------------------------------
# -------------------------------------------------------------------
# Importação de pacotes:
from selenium import webdriver
import time
# -------------------------------------------------------------------
# Função para abrir o navegado na página do dashboard:
time.sleep(13)     # Tempo de espera para que os modelo_analise_de_sentimentos.py, dashboard.py e coleta.py rodem.
driver = webdriver.Firefox()
driver.get("http://127.0.0.1:8050/")
# -------------------------------------------------------------------
# Função para atualizar a página períodicamente:
while True:
    time.sleep(25)
    driver.refresh()
driver.quit()
