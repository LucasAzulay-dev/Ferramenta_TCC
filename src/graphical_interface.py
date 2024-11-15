import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk
import fitz  # PyMuPDF
from Ferramenta_TCC import executar_ferramenta
from utils import adicionar_ao_log, configurar_log_widget, adicionar_ao_log_error
import os

pdf_files_path = []
pdf_index = 0
page_index = 0

def select_excel():
    excel_file_path = filedialog.askopenfilename(title="Select Excel File", filetypes=[("Excel files", ".xlsx .xls")])
    entry_excel.delete(0, tk.END)
    entry_excel.insert(0, excel_file_path)

def select_sut():
    sut_file_path = filedialog.askopenfilename(title="Select SUT File", filetypes=[("C files", "*.c")])
    entry_sut.delete(0, tk.END)
    entry_sut.insert(0, sut_file_path)

#é pra selecionar uma pasta com todos os arquivos para compilação
def select_folder():
    folder_path = filedialog.askdirectory(title="Select Folder with Files to Compile")
    entry_folder.delete(0, tk.END)
    entry_folder.insert(0, folder_path)

def display_pdf(pdf_files_path,index, page_num=0):
    if not pdf_files_path:
        return 0
    global page_index
    if 0 <= index < len(pdf_files_path):
        try:
            doc = fitz.open(pdf_files_path[index])
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
                
                #adicionar_ao_log(f"Displaying page {page_index + 1} of {total_pages} from PDF {index + 1}")
            else:
                adicionar_ao_log("Page number out of range.")
            
            doc.close()
        except Exception as e:
            messagebox.showerror("Error", f"Error opening PDF: {e}")

def next_pdf():
    global pdf_index, page_index, pdf_files_path
    if pdf_index < len(pdf_files_path) - 1:
        pdf_index += 1
        page_index = 0
        display_pdf(pdf_files_path, pdf_index, page_index)

def previous_pdf():
    global pdf_index, page_index, pdf_files_path
    if pdf_index > 0:
        pdf_index -= 1
        page_index = 0
        display_pdf(pdf_files_path, pdf_index, page_index)

def next_page():
    global pdf_index, page_index, pdf_files_path
    display_pdf(pdf_files_path, pdf_index, page_index + 1)

def previous_page():
    global pdf_index, page_index, pdf_files_path
    display_pdf(pdf_files_path, pdf_index, page_index - 1)

def execute():
    excel_file_path = entry_excel.get()
    sut_file_path = entry_sut.get()
    function_name = entry_func_name.get()
    compiler = compiler_var.get()
    folder_path = entry_folder.get()
    buffer_length = entry_buffer_name.get()

    if not excel_file_path or not sut_file_path or not function_name:
        messagebox.showwarning("Warning", "Please fill all fields.")
        return
    
    adicionar_ao_log("Starting tool execution...")
    window.update_idletasks()

    try:
        if(not buffer_length):
            buffer_length = 33554432
        
        global pdf_files_path

        pdf_files_path = executar_ferramenta(excel_file_path, sut_file_path, function_name, compiler,buffer_length)
        
        if(not pdf_files_path):
            adicionar_ao_log_error("ERROR: DC/CC report not generated properly.")
            return

        output_path = "output"
        output_abs_path = os.path.abspath(output_path)

        #os.startfile(output_path, 'open')     #uncomment to open the folder at the end

        global pdf_index, page_index
        pdf_index = 0
        page_index = 0
        display_pdf(pdf_files_path, pdf_index, page_index)
        adicionar_ao_log("Execution completed.")
        adicionar_ao_log(f"Outputs can be find at {output_abs_path}.")

    except Exception as e:
        adicionar_ao_log_error(f"Execution error: {e}")
        messagebox.showerror("Error", f"An error occurred: {e}")

if __name__ == "__main__":
    window = tk.Tk()
    window.title("TCC Tool")
    window.geometry("1200x720")
    window.configure(bg="#f5f5f5")

    default_font = ("Helvetica", 10, "bold")
    title_font = ("Helvetica", 12, "bold")
    button_style = {"font": default_font, "bg": "#4a90e2", "fg": "white", "activebackground": "#357ABD", "activeforeground": "white"}

    left_frame = ttk.Frame(window, padding="10")
    left_frame.grid(row=0, column=0, sticky="nswe")
    right_frame = ttk.Frame(window, padding="10")
    right_frame.grid(row=0, column=1, sticky="nswe")

    window.grid_columnconfigure(0, weight=1)
    window.grid_columnconfigure(1, weight=2)
    window.grid_rowconfigure(0, weight=1)  

    frame_excel = ttk.Frame(left_frame)
    frame_excel.pack(pady=5, fill="x")
    label_excel = ttk.Label(frame_excel, text="Excel File:", font=default_font)
    label_excel.pack(side="left")
    entry_excel = ttk.Entry(frame_excel, width=40, font=default_font)
    entry_excel.pack(side="left", padx=5)
    button_excel = tk.Button(frame_excel, text="Select", command=select_excel, **button_style)
    button_excel.pack(side="left")

    frame_sut = ttk.Frame(left_frame)
    frame_sut.pack(pady=5, fill="x")
    label_sut = ttk.Label(frame_sut, text="SUT File:", font=default_font)
    label_sut.pack(side="left")
    entry_sut = ttk.Entry(frame_sut, width=40, font=default_font)
    entry_sut.pack(side="left", padx=5)
    button_sut = tk.Button(frame_sut, text="Select", command=select_sut, **button_style)
    button_sut.pack(side="left")

    frame_folder = ttk.Frame(left_frame)
    frame_folder.pack(pady=5, fill="x")
    label_folder = ttk.Label(frame_folder, text="Folder with Files to Compile:", font=default_font)
    label_folder.pack(side="left")
    entry_folder = ttk.Entry(frame_folder, width=40, font=default_font)
    entry_folder.pack(side="left", padx=5)
    button_folder = tk.Button(frame_folder, text="Select", command=select_folder, **button_style)
    button_folder.pack(side="left")

    frame_func = ttk.Frame(left_frame)
    frame_func.pack(pady=5, fill="x")
    label_func_name = ttk.Label(frame_func, text="Function Name:", font=default_font)
    label_func_name.pack(side="left")
    entry_func_name = ttk.Entry(frame_func, width=40, font=default_font)
    entry_func_name.pack(side="left", padx=5)

    frame_buffer = ttk.Frame(left_frame)
    frame_buffer.pack(pady=5, fill="x")
    label_buffer_name = ttk.Label(frame_buffer, text="Buffer length in bytes (optional):", font=default_font)
    label_buffer_name.pack(side="left")
    entry_buffer_name = ttk.Entry(frame_buffer, width=40, font=default_font)
    entry_buffer_name.pack(side="left", padx=5)

    frame_compiler = ttk.Frame(left_frame)
    frame_compiler.pack(pady=5, fill="x")
    label_compiler = ttk.Label(frame_compiler, text="Compiler Type:", font=default_font)
    label_compiler.pack(side="left")
    compiler_var = tk.StringVar(value="gcc")
    radio_gcc = tk.Radiobutton(frame_compiler, text="gcc", variable=compiler_var, value="gcc", font=default_font)
    radio_clang = tk.Radiobutton(frame_compiler, text="clang", variable=compiler_var, value="clang", font=default_font)
    radio_gcc.pack(side="left", padx=5)
    radio_clang.pack(side="left", padx=5)
    button_execute = tk.Button(left_frame, text="Run Tool", command=execute, **button_style)
    button_execute.pack(pady=20)

    log_frame = ttk.Frame(left_frame)
    log_frame.pack(pady=10, fill="both", expand=True)
    log_label = ttk.Label(log_frame, text="Execution Log:", font=title_font)
    log_label.pack(anchor="w")
    log_display = tk.Text(log_frame, wrap="word", height=10, state="normal", relief="sunken", bg="#e6e6e6", font=default_font)
    log_display.pack(fill="both", expand=True)
    log_display.tag_configure("black", foreground="black")
    log_display.tag_configure("red", foreground="red")
    log_display.config(state="disable")
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
    button_previous_pdf = tk.Button(navigation_frame, text="Previous PDF", command=previous_pdf, **button_style)
    button_previous_pdf.pack(side="left", padx=5)
    button_next_pdf = tk.Button(navigation_frame, text="Next PDF", command=next_pdf, **button_style)
    button_next_pdf.pack(side="left", padx=5)
    button_previous_page = tk.Button(navigation_frame, text="Previous Page", command=previous_page, **button_style)
    button_previous_page.pack(side="left", padx=5)
    button_next_page = tk.Button(navigation_frame, text="Next Page", command=next_page, **button_style)
    button_next_page.pack(side="left", padx=5)

    window.mainloop()
