import requests
import yaml

# Carregar configurações do arquivo config.yaml
with open('config.yaml', 'r', encoding='utf-8') as configfile:
    config = yaml.safe_load(configfile)

DISCORD_WEBHOOK_URL = config["DEFAULT"]["DISCORD_WEBHOOK_URL"]

def send_discord_message(content: str):
    payload = {
        "content": content,
        "username": "Notificação importante!!",
        "avatar_url": "https://cdn.pixabay.com/photo/2015/12/16/17/41/bell-1096280_1280.png",
        "tts": False
    }
    try:
        response = requests.post(DISCORD_WEBHOOK_URL, json=payload)
        if response.status_code == 204:
            print("Mensagem enviada com sucesso para o Discord")
        else:
            print(f"Erro ao enviar mensagem para o Discord: {response.status_code}")
    except Exception as e:
        print(f"Erro ao enviar mensagem para o Discord: {e}")

# Exemplo de uso
send_discord_message("Teste de mensagem do webhook do Discord")