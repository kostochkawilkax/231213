import pandas as pd
from tkinter import Tk, filedialog, messagebox, Text, Scrollbar, Frame, Button, Label
import io
import sys


class UberDataAnalyzer:
    def __init__(self):
        self.root = Tk()
        self.root.title("Анализ данных Uber - Kostochka Edition")
        self.root.geometry("1000x800")
        self.root.configure(bg='#fff0f5')
        self.df = None
        self.setup_ui()

    def setup_ui(self):
        """Создание интерфейса в розовых тонах"""

        # Главный контейнер с нежными отступами
        main_container = Frame(self.root, bg='#fff0f5', padx=30, pady=25)
        main_container.pack(fill="both", expand=True)

        # Заголовок в стиле розовой темы
        header_frame = Frame(main_container, bg='#fff0f5')
        header_frame.pack(fill="x", pady=(0, 25))

        title_label = Label(header_frame,
                            text="Анализ данных Uber",
                            font=("Comic Sans MS", 24, "bold"),
                            bg='#fff0f5',
                            fg='#d63384')
        title_label.pack(pady=(0, 5))

        subtitle_label = Label(header_frame,
                               text="Kostochka Edition",
                               font=("Comic Sans MS", 14, "italic"),
                               bg='#fff0f5',
                               fg='#e83e8c')
        subtitle_label.pack()

        # Разделительная линия
        separator = Frame(header_frame, height=2, bg='#f8bbd9')
        separator.pack(fill="x", pady=15)

        # Панель управления с розовым оформлением
        control_frame = Frame(main_container, bg='#fff0f5')
        control_frame.pack(fill="x", pady=20)

        # Контейнер для кнопок с равномерным распределением
        button_container = Frame(control_frame, bg='#fff0f5')
        button_container.pack(fill="x")

        # Розовая кнопка загрузки файла
        self.load_btn = Button(button_container,
                               text="📁 Загрузить CSV файл",
                               command=self.load_file,
                               font=("Comic Sans MS", 12, "bold"),
                               bg='#e83e8c',
                               fg='white',
                               activebackground='#d63384',
                               activeforeground='white',
                               relief="flat",
                               bd=0,
                               padx=20,
                               pady=12,
                               cursor="hand2")
        self.load_btn.pack(side="left", padx=(0, 10), fill="x", expand=True)

        # Кнопка статистического обзора
        self.stats_btn = Button(button_container,
                                text="📊 Обзор данных",
                                command=self.show_data_overview,
                                font=("Comic Sans MS", 12, "bold"),
                                bg='#ff69b4',
                                fg='white',
                                activebackground='#ff1493',
                                activeforeground='white',
                                relief="flat",
                                bd=0,
                                padx=20,
                                pady=12,
                                cursor="hand2",
                                state="disabled")
        self.stats_btn.pack(side="left", padx=(0, 10), fill="x", expand=True)

        # Розовая кнопка анализа
        self.analyze_btn = Button(button_container,
                                  text="✨ Полный анализ",
                                  command=self.analyze_data,
                                  font=("Comic Sans MS", 12, "bold"),
                                  bg='#db7093',
                                  fg='white',
                                  activebackground='#c71585',
                                  activeforeground='white',
                                  relief="flat",
                                  bd=0,
                                  padx=20,
                                  pady=12,
                                  cursor="hand2",
                                  state="disabled")
        self.analyze_btn.pack(side="left", fill="x", expand=True)

        # Статусная панель
        status_frame = Frame(control_frame, bg='#fff0f5')
        status_frame.pack(fill="x", pady=15)

        self.status_label = Label(status_frame,
                                  text="🌸 Готов к анализу. Пожалуйста, загрузите CSV файл.",
                                  font=("Comic Sans MS", 11),
                                  bg='#fff0f5',
                                  fg='#e83e8c',
                                  justify="center")
        self.status_label.pack()

        # Область вывода в розовых тонах
        output_frame = Frame(main_container, bg='#fff0f5')
        output_frame.pack(fill="both", expand=True, pady=(15, 0))

        # Заголовок области вывода
        output_header = Frame(output_frame, bg='#fff0f5')
        output_header.pack(fill="x", pady=(0, 10))

        output_title = Label(output_header,
                             text="Результаты анализа",
                             font=("Comic Sans MS", 14, "bold"),
                             bg='#fff0f5',
                             fg='#d63384')
        output_title.pack(side="left")

        # Розовая кнопка очистки
        clear_btn = Button(output_header,
                           text="🧹 Очистить вывод",
                           command=self.clear_output,
                           font=("Comic Sans MS", 10),
                           bg='#f8bbd9',
                           fg='#c2185b',
                           relief="flat",
                           bd=0,
                           padx=15,
                           pady=6,
                           cursor="hand2")
        clear_btn.pack(side="right")

        # Текстовое поле в стиле розовой темы
        text_container = Frame(output_frame, bg='#fce4ec', relief="flat", bd=2)
        text_container.pack(fill="both", expand=True)

        self.text_area = Text(text_container,
                              wrap="word",
                              font=('Comic Sans MS', 10),
                              bg='#fffafa',
                              fg='#880e4f',
                              insertbackground='#e91e63',
                              selectbackground='#f8bbd9',
                              relief="flat",
                              padx=15,
                              pady=15)

        # Настройка стилей текста для розового отображения
        self.text_area.tag_configure("header",
                                     foreground='#d63384',
                                     font=('Arial Rounded MT Bold', 12, 'bold'))

        self.text_area.tag_configure("subheader",
                                     foreground='#e91e63',
                                     font=('Arial Rounded MT Bold', 11))

        self.text_area.tag_configure("success",
                                     foreground='#c2185b',
                                     font=('Segoe UI', 10, 'bold'))

        self.text_area.tag_configure("warning",
                                     foreground='#ff6b95',
                                     font=('Segoe UI', 10, 'bold'))

        self.text_area.tag_configure("error",
                                     foreground='#d81b60',
                                     font=('Segoe UI', 10, 'bold'))

        self.text_area.tag_configure("emphasis",
                                     foreground='#ad1457',
                                     font=('Segoe UI', 10))

        self.text_area.tag_configure("muted",
                                     foreground='#e91e63',
                                     font=('Segoe UI', 10, 'italic'))

        self.text_area.tag_configure("data",
                                     foreground='#880e4f',
                                     font=('Consolas', 9))

        self.text_area.tag_configure("highlight",
                                     foreground='#ec407a',
                                     font=('Consolas', 9, 'bold'))

        # Прокрутка в розовом стиле
        scrollbar = Scrollbar(text_container,
                              command=self.text_area.yview,
                              bg='#f8bbd9',
                              troughcolor='#fce4ec')
        self.text_area.config(yscrollcommand=scrollbar.set)

        self.text_area.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Статус бар внизу в розовом стиле
        status_bar = Frame(main_container, bg='#e91e63', height=25)
        status_bar.pack(fill="x", pady=(15, 0))
        status_bar.pack_propagate(False)

        self.stats_label = Label(status_bar,
                                 text="📈 Записей: 0 | Колонок: 0 | Статус: Готов",
                                 font=("Segoe UI", 10),
                                 bg='#e91e63',
                                 fg='#fff0f5')
        self.stats_label.pack(side="left", padx=15, pady=4)

    def clear_output(self):
        """Очистка области вывода"""
        self.text_area.delete(1.0, "end")

    def log_message(self, message, tag=None):
        """Логирование сообщений с розовым форматированием"""
        if tag:
            self.text_area.insert("end", message + "\n", tag)
        else:
            self.text_area.insert("end", message + "\n")
        self.text_area.see("end")
        self.root.update()

    def load_file(self):
        """Загрузка CSV файла"""
        file_path = filedialog.askopenfilename(
            title="Выберите CSV файл с данными Uber",
            filetypes=[("CSV files", "*.csv"), ("Все файлы", "*.*")]
        )

        if file_path:
            try:
                self.status_label.config(text="🌸 Загрузка файла, пожалуйста подождите...")
                self.load_btn.config(state="disabled")

                self.df = pd.read_csv(file_path)

                # Обновляем статус
                file_name = file_path.split('/')[-1]
                self.status_label.config(text=f"🌸 Файл успешно загружен: {file_name}")
                self.stats_btn.config(state="normal")
                self.analyze_btn.config(state="normal")
                self.stats_label.config(
                    text=f"📈 Записей: {self.df.shape[0]:,} | Колонок: {self.df.shape[1]} | Статус: Готов к анализу")

                # Показываем информацию о файле
                self.clear_output()
                self.log_message("Информация о файле", "header")
                self.log_message("=" * 50, "subheader")
                self.log_message(f"📁 Файл: {file_path}", "subheader")
                self.log_message(f"📊 Размер данных: {self.df.shape[0]:,} строк, {self.df.shape[1]} колонок", "success")
                self.log_message("", "")
                self.log_message("Структура данных:", "subheader")

                for i, col in enumerate(self.df.columns, 1):
                    self.log_message(f"  {i:2d}. {col}", "data")

                messagebox.showinfo("Успех",
                                    f"🌸 Файл успешно загружен.\n\n"
                                    f"📈 Строк: {self.df.shape[0]:,}\n"
                                    f"📊 Колонок: {self.df.shape[1]}\n\n"
                                    f"Теперь вы можете приступить к анализу.")

            except Exception as e:
                messagebox.showerror("Ошибка", f"❌ Не удалось загрузить файл:\n{str(e)}")
                self.status_label.config(text="❌ Ошибка загрузки файла")
            finally:
                self.load_btn.config(state="normal")

    def show_data_overview(self):
        """Показать статистический обзор данных"""
        if self.df is None:
            messagebox.showerror("Ошибка", "🌸 Пожалуйста, сначала загрузите файл.")
            return

        try:
            self.stats_btn.config(state="disabled", bg='#f8bbd9')
            self.status_label.config(text="🌸 Генерация обзора данных...")

            self.clear_output()
            self.perform_data_overview()

            self.status_label.config(text="🌸 Обзор данных завершен.")
            self.stats_btn.config(state="normal", bg='#ff69b4')

        except Exception as e:
            messagebox.showerror("Ошибка обзора", f"❌ Ошибка при создании обзора:\n{str(e)}")
            self.status_label.config(text="❌ Ошибка обзора")
            self.stats_btn.config(state="normal", bg='#ff69b4')

    def perform_data_overview(self):
        """Статистический обзор данных"""
        self.log_message("🌸 Статистический обзор данных", "header")
        self.log_message("=" * 60, "subheader")

        # Основная информация о датасете
        self.log_message(f"\n📊 Размер набора данных: {self.df.shape[0]:,} строк × {self.df.shape[1]} колонок", "success")

        # Подсчет пропущенных значений
        self.log_message("\n1. 🎯 Анализ пропущенных значений:", "subheader")
        self.log_message("-" * 50, "muted")

        missing_data = self.df.isnull().sum()
        missing_percent = (missing_data / len(self.df)) * 100

        missing_info = pd.DataFrame({
            'Column': missing_data.index,
            'Missing_Count': missing_data.values,
            'Missing_Percent': missing_percent.values
        })

        for _, row in missing_info.iterrows():
            if row['Missing_Count'] > 0:
                self.log_message(f"  {row['Column']}: {row['Missing_Count']:,} ({row['Missing_Percent']:.1f}%)",
                                 "warning")
            else:
                self.log_message(f"  {row['Column']}: ✅ Нет пропущенных значений", "success")

        self.log_message("-" * 50, "muted")

        # Уникальные значения в категориальных столбцах
        self.log_message("\n2. 🎭 Анализ категориальных колонок:", "subheader")
        self.log_message("-" * 50, "muted")

        # Автоматическое определение категориальных столбцов
        categorical_columns = self.df.select_dtypes(include=['object']).columns

        for col in categorical_columns:
            unique_count = self.df[col].nunique()
            self.log_message(f"\n  {col}:", "emphasis")
            self.log_message(f"    Уникальных значений: {unique_count}", "data")

            # Показываем топ-10 самых частых значений
            value_counts = self.df[col].value_counts().head(10)
            if len(value_counts) > 0:
                self.log_message("    Топ значения:", "data")
                for value, count in value_counts.items():
                    percent = (count / len(self.df)) * 100
                    self.log_message(f"      '{value}': {count:,} ({percent:.1f}%)", "data")

        self.log_message("-" * 50, "muted")

        # Детальный анализ Booking Status и Vehicle Type
        self.log_message("\n3. 🔍 Детальный анализ ключевых колонок:", "subheader")
        self.log_message("-" * 50, "muted")

        # Анализ Booking Status
        booking_status_col = self.find_booking_status_column()
        if booking_status_col:
            self.log_message(f"\n  📋 Статус бронирования ({booking_status_col}):", "emphasis")
            status_counts = self.df[booking_status_col].value_counts()
            for status, count in status_counts.items():
                percent = (count / len(self.df)) * 100
                self.log_message(f"    {status}: {count:,} ({percent:.1f}%)", "highlight")
        else:
            self.log_message("\n  📋 Колонка статуса бронирования не найдена", "warning")

        # Анализ Vehicle Type
        vehicle_type_col = self.find_vehicle_type_column()
        if vehicle_type_col:
            self.log_message(f"\n  🚗 Тип транспортного средства ({vehicle_type_col}):", "emphasis")
            vehicle_counts = self.df[vehicle_type_col].value_counts()
            for vehicle, count in vehicle_counts.items():
                percent = (count / len(self.df)) * 100
                self.log_message(f"    {vehicle}: {count:,} ({percent:.1f}%)", "highlight")
        else:
            self.log_message("\n  🚗 Колонка типа транспортного средства не найдена", "warning")

        self.log_message("-" * 50, "muted")

        # Общая статистика по числовым колонкам
        self.log_message("\n4. 📈 Сводка по числовым колонкам:", "subheader")
        self.log_message("-" * 50, "muted")

        numerical_columns = self.df.select_dtypes(include=['int64', 'float64']).columns
        if len(numerical_columns) > 0:
            for col in numerical_columns:
                self.log_message(f"\n  {col}:", "emphasis")
                stats = self.df[col].describe()
                self.log_message(f"    Количество: {stats['count']:,}", "data")
                self.log_message(f"    Среднее: {stats['mean']:.2f}", "data")
                self.log_message(f"    Стандартное отклонение: {stats['std']:.2f}", "data")
                self.log_message(f"    Минимум: {stats['min']:.2f}", "data")
                self.log_message(f"    25%: {stats['25%']:.2f}", "data")
                self.log_message(f"    50%: {stats['50%']:.2f}", "data")
                self.log_message(f"    75%: {stats['75%']:.2f}", "data")
                self.log_message(f"    Максимум: {stats['max']:.2f}", "data")
        else:
            self.log_message("  📊 Числовые колонки не найдены", "muted")

        self.log_message("-" * 50, "muted")

        # Итоговая сводка
        self.log_message("\n🌸 Итоговая сводка:", "subheader")
        total_missing = missing_data.sum()
        total_cells = self.df.shape[0] * self.df.shape[1]
        completeness = ((total_cells - total_missing) / total_cells) * 100

        self.log_message(f"  📊 Полнота данных: {completeness:.1f}%", "success")
        self.log_message(f"  ❌ Всего пропущенных значений: {total_missing:,}", "warning" if total_missing > 0 else "success")
        self.log_message(f"  🎭 Категориальных колонок: {len(categorical_columns)}", "data")
        self.log_message(f"  📈 Числовых колонок: {len(numerical_columns)}", "data")

    def find_booking_status_column(self):
        """Найти столбец Booking Status"""
        for col in self.df.columns:
            if 'status' in col.lower():
                return col
        return None

    def find_vehicle_type_column(self):
        """Найти столбец Vehicle Type"""
        for col in self.df.columns:
            if 'vehicle' in col.lower() and 'type' in col.lower():
                return col
        return None

    def analyze_data(self):
        """Выполнение анализа данных"""
        if self.df is None:
            messagebox.showerror("Ошибка", "🌸 Пожалуйста, сначала загрузите файл.")
            return

        try:
            self.analyze_btn.config(state="disabled", bg='#f8bbd9')
            self.status_label.config(text="🌸 Выполнение анализа...")

            self.clear_output()
            self.perform_full_analysis()

            self.status_label.config(text="🌸 Анализ успешно завершен.")
            self.analyze_btn.config(state="normal", bg='#db7093')

        except Exception as e:
            messagebox.showerror("Ошибка анализа", f"❌ Ошибка во время анализа:\n{str(e)}")
            self.status_label.config(text="❌ Ошибка анализа")
            self.analyze_btn.config(state="normal", bg='#db7093')

    def perform_full_analysis(self):
        """Полный анализ данных по ТЗ"""

        # Шаг 1: Загрузка и первичный осмотр данных
        self.log_message("\n🌸 Шаг 1: Загрузка и первичный осмотр данных", "header")
        self.log_message("=" * 60, "subheader")

        # 1. Информация о загрузке
        self.log_message("\n1. ✅ Данные успешно загружены в DataFrame", "success")

        # 2. Первые 5 строк
        self.log_message("\n2. 📄 Первые 5 строк набора данных:", "subheader")
        self.log_message("-" * 50, "muted")
        self.log_message(str(self.df.head()), "data")
        self.log_message("-" * 50, "muted")

        # 3. Общая информация
        self.log_message("\n3. ℹ️ Информация о наборе данных:", "subheader")
        self.log_message("-" * 50, "muted")
        buffer = io.StringIO()
        self.df.info(buf=buffer)
        info_text = buffer.getvalue()
        for line in info_text.split('\n'):
            if line.strip():
                self.log_message(line, "data")
        self.log_message("-" * 50, "muted")

        # 4. Статистическое описание
        self.log_message("\n4. 📊 Статистическое описание числовых колонок:", "subheader")
        self.log_message("-" * 50, "muted")
        self.log_message(str(self.df.describe()), "data")
        self.log_message("-" * 50, "muted")

        # 5. Количество строк и столбцов
        self.log_message(f"\n5. 📈 Размеры набора данных: {self.df.shape[0]:,} строк, {self.df.shape[1]} колонок", "success")

        # Шаг 3: Выборка и фильтрация данных
        self.log_message("\n\n🌸 Шаг 3: Выборка и фильтрация данных", "header")
        self.log_message("=" * 60, "subheader")

        # Находим нужные столбцы
        column_mapping = self.find_columns()
        self.log_message(f"\n🔍 Обнаруженные колонки: {column_mapping}", "subheader")

        # Выполняем анализ по пунктам ТЗ
        self.execute_analysis_steps(column_mapping)

        # Итоги
        self.log_message("\n\n🌸 Анализ завершен", "header")
        self.log_message("=" * 60, "subheader")
        self.log_message(f"✅ Обработано: {self.df.shape[0]:,} записей, {self.df.shape[1]} колонок", "success")
        self.log_message("💖 Спасибо за использование Анализа данных Uber - Kostochka edition 💖", "muted")

    def execute_analysis_steps(self, column_mapping):
        """Выполнение конкретных шагов анализа из ТЗ"""

        # 1. Выборка столбцов
        self.log_message("\n1. 🎯 Выборка конкретных колонок:", "subheader")
        selected_data = self.select_columns(column_mapping)
        if selected_data is not None:
            self.log_message("📄 Первые 5 строк выборки:", "emphasis")
            self.log_message(str(selected_data.head()), "data")
        else:
            self.log_message("❌ Необходимые колонки не найдены", "emphasis")

        # 2. Фильтрация отмененных водителем
        self.log_message("\n2. 🚫 Фильтр: 'Отменено водителем':", "subheader")
        cancelled_data = self.filter_cancelled(column_mapping)
        if cancelled_data is not None:
            self.log_message(f"📊 Найдено записей: {len(cancelled_data):,}", "emphasis")
            if len(cancelled_data) > 0:
                self.log_message("📄 Первые 5 строк:", "emphasis")
                self.log_message(str(cancelled_data.head()), "data")
            else:
                self.log_message("📭 Нет записей, соответствующих критериям", "muted")

        # 3. Фильтрация Auto + Booking Value > 500
        self.log_message("\n3. 🚗 Фильтр: 'Auto' со значением бронирования > 500:", "subheader")
        auto_data = self.filter_auto_high_value(column_mapping)
        if auto_data is not None:
            self.log_message(f"📊 Найдено записей: {len(auto_data):,}", "emphasis")
            if len(auto_data) > 0:
                self.log_message("📄 Первые 5 строк:", "emphasis")
                self.log_message(str(auto_data.head()), "data")
            else:
                self.log_message("📭 Нет записей, соответствующих критериям", "muted")

        # 4. Фильтрация за март 2024
        self.log_message("\n4. 📅 Фильтр: Бронирования за март 2024:", "subheader")
        march_data = self.filter_march_2024(column_mapping)
        if march_data is not None:
            self.log_message(f"📊 Найдено записей: {len(march_data):,}", "emphasis")
            if len(march_data) > 0:
                self.log_message("📄 Первые 5 строк:", "emphasis")
                self.log_message(str(march_data.head()), "data")
            else:
                self.log_message("📭 Нет записей, соответствующих критериям", "muted")

    def find_columns(self):
        """Автоматическое определение столбцов по ключевым словам"""
        column_mapping = {}

        for col in self.df.columns:
            col_lower = col.lower()

            if 'booking' in col_lower and 'id' in col_lower:
                column_mapping['booking_id'] = col
            elif 'datetime' in col_lower or ('date' in col_lower and 'time' in col_lower):
                column_mapping['booking_datetime'] = col
            elif 'status' in col_lower:
                column_mapping['booking_status'] = col
            elif 'vehicle' in col_lower and 'type' in col_lower:
                column_mapping['vehicle_type'] = col
            elif 'payment' in col_lower and 'method' in col_lower:
                column_mapping['payment_method'] = col
            elif ('value' in col_lower and 'booking' in col_lower) or 'amount' in col_lower or 'price' in col_lower:
                column_mapping['booking_value'] = col

        return column_mapping

    def select_columns(self, column_mapping):
        """Выборка нужных столбцов"""
        needed_cols = ['booking_id', 'booking_datetime', 'booking_status', 'vehicle_type', 'payment_method']
        available_cols = []

        for col in needed_cols:
            if col in column_mapping:
                available_cols.append(column_mapping[col])

        if len(available_cols) >= 3:
            return self.df[available_cols]
        return None

    def filter_cancelled(self, column_mapping):
        """Фильтрация отмененных водителем бронирований"""
        if 'booking_status' not in column_mapping:
            return None

        status_col = column_mapping['booking_status']
        status_variants = ['Cancelled by Driver', 'Canceled by Driver', 'Cancelled', 'Canceled', 'Driver Cancelled']

        for status in status_variants:
            filtered = self.df[self.df[status_col] == status]
            if len(filtered) > 0:
                return filtered

        return self.df[self.df[status_col].str.contains('cancel', case=False, na=False)]

    def filter_auto_high_value(self, column_mapping):
        """Фильтрация Auto с Booking Value > 500"""
        if 'vehicle_type' not in column_mapping or 'booking_value' not in column_mapping:
            return None

        vehicle_col = column_mapping['vehicle_type']
        value_col = column_mapping['booking_value']
        auto_variants = ['Auto', 'AUTO', 'auto']

        for auto_type in auto_variants:
            filtered = self.df[(self.df[vehicle_col] == auto_type) & (self.df[value_col] > 500)]
            if len(filtered) > 0:
                return filtered

        return self.df[(self.df[vehicle_col].str.contains('auto', case=False, na=False)) & (self.df[value_col] > 500)]

    def filter_march_2024(self, column_mapping):
        """Фильтрация бронирований за март 2024"""
        if 'booking_datetime' not in column_mapping:
            return None

        date_col = column_mapping['booking_datetime']

        try:
            self.df[date_col] = pd.to_datetime(self.df[date_col])
            march_2024 = self.df[
                (self.df[date_col] >= '2024-03-01') &
                (self.df[date_col] <= '2024-03-31')
                ]
            return march_2024
        except:
            return None

    def run(self):
        self.root.mainloop()


# Запуск приложения
if __name__ == "__main__":
    app = UberDataAnalyzer()
    app.run()