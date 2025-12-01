import threading
import time
import requests
import os

def keep_alive():
    url = os.getenv('RENDER_EXTERNAL_URL')
    if not url:
        print('Variável de ambiente RENDER_EXTERNAL_URL não definida.')
        return
    def ping():
        while True:
            try:
                print(f'Pingando {url}...')
                requests.get(url)
            except Exception as e:
                print(f'Erro ao pingar: {e}')
            time.sleep(300)  # 5 minutos
    thread = threading.Thread(target=ping, daemon=True)
    thread.start()
