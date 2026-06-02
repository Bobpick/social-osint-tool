import requests
import re
import os
import json
import time
from datetime import datetime

def limpar():
    os.system("clear")

def pausa():
    input("\nENTER pra continuar...")

# --------------------
# UTIL
# --------------------

def banner():
    print("""
╔══════════════════════════════╗
║        OSINT DASHBOARD       ║
╚══════════════════════════════╝
""")

def menu():
    while True:
        limpar()
        banner()

        print("[1] TikTok OSINT")
        print("[2] Instagram OSINT")
        print("[3] Sair")

        op = input("\nEscolha: ")

        if op == "1":
            tiktok_osint()

        elif op == "2":
            instagram_osint()

        elif op == "3":
            print("Saindo...")
            break

        else:
            print("Opção inválida")
            time.sleep(1)

# --------------------
# TIKTOK OSINT (TEU CÓDIGO)
# --------------------
def tiktok_osint():
    limpar()

    print("\033[1;36m")
    os.system('toilet -f future "TikTok"')

    print("""
╔══════════════════════════════╗
║       TIKTOK OSINT TOOL      ║
╚══════════════════════════════╝
""")

    user = input("\nDigite o @: ").strip().replace("@", "")

    if not user:
        print("Usuário vazio.")
        pausa()
        return

    print("\nBuscando perfil...")
    time.sleep(1)

    url = f"https://www.tiktok.com/@{user}"

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:
        r = requests.get(url, headers=headers, timeout=10)
    except:
        print("\nErro de conexão.")
        pausa()
        return

    if r.status_code != 200:
        print("\nUsuário não encontrado ou bloqueado.")
        pausa()
        return

    texto = r.text

    def pegar(regex):
        match = re.search(regex, texto)
        return match.group(1) if match else "Não encontrado"

    def safe_int(v):
        try:
            return int(v)
        except:
            return v

    nickname = pegar(r'"nickname":"(.*?)"')
    bio = pegar(r'"signature":"(.*?)"').replace("\\n", "\n")

    seguidores = safe_int(pegar(r'"followerCount":(.*?),'))
    seguindo = safe_int(pegar(r'"followingCount":(.*?),'))
    curtidas = safe_int(pegar(r'"heartCount":(.*?),'))
    videos = safe_int(pegar(r'"videoCount":(.*?),'))
    verificado = pegar(r'"verified":(true|false)')

    dados = {
        "user": user,
        "url": url,
        "nickname": nickname,
        "bio": bio,
        "seguidores": seguidores,
        "seguindo": seguindo,
        "curtidas": curtidas,
        "videos": videos,
        "verificado": verificado,
        "timestamp": str(datetime.now())
    }

    print("\n━━━━━━━━━━━━━━━━━━━━━━")
    print("📌 PERFIL ENCONTRADO")
    print("━━━━━━━━━━━━━━━━━━━━━━")

    print(f"\nURL: {url}")
    print(f"Nickname: {nickname}")
    print(f"Bio: {bio}")

    if bio and "insta" in bio.lower():
        print("\n📸 Possível Instagram encontrado na bio!")

    print(f"\nSeguidores: {seguidores}")
    print(f"Seguindo: {seguindo}")
    print(f"Curtidas: {curtidas}")
    print(f"Vídeos: {videos}")
    print(f"Verificado: {verificado}")

    print("\n━━━━━━━━━━━━━━━━━━━━━━")
    print("📦 JSON EXPORT")
    
    input("\nENTER pra voltar ao menu...")
    return

def instagram_osint():
    user = input("\nDigite o @: ").strip().replace("@", "")

    if not user:
        print("Usuário vazio.")
        return

    url = f"https://www.instagram.com/{user}/"

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    print("\n🔎 Buscando perfil...")

    try:
        r = requests.get(url, headers=headers, timeout=10)
    except Exception as e:
        print("❌ Erro de conexão:", e)
        return

    if r.status_code != 200:
        print("❌ Perfil não encontrado ou bloqueado (HTTP", r.status_code, ")")
        return

    html = r.text

    # tenta pegar dados básicos do HTML
    title = re.search(r'<title>(.*?)</title>', html)
    description = re.search(r'"description":"(.*?)"', html)

    title = title.group(1) if title else "Não encontrado"
    description = description.group(1) if description else "Não encontrado"

    dados = {
        "user": user,
        "url": url,
        "title": title,
        "description": description,
        "timestamp": str(datetime.now())
    }

    print("\n━━━━━━━━━━━━━━━━━━━━━━")
    print("📌 PERFIL ENCONTRADO")
    print("━━━━━━━━━━━━━━━━━━━━━━")

    print("User:", user)
    print("Title:", title)
    print("Description:", description)

    print("\n📦 JSON:")
    print(json.dumps(dados, indent=4, ensure_ascii=False))

    input("\nENTER pra voltar...")

if __name__ == "__main__":
    menu()
