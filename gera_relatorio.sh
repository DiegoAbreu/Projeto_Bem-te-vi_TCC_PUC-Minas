# Projeto: Bem-te-vi
# Autor: Diego Abreu
# Arquivo: gera_relatorio.sh
# Resumo: Arquivo para gerar relatório completo da análise.
# -------------------------------------------------------------------
# -------------------------------------------------------------------
# Limpa saídas de usos anteriores do notebook:
jupyter nbconvert --ClearOutputPreprocessor.enabled=True --inplace relatorio.ipynb
# Executa o notebook relatorio pela primeira vez:
jupyter nbconvert --to notebook --execute --inplace relatorio.ipynb
# Executa o notebook relatorio pela segunda vez e exporta para html
jupyter nbconvert --to notebook --execute --inplace relatorio.ipynb
