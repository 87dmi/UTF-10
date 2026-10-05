import tkinter as tk
from tkinter import filedialog, messagebox
import string

# =====================================================================
# 1. CORE UTF-10 ENCODING ENGINE (12x12 Grid, Base-12)
# =====================================================================
rus_lowercase = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"
ALL_SYMBOLS = [" ", "\n", "=", "+", "-", "*", "/", "(", ")"] + list(string.digits) + list(rus_lowercase) + list(rus_lowercase.upper()) + list(string.ascii_lowercase) + list(string.ascii_uppercase)
CHAR_TO_UTF10 = {char: f"{i // 12},{i % 12}" for i, char in enumerate(ALL_SYMBOLS)}
UTF10_TO_CHAR = {f"{i // 12},{i % 12}": char for i, char in enumerate(ALL_SYMBOLS)}

def encode_utf10(text):
    return " ".join([CHAR_TO_UTF10.get(char, "0,0") for char in text])

def decode_utf10(utf10_string):
    if not utf10_string.strip(): return ""
    return "".join([UTF10_TO_CHAR.get(pair, "?") for pair in utf10_string.split(" ")])

def load_config():
    return {"secret_active": True, "theme": "matrix"}

# =====================================================================
# 2. MIX-SCRIPT INTERPRETER
# =====================================================================
def run_u10_script(source_code):
    lines = decode_utf10(encode_utf10(source_code)).split('\n')
    variables = {}
    output = ["--- Запуск программы на MIX-Script (.MIX) ---"]
    for line_num, line in enumerate(lines, 1):
        line = line.strip()
        if not line or line.startswith("#"): continue
        try:
            if "=" in line and not (line.startswith("print ") or line.startswith("принт ") or line.startswith("печать ")):
                var_name, var_value = line.split("=", 1)
                var_name, var_value = var_name.strip(), var_value.strip()
                expr = var_value
                for v_name, v_val in variables.items():
                    expr = expr.replace(v_name, str(v_val))
                try: variables[var_name] = int(eval(expr))
                except: variables[var_name] = var_value
            elif line.startswith("print ") or line.startswith("принт ") or line.startswith("печать "):
                cmd_len = 6 if (line.startswith("print ") or line.startswith("принт ")) else 7
                target = line[cmd_len:].strip()
                if target.startswith("(") and target.endswith(")"):
                    expr = target[1:-1].strip()
                    for v_name, v_val in variables.items():
                        expr = expr.replace(v_name, str(v_val))
                    try: output.append(str(int(eval(expr))))
                    except: output.append(f"Ошибка математики в скобках: {target}")
                else:
                    output.append(f"{variables[target]}" if target in variables else f"{target}")
            else:
                output.append(f"Ошибка (строка {line_num}): Неизвестная команда '{line}'")
        except Exception as e:
            output.append(f"Системная ошибка на строке {line_num}: {str(e)}")
    output.append("--- Программа завершена ---")
    return "\n".join(output)

# =====================================================================
# 3. INTERFACE ARCHITECTURE CLASS (Grid Layout Wireframe)
# =====================================================================
class DashboardApp:
    def __init__(self, root, cfg):
        self.root = root
        self.current_mode = "code"
        
        self.root.title("MIX-Studio v9.5")
        self.root.geometry("1100x750")
        self.root.configure(bg="#000000")
        
        self.root.grid_columnconfigure(0, weight=3)
        self.root.grid_columnconfigure(1, weight=1, minsize=350)
        self.root.grid_rowconfigure(0, weight=1)
        
        # Left main panel layout
        self.left_panel = tk.Frame(self.root, bg="#000000")
        self.left_panel.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        
        self.frame_top_menu = tk.Frame(self.left_panel, bg="#000000")
        self.frame_top_menu.pack(fill="x", anchor="w", pady=5)
        
        self.btn_mode_switch = tk.Button(self.frame_top_menu, text="🖼️ Перейти к Графической Базе", bg="#000000", fg="#00FF00", activebackground="#00FF00", activeforeground="#000000", font=("Arial", 9, "bold"), bd=1, relief="solid", command=self.toggle_view_mode)
        self.btn_mode_switch.pack(side="left", padx=2)
        
        tk.Label(self.frame_top_menu, text=" 📋 Шаблоны:", fg="#FFFFFF", bg="#000000", font=("Arial", 9, "bold")).pack(side="left", padx=5)
        tk.Button(self.frame_top_menu, text="📊 Status", bg="#000000", fg="#00FF00", font=("Arial", 9), bd=1, relief="solid", command=lambda: self.load_template("status")).pack(side="left", padx=2)
        tk.Button(self.frame_top_menu, text="🧮 Math", bg="#000000", fg="#00FF00", font=("Arial", 9), bd=1, relief="solid", command=lambda: self.load_template("math")).pack(side="left", padx=2)
        tk.Button(self.frame_top_menu, text="📡 Ping", bg="#000000", fg="#00FF00", font=("Arial", 9), bd=1, relief="solid", command=lambda: self.load_template("ping")).pack(side="left", padx=2)
        tk.Button(self.frame_top_menu, text="🧹 Clean", bg="#000000", fg="#00FF00", font=("Arial", 9), bd=1, relief="solid", command=lambda: self.load_template("clean")).pack(side="left", padx=2)
        tk.Button(self.frame_top_menu, text="🔑 Pass", bg="#000000", fg="#00FF00", font=("Arial", 9), bd=1, relief="solid", command=lambda: self.load_template("pass")).pack(side="left", padx=2)
        
        self.lbl_left_title = tk.Label(self.left_panel, text="📝 ИСХОДНЫЙ КОД (.MIX):", fg="#FFFFFF", bg="#000000", font=("Arial", 10, "bold"))
        self.lbl_left_title.pack(anchor="w", pady=2)
        
        self.code_area = tk.Text(self.left_panel, bg="#000000", fg="#00FF00", insertbackground="#00FF00", font=("Consolas", 12), bd=1, relief="solid")
        self.code_area.pack(fill="both", expand=True, pady=5)
        self.code_area.insert("1.0", "принт (1+1)\nбаза = 10\nпечать MIX-Script готов!")
        
        self.frame_code_controls = tk.Frame(self.left_panel, bg="#000000")
        self.frame_code_controls.pack(fill="x", pady=2)
        tk.Button(self.frame_code_controls, text="▶ Запустить MIX-Script код", bg="#000000", fg="#00FF00", font=("Arial", 10, "bold"), bd=1, relief="solid", command=self.execute_code).pack(side="left", expand=True, fill="x", padx=2)
        tk.Button(self.frame_code_controls, text="💥 Скопировать текстовый шифр", bg="#000000", fg="#00FF00", font=("Arial", 10, "bold"), bd=1, relief="solid", command=self.copy_text_cipher).pack(side="right", expand=True, fill="x", padx=2)
        
        self.img_code_area = tk.Text(self.left_panel, bg="#000000", fg="#00FF00", insertbackground="#00FF00", font=("Consolas", 11), bd=1, relief="solid")
        self.frame_img_controls = tk.Frame(self.left_panel, bg="#000000")
        tk.Button(self.frame_img_controls, text="📸 Зашифровать Картинку", bg="#000000", fg="#00FF00", font=("Arial", 10, "bold"), bd=1, relief="solid", command=self.load_and_encrypt_image).pack(side="left", expand=True, fill="x", padx=2)
        tk.Button(self.frame_img_controls, text="🖼️ Показать из шифра", bg="#000000", fg="#00FF00", font=("Arial", 10, "bold"), bd=1, relief="solid", command=self.show_decrypted_image).pack(side="left", expand=True, fill="x", padx=2)
        tk.Button(self.frame_img_controls, text="💥 Скопировать граф. шифр", bg="#000000", fg="#00FF00", font=("Arial", 10, "bold"), bd=1, relief="solid", command=self.copy_img_cipher).pack(side="right", expand=True, fill="x", padx=2)
        self.canvas_view = tk.Canvas(self.left_panel, width=150, height=150, bg="#000000", bd=0, highlightthickness=1, highlightbackground="#333333")
        
        tk.Label(self.left_panel, text="📟 Консоль вывода ядра:", fg="#FFFFFF", bg="#000000", font=("Arial", 10, "bold")).pack(anchor="w", pady=2)
        self.console_area = tk.Text(self.left_panel, height=6, bg="#000000", fg="#00FF00", state=tk.DISABLED, font=("Consolas", 11), bd=1, relief="solid")
        self.console_area.pack(fill="x", pady=2)
        
        # Right decoder column structure
        self.right_panel = tk.Frame(self.root, bg="#000000", bd=1, relief="solid")
        self.right_panel.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        
        tk.Label(self.right_panel, text="🕵️‍♂️ ДЕКОДЕР UTF-10 v2.1:", fg="#00FF00", bg="#000000", font=("Arial", 11, "bold")).pack(anchor="w", padx=10, pady=10)
        tk.Label(self.right_panel, text="Вставь шифр (координаты):", fg="#FFFFFF", bg="#000000", font=("Arial", 9)).pack(anchor="w", padx=10)
        
        self.decoder_input_area = tk.Text(self.right_panel, height=8, bg="#000000", fg="#00FF00", insertbackground="#00FF00", font=("Consolas", 11), bd=1, relief="solid")
        self.decoder_input_area.pack(fill="x", padx=10, pady=5)
        self.decoder_input_area.insert("1.0", "2,11 3,0 2,4 2,9 3,2")
        
        tk.Button(self.right_panel, text="🔍 РАСШИФРОВАТЬ ДАННЫЕ", bg="#000000", fg="#00FF00", font=("Arial", 10, "bold"), bd=1, relief="solid", command=self.decode_input_text).pack(fill="x", padx=10, pady=10)
        
        self.decoder_output_area = tk.Text(self.right_panel, bg="#000000", fg="#FFFFFF", font=("Consolas", 12, "bold"), bd=1, relief="solid")
        self.decoder_output_area.pack(fill="both", expand=True, padx=10, pady=10)

    def toggle_view_mode(self):
        if self.current_mode == "code":
            self.current_mode = "img"
            self.lbl_left_title.config(text="🖼️ ГРАФИЧЕСКАЯ БАЗА (.IMG):")
            self.code_area.pack_forget()
            self.frame_code_controls.pack_forget()
            self.img_code_area.pack(fill="both", expand=True, pady=5)
            self.frame_img_controls.pack(fill="x", pady=5)
            self.canvas_view.pack(pady=10)
            self.btn_mode_switch.config(text="📝 Перейти к Редактору Кода")
        else:
            self.current_mode = "code"
