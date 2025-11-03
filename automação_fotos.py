import requests
import random
from datetime import datetime
import os

# Pegar tokens das variáveis de ambiente (GitHub Secrets)
ACCESS_TOKEN = os.environ.get('FB_ACCESS_TOKEN')
PAGE_ID = os.environ.get('FB_PAGE_ID')
INSTAGRAM_ID = os.environ.get('INSTAGRAM_ID')
PINTEREST_TOKEN = os.environ.get('PINTEREST_TOKEN')
PINTEREST_BOARD_NAME = 'EBOOKS TRANSFORMADORES'

# === EBOOKS (resto do código igual) ===
ebooks = {
    'ia_pratica': {
        'nome': 'IA na Prática',
        'landing_page': 'https://ronildomatos.github.io/ebook-ia-na-pratica/',
        'preco': '27,00',
        'mensagens': [
            "🚀 Domine a IA em 7 dias!\n\n📚 R$27 (de R$97)\n✨ +3 bônus\n\n👉 {link}\n\n#IA #Tecnologia",
        ],
        'imagens': ["https://i.ibb.co/p6NJtV0N/imagem1.jpg", "https://i.ibb.co/YB3vGfkp/imagem2.jpg"]
    },
    'atlas_3i': {
        'nome': '3I Atlas',
        'landing_page': 'https://kiwify.app/Kj3xEQC',
        'preco': '19,90',
        'mensagens': [
            "🌌 Descubra o asteroide 3I Atlas!\n\n📖 eBook completo\n👉 {link}\n\n#Astronomia",
        ],
        'imagens': ["https://i.imgur.com/1esSXzC.jpg"]
    },
    'oracoes_destinos': {
        'nome': 'Orações que Mudam Destinos',
        'landing_page': 'https://kiwify.app/XY7k3Xk',
        'preco': '17,00',
        'mensagens': [
            "🙏 Transforme pela fé!\n\n✨ Orações poderosas\n👉 {link}\n\n#Fe",
        ],
        'imagens': ["https://i.imgur.com/2JxvfwW.jpg"]
    }
}

def obter_board_id():
    try:
        url = 'https://api.pinterest.com/v5/boards'
        headers = {'Authorization': f'Bearer {PINTEREST_TOKEN}', 'Content-Type': 'application/json'}
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            for board in response.json().get('items', []):
                if board['name'].upper() == PINTEREST_BOARD_NAME.upper():
                    return board['id']
    except:
        pass
    return None

def postar_facebook(ebook, mensagem, imagem_url):
    try:
        url = f'https://graph.facebook.com/v24.0/{PAGE_ID}/photos'
        payload = {'message': mensagem, 'url': imagem_url, 'access_token': ACCESS_TOKEN}
        response = requests.post(url, data=payload)
        if response.status_code == 200:
            print(f'✅ FACEBOOK: Postado!')
            return True
        else:
            print(f'❌ FACEBOOK: Erro {response.status_code}')
            return False
    except Exception as e:
        print(f'❌ FACEBOOK: {e}')
        return False

def postar_instagram(ebook, mensagem, imagem_url):
    try:
        media_url = f'https://graph.facebook.com/v24.0/{INSTAGRAM_ID}/media'
        media_payload = {'image_url': imagem_url, 'caption': mensagem, 'access_token': ACCESS_TOKEN}
        media_response = requests.post(media_url, data=media_payload)
        
        if media_response.status_code == 200:
            creation_id = media_response.json().get('id')
            publish_url = f'https://graph.facebook.com/v24.0/{INSTAGRAM_ID}/media_publish'
            publish_payload = {'creation_id': creation_id, 'access_token': ACCESS_TOKEN}
            publish_response = requests.post(publish_url, data=publish_payload)
            
            if publish_response.status_code == 200:
                print(f'✅ INSTAGRAM: Postado!')
                return True
        print(f'❌ INSTAGRAM: Erro')
        return False
    except Exception as e:
        print(f'❌ INSTAGRAM: {e}')
        return False

def postar_pinterest(ebook, mensagem, imagem_url):
    try:
        board_id = obter_board_id()
        if not board_id:
            print('⚠️ PINTEREST: Board não encontrado')
            return False
        
        url = 'https://api.pinterest.com/v5/pins'
        headers = {'Authorization': f'Bearer {PINTEREST_TOKEN}', 'Content-Type': 'application/json'}
        payload = {
            'board_id': board_id,
            'title': ebook['nome'],
            'description': mensagem[:500],
            'link': ebook['landing_page'],
            'media_source': {'source_type': 'image_url', 'url': imagem_url}
        }
        response = requests.post(url, headers=headers, json=payload)
        
        if response.status_code == 201:
            print(f'✅ PINTEREST: Postado!')
            return True
        else:
            print(f'❌ PINTEREST: Erro {response.status_code}')
            return False
    except Exception as e:
        print(f'❌ PINTEREST: {e}')
        return False

# === EXECUÇÃO ===
print("="*80)
print("🤖 BOT DE POSTAGENS - FOTOS")
print(f"✅ {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
print("="*80)

ebook_escolhido = random.choice(list(ebooks.keys()))
ebook = ebooks[ebook_escolhido]
mensagem = random.choice(ebook['mensagens']).format(link=ebook['landing_page'])
imagem_url = random.choice(ebook['imagens'])

print(f"\n📚 eBook: {ebook['nome']}")

postar_facebook(ebook, mensagem, imagem_url)
postar_instagram(ebook, mensagem, imagem_url)
postar_pinterest(ebook, mensagem, imagem_url)

print("\n" + "="*80)
print("✅ CONCLUÍDO!")
print("="*80)
```

---

### **2. `requirements.txt`**
```
requests==2.32.5
Pillow==12.0.0
imageio-ffmpeg==0.5.1
