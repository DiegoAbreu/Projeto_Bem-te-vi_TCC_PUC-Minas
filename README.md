# Projeto bem-te-vi
Trabalho de conclusão do curso de Pós-Graduação em Ciência de dados e Big Data | PUC-Minas(2018/2019).
- [PDF completo do Trabalho de Conclusão de Curso](https://drive.google.com/open?id=1k4UOzioGtjEBw3nSbZ6QHdm_-E3tmEnt)
***
![](https://raw.githubusercontent.com/DiegoAbreu/Projeto_Bem-te-vi_TCC_PUC-Minas/master/imagens/bem-te-vi-cabecalho.png)
***
### O que é?
O bem-te-vi é uma ferramenta em liguagem python para monitoramento e análise de dados de rede social. Mas precisamente o Twitter. A ferramenta permite que o usuário possa acompanhar um determinado tema na rede através de um dashboard de monitoramento com análises quantitativas e qualitativas. E posteriormente, também gerar relatórios.

![](https://raw.githubusercontent.com/DiegoAbreu/Projeto_Bem-te-vi_TCC_PUC-Minas/master/imagens/bem-te-vo_dashboard.gif)

***
### Como funciona?

Este projeto é composto resumidamente pelas etapas: coleta de dados, análises e apesentação. Os dados são os tweets públicos criados pelos usuários da rede sobre um determinado tema, que podemos definir por palavras-chave. Para a coleta, utilizamos a API do Twitter e a biblioteca Tweepy, que analisam os tweets e capturam aqueles que contenham as palavras-chave. Os dados capturados são armazenados em um banco de dados.
Os dados armazenados são acessados e passam por tratamentos e análises. Por fim, as análises são apresentadas em forma de um dashboard para visualização imediata e de relatórios para posterior. 

![](https://raw.githubusercontent.com/DiegoAbreu/Projeto_Bem-te-vi_TCC_PUC-Minas/master/imagens/bem-te-vi_estrutura_geral.png)


No arquivo "passo_a_passo_bem-te-vi.html" desde projeto explica cada etapa em detalhes. Recomendamos sua leitura para melhor compreensão.

***
### Como usar?
**Ambiente:**

Para utilizar o projeto bem-te-vi você precisará ter instalado no seu computador:
- [Chaves da API do Twitter](https://developer.twitter.com/) - Aqui tem um [tutorial](https://docs.daplab.ch/twitter_account/) bem explicado.
- [Navegador Mozilla Firefox](https://www.mozilla.org/pt-BR/firefox/new/);
- [Gecko driver](https://github.com/mozilla/geckodriver/releases);
- [Banco de dados MongoDB](https://www.mongodb.com/);
- [Robo 3T - Interface para MongoDB](https://robomongo.org/download);
- [Linguagem Python](https://www.python.org/);
- [Anaconda](https://www.anaconda.com/);

Obs.: Podem ser utilizados outros navegadores e banco de dados, porém é necessário alterar as partes de código que os utilizam.

Faça o download desse projeto e execute os comandos abaixo no terminal:
```
$ sudo apt install python3-pip
$ sudo apt install virtualenv
$ virtualenv venv -p python3
$ source venv/bin/activate
$ pip install -r requirements.txt
```
Caso tenha dificuldade em configurar o ambiente ou deseje uma opção mais prática, é possível baixar uma imagem do SO Linux Ubuntu com o ambiente já configurado e utilizar em um software de virtulização como Virtualbox ou Vmware:
- [Virtualbox](https://www.virtualbox.org/)
- [Imagem Ubuntu bem-te-vi](https://diegoabreu.com/downloads/bem-te-vi.ova) - Usuário: bem-te-vi; Senha: admin;

Com o ambiente já preparado, abra o arquivo "chaves.py" e preecha o arquivo com as informações solicitadas.
Verifique se a conexão com o MongoDB está funcionando corretamente. Você pode fazer isso pelo terminal, ou simplesmente abrindo o Robo 3T.
Caso tenha algum problema, você pode reiniciar a conexão do mongo com o seguinte comando no terminal:
```
sudo systemctl restart mongod.service
```
Realizadas essas etapas, você já pode executar os seguintes processos com o bem-te-vi:

**- Coleta:**

Via terminal, entre no diretório do projeto e execute o comando:
```
python coleta_tweets.py
```
Feche o terminal quando quiser encerrar a coleta.

**- Coleta + Monitoramento simultâneo:**

Via terminal, entre no diretório do projeto e execute o comando:
```
python executa_todos.py
```
Funcionamento:

![](https://raw.githubusercontent.com/DiegoAbreu/Projeto_Bem-te-vi_TCC_PUC-Minas/master/imagens/bem-te-vi_processo_monitoramento.png)

Video de demonstração do processo de monitoramento:

[![](https://raw.githubusercontent.com/DiegoAbreu/Projeto_Bem-te-vi_TCC_PUC-Minas/master/imagens/bem-te-vi_demo_screen_shot.png)](http://www.youtube.com/watch?v=jTVRj5S1Wn8 "")


Feche o terminal quando quiser encerrar.

**- Gerar arquivos de relatório:**

Via terminal, entre no diretório do projeto e execute o comando:
```
bash gera_relatorio.sh
```
Verifique os arquivos que foram criados no diretório "relatorios". Lá, você encontrará um .html com todos os gráficos das análises, um .csv com os dados coletados e os dados obtidos, por fim, um outro html contendo o dashboard no estado final da coleta.

***

### Estudos de caso feitos com o bem-te-vi:

- [02/10/19 - Grêmio x Flamengo - Semifinal Copa Libertadores da América](https://diegoabreu.com/Uploads/tcc/grexfla.pdf)
- [06/10/19 - último dia do Rock in Rio 2019](https://diegoabreu.com/Uploads/tcc/rockinrio.pdf)

***
![](https://raw.githubusercontent.com/DiegoAbreu/Projeto_Bem-te-vi_TCC_PUC-Minas/master/imagens/bem-te-vi-rodape.png)
