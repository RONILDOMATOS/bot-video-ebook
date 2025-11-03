import requests
import random
from datetime import datetime
import tempfile
import os
import subprocess
from PIL import Image as PILImage, ImageDraw, ImageFont

# Configurar FFmpeg
try:
    from imageio_ffmpeg import get_ffmpeg_exe
    FFMPEG_BINARY = get_ffmpeg_exe()
except:
    FFMPEG_BINARY = 'ffmpeg'

# === CONFIGURAÇÕES (pega dos secrets do GitHub) ===
ACCESS_TOKEN = os.environ.get('FB_ACCESS_TOKEN')
PAGE_ID = os.environ.get('FB_PAGE_ID')

# === EBOOKS ===
ebooks = {
    'ia_pratica': {
        'nome': 'IA na Prática',
        'landing_page': 'https://ronildomatos.github.io/ebook-ia-na-pratica/',
        'preco': '27,00',
        'mensagens': [
            "🚀 Domine a IA em 7 dias!\n\n📚 R$27 (de R$97)\n👉 {link}\n\n#IA #Tecnologia",
        ],
        'imagens': ["https://i.ibb.co/p6NJtV0N/imagem1.jpg", "https://i.ibb.co/YB3vGfkp/imagem2.jpg"]
    },
    'atlas_3i': {
        'nome': '3I Atlas',
        'landing_page': 'https://kiwify.app/Kj3xEQC',
        'preco': '19,90',
        'mensagens': [
            "🌌 Asteroide 3I Atlas!\n\n📖 eBook completo\n👉 {link}\n\n#Astronomia",
        ],
        'imagens': ["https://i.imgur.com/1esSXzC.jpg", "https://i.imgur.com/4goqlaB.jpg"]
    },
    'oracoes_destinos': {
        'nome': 'Orações que Mudam Destinos',
        'landing_page': 'https://kiwify.app/XY7k3Xk',
        'preco': '17,00',
        'mensagens': [
            "🙏 Transforme pela fé!\n\n✨ Orações poderosas\n👉 {link}\n\n#Fe",
        ],
        'imagens': ["https://i.imgur.com/2JxvfwW.jpg", "https://i.imgur.com/xABhsUd.jpg"]
    }
}

def criar_video_simples(ebook, imagem_url):
    """Cria vídeo com Pillow + FFmpeg"""
    print(f"\n🎬 Criando vídeo: {ebook['nome']}")
    
    try:
        print(f"   📥 Baixando imagem...")
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(imagem_url, timeout=10, headers=headers)
        
        if 'image' not in response.headers.get('content-type', ''):
            if 'imgur.com' in imagem_url and not imagem_url.endswith(('.jpg', '.png')):
                imagem_url = imagem_url + '.jpg'
                response = requests.get(imagem_url, timeout=10, headers=headers)
        
        temp_img = tempfile.NamedTemporaryFile(delete=False, suffix='.jpg')
        temp_img.write(response.content)
        temp_img.close()
        print(f"   ✅ Imagem baixada")
        
        img = PILImage.open(temp_img.name).convert('RGB')
        img = img.resize((1080, 1080), PILImage.Resampling.LANCZOS)
        
        print(f"   🎨 Processando frames...")
        frames = []
        
        for i in range(120):
            frame = img.copy()
            draw = ImageDraw.Draw(frame)
            
            try:
                font_nome = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 60)
                font_preco = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 80)
                font_cta = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 40)
            except:
                font_nome = ImageFont.load_default()
                font_preco = ImageFont.load_default()
                font_cta = ImageFont.load_default()
            
            texto_nome = ebook['nome']
            bbox = draw.textbbox((0, 0), texto_nome, font=font_nome)
            w = bbox[2] - bbox[0]
            x = (1080 - w) // 2
            
            for adj in range(-2, 3):
                for adj2 in range(-2, 3):
                    draw.text((x+adj, 100+adj2), texto_nome, fill='black', font=font_nome)
            draw.text((x, 100), texto_nome, fill='white', font=font_nome)
            
            texto_preco = f"R$ {ebook['preco']}"
            bbox = draw.textbbox((0, 0), texto_preco, font=font_preco)
            w = bbox[2] - bbox[0]
            x = (1080 - w) // 2
            
            for adj in range(-3, 4):
                for adj2 in range(-3, 4):
                    draw.text((x+adj, 900+adj2), texto_preco, fill='black', font=font_preco)
            draw.text((x, 900), texto_preco, fill='#00FF00', font=font_preco)
            
            texto_cta = "ADQUIRA AGORA"
            bbox = draw.textbbox((0, 0), texto_cta, font=font_cta)
            w = bbox[2] - bbox[0]
            x = (1080 - w) // 2
            
            for adj in range(-2, 3):
                for adj2 in range(-2, 3):
                    draw.text((x+adj, 980+adj2), texto_cta, fill='black', font=font_cta)
            draw.text((x, 980), texto_cta, fill='yellow', font=font_cta)
            
            frames.append(frame)
        
        print(f"   💾 Salvando GIF...")
        gif_path = f"temp_{datetime.now().strftime('%Y%m%d_%H%M%S')}.gif"
        frames[0].save(gif_path, save_all=True, append_images=frames[1:], duration=42, loop=0)
        
        print(f"   🎬 Convertendo para MP4...")
        video_path = f"video_ebook_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp4"
        
        result = subprocess.run([
            FFMPEG_BINARY, '-i', gif_path,
            '-c:v', 'libx264',
            '-pix_fmt', 'yuv420p',
            '-y', video_path
        ], capture_output=True)
        
        os.remove(temp_img.name)
        os.remove(gif_path)
        
        if os.path.exists(video_path):
            print(f"   ✅ Vídeo criado!")
            return video_path
        else:
            print(f"   ❌ Falhou")
            return None
        
    except Exception as e:
        print(f"   ❌ Erro: {e}")
        return None

def postar_video_facebook(ebook, mensagem, video_path):
    try:
        print(f"\n📤 Postando no Facebook...")
        url = f'https://graph.facebook.com/v24.0/{PAGE_ID}/videos'
        
        with open(video_path, 'rb') as video_file:
            payload = {'description': mensagem, 'access_token': ACCESS_TOKEN}
            files = {'file': video_file}
            response = requests.post(url, data=payload, files=files, timeout=180)
        
        if response.status_code == 200:
            video_id = response.json().get('id')
            print(f'✅ Postado! ID: {video_id}')
            return True
        else:
            print(f'❌ Erro {response.status_code}: {response.json()}')
            return False
    except Exception as e:
        print(f'❌ Erro: {e}')
        return False

# === EXECUÇÃO ===
print("="*80)
print("🎬 BOT DE VÍDEOS")
print(f"✅ {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
print("="*80)

ebook_escolhido = random.choice(list(ebooks.keys()))
ebook = ebooks[ebook_escolhido]
mensagem = random.choice(ebook['mensagens']).format(link=ebook['landing_page'])
imagem_url = random.choice(ebook['imagens'])

print(f"\n📚 eBook: {ebook['nome']}")

video_path = criar_video_simples(ebook, imagem_url)

if video_path:
    sucesso = postar_video_facebook(ebook, mensagem, video_path)
    if os.path.exists(video_path):
        os.remove(video_path)
    print("\n" + "="*80)
    print("🎉 SUCESSO!" if sucesso else "⚠️ ERRO")
    print("="*80)
else:
    print("\n" + "="*80)
    print("❌ FALHA")
    print("="*80)
