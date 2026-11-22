import time
from pathlib import Path
import shutil

# Mapeamento de categorias e suas respectivas extensões
DIRECTORY_MAPPING = {
    "Imagens": [".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg", ".ico"],
    "Documentos": [".pdf", ".docx", ".doc", ".txt", ".xlsx", ".pptx", ".csv", ".odt"],
    "Instaladores": [".exe", ".msi", ".dmg", ".pkg", ".deb", ".rpm"],
    "Compactados": [".zip", ".rar", ".7z", ".tar", ".gz"],
    "Codigo": [".py", ".js", ".html", ".css", ".json", ".sql", ".cpp", ".java"],
    "Midia": [".mp4", ".mkv", ".avi", ".mp3", ".wav", ".flac"]
}

def organizar_pasta(pasta_alvo):
    caminho_base = Path(pasta_alvo)
    if not caminho_base.exists():
        print(f"Erro: A pasta {caminho_base} não foi encontrada.")
        return

    for arquivo in caminho_base.iterdir():
        # Ignora subdiretórios e arquivos temporários/ocultos (ex: em Downloads do navegador)
        if arquivo.is_dir() or arquivo.name.startswith('.') or arquivo.suffix in ['.crdownload', '.tmp']:
            continue
        
        extensao = arquivo.suffix.lower()
        movido = False

        for pasta_destino, extensoes in DIRECTORY_MAPPING.items():
            if extensao in extensoes:
                pasta_dir = caminho_base / pasta_destino
                pasta_dir.mkdir(exist_ok=True)
                
                destino_final = pasta_dir / arquivo.name
                
                # Tratamento de conflito: se o arquivo já existe, adiciona um sufixo numérico
                contador = 1
                while destino_final.exists():
                    destino_final = pasta_dir / f"{arquivo.stem}_{contador}{arquivo.suffix}"
                    contador += 1
                    
                shutil.move(str(arquivo), str(destino_final))
                print(f"[Organizado] {arquivo.name} -> {pasta_destino}/")
                movido = True
                break
        
        # Se a extensão não estiver mapeada, vai para a pasta 'Outros'
        if not movido:
            pasta_outros = caminho_base / "Outros"
            pasta_outros.mkdir(exist_ok=True)
            destino_final = pasta_outros / arquivo.name
            
            contador = 1
            while destino_final.exists():
                destino_final = pasta_outros / f"{arquivo.stem}_{contador}{arquivo.suffix}"
                contador += 1
                
            shutil.move(str(arquivo), str(destino_final))
            print(f"[Outros] {arquivo.name} -> Outros/")

if __name__ == "__main__":
    # Pega automaticamente a pasta Downloads do usuário atual
    pasta_downloads = Path.home() / "Downloads"
    
    print(f"Iniciando monitoramento da pasta: {pasta_downloads}")
    print("Pressione Ctrl+C para encerrar o script a qualquer momento.\n")
    
    try:
        while True:
            organizar_pasta(pasta_downloads)
            # Intervalo de verificação em segundos (ajuste conforme preferir)
            time.sleep(10)
    except KeyboardInterrupt:
        print("\nMonitoramento encerrado com sucesso.")