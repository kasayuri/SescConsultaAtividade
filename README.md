# SescConsultaGMF

Este projeto automatiza a consulta de inscrições abertas para atividades de algum curso no Sesc SP e envia notificações para um canal do Discord. Foi utilizado devcontainers, com Python3 e navegador Edge

## Descrição

O script `ConsultaSesc.py` utiliza Selenium WebDriver para automatizar o processo de login no site do Sesc SP, pesquisa por atividades do curso informado e verifica se há inscrições abertas nas unidades selecionadas. Caso encontre inscrições abertas, o script envia uma mensagem para um webhook do Discord configurado.

## Requisitos

- Python 3.x
- Selenium
- Requests
- selenium
- configparser

## Instalação

1. Clone o repositório:
    ```sh
    git clone https://github.com/kasayuri/SescConsultaAtividade.git
    cd SescConsultaAtividade
    ```

2. Crie um ambiente virtual e ative-o:
    ```sh
    python -m venv .venv
    .venv\Scripts\activate  # No Windows
    source .venv/bin/activate  # No Linux/Mac
    ```

3. Instale as dependências:
    ```sh
    pip install -r requirements.txt
    ```

4. Gere um webhook no Discord e configure o arquivo [config.yaml](http://_vscodecontentref_/0) com suas informações:
    ```ini
    [DEFAULT]
    DISCORD_WEBHOOK_URL = https://discord.com/api/webhooks/your_webhook_url
    USERNAME = seu_usuario
    PASSWORD = sua_senha
    ```

## Uso

Execute o script [ConsultaSesc.py](http://_vscodecontentref_/1):
```sh
python ConsultarSesc.py