import time
import requests
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

# Configurações
URL_PRODUTO = "COLOQUE_AQUI_O_LINK_DA_MEMORIA_RAM"
PRECO_ALVO = 250.00  # Valor máximo que você quer pagar
DISCORD_WEBHOOK_URL = "COLOQUE_AQUI_SEU_WEBHOOK_DO_DISCORD"

def enviar_alerta(titulo, preco, link):
    mensagem = {
        "content": f"🚨 **PROMOÇÃO ENCONTRADA!** 🚨\n\n**Produto:** {titulo}\n**Preço:** R$ {preco:.2f}\n**Link:** {link}"
    }
    requests.post(DISCORD_WEBHOOK_URL, json=mensagem)
    print("Alerta enviado com sucesso!")

def verificar_preco():
    print("Verificando preço...")
    with sync_playwright() as p:
        # Abre o navegador em modo headless (invisível)
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        
        try:
            page.goto(URL_PRODUTO, timeout=60000)
            # Espera um pouco para garantir que o preço carregou na tela
            page.wait_for_timeout(3000) 
            
            html = page.content()
            soup = BeautifulSoup(html, "html.parser")
            
            # ATENÇÃO: Você precisará inspecionar o site (F12) para pegar a tag/classe exata
            titulo_elemento = soup.find("h1") 
            preco_elemento = soup.find("h4", class_="classe-do-preco-aqui") # Exemplo fictício
            
            if titulo_elemento and preco_elemento:
                titulo = titulo_elemento.get_text(strip=True)
                # Limpa o texto do preço: "R$ 239,90" -> 239.90
                preco_texto = preco_elemento.get_text(strip=True)
                preco_limpo = float(preco_texto.replace("R$", "").replace(".", "").replace(",", ".").strip())
                
                print(f"Produto: {titulo} | Preço atual: R$ {preco_limpo:.2f}")
                
                if preco_limpo <= PRECO_ALVO:
                    enviar_alerta(titulo, preco_limpo, URL_PRODUTO)
            else:
                print("Não foi possível encontrar os elementos na página. Verifique os seletores.")
                
        except Exception as e:
            print(f"Erro ao acessar a página: {e}")
        finally:
            browser.close()

# Loop para rodar a cada 30 minutos (1800 segundos)
if __name__ == "__main__":
    while True:
        verificar_preco()
        print("Aguardando 30 minutos para a próxima verificação...\n")
        time.sleep(1800)
