import tkinter as tk
from tkinter import ttk, messagebox
import random
import string
import json
import os
from datetime import datetime


# ========== ОСНОВНОЙ КЛАСС ПРИЛОЖЕНИЯ ==========

class PasswordGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("Random Password Generator")
        self.root.geometry("800x650")
        self.root.resizable(False, False)
        self.root.configure(bg="#1e1e2e")

        # Переменные для настроек
        self.password_length = tk.IntVar(value=12)
        self.use_uppercase = tk.BooleanVar(value=True)
        self.use_lowercase = tk.BooleanVar(value=True)
        self.use_digits = tk.BooleanVar(value=True)
        self.use_symbols = tk.BooleanVar(value=True)

        # История паролей
        self.history = []
        self.history_file = "password_history.json"

        # Загрузка истории из файла
        self.load_history()

        # Создание интерфейса
        self.setup_ui()

        # Генерация первого пароля
        self.generate_password()

    def setup_ui(self):
        # Заголовок
        title_label = tk.Label(
            self.root,
            text="🔐 RANDOM PASSWORD GENERATOR 🔐",
            font=("Arial", 20, "bold"),
            bg="#1e1e2e",
            fg="#cba6f7"
        )
        title_label.pack(pady=15)

        # Основной контейнер
        main_container = tk.Frame(self.root, bg="#1e1e2e")
        main_container.pack(fill="both", expand=True, padx=20, pady=10)

        # ========== ЛЕВАЯ ПАНЕЛЬ (НАСТРОЙКИ) ==========
        left_panel = tk.Frame(main_container, bg="#1e1e2e")
        left_panel.pack(side="left", fill="both", expand=True, padx=(0, 10))

        # Фрейм отображения пароля
        display_frame = tk.LabelFrame(
            left_panel,
            text="Сгенерированный пароль",
            font=("Arial", 12, "bold"),
            bg="#1e1e2e",
            fg="#cdd6f4",
            relief="ridge",
            borderwidth=2
        )
        display_frame.pack(fill="x", pady=(0, 15))

        self.password_entry = tk.Entry(
            display_frame,
            font=("Courier", 14, "bold"),
            justify="center",
            state="readonly",
            readonlybackground="#313244",
            fg="#a6e3a1",
            relief="solid",
            borderwidth=2
        )
        self.password_entry.pack(fill="x", padx=10, pady=10)

        # Кнопка копирования
        copy_btn = tk.Button(
            display_frame,
            text="📋 Копировать в буфер",
            command=self.copy_to_clipboard,
            font=("Arial", 10),
            bg="#89b4fa",
            fg="#1e1e2e",
            activebackground="#89b4fa",
            cursor="hand2",
            relief="flat",
            padx=10,
            pady=5
        )
        copy_btn.pack(pady=(0, 10))

        # Фрейм настроек
        settings_frame = tk.LabelFrame(
            left_panel,
            text="Настройки пароля",
            font=("Arial", 12, "bold"),
            bg="#1e1e2e",
            fg="#cdd6f4",
            relief="ridge",
            borderwidth=2
        )
        settings_frame.pack(fill="x", pady=(0, 15))

        # Ползунок длины пароля
        length_frame = tk.Frame(settings_frame, bg="#1e1e2e")
        length_frame.pack(fill="x", padx=10, pady=10)

        tk.Label(
            length_frame,
            text="Длина пароля:",
            font=("Arial", 11),
            bg="#1e1e2e",
            fg="#cdd6f4"
        ).pack(side="left")

        self.length_value = tk.Label(
            length_frame,
            text="12",
            font=("Arial", 11, "bold"),
            bg="#1e1e2e",
            fg="#f9e2af"
        )
        self.length_value.pack(side="left", padx=10)

        self.length_slider = tk.Scale(
            length_frame,
            from_=4,
            to=32,
            orient="horizontal",
            variable=self.password_length,
            command=self.update_length_label,
            bg="#1e1e2e",
            fg="#cdd6f4",
            highlightthickness=0,
            troughcolor="#313244",
            sliderlength=20,
            length=200
        )
        self.length_slider.pack(side="left", padx=10)

        # Чекбоксы
        options_frame = tk.Frame(settings_frame, bg="#1e1e2e")
        options_frame.pack(fill="x", padx=10, pady=5)

        self.cb_upper = tk.Checkbutton(
            options_frame,
            text="Заглавные буквы (A-Z)",
            variable=self.use_uppercase,
            command=self.validate_options,
            bg="#1e1e2e",
            fg="#cdd6f4",
            selectcolor="#1e1e2e",
            activebackground="#1e1e2e"
        )
        self.cb_upper.pack(anchor="w", pady=2)

        self.cb_lower = tk.Checkbutton(
            options_frame,
            text="Строчные буквы (a-z)",
            variable=self.use_lowercase,
            command=self.validate_options,
            bg="#1e1e2e",
            fg="#cdd6f4",
            selectcolor="#1e1e2e",
            activebackground="#1e1e2e"
        )
        self.cb_lower.pack(anchor="w", pady=2)

        self.cb_digits = tk.Checkbutton(
            options_frame,
            text="Цифры (0-9)",
            variable=self.use_digits,
            command=self.validate_options,
            bg="#1e1e2e",
            fg="#cdd6f4",
            selectcolor="#1e1e2e",
            activebackground="#1e1e2e"
        )
        self.cb_digits.pack(anchor="w", pady=2)

        self.cb_symbols = tk.Checkbutton(
            options_frame,
            text="Спецсимволы (!@#$%^&*()_+-=)",
            variable=self.use_symbols,
            command=self.validate_options,
            bg="#1e1e2e",
            fg="#cdd6f4",
            selectcolor="#1e1e2e",
            activebackground="#1e1e2e"
        )
        self.cb_symbols.pack(anchor="w", pady=2)

        # Кнопка генерации
        generate_btn = tk.Button(
            settings_frame,
            text="🔄 СГЕНЕРИРОВАТЬ ПАРОЛЬ",
            command=self.generate_password,
            font=("Arial", 12, "bold"),
            bg="#a6e3a1",
            fg="#1e1e2e",
            activebackground="#a6e3a1",
            cursor="hand2",
            relief="flat",
            padx=20,
            pady=8
        )
        generate_btn.pack(pady=15)

        # ========== ПРАВАЯ ПАНЕЛЬ (ИСТОРИЯ) ==========
        right_panel = tk.Frame(main_container, bg="#1e1e2e")
        right_panel.pack(side="right", fill="both", expand=True, padx=(10, 0))

        history_frame = tk.LabelFrame(
            right_panel,
            text="История паролей",
            font=("Arial", 12, "bold"),
            bg="#1e1e2e",
            fg="#cdd6f4",
            relief="ridge",
            borderwidth=2
        )
        history_frame.pack(fill="both", expand=True)

        # Таблица истории (Treeview)
        columns = ("№", "Дата", "Длина", "Пароль")
        self.history_tree = ttk.Treeview(
            history_frame,
            columns=columns,
            show="headings",
            height=12,
            style="Custom.Treeview"
        )

        # Настройка стиля таблицы
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Custom.Treeview",
                        background="#313244",
                        foreground="#cdd6f4",
                        fieldbackground="#313244",
                        rowheight=25)
        style.configure("Custom.Treeview.Heading",
                        background="#1e1e2e",
                        foreground="#cba6f7",
                        font=("Arial", 10, "bold"))
        style.map("Custom.Treeview",
                  background=[("selected", "#89b4fa")])

        # Настройка колонок
        self.history_tree.heading("№", text="№")
        self.history_tree.heading("Дата", text="Дата и время")
        self.history_tree.heading("Длина", text="Длина")
        self.history_tree.heading("Пароль", text="Пароль")

        self.history_tree.column("№", width=40, anchor="center")
        self.history_tree.column("Дата", width=130)
        self.history_tree.column("Длина", width=60, anchor="center")
        self.history_tree.column("Пароль", width=220)

        # Скроллбар
        scrollbar = ttk.Scrollbar(
            history_frame,
            orient="vertical",
            command=self.history_tree.yview
        )
        self.history_tree.configure(yscrollcommand=scrollbar.set)

        self.history_tree.pack(side="left", fill="both", expand=True, padx=(5, 0), pady=5)
        scrollbar.pack(side="right", fill="y", padx=(0, 5), pady=5)

        # Кнопки управления историей
        history_btn_frame = tk.Frame(history_frame, bg="#1e1e2e")
        history_btn_frame.pack(fill="x", pady=(0, 10))

        clear_btn = tk.Button(
            history_btn_frame,
            text="🗑 Очистить историю",
            command=self.clear_history,
            font=("Arial", 9),
            bg="#f38ba8",
            fg="#1e1e2e",
            cursor="hand2",
            relief="flat",
            padx=10
        )
        clear_btn.pack(side="left", padx=10)

        save_btn = tk.Button(
            history_btn_frame,
            text="💾 Сохранить историю",
            command=self.save_history,
            font=("Arial", 9),
            bg="#89b4fa",
            fg="#1e1e2e",
            cursor="hand2",
            relief="flat",
            padx=10
        )
        save_btn.pack(side="left", padx=5)

        export_btn = tk.Button(
            history_btn_frame,
            text="📎 Экспорт в JSON",
            command=self.export_history,
            font=("Arial", 9),
            bg="#f9e2af",
            fg="#1e1e2e",
            cursor="hand2",
            relief="flat",
            padx=10
        )
        export_btn.pack(side="left", padx=5)

        # Обновление отображения истории
        self.update_history_display()

    def update_length_label(self, value):
        """Обновление метки длины пароля"""
        self.length_value.config(text=str(int(float(value))))

    def validate_options(self):
        """Проверка, что выбран хотя бы один тип символов"""
        if not (self.use_uppercase.get() or self.use_lowercase.get() or
                self.use_digits.get() or self.use_symbols.get()):
            messagebox.showwarning(
                "Предупреждение",
                "Выберите хотя бы один тип символов для генерации пароля!\nВключён тип 'Строчные буквы' по умолчанию."
            )
            self.use_lowercase.set(True)

    def get_character_set(self):
        """Получение набора символов на основе выбранных опций"""
        chars = ""
        if self.use_uppercase.get():
            chars += string.ascii_uppercase
        if self.use_lowercase.get():
            chars += string.ascii_lowercase
        if self.use_digits.get():
            chars += string.digits
        if self.use_symbols.get():
            chars += "!@#$%^&*()_+-=[]{}|;:,.<>?"
        return chars

    def generate_password(self):
        """Генерация случайного пароля"""
        length = self.password_length.get()

        # Проверка корректности длины
        if length < 4:
            messagebox.showerror("Ошибка", "Минимальная длина пароля - 4 символа!")
            self.password_length.set(4)
            length = 4
        elif length > 32:
            messagebox.showerror("Ошибка", "Максимальная длина пароля - 32 символа!")
            self.password_length.set(32)
            length = 32

        # Получение набора символов
        characters = self.get_character_set()

        # Проверка, что есть доступные символы
        if not characters:
            messagebox.showerror("Ошибка", "Выберите хотя бы один тип символов!")
            return None

        # Генерация пароля
        password = ''.join(random.choice(characters) for _ in range(length))

        # Обновление отображения
        self.password_entry.config(state="normal")
        self.password_entry.delete(0, tk.END)
        self.password_entry.insert(0, password)
        self.password_entry.config(state="readonly")

        # Добавление в историю
        self.add_to_history(password, length)

        return password

    def add_to_history(self, password, length):
        """Добавление пароля в историю"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.history.insert(0, {
            "timestamp": timestamp,
            "length": length,
            "password": password
        })

        # Ограничение истории (последние 50 паролей)
        if len(self.history) > 50:
            self.history = self.history[:50]

        self.update_history_display()
        self.save_history()

    def update_history_display(self):
        """Обновление отображения истории в таблице"""
        # Очистка текущего отображения
        for item in self.history_tree.get_children():
            self.history_tree.delete(item)

        # Добавление записей
        for i, entry in enumerate(self.history, 1):
            self.history_tree.insert("", "end", values=(
                i,
                entry["timestamp"],
                entry["length"],
                entry["password"]
            ))

    def copy_to_clipboard(self):
        """Копирование пароля в буфер обмена"""
        password = self.password_entry.get()
        if password:
            self.root.clipboard_clear()
            self.root.clipboard_append(password)
            messagebox.showinfo("Успех", "✅ Пароль скопирован в буфер обмена!")

    def clear_history(self):
        """Очистка истории"""
        if messagebox.askyesno("Подтверждение", "Вы уверены, что хотите очистить всю историю паролей?"):
            self.history = []
            self.update_history_display()
            self.save_history()
            messagebox.showinfo("Успех", "🗑 История успешно очищена!")

    def save_history(self):
        """Сохранение истории в JSON файл"""
        try:
            with open(self.history_file, "w", encoding="utf-8") as f:
                json.dump(self.history, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Ошибка сохранения: {e}")

    def load_history(self):
        """Загрузка истории из JSON файла"""
        if os.path.exists(self.history_file):
            try:
                with open(self.history_file, "r", encoding="utf-8") as f:
                    self.history = json.load(f)
            except Exception as e:
                print(f"Ошибка загрузки: {e}")
                self.history = []
        else:
            self.history = []

    def export_history(self):
        """Экспорт истории в отдельный JSON файл"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        export_file = f"passwords_export_{timestamp}.json"

        try:
            with open(export_file, "w", encoding="utf-8") as f:
                json.dump(self.history, f, ensure_ascii=False, indent=2)
            messagebox.showinfo("Успех", f"✅ История экспортирована в файл:\n{export_file}")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось экспортировать историю: {e}")


# ========== ЗАПУСК ПРИЛОЖЕНИЯ ==========

if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordGenerator(root)
    root.mainloop()