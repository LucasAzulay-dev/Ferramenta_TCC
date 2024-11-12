from datetime import datetime

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


