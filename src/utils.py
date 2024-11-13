from datetime import datetime
import os

log_widget = None  # Variável global para armazenar o widget de log

def configurar_log_widget(widget):
    global log_widget
    log_widget = widget

def adicionar_ao_log(mensagem):
    print(mensagem)
    if log_widget:
        timestamp = datetime.now().strftime("[%Y-%m-%d %H:%M:%S] ")
        log_widget.insert("end", timestamp + mensagem + "\n")
        log_widget.see("end")
        log_widget.update_idletasks()

def Create_output_folder(base_path="output"):
    try:
        adicionar_ao_log("Creating Output folder...")
        # Define o caminho da pasta principal
        pasta_principal = os.path.join(base_path)
        
        # Lista com os nomes das subpastas
        subpastas = ["InstrumentedSUT", "TestDriver", "Report", "OutputBuffer"]
        
        # Cria a pasta principal, se não existir
        if not os.path.exists(pasta_principal):
            os.makedirs(pasta_principal)
        
        # Cria as subpastas dentro da pasta principal
        for subpasta in subpastas:
            caminho_subpasta = os.path.join(pasta_principal, subpasta)
            if not os.path.exists(caminho_subpasta):
                os.makedirs(caminho_subpasta)

        adicionar_ao_log("Output folder created successfully.")
        return 0
    except:
        error = f"ERROR: Output folder not created properly." # {e.stderr}
        adicionar_ao_log(error)
        return error
