import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.edge.options import Options as EdgeOptions
import time
import yaml
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def load_config():
    """Carregar configurações do arquivo config.yaml."""
    try:
        with open('config.yaml', 'r', encoding='utf-8') as configfile:
            return yaml.safe_load(configfile)
    except FileNotFoundError:
        logging.error("Arquivo config.yaml não encontrado.")
        raise
    except yaml.YAMLError as e:
        logging.error(f"Erro ao carregar config.yaml: {e}")
        raise

def setup_driver(edge_driver_location):
    """Configurar e iniciar o WebDriver do Edge."""
    options = EdgeOptions()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    # options.add_argument("--headless")  # Ative para execução sem interface gráfica
    service = EdgeService(edge_driver_location)
    return webdriver.Edge(service=service, options=options)

def login(driver, url_login, username, password):
    """Realizar login no sistema."""
    try:
        driver.get(url_login + "?path=login-sesc")
        time.sleep(5)

        # Preencher CPF
        cpf_input = driver.find_element(By.NAME, "cpf")
        cpf_input.send_keys(username)
        time.sleep(1)

        # Clicar no botão "CONTINUAR"
        driver.find_element(By.XPATH, "//button[@type='submit']").click()
        time.sleep(3)

        # Preencher senha
        senha_input = driver.find_element(By.XPATH, "//input[@type='password']")
        senha_input.send_keys(password)
        time.sleep(2)

        # Clicar no botão "CONTINUAR" após a senha
        driver.find_element(By.XPATH, "//button[@type='submit']").click()
        time.sleep(2)

        # Verificar se o login foi bem-sucedido
        if not "login-sesc" in driver.current_url:
            logging.info("✅ Login realizado com sucesso e página de atividades carregada!")
        else:
            logging.error("❌ Erro ao logar no sistema.")
            raise Exception("Falha no login")
    except Exception as e:
        logging.error(f"Erro durante o login: {e}")
        raise

def buscar_atividades(driver, unidades_selecionadas, categoria_curso, publico_geral, nome_curso, unidades):
    """Buscar atividades disponíveis e verificar inscrições abertas."""
    unidades_com_vagas = []
    try:
        # Procurar atividades
        driver.get(driver.current_url + "/?path=lista-atividades")
        time.sleep(3)

        # Buscar na caixa de pesquisa
        caixa_procurar = driver.find_element(By.XPATH, "//input[@type='search']")
        caixa_procurar.send_keys(nome_curso.lower())
        time.sleep(3)
        
        btn_procurar = driver.find_element(By.XPATH, "//button[@class='MuiButtonBase-root MuiIconButton-root']")
        btn_procurar.click()
        time.sleep(1) 

        # Selecionar categoria
        categoria = driver.find_element(By.XPATH, f"//li[contains(., '{categoria_curso}')]")
        categoria.click()
        time.sleep(1)

        # Selecionar público geral, se necessário
        if publico_geral:
            publico_geral_element = driver.find_element(By.XPATH, "//li[contains(., 'Público em Geral')]")
            publico_geral_element.click()
            time.sleep(1)

        # Verificar unidades selecionadas
        for unidade in unidades_selecionadas:
            unidade = unidade.strip()
            try:
                elemento = driver.find_element(By.XPATH, f"//li[contains(., '{unidade}')]")
                elemento.click()
                logging.info(f"✅ Selecionado: {unidade}")
                time.sleep(1)
            except Exception as e:
                logging.warning(f"❌ Erro ao selecionar '{unidade}': {e}")

        # Procurar atividades com inscrições abertas
        atividades = driver.find_elements(By.XPATH, "//tr[@class='MuiTableRow-root']")
        for atividade in atividades:
            try:
                unidade_element = atividade.find_element(By.XPATH, ".//div[contains(text(), 'Sesc')]")
                print(unidade_element.text)
                unidade = next((key for key, value in unidades.items() if value == unidade_element.text), None)
                print('UNIDADE_element:' + unidade)

                # unidade = unidade_element.text.replace('Sesc', '').strip()

                if any(u in unidade for u in unidades_selecionadas):
                    botao_inscrever = atividade.find_elements(By.XPATH, ".//span[contains(text(), 'Inscrever')]")
                    if botao_inscrever:
                        unidades_com_vagas.append(unidade)
            except Exception as e:
                logging.warning(f"⚠ Erro ao verificar a atividade: {e}")

    except Exception as e:
        logging.error(f"Erro ao buscar atividades: {e}")
        raise

    return unidades_com_vagas

def send_discord_message(webhook_url, content):
    """Enviar mensagem ao Discord."""
    payload = {
        "content": content,
        "username": "Notificação importante!!",
        "avatar_url": "https://cdn.discordapp.com/avatars/1234567890/abcdef1234567890abcdef1234567890.png",
        "tts": False
    }
    try:
        response = requests.post(webhook_url, json=payload)
        if response.status_code == 204:
            logging.info("Mensagem enviada com sucesso para o Discord")
        else:
            logging.error(f"Erro ao enviar mensagem para o Discord: {response.status_code}")
    except Exception as e:
        logging.error(f"Erro ao enviar mensagem para o Discord: {e}")

def main():
    config = load_config()

    DISCORD_WEBHOOK_URL = config["DEFAULT"]["DISCORD_WEBHOOK_URL"]
    EDGE_DRIVER_LOCATION = config["DEFAULT"]["EDGE_DRIVER_LOCATION"]
    USERNAME = config["DEFAULT"]["USERNAME"]
    PASSWORD = config["DEFAULT"]["PASSWORD"]
    PUBLICO_GERAL = config["DEFAULT"]["PUBLICO_GERAL"]
    UNIDADES_SELECIONADAS = config["DEFAULT"]["UNIDADES_SELECIONADAS"]
    URL_LOGIN = config["DEFAULT"]["URL_LOGIN"]
    CATEGORIA_CURSO = config["DEFAULT"]["CATEGORIA_CURSO"]
    NOME_CURSO = config["DEFAULT"]["NOME_CURSO"]
    UNIDADES = config["UNIDADES"]

    driver = setup_driver(EDGE_DRIVER_LOCATION)

    try:
        login(driver, URL_LOGIN, USERNAME, PASSWORD)
        unidades_com_vagas = buscar_atividades(driver, UNIDADES_SELECIONADAS, CATEGORIA_CURSO, PUBLICO_GERAL, NOME_CURSO, UNIDADES)

        if unidades_com_vagas:
            message = f"\n🔔 Unidades com inscrições abertas para {NOME_CURSO}:\n" + "\n".join(f"- {u}" for u in unidades_com_vagas)
            logging.info(message)
            send_discord_message(DISCORD_WEBHOOK_URL, message)
        else:
            aviso = f"❌ Nenhuma unidade selecionada tem inscrições abertas para {NOME_CURSO}."
            logging.info(aviso)
            send_discord_message(DISCORD_WEBHOOK_URL, aviso)

    finally:
        driver.quit()

if __name__ == "__main__":
    main()