import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk
import fitz
from Ferramenta_TCC import executar_ferramenta

def selecionar_excel():
    caminho_excel = filedialog.askopenfilename(title="Selecione o arquivo Excel", filetypes=[("Excel files", "*.xlsx")])
    entry_excel.delete(0, tk.END)
    entry_excel.insert(0, caminho_excel)

def selecionar_sut():
    caminho_sut = filedialog.askopenfilename(title="Selecione o arquivo do SUT", filetypes=[("C files", "*.c")])
    entry_sut.delete(0, tk.END)
    entry_sut.insert(0, caminho_sut)

def adicionar_ao_log(mensagem):
    log_display.insert(tk.END, mensagem + "\n")
    log_display.see(tk.END)

def exibir_pdf(pdf_path):
    try:
        doc = fitz.open(pdf_path)
        
        page = doc.load_page(0)
        pix = page.get_pixmap()
        
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        img_tk = ImageTk.PhotoImage(img)
        
        pdf_canvas.create_image(0, 0, anchor="nw", image=img_tk)
        pdf_canvas.image = img_tk
        pdf_canvas.config(scrollregion=pdf_canvas.bbox("all")) 
        
        doc.close()
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao abrir o PDF: {e}")

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
        adicionar_ao_log("Execução concluída com sucesso.")
        
        pdf_path = "estrutura_sut.pdf"
        exibir_pdf(pdf_path)

    except Exception as e:
        adicionar_ao_log(f"Erro durante a execução: {e}")
        messagebox.showerror("Erro", f"Ocorreu um erro: {e}")

janela = tk.Tk()
janela.title("Ferramenta TCC")
janela.geometry("800x600")

style = ttk.Style()
style.configure("TFrame", background="#f0f0f0")
style.configure("TLabel", background="#f0f0f0", font=("Arial", 10))
style.configure("TButton", font=("Arial", 10))

main_frame = ttk.Panedwindow(janela, orient=tk.HORIZONTAL)
main_frame.pack(fill="both", expand=True)

left_frame = ttk.Frame(main_frame, padding="10")
main_frame.add(left_frame, weight=1)

frame_excel = ttk.Frame(left_frame)
frame_excel.pack(pady=5, fill="x")
label_excel = ttk.Label(frame_excel, text="Arquivo Excel:")
label_excel.pack(side="left")
entry_excel = ttk.Entry(frame_excel, width=50)
entry_excel.pack(side="left", padx=5)
botao_excel = ttk.Button(frame_excel, text="Selecionar", command=selecionar_excel)
botao_excel.pack(side="left")

frame_sut = ttk.Frame(left_frame)
frame_sut.pack(pady=5, fill="x")
label_sut = ttk.Label(frame_sut, text="Arquivo SUT:")
label_sut.pack(side="left")
entry_sut = ttk.Entry(frame_sut, width=50)
entry_sut.pack(side="left", padx=5)
botao_sut = ttk.Button(frame_sut, text="Selecionar", command=selecionar_sut)
botao_sut.pack(side="left")

frame_func = ttk.Frame(left_frame)
frame_func.pack(pady=5, fill="x")
label_func_name = ttk.Label(frame_func, text="Nome da Função:")
label_func_name.pack(side="left")
entry_func_name = ttk.Entry(frame_func, width=50)
entry_func_name.pack(side="left", padx=5)

frame_compiler = ttk.Frame(left_frame)
frame_compiler.pack(pady=5, fill="x")
label_compiler = ttk.Label(frame_compiler, text="Tipo de Compilador:")
label_compiler.pack(side="left")
compiler_var = tk.StringVar(value="gcc")
radio_gcc = ttk.Radiobutton(frame_compiler, text="gcc", variable=compiler_var, value="gcc")
radio_clang = ttk.Radiobutton(frame_compiler, text="clang", variable=compiler_var, value="clang")
radio_gcc.pack(side="left", padx=5)
radio_clang.pack(side="left", padx=5)

botao_executar = ttk.Button(left_frame, text="Executar Ferramenta", command=executar)
botao_executar.pack(pady=20)

log_frame = ttk.Frame(left_frame)
log_frame.pack(pady=10, fill="both", expand=True)
log_label = ttk.Label(log_frame, text="Log de Execução:", font=("Arial", 10, "bold"))
log_label.pack(anchor="w")
log_display = tk.Text(log_frame, wrap="word", height=8, state="normal", relief="sunken", bg="#f7f7f7", font=("Arial", 10))
log_display.pack(fill="both", expand=True)

right_frame = ttk.Frame(main_frame, padding="10")
main_frame.add(right_frame, weight=3)

pdf_canvas = tk.Canvas(right_frame)
pdf_canvas.pack(side="left", fill="both", expand=True)

scroll_x = tk.Scrollbar(right_frame, orient="horizontal", command=pdf_canvas.xview)
scroll_x.pack(side="bottom", fill="x")
scroll_y = tk.Scrollbar(right_frame, orient="vertical", command=pdf_canvas.yview)
scroll_y.pack(side="right", fill="y")

pdf_canvas.configure(xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)

janela.mainloop()
