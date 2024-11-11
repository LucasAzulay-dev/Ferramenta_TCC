import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk
import fitz  # PyMuPDF
from Ferramenta_TCC import executar_ferramenta, relatorio
from datetime import datetime
from utils import adicionar_ao_log, configurar_log_widget

pdf_files = ["estrutura_sut.pdf", "dc_cc_analysis_report.pdf"]
pdf_index = 0
page_index = 0

def selecionar_excel():
    caminho_excel = filedialog.askopenfilename(title="Selecione o arquivo Excel", filetypes=[("Excel files", "*.xlsx")])
    entry_excel.delete(0, tk.END)
    entry_excel.insert(0, caminho_excel)

def selecionar_sut():
    caminho_sut = filedialog.askopenfilename(title="Selecione o arquivo do SUT", filetypes=[("C files", "*.c")])
    entry_sut.delete(0, tk.END)
    entry_sut.insert(0, caminho_sut)

def exibir_pdf(index, page_num=0):
    global page_index
    if 0 <= index < len(pdf_files):
        try:
            doc = fitz.open(pdf_files[index])
            total_pages = doc.page_count
            
            if 0 <= page_num < total_pages:
                page_index = page_num
                page = doc.load_page(page_index)
                pix = page.get_pixmap()
                
                img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
                img_tk = ImageTk.PhotoImage(img)
                
                pdf_canvas.create_image(0, 0, anchor="nw", image=img_tk)
                pdf_canvas.image = img_tk
                pdf_canvas.config(scrollregion=pdf_canvas.bbox("all"))
                
                adicionar_ao_log(f"Exibindo página {page_index + 1} de {total_pages} do PDF {index + 1}")
            else:
                adicionar_ao_log("Número de página fora dos limites.")
            
            doc.close()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao abrir o PDF: {e}")

def proximo_pdf():
    global pdf_index, page_index
    if pdf_index < len(pdf_files) - 1:
        pdf_index += 1
        page_index = 0
        exibir_pdf(pdf_index, page_index)

def anterior_pdf():
    global pdf_index, page_index
    if pdf_index > 0:
        pdf_index -= 1
        page_index = 0
        exibir_pdf(pdf_index, page_index)

def proxima_pagina():
    global pdf_index, page_index
    exibir_pdf(pdf_index, page_index + 1)

def pagina_anterior():
    global pdf_index, page_index
    exibir_pdf(pdf_index, page_index - 1)

def executar():
    excel_file_path = entry_excel.get()
    code_path = entry_sut.get()
    function_name = entry_func_name.get()
    compiler = compiler_var.get()

    if not excel_file_path or not code_path or not function_name:
        messagebox.showwarning("Aviso", "Por favor, preencha todos os campos.")
        return
    
    adicionar_ao_log("Iniciando execução da ferramenta...")
    janela.update_idletasks()

    try:
        executar_ferramenta(excel_file_path, code_path, function_name, compiler)
        adicionar_ao_log(str(relatorio()))
        
        adicionar_ao_log("Execução concluída com sucesso.")
        
        global pdf_index, page_index
        pdf_index = 0
        page_index = 0
        exibir_pdf(pdf_index, page_index)
        
    except Exception as e:
        adicionar_ao_log(f"Erro durante a execução: {e}")
        messagebox.showerror("Erro", f"Ocorreu um erro: {e}")

if __name__ == "__main__":
    janela = tk.Tk()
    janela.title("Ferramenta TCC")
    janela.geometry("1000x600")
    janela.configure(bg="#f5f5f5")

    fonte_padrao = ("Helvetica", 10, "bold")
    fonte_titulo = ("Helvetica", 12, "bold")
    estilo_botao = {"font": fonte_padrao, "bg": "#4a90e2", "fg": "white", "activebackground": "#357ABD", "activeforeground": "white"}

    left_frame = ttk.Frame(janela, padding="10")
    left_frame.grid(row=0, column=0, sticky="nswe")
    right_frame = ttk.Frame(janela, padding="10")
    right_frame.grid(row=0, column=1, sticky="nswe")

    janela.grid_columnconfigure(0, weight=1)
    janela.grid_columnconfigure(1, weight=2)
    janela.grid_rowconfigure(0, weight=1)  

    frame_excel = ttk.Frame(left_frame)
    frame_excel.pack(pady=5, fill="x")
    label_excel = ttk.Label(frame_excel, text="Arquivo Excel:", font=fonte_padrao)
    label_excel.pack(side="left")
    entry_excel = ttk.Entry(frame_excel, width=40, font=fonte_padrao)
    entry_excel.pack(side="left", padx=5)
    botao_excel = tk.Button(frame_excel, text="Selecionar", command=selecionar_excel, **estilo_botao)
    botao_excel.pack(side="left")

    frame_sut = ttk.Frame(left_frame)
    frame_sut.pack(pady=5, fill="x")
    label_sut = ttk.Label(frame_sut, text="Arquivo SUT:", font=fonte_padrao)
    label_sut.pack(side="left")
    entry_sut = ttk.Entry(frame_sut, width=40, font=fonte_padrao)
    entry_sut.pack(side="left", padx=5)
    botao_sut = tk.Button(frame_sut, text="Selecionar", command=selecionar_sut, **estilo_botao)
    botao_sut.pack(side="left")

    frame_func = ttk.Frame(left_frame)
    frame_func.pack(pady=5, fill="x")
    label_func_name = ttk.Label(frame_func, text="Nome da Função:", font=fonte_padrao)
    label_func_name.pack(side="left")
    entry_func_name = ttk.Entry(frame_func, width=40, font=fonte_padrao)
    entry_func_name.pack(side="left", padx=5)

    frame_compiler = ttk.Frame(left_frame)
    frame_compiler.pack(pady=5, fill="x")
    label_compiler = ttk.Label(frame_compiler, text="Tipo de Compilador:", font=fonte_padrao)
    label_compiler.pack(side="left")
    compiler_var = tk.StringVar(value="gcc")
    radio_gcc = tk.Radiobutton(frame_compiler, text="gcc", variable=compiler_var, value="gcc", font=fonte_padrao)
    radio_clang = tk.Radiobutton(frame_compiler, text="clang", variable=compiler_var, value="clang", font=fonte_padrao)
    radio_gcc.pack(side="left", padx=5)
    radio_clang.pack(side="left", padx=5)
    botao_executar = tk.Button(left_frame, text="Executar Ferramenta", command=executar, **estilo_botao)
    botao_executar.pack(pady=20)

    log_frame = ttk.Frame(left_frame)
    log_frame.pack(pady=10, fill="both", expand=True)
    log_label = ttk.Label(log_frame, text="Log de Execução:", font=fonte_titulo)
    log_label.pack(anchor="w")
    log_display = tk.Text(log_frame, wrap="word", height=10, state="normal", relief="sunken", bg="#e6e6e6", font=fonte_padrao)
    log_display.pack(fill="both", expand=True)
    configurar_log_widget(log_display)

    pdf_frame = ttk.Frame(right_frame)
    pdf_frame.pack(fill="both", expand=True)
    pdf_canvas = tk.Canvas(pdf_frame, bg="white")
    pdf_canvas.pack(side="left", fill="both", expand=True)

    scroll_x = tk.Scrollbar(pdf_frame, orient="horizontal", command=pdf_canvas.xview)
    scroll_x.pack(side="bottom", fill="x")
    scroll_y = tk.Scrollbar(pdf_frame, orient="vertical", command=pdf_canvas.yview)
    scroll_y.pack(side="right", fill="y")
    pdf_canvas.configure(xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)

    navigation_frame = ttk.Frame(right_frame)
    navigation_frame.pack(pady=10)
    botao_anterior_pdf = tk.Button(navigation_frame, text="PDF Anterior", command=anterior_pdf, **estilo_botao)
    botao_anterior_pdf.pack(side="left", padx=5)
    botao_proximo_pdf = tk.Button(navigation_frame, text="Próximo PDF", command=proximo_pdf, **estilo_botao)
    botao_proximo_pdf.pack(side="left", padx=5)
    botao_anterior_pagina = tk.Button(navigation_frame, text="Página Anterior", command=pagina_anterior, **estilo_botao)
    botao_anterior_pagina.pack(side="left", padx=5)
    botao_proxima_pagina = tk.Button(navigation_frame, text="Próxima Página", command=proxima_pagina, **estilo_botao)
    botao_proxima_pagina.pack(side="left", padx=5)

    janela.mainloop()
