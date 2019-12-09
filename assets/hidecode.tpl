<!--
  Projeto: Bem-te-vi
  Autor: Diego Abreu
  Arquivo: hidecode.tpl
  Resumo: Este arquivo possui código para excluir as células com código durante
          a exportação do relatório para html. Ele é usado junto ao comando
          nbconvert no arquivo relatório.ipynb. -->

{%- extends 'full.tpl' -%}
{% block input_group %}
    {%- if cell.metadata.get('nbconvert', {}).get('show_code', False) -%}
        ((( super() )))
    {%- endif -%}
{% endblock input_group %}
