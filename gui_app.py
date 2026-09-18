import os
import sys
import pandas as pd
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
from PySide6.QtCore import Qt, QTimer
from PySide6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QLineEdit, QScrollArea, QFrame, QFileDialog, 
                             QMessageBox, QStackedWidget, QSizePolicy, QDialog, QTextEdit)
from PySide6.QtGui import QFont, QPixmap

# ⚔️ ОФИЦИАЛЬНЫЙ РЕЕСТР ПРЕДМЕТОВ FOXHOLE CLAN SINDARIS
try:
    import item_codes
    ITEM_NAME_TO_CODE = {v: k for k, v in item_codes.ITEM_CODES.items()}
    ITEM_OPTIONS = sorted(list(ITEM_NAME_TO_CODE.keys()))
except:
    ITEM_OPTIONS = [
        ".44 Магнум", "12.7-мм", "120-мм", "14.5mm", "150-мм", "20мм", "250mm “Fury” Shell",
        "250mm “Purity” Shell", "300-мм", "30мм", "40-мм", "68мм", "7.52-мм", "7.62-мм",
        "7.92-мм", "8-мм", "912 Shrike Rounds", "94.5мм", "950-70b Зенитный снаряд", "9-мм",
        "A3 Harpa Осколочная граната", "Aalto Автоматическая винтовка 24", "Abisme AT-99 Mine",
        "Alligator Charge", "Argenti r.II Винтовка", "B2 Varsi Anti-Tank Grenade", "Bane 45",
        "Blakerow 871", "Bomastone Граната", "Bonesaw MK.3", "Booker Greyhound Model 910",
        "Buckhorn CCQ-18", "Catara mo.II", "Clancy Cinder M3", "Clancy-Raca M4", "Cometa T2-9",
        "Crow’s Foot Mine", "Cutler Foebreaker", "Cutler Launcher 4", "Daucus isg.III",
        "Ferro 879", "Fuscina pi.I", "GA6 “Cestus”", "Ignifist 30", "KRF1-750 Dragonfly",
        "KRR2-790 Omen", "KRR3-792 Auger", "Lamentum mm.IV", "Malone MK.2", "Malone Ratcatcher MK.1",
        "Mammon 91-b", "No.2 Loughcaster", "No.2B Hawthorne", "No.4 The Pillory Scattergun",
        "Noble Firebrand Mk. XVII", "Noble Widow MK. XIV", "O’Brien V.101 Freeman", "O’Brien V.110",
        "O’Brien V.113 Gravekeeper", "O’Brien V.112", "O’Brien v.200 Squire", "O’Brien V.130 Wild Jack",
        "Swallowtail emergency services", "Volta r.I Repeater", "Базовые материалы", "Бинты", "Бинокль",
        "Бронебойный навесной/РПГ", "Бронебойный/РПГ", "Ведро для воды", "Ветроуказатель",
        "Вода", "Гаечный ключ", "Газовая граната", "Детонатор Хавок Заряда", "Дизель",
        "Дробь", "Дымовая граната PT-815", "Зажигал. минометный снаряд", "Зенитный снаряд “Absol”",
        "Колючая проволока", "Кувалда", "Лопата", "Металлическая балка", "Мешок с песком",
        "Миномёт Cremari", "Минометный Снаряд", "Молоток", "Набор для прослушивания",
        "Набор Первой Помощи", "Нестабильные материалы", "Огнемётное топливо", "Осколочная граната A3 Harpa",
        "Осколочный минометный снаряд", "Осветительный Минометный Снаряд", "Плазма", "Повреждённый Колониальный авиадвигатель",
        "Подствольный гранатомёт", "Порох", "Припасы Обслуживания", "Противогаз", "Радиорюкзак",
        "Рация", "Реанимационный набор", "Редкий металл", "Реликтовые материалы", "РПГ",
        "РПГ \"Carnyx\"", "Рюкзак Десантника", "Сапёрное снаряжение", "Сирена воздушной тревоги",
        "Сборочные материалы I", "Сборочные материалы II", "Солдатские припасы (Имки)", "Сталь",
        "Строительные материалы", "Торпеда \"Quillback\"", "Тренога", "Труба", "Тяжелое топливо",
        "Тяжёлый порох", "Фильтр для противогаза", "Флаг Колонистов", "Флаг Варденов", "Хавок Заряд",
        "Шинель специалиста", "Штурмовая винтовка Aalto 24", "Штурмовая винковк Booker Model 838"
    ]
    ITEM_NAME_TO_CODE = {x: "UnknownCode" for x in ITEM_OPTIONS}

# 🗺️ НАЧАЛЬНАЯ МАТРИЦА РЕГИОНОВ И ИСТОРИИ ИЗМЕНЕНИЙ СКЛАДОВ
STOCKPILE_TIMERS_DATABASE = [
    {"ID": 0, "Region": "Clanshead Valley", "Location": "Порт Clanshead", "TimeLeft": 56257, "History": ["[СИСТЕМА]: Инициализация терминала секторов."]},
    {"ID": 1, "Region": "The Linn of Lights", "Location": "Склад снабжения Запад", "TimeLeft": 3420, "History": ["[СИСТЕМА]: Обнаружена критическая просадка по времени."]},
    {"ID": 2, "Region": "Heartlands HQ", "Location": "Центральный Лог-Хаб", "TimeLeft": 86400, "History": ["[СИСТЕМА]: Склад зарегистрирован интендантской службой."]},
    {"ID": 3, "Region": "Marban Hollow", "Location": "Передовой бункер", "TimeLeft": 12450, "History": ["[СИСТЕМА]: Запущена резервная линия мониторинга."]},
    {"ID": 4, "Region": "Drowned Vale", "Location": "Морской Док", "TimeLeft": 1800, "History": ["[СИСТЕМА]: Зафиксирован дефицит поставок."]}
]

# 📝 ТАКТИЧЕСКИЙ СПИСОК КАСТОМНЫХ ФРАЗ ШТАБА
TACTICAL_CUSTOM_PHRASES = [
    "Работай сука",
    "Сделай САНДАЛИС снова великим!",
    "💀ЦЫГАНИС на связи. Спутниковый мониторинг шейкелей колонистов...",
    "Розыгрыш карвалола"
]

def get_resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'): 
        return os.path.join(sys._MEIPASS, relative_path)
    # Исправленный запуск через Python 3.14 (берем строго нулевой индекс sys.argv)
    return os.path.join(os.path.abspath(os.path.dirname(sys.argv[0])), relative_path)
class LogisticsStudioApp(QWidget):
    def __init__(self):
        super().__init__()
        
        # 👑 1. ПЕРЕМЕННЫЕ ИНИЦИАЛИЗАЦИИ ШРИФТОВ
        self.font_interface = QFont("Arial", 10, QFont.Weight.Bold)
        self.font_ticker = QFont("Consolas", 10, QFont.Weight.Bold)
        
        # 🔥 2. ГРАФИЧЕСКИЙ ДВИЖОК СВЕРХПЛАВНОГО КОНВЕЙЕРА (60 FPS)
        self.timer_labels = {}             # Ссылки на текстовые поля времени
        self.ticker_pixmap_offset = 0.0    # Точная субпиксельная координата X
        self.ticker_image_width = 0        # Физическая длина сгенерированной ленты
        
        # ⚙️ 3. КИНЕТИЧЕСКИЙ ДВИЖОК И ТАКТИЧЕСКИЕ ДАННЫЕ СНАБЖЕНИЯ
        self.ticker_offset = 0  
        self.raw_ticker_text = "ЗАГРУЗКА ВОЕННЫХ СПУТНИКОВ СЕКТОРА..."
        self.plain_ticker_text = ""
        self.current_order = {}
        self.storage_data = [] 
        self.timers_list = STOCKPILE_TIMERS_DATABASE
        
        # Переменные управления случайными радиоперехватами штаба
        self.active_custom_phrase = ""      # Текущая отображаемая фраза
        self.phrase_hold_seconds = 0       # Сколько секунд ей осталось висеть
        
        # 🖥️ 4. КОНФИГУРАЦИЯ ГЛАВНОГО ОКНА SINDARIS EDITION
        self.setWindowTitle("⚡ SINDARIS LOGISTICS OVERWATCH CONTROL TERMINAL")
        self.setGeometry(100, 100, 1350, 900)
        self.setMinimumSize(1150, 850)
        
                # Сохраняем текстовые QSS-стили обеих тем для мгновенного переключения на лету
        self.THEME_LIGHT_KHAKI = """
            QWidget { background-color: #dcd6cd; color: #2b2e2b; font-family: 'Segoe UI', Arial, sans-serif; }
            QFrame { background-color: #c9c0b5; border: 2px solid #9c8f80; border-radius: 6px; }
            QLineEdit { background-color: #f4f1eb; color: #1b1d1b; border: 1px solid #9c8f80; padding: 7px; border-radius: 4px; font-weight: bold; }
            QLineEdit:hover { border: 1px solid #7c6f60; background-color: #ffffff; }
            QLineEdit:focus { border: 2px solid #4a5c31; background-color: #ffffff; }
            QPushButton { background-color: #b5bc9a; color: #1e2417; border: 1px solid #7e8761; padding: 8px 12px; border-radius: 4px; font-weight: bold; }
            QPushButton:hover { background-color: #4a5c31; color: #ffffff; border: 1px solid #354222; }
            QPushButton:pressed { background-color: #354222; padding-left: 14px; padding-top: 9px; }
            QPushButton:checked { background-color: #a64f4f; color: #ffffff; border: 1px solid #7a3333; }
            QPushButton:checked:hover { background-color: #b83232; }
            QScrollArea { border: 2px solid #9c8f80; background-color: #ebe6df; border-radius: 4px; }
            QTextEdit { background-color: #f4f1eb; color: #2b4c1e; border: 1px solid #9c8f80; font-family: 'Consolas', monospace; border-radius: 4px; }
        """

        self.THEME_DARK_CYBERPUNK = """
            QWidget { background-color: #0c0e0c; color: #e5e7eb; font-family: 'Segoe UI', Arial, sans-serif; }
            QFrame { background-color: #121512; border: 1px solid #1c221c; border-radius: 6px; }
            QLineEdit { background-color: #060706; color: #ffffff; border: 1px solid #222922; padding: 7px; border-radius: 4px; }
            QLineEdit:hover { border: 1px solid #4d614d; background-color: #090b09; }
            QLineEdit:focus { border: 1px solid #a3e635; background-color: #0d100d; }
            QPushButton { background-color: #181d18; color: #d1d5db; border: 1px solid #283328; padding: 8px 12px; border-radius: 4px; font-weight: bold; }
            QPushButton:hover { background-color: #a3e635; color: #0c0e0c; border: 1px solid #ffffff; }
            QPushButton:pressed { background-color: #84cc16; padding-left: 14px; padding-top: 9px; }
            QPushButton:checked { background-color: #3f1616; color: #f87171; border: 1px solid #ef4444; }
            QPushButton:checked:hover { background-color: #ef4444; color: #ffffff; }
            QScrollArea { border: 1px solid #1c221c; background-color: #060706; border-radius: 4px; }
            QTextEdit { background-color: #060706; color: #86efac; border: 1px solid #222922; font-family: 'Consolas', monospace; border-radius: 4px; }
        """
        
        # По умолчанию активируем тему светлого хаки
        self.is_dark_theme = False
        self.setStyleSheet(self.THEME_LIGHT_KHAKI)
        
        # 🏛️ ПОРЯДОК РАЗВЕРТЫВАНИЯ СТРУКТУРЫ ИНТЕРФЕЙСА
        self.init_ui()
        self.setup_workspace()
        
        # Переключаем контейнер на первую страницу при старте
        self.pages_container.setCurrentIndex(0)
        
        # ⏱️ ТАЙМЕР №1: Расчет алертов и времени (1 Гц)
        self.global_timer = QTimer(self)
        self.global_timer.timeout.connect(self.update_tactical_timers)
        self.global_timer.start(1000)

        # 🏃‍♂️ ТАЙМЕР №2: Отрисовка плавной графики (60 Гц)
        self.animation_timer = QTimer(self)
        self.animation_timer.timeout.connect(self.animate_ticker)
        self.animation_timer.start(16)

        # ⏱️ ТАЙМЕР №3: Бесшумный авто-мониторинг папки сканера (1 Гц)
        self.auto_sync_timer = QTimer(self)
        self.auto_sync_timer.timeout.connect(self.auto_load_scanner_file)
        self.auto_sync_timer.start(1000)

        # Стартовый сбор данных и запуск алертов
        self.update_tactical_timers()



    def init_ui(self):
        # ГЛАВНЫЙ ВЕРТИКАЛЬНЫЙ МАКЕТ ВСЕГО ОКНА
        window_wrapper = QVBoxLayout(self)
        window_wrapper.setContentsMargins(10, 10, 10, 10)
        window_wrapper.setSpacing(10)

        # ================================================================
        # 👑 ГЛОБАЛЬНАЯ СКВОЗНАЯ ШАПКА HUD (Видна во всех разделах)
        # ================================================================
        self.logo_frame = QFrame()
        self.logo_frame.setFixedHeight(65)
        self.logo_frame.setStyleSheet("background-color: #141714; border: 1px solid #222922; border-radius: 6px;")
        logo_layout = QHBoxLayout(self.logo_frame)
        logo_layout.setContentsMargins(15, 5, 15, 5)
        logo_layout.setSpacing(15)

        # Контейнер для бегущей строки секторов
        self.ticker_frame = QFrame()
        self.ticker_frame.setStyleSheet("background-color: #060806; border: 1px solid #1c221c; border-radius: 4px;")
        self.ticker_frame.setFixedHeight(45)
        
        # Текстовый виджет бегущей строки внутри фрейма
        self.lbl_ticker_text = QLabel(self.raw_ticker_text, self.ticker_frame)
        self.lbl_ticker_text.setFont(self.font_ticker)
        self.lbl_ticker_text.setStyleSheet("color: #ff4545; font-weight: bold; background: transparent; border: none;")
        self.lbl_ticker_text.setMinimumWidth(12000) 
        self.lbl_ticker_text.move(200, 14) 
        
        logo_layout.addWidget(self.ticker_frame, 1)
        window_wrapper.addWidget(self.logo_frame)

        # НИЖНЯЯ РАБОЧАЯ ОБЛАСТЬ (Разделяется на Сайдбар слева и Контент справа)
        app_layout = QHBoxLayout()
        app_layout.setContentsMargins(0, 0, 0, 0)
        app_layout.setSpacing(10)
        
        # ================================================================
        # 🧭 ЛЕВАЯ СТОРОНА: ВЫЕЗДНОЙ SIDEBAR УПРАВЛЕНИЯ (Sindaris HQ)
        # ================================================================
        self.sidebar_frame = QFrame()
        self.sidebar_frame.setFixedWidth(75) 
        self.sidebar_frame.setStyleSheet("background-color: #141714; border: 1px solid #222922; border-radius: 6px;")
        self.sidebar_layout = QVBoxLayout(self.sidebar_frame)
        self.sidebar_layout.setContentsMargins(10, 15, 10, 15)
        self.sidebar_layout.setSpacing(15)
        self.sidebar_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        # 👑 Фирменный логотип клана SINDARIS (Верхушка Sidebar)
        self.lbl_sidebar_logo = QLabel()
        logo_path = get_resource_path(os.path.join("scr", "clan-logo.png"))
        if os.path.exists(logo_path):
            try:
                pixmap = QPixmap(logo_path)
                self.sidebar_logo_pixmap = pixmap.scaledToHeight(45, Qt.TransformationMode.SmoothTransformation)
                self.lbl_sidebar_logo.setPixmap(self.sidebar_logo_pixmap)
            except: pass
        self.lbl_sidebar_logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.sidebar_layout.addWidget(self.lbl_sidebar_logo)
        
        # ⚡ ГЛАВНАЯ КНОПКА-ГАЛОЧКА (Переключатель раскрытия боковой панели)
        self.btn_toggle_sidebar = QPushButton("❯") 
        self.btn_toggle_sidebar.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        self.btn_toggle_sidebar.setStyleSheet("background-color: #222922; color: #a3e635; border: 1px solid #2c352c; height: 35px;")
        self.btn_toggle_sidebar.setCheckable(True)
        self.btn_toggle_sidebar.clicked.connect(self.toggle_sidebar_menu)
        self.sidebar_layout.addWidget(self.btn_toggle_sidebar)
        
        # РАЗДЕЛ №1: Кнопка перехода к Логистическим Операциям
        self.btn_nav_ops = QPushButton("🖥️")
        self.btn_nav_ops.setFont(self.font_interface)
        self.btn_nav_ops.setStyleSheet("background-color: #1d221d; color: #ffffff; height: 40px;")
        self.btn_nav_ops.clicked.connect(lambda: self.pages_container.setCurrentIndex(0))
        self.sidebar_layout.addWidget(self.btn_nav_ops)
        
        # РАЗДЕЛ №2: Кнопка перехода к Матрице Таймеров Складов
        self.btn_nav_timers = QPushButton("⏳")
        self.btn_nav_timers.setFont(self.font_interface)
        self.btn_nav_timers.setStyleSheet("background-color: #1d221d; color: #ffffff; height: 40px;")
        self.btn_nav_timers.clicked.connect(lambda: self.pages_container.setCurrentIndex(1))
        self.sidebar_layout.addWidget(self.btn_nav_timers)

        # Добавляем невидимую тактическую пружину, чтобы вытолкнуть переключатель темы в самый низ
        self.sidebar_layout.addStretch(1)
        
        # ⚡ ГЛАВНЫЙ ПЕРЕКЛЮЧАТЕЛЬ ДЕНЬ / НОЧЬ
        self.btn_toggle_theme = QPushButton("🌓")
        self.btn_toggle_theme.setFont(self.font_interface)
        self.btn_toggle_theme.setStyleSheet("background-color: #222922; color: #a3e635; height: 35px;")
        self.btn_toggle_theme.clicked.connect(self.switch_terminal_theme)
        self.sidebar_layout.addWidget(self.btn_toggle_theme)
        
        app_layout.addWidget(self.sidebar_frame)
        
        # ================================================================
        # 🎭 ПРАВАЯ СТОРОНА: СВЕРХБЫСТРЫЙ КОНТЕЙНЕР СТРАНИЦ ТЕРМИНАЛА
        # ================================================================
        self.pages_container = QStackedWidget()
        app_layout.addWidget(self.pages_container, 1) 
        
        self.page_operations = QWidget()
        self.page_timers_matrix = QWidget()
        
        self.pages_container.addWidget(self.page_operations)
        self.pages_container.addWidget(self.page_timers_matrix)
        
        window_wrapper.addLayout(app_layout)

    def toggle_sidebar_menu(self):
        """Метод управления выездом боковой панели и изменением текста кнопок."""
        if self.btn_toggle_sidebar.isChecked():
            self.sidebar_frame.setFixedWidth(210)
            self.btn_toggle_sidebar.setText("❮")
            self.btn_nav_ops.setText("🖥️  1. ОПЕРАЦИИ")
            self.btn_nav_timers.setText("⏳  2. ТАЙМЕРЫ СКЛАДОВ")
            self.btn_toggle_theme.setText("🌓  ТЕМА TERMINAL") # Текст при раскрытии
        else:
            self.sidebar_frame.setFixedWidth(75)
            self.btn_toggle_sidebar.setText("❯")
            self.btn_nav_ops.setText("🖥️")
            self.btn_nav_timers.setText("⏳")
            self.btn_toggle_theme.setText("🌓") # Текст при свертывании

    def switch_terminal_theme(self):
        """Интеллектуальное переключение глобальной темы оформления терминала на лету с исправлением цветов текста."""
        self.is_dark_theme = not self.is_dark_theme
        
        if self.is_dark_theme:
            self.setStyleSheet(self.THEME_DARK_CYBERPUNK)
        else:
            self.setStyleSheet(self.THEME_LIGHT_KHAKI)
            
        # Принудительно заставляем оба раздела перерисовать свои внутренности под новые цвета
        if hasattr(self, 'left_frame'):
            if self.is_dark_theme:
                # ТЁМНАЯ ТЕМА: возвращаем глубокий графит и контрастный светлый текст
                self.left_frame.setStyleSheet("background-color: #141714; border: 1px solid #222922; border-radius: 6px;")
                self.right_frame.setStyleSheet("background-color: #141714; border: 1px solid #222922; border-radius: 6px;")
                self.scroll_storage.setStyleSheet("border: 1px solid #222922; background-color: #0b0c0a;")
                self.scroll_dropdown.setStyleSheet("border: 1px solid #222922; background-color: #0b0c0a;")
                self.scroll_order.setStyleSheet("border: 1px solid #222922; background-color: #0b0c0a;")
                self.storage_widget.setStyleSheet("background-color: #0b0c0a;")
                self.dropdown_widget.setStyleSheet("background-color: #0b0c0a;")
                self.order_widget.setStyleSheet("background-color: #0b0c0a;")
                
                # Исправляем заголовки под ночную тему (делаем их ярко-белыми и неоново-зелеными)
                self.item_btn_selector.setStyleSheet("background-color: #0b0c0a; color: #86efac; border: 1px solid #222922; padding: 8px; border-radius: 4px;")
                if hasattr(self, 'lbl_left_title'): self.lbl_left_title.setStyleSheet("color: #ffffff; background: transparent; border: none;")
                if hasattr(self, 'lbl_right_title'): self.lbl_right_title.setStyleSheet("color: #a3e635; background: transparent; border: none;")
            else:
                # СВЕТЛАЯ ТЕМА: возвращаем брутальный пустынный матовый хаки
                self.left_frame.setStyleSheet("background-color: #c9c0b5; border: 2px solid #9c8f80; border-radius: 6px;")
                self.right_frame.setStyleSheet("background-color: #c9c0b5; border: 2px solid #9c8f80; border-radius: 6px;")
                self.scroll_storage.setStyleSheet("border: 2px solid #9c8f80; background-color: #f4f1eb;")
                self.scroll_dropdown.setStyleSheet("border: 2px solid #9c8f80; background-color: #f4f1eb;")
                self.scroll_order.setStyleSheet("border: 2px solid #9c8f80; background-color: #f4f1eb;")
                self.storage_widget.setStyleSheet("background-color: #f4f1eb;")
                self.dropdown_widget.setStyleSheet("background-color: #f4f1eb;")
                self.order_widget.setStyleSheet("background-color: #f4f1eb;")
                
                # Исправляем заголовки под дневную тему (делаем их темно-армейскими)
                self.item_btn_selector.setStyleSheet("background-color: #f4f1eb; color: #2b4c1e; border: 1px solid #9c8f80; padding: 8px; border-radius: 4px; font-weight: bold;")
                if hasattr(self, 'lbl_left_title'): self.lbl_left_title.setStyleSheet("color: #1e2417; background: transparent; border: none;")
                if hasattr(self, 'lbl_right_title'): self.lbl_right_title.setStyleSheet("color: #4a5c31; background: transparent; border: none;")
        
        # Перерисовываем внутренние элементы, чтобы они подхватили QSS-стили новой темы
        self.refresh_storage_display()
        self.refresh_order_display()
        self.render_dropdown_buttons(ITEM_OPTIONS)
        self.rebuild_timers_cards()



    def setup_workspace(self):
        # Внутренняя разметка для Раздела №1 (Операции)
        ops_layout = QHBoxLayout(self.page_operations)
        ops_layout.setContentsMargins(5, 5, 5, 5)
        ops_layout.setSpacing(12)

        # ================================================================
        # ЛЕВАЯ СТОРОНА: МОНИТОР СКЛАДА (Песочный матовый армейский стиль)
        # ================================================================
        self.left_frame = QFrame()
        self.left_frame.setStyleSheet("""
            background-color: #c9c0b5; 
            border: 2px solid #9c8f80; 
            border-radius: 6px;
        """)
        left_layout = QVBoxLayout(self.left_frame)
        left_layout.setContentsMargins(18, 18, 18, 18)

        self.lbl_left_title = QLabel("📦 МОНИТОР ТЕКУЩИХ ЗАПАСОВ СКЛАДА")
        self.lbl_left_title.setFont(QFont("Arial", 11, QFont.Weight.Bold))
        self.lbl_left_title.setStyleSheet("color: #1e2417; border: none; background: transparent;")
        left_layout.addWidget(self.lbl_left_title)


        l_ctrl = QHBoxLayout()
        btn_json = QPushButton("📂 ЗАГРУЗИТЬ JSON СКАНЕРА")
        btn_json.setFont(self.font_interface)
        l_ctrl.addWidget(btn_json)

        btn_clip = QPushButton("📋 ВСТАВИТЬ ИЗ БУФЕРА")
        btn_clip.setFont(self.font_interface)
        l_ctrl.addWidget(btn_clip)
        left_layout.addLayout(l_ctrl)

        self.scroll_storage = QScrollArea()
        self.scroll_storage.setWidgetResizable(True)
        self.scroll_storage.setStyleSheet("""
            border: 1px solid #9c8f80; 
            background-color: #f4f1eb;
        """)
        self.storage_widget = QWidget()
        self.storage_widget.setStyleSheet("background-color: #f4f1eb;")
        self.storage_layout = QVBoxLayout(self.storage_widget)
        self.storage_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.scroll_storage.setWidget(self.storage_widget)
        left_layout.addWidget(self.scroll_storage)

        self.btn_mode_left = QPushButton("РЕЖИМ: ЭКСПОРТ ДАННЫХ")
        self.btn_mode_left.setCheckable(True)
        self.btn_mode_left.setFont(self.font_interface)
        left_layout.addWidget(self.btn_mode_left)

        l_btn_grid = QHBoxLayout()
        for txt in ["TXT", "XLSX", "PNG", "PNG в Буфер"]:
            fmt = "png_buffer" if txt == "PNG в Буфер" else txt.lower()
            b = QPushButton(txt)
            b.setFont(self.font_interface)
            b.clicked.connect(lambda checked=False, f=fmt: self.handle_file_action("склад", f))
            l_btn_grid.addWidget(b)
        left_layout.addLayout(l_btn_grid)
        ops_layout.addWidget(self.left_frame)

        # ================================================================
        # ПРАВАЯ СТОРОНА: КОНСТРУКТОР ЗАКАЗА (Песочный матовый армейский стиль)
        # ================================================================
        self.right_frame = QFrame()
        self.right_frame.setStyleSheet("""
            background-color: #c9c0b5; 
            border: 2px solid #9c8f80; 
            border-radius: 6px;
        """)
        right_layout = QVBoxLayout(self.right_frame)
        right_layout.setContentsMargins(18, 18, 18, 18)

        self.lbl_right_title = QLabel("🛒 КОНСТРУКТОР СНАБЖЕНИЯ БАЗЫ")
        self.lbl_right_title.setFont(QFont("Arial", 11, QFont.Weight.Bold))
        self.lbl_right_title.setStyleSheet("color: #4a5c31; border: none; background: transparent;")
        right_layout.addWidget(self.lbl_right_title)


        s_layout = QHBoxLayout()
        self.item_btn_selector = QLabel("Выбрать предмет из матрицы ниже...")
        self.item_btn_selector.setStyleSheet("""
            background-color: #f4f1eb; 
            color: #2b4c1e; 
            border: 1px solid #9c8f80; 
            padding: 8px; 
            border-radius: 4px;
            font-weight: bold;
        """)
        self.item_btn_selector.setFont(self.font_interface)
        s_layout.addWidget(self.item_btn_selector, 3)

        self.count_input = QLineEdit()
        self.count_input.setPlaceholderText("КОЛ-ВО")
        self.count_input.setFont(self.font_interface)
        s_layout.addWidget(self.count_input, 1)

        btn_add = QPushButton("ДОБАВИТЬ В ЗАКАЗ")
        btn_add.setFont(self.font_interface)
        btn_add.clicked.connect(self.add_item_to_order)
        s_layout.addWidget(btn_add)
        right_layout.addLayout(s_layout)

        self.filter_input = QLineEdit()
        self.filter_input.setPlaceholderText("🔍 ИНТЕРАКТИВНЫЙ ФИЛЬТР МАТРИЦЫ ПРЕДМЕТОВ...")
        self.filter_input.setFont(self.font_interface)
        self.filter_input.textChanged.connect(self.filter_items)
        right_layout.addWidget(self.filter_input)

        self.scroll_dropdown = QScrollArea()
        self.scroll_dropdown.setWidgetResizable(True)
        self.scroll_dropdown.setFixedHeight(120)
        self.scroll_dropdown.setStyleSheet("""
            border: 1px solid #9c8f80; 
            background-color: #f4f1eb;
        """)
        self.dropdown_widget = QWidget()
        self.dropdown_widget.setStyleSheet("background-color: #f4f1eb;")
        self.dropdown_layout = QVBoxLayout(self.dropdown_widget)
        self.dropdown_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.scroll_dropdown.setWidget(self.dropdown_widget)
        right_layout.addWidget(self.scroll_dropdown)

        btn_clear = QPushButton("⚠️ ПОЛНАЯ ОЧИСТКА ТЕКУЩЕГО ЗАКАЗА")
        btn_clear.setStyleSheet("""
            background-color: #d9c3c3; 
            color: #7a2828; 
            border: 1px solid #b88686; 
            padding: 6px; 
            border-radius: 4px;
            font-weight: bold;
        """)
        btn_clear.setFont(self.font_interface)
        btn_clear.clicked.connect(self.clear_order)
        right_layout.addWidget(btn_clear)

        self.scroll_order = QScrollArea()
        self.scroll_order.setWidgetResizable(True)
        self.scroll_order.setStyleSheet("""
            border: 1px solid #9c8f80; 
            background-color: #f4f1eb;
        """)
        self.order_widget = QWidget()
        self.order_widget.setStyleSheet("background-color: #f4f1eb;")
        self.order_layout = QVBoxLayout(self.order_widget)
        self.order_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.scroll_order.setWidget(self.order_widget)
        right_layout.addWidget(self.scroll_order)

        self.btn_mode_right = QPushButton("РЕЖИМ: ЭКСПОРТ ДАННЫХ")
        self.btn_mode_right.setCheckable(True)
        self.btn_mode_right.setFont(self.font_interface)
        right_layout.addWidget(self.btn_mode_right)

        r_btn_grid = QHBoxLayout()
        for txt in ["TXT", "XLSX", "PNG", "PNG в Буфер"]:
            fmt = "png_buffer" if txt == "PNG в Буфер" else txt.lower()
            b = QPushButton(txt)
            b.setFont(self.font_interface)
            b.clicked.connect(lambda checked=False, f=fmt: self.handle_file_action("заказ", f))
            r_btn_grid.addWidget(b)
        right_layout.addLayout(r_btn_grid)
        ops_layout.addWidget(self.right_frame)

        self.render_dropdown_buttons(ITEM_OPTIONS)
        self.refresh_order_display()
        self.setup_timers_matrix_workspace()

    def setup_timers_matrix_workspace(self):
        # ЗАЩИТА QT: Если макет у страницы уже есть — не создаем его заново (убирает 1 FPS лаги!)
        if not self.page_timers_matrix.layout():
            timers_layout = QVBoxLayout(self.page_timers_matrix)
            timers_layout.setContentsMargins(15, 15, 15, 15)
            timers_layout.setSpacing(10)
            
            # Информационный счётчик рисков снабжения
            self.telemetry_frame = QFrame()
            self.telemetry_frame.setFixedHeight(35)
            self.telemetry_frame.setStyleSheet("background-color: #141714; border: 1px solid #222922; border-radius: 4px;")
            telemetry_layout = QHBoxLayout(self.telemetry_frame)
            telemetry_layout.setContentsMargins(15, 0, 15, 0)
            
            # Боевые индикаторы статистики рисков деспавна
            self.lbl_crit_stat = QLabel("🚨 КРИТИЧЕСКИ (<1ч): 0 БАЗ")
            self.lbl_crit_stat.setFont(QFont("Arial", 9, QFont.Weight.Bold))
            self.lbl_crit_stat.setStyleSheet("color: #ef4444; background: transparent;")
            telemetry_layout.addWidget(self.lbl_crit_stat)
            
            self.lbl_warn_stat = QLabel("⚠️ ВНИМАНИЕ (<24ч): 0 БАЗ")
            self.lbl_warn_stat.setFont(QFont("Arial", 9, QFont.Weight.Bold))
            self.lbl_warn_stat.setStyleSheet("color: #f59e0b; background: transparent;")
            telemetry_layout.addWidget(self.lbl_warn_stat, 0, Qt.AlignmentFlag.AlignCenter)
            
            self.lbl_safe_stat = QLabel("✅ В БЕЗОПАСНОСТИ (>1д): 0 БАЗ")
            self.lbl_safe_stat.setFont(QFont("Arial", 9, QFont.Weight.Bold))
            self.lbl_safe_stat.setStyleSheet("color: #a3e635; background: transparent;")
            telemetry_layout.addWidget(self.lbl_safe_stat, 0, Qt.AlignmentFlag.AlignRight)
            
            timers_layout.addWidget(self.telemetry_frame)
            
            # Скролл-зона для парящих карточек складов
            self.scroll_timers = QScrollArea()
            self.scroll_timers.setWidgetResizable(True)
            self.scroll_timers.setStyleSheet("border: none; background-color: transparent;")
            
            self.timers_widget = QWidget()
            self.timers_widget.setStyleSheet("background-color: transparent;")
            self.timers_list_layout = QVBoxLayout(self.timers_widget)
            self.timers_list_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
            self.scroll_timers.setWidget(self.timers_widget)
            
            timers_layout.addWidget(self.scroll_timers)
        
        # Перестраиваем карточки складов с текстурой card-bg.jpg
        self.rebuild_timers_cards()


    def rebuild_timers_cards(self):
        """ТЯЖЕЛАЯ ОПЕРАЦИЯ: Формирует структуру ярких, контрастных карточек и накладывает card-bg.jpg."""
        while self.timers_list_layout.count():
            item = self.timers_list_layout.takeAt(0)
            if item.widget(): 
                item.widget().deleteLater()
        
        self.timer_labels.clear()
        sorted_stockpiles = sorted(self.timers_list, key=lambda x: x["TimeLeft"])
        
        # Проверяем наличие вашего ассета с рамкой в папке scr/
        card_bg_path = get_resource_path(os.path.join("scr", "card-bg.jpg"))
        has_bg = os.path.exists(card_bg_path)
        
        for idx, s in enumerate(sorted_stockpiles):
            card = QFrame()
            card.setFixedHeight(75) # Чуть увеличим высоту для лучшего зазора текста
            ts = s["TimeLeft"]
            
            # Настраиваем ПЛОТНЫЕ контрастные цвета фонов и НЕОНОВЫХ рамок
            if ts < 3600:
                border_c = "#ff4545"      # Яркий красный контур
                fallback_bg = "#2e1414"   # Плотный красно-бордовый фон
                text_c = "#ffffff"        # Кристально белый текст для читаемости
                time_c = "#ff5555"        # Светящееся время
            elif ts < 86400:
                border_c = "#f59e0b"      # Яркий оранжевый контур
                fallback_bg = "#2b2015"   # Плотный оранжево-коричневый фон
                text_c = "#ffffff"
                time_c = "#ff9900"
            else:
                border_c = "#3b473b"      # Технологичный стальной контур
                fallback_bg = "#161a16"   # Глубокий графитово-зеленый фон
                text_c = "#ffffff"
                time_c = "#a3e635"        # Лаймовое безопасное время
                
            # Если картинка на месте — вшиваем её, если нет — накладываем наши новые плотные Sci-Fi фоны
            if has_bg:
                style_string = f"""
                    QFrame {{ 
                        background-image: url('{card_bg_path.replace(os.sep, "/")}'); 
                        background-position: center; 
                        background-repeat: no-repeat; 
                        border: 2px solid {border_c}; 
                        border-left: 6px solid {time_c}; 
                        border-radius: 6px; 
                    }} 
                    QFrame:hover {{ 
                        background-color: #223022;
                        border: 2px solid #a3e635; 
                    }}
                """
            else:
                style_string = f"""
                    QFrame {{ 
                        background-color: {fallback_bg}; 
                        border: 2px solid {border_c}; 
                        border-left: 6px solid {time_c}; 
                        border-radius: 6px; 
                    }} 
                    QFrame:hover {{ 
                        background-color: #1f291f; 
                        border: 2px solid #a3e635; 
                    }}
                """
            card.setStyleSheet(style_string)
            
            cl = QHBoxLayout(card)
            cl.setContentsMargins(20, 0, 20, 0)
            
            # Контрастная инфо-панель (Текст стал белым и крупным)
            lbl_info = QLabel(f"📍 {s['Region'].upper()}   ▶   {s['Location']}")
            lbl_info.setFont(QFont("Arial", 11, QFont.Weight.Bold))
            lbl_info.setStyleSheet(f"color: {text_c}; background: transparent; border: none;")
            cl.addWidget(lbl_info)
            
            # Электронный таймер (Увеличили размер шрифта до 15 для идеальной читаемости)
            lbl_time = QLabel("--:--:--")
            lbl_time.setFont(QFont("Consolas", 15, QFont.Weight.Bold))
            lbl_time.setStyleSheet(f"color: {time_c}; background: transparent; border: none;")
            cl.addWidget(lbl_time, 0, Qt.AlignmentFlag.AlignRight)
            
            # Связываем ссылку на текстовое поле с ID склада
            self.timer_labels[s["ID"]] = lbl_time
            
            # Кнопка ручного ввода таймеров и просмотра логов
            btn_manage = QPushButton("УПРАВЛЕНИЕ")
            btn_manage.setFixedSize(110, 34)
            btn_manage.setFont(self.font_interface)
            btn_manage.setStyleSheet("""
                QPushButton { 
                    background-color: #242b24; 
                    color: #ffffff; 
                    border: 1px solid #3d4a3d; 
                    border-radius: 4px; 
                } 
                QPushButton:hover { 
                    background-color: #a3e635; 
                    color: #000000; 
                    font-weight: bold; 
                    border: 1px solid #ffffff; 
                }
            """)
            btn_manage.clicked.connect(lambda checked=False, sid=s["ID"]: self.open_stockpile_manager(sid))
            cl.addWidget(btn_manage, 0, Qt.AlignmentFlag.AlignRight)
            
            self.timers_list_layout.addWidget(card)
            
        # Запускаем первичный легкий подсчет текста времени
        self.refresh_timers_matrix_display()

            
        # Запускаем первичный легкий подсчет текста времени
        self.refresh_timers_matrix_display()
    def open_stockpile_manager(self, stockpile_id):
        """Интерактивное окно: раздельный ввод Дней/Часов/Минут и сохранение логов."""
        s = next(x for x in self.timers_list if x["ID"] == stockpile_id)

        dialog = QDialog(self)
        dialog.setWindowTitle(f"🛠️ КАНАЛ СВЯЗИ: {s['Location']}")
        dialog.setFixedSize(550, 500)
        dialog.setStyleSheet("background-color: #141714; color: #e5e7eb;")

        dl = QVBoxLayout(dialog)
        dl.setContentsMargins(15, 15, 15, 15)
        dl.setSpacing(10)

        dl.addWidget(QLabel(f"🗺️ Регион: {s['Region']}"))
        dl.addWidget(QLabel(f"📍 Локация: {s['Location']}"))

        # Консоль вывода истории логов
        dl.addWidget(QLabel("📜 ИСТОРИЯ ОБНОВЛЕНИЙ И ЛОГОВ СКЛАДА:"))
        log_view = QTextEdit()
        log_view.setReadOnly(True)
        log_view.setPlainText("\n".join(s["History"]))
        dl.addWidget(log_view)

        # ⏱️ ТАКТИЧЕСКИЙ БЛОК РАЗДЕЛЬНОГО ВВОДА ВРЕМЕНИ
        time_input_frame = QFrame()
        time_input_frame.setStyleSheet("background-color: #0b0c0a; border: 1px solid #222922; border-radius: 4px;")
        time_input_layout = QHBoxLayout(time_input_frame)
        time_input_layout.setContentsMargins(10, 10, 10, 10)

        time_input_layout.addWidget(QLabel("ДНИ:"))
        days_input = QLineEdit()
        days_input.setPlaceholderText("0")
        days_input.setFixedWidth(50)
        days_input.setAlignment(Qt.AlignmentFlag.AlignCenter)
        time_input_layout.addWidget(days_input)

        time_input_layout.addWidget(QLabel("ЧАСЫ:"))
        hours_input = QLineEdit()
        hours_input.setPlaceholderText("0")
        hours_input.setFixedWidth(50)
        hours_input.setAlignment(Qt.AlignmentFlag.AlignCenter)
        time_input_layout.addWidget(hours_input)

        time_input_layout.addWidget(QLabel("МИНУТЫ:"))
        mins_input = QLineEdit()
        mins_input.setPlaceholderText("0")
        mins_input.setFixedWidth(50)
        mins_input.setAlignment(Qt.AlignmentFlag.AlignCenter)
        time_input_layout.addWidget(mins_input)

        dl.addWidget(time_input_frame)

        # Кнопки быстрых команд интенданта
        btn_layout = QHBoxLayout()
        
        btn_reset = QPushButton("♻️ СБРОСИТЬ НА 48 ЧАСОВ")
        btn_reset.setStyleSheet("background-color: #1e291b; color: #a3e635; font-weight: bold; border: 1px solid #16a34a; padding: 10px;")
        
        btn_apply = QPushButton("✅ ПРИМЕНИТЬ ТАЙМЕР")
        btn_apply.setStyleSheet("background-color: #1d221d; color: #ffffff; font-weight: bold; border: 1px solid #2c352c; padding: 10px;")

        btn_layout.addWidget(btn_reset)
        btn_layout.addWidget(btn_apply)
        dl.addLayout(btn_layout)

        # Логика обработки и пересчета времени в секунды
        def reset_to_max():
            s["TimeLeft"] = 172800  # 48 часов
            now_str = datetime.now().strftime("%d.%m / %H:%M:%S")
            s["History"].append(f"[{now_str}] Интендант выполнил быстрый сброс таймера на базовые 48 часов.")
            log_view.setPlainText("\n".join(s["History"]))
            self.rebuild_timers_cards()

        def apply_custom_time():
            d_txt = days_input.text().strip() or "0"
            h_txt = hours_input.text().strip() or "0"
            m_txt = mins_input.text().strip() or "0"
            
            if d_txt.isdigit() and h_txt.isdigit() and m_txt.isdigit():
                total_seconds = (int(d_txt) * 86400) + (int(h_txt) * 3600) + (int(m_txt) * 60)
                
                if total_seconds > 0:
                    s["TimeLeft"] = total_seconds
                    now_str = datetime.now().strftime("%d.%m / %H:%M:%S")
                    s["History"].append(f"[{now_str}] Установлено новое время удержания: {d_txt}д {h_txt}ч {m_txt}м.")
                    log_view.setPlainText("\n".join(s["History"]))
                    
                    days_input.clear()
                    hours_input.clear()
                    mins_input.clear()
                    self.rebuild_timers_cards()
                else:
                    QMessageBox.warning(dialog, "СБОЙ", "Итоговое время должно быть больше 0 секунд!")
            else:
                QMessageBox.warning(dialog, "СБОЙ СИНТАКСИСА", "Заполняйте поля только числовыми значениями!")

        btn_reset.clicked.connect(reset_to_max)
        btn_apply.clicked.connect(apply_custom_time)

        dialog.exec()
    def auto_load_scanner_file(self):
        """ФОНОВЫЙ МОНИТОРИНГ: Автоматически считывает stockpile.txt каждую секунду без кнопок."""
        file_path = r"D:\Games\foxhole-stockpiles-main\stockpile.txt"
        if not os.path.exists(file_path):
            return
        try:
            parsed = []
            with open(file_path, "r", encoding="utf-8") as file:
                lines = file.readlines()
                
            for idx, line in enumerate(lines):
                line = line.strip()
                if not line:
                    continue
                
                # Защита: пропускаем первую техническую строку сканера с координатами
                if idx == 0 and any(m in line.lower() for m in ["public", "private", "x:", "y:", "valley", "port", "king"]):
                    continue
                    
                # Распиливаем строку по последней запятой
                if "," in line:
                    parts = line.rsplit(",", 1)
                    item_name = parts[0].strip()
                    count_str = parts[1].strip()
                    
                    if count_str.isdigit():
                        count_val = int(count_str)
                        # ЖЕСТКИЙ ФИЛЬТР: Отсекаем предметы с количеством 0
                        if count_val > 0:
                            parsed.append({"Name": item_name, "Count": count_val})
            
            # Обновляем экран склада только если содержимое файла реально изменилось
            if parsed and parsed != getattr(self, 'last_parsed_data', None):
                self.last_parsed_data = parsed
                self.storage_data = parsed
                self.refresh_storage_display()
        except:
            pass

    def refresh_storage_display(self):
        while self.storage_layout.count():
            item = self.storage_layout.takeAt(0)
            if item.widget(): 
                item.widget().deleteLater()
                
        for idx, x in enumerate(self.storage_data):
            row = QFrame()
            row.setFixedHeight(36)
            
            # Адаптация под светлую тему: чередующиеся песочные строки с оливковым hover-эффектом
            row.setStyleSheet(f"""
                QFrame {{ 
                    background-color: {'#ebe4db' if idx % 2 == 0 else 'transparent'}; 
                    border: 1px solid transparent; 
                    border-radius: 4px; 
                }} 
                QFrame:hover {{ 
                    background-color: #d2d9be; 
                    border: 1px solid #7e8761; 
                }}
            """)
            
            row_layout = QHBoxLayout(row)
            row_layout.setContentsMargins(10, 0, 10, 0)
            
            lbl_name = QLabel(f"• {x['Name']}")
            lbl_name.setFont(self.font_interface)
            lbl_name.setStyleSheet("color: #1b1d1b; background: transparent; border: none;")
            row_layout.addWidget(lbl_name)
            
            p = QFrame()
            p.setFixedSize(80, 24)
            p.setStyleSheet("""
                background-color: #e2ebd5; 
                border: 1px solid #7e8761; 
                border-radius: 4px;
            """)
            pl = QVBoxLayout(p)
            pl.setContentsMargins(0, 0, 0, 0)
            
            lbl_c = QLabel(f"{x['Count']} шт.")
            lbl_c.setFont(self.font_interface)
            lbl_c.setStyleSheet("color: #2b4c1e; background: transparent; border: none;")
            lbl_c.setAlignment(Qt.AlignmentFlag.AlignCenter)
            pl.addWidget(lbl_c)
            
            row_layout.addWidget(p)
            self.storage_layout.addWidget(row)

    def refresh_order_display(self):
        while self.order_layout.count():
            item = self.order_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
                
        if not self.current_order:
            empty = QFrame()
            empty.setFixedHeight(45)
            empty.setStyleSheet("""
                background-color: #f7e6e6; 
                border: 1px solid #c79595; 
                border-radius: 4px;
            """)
            el = QVBoxLayout(empty)
            lbl = QLabel("Заказ пуст. Выберите предметы из матрицы выше...")
            lbl.setFont(self.font_interface)
            lbl.setStyleSheet("color: #8c2b2b; background: transparent; border: none;")
            lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
            el.addWidget(lbl)
            self.order_layout.addWidget(empty)
            return
            
        for idx, (item, count) in enumerate(self.current_order.items()):
            row = QFrame()
            row.setFixedHeight(36)
            row.setStyleSheet(f"""
                QFrame {{ 
                    background-color: {'#ebe4db' if idx % 2 == 0 else 'transparent'}; 
                    border: 1px solid transparent; 
                    border-radius: 4px; 
                }} 
                QFrame:hover {{ 
                    background-color: #cbd9be; 
                    border: 1px solid #64734d; 
                }}
            """)
            
            row_layout = QHBoxLayout(row)
            row_layout.setContentsMargins(10, 0, 10, 0)
            
            lbl_name = QLabel(f"• {item}")
            lbl_name.setFont(self.font_interface)
            lbl_name.setStyleSheet("color: #1b1d1b; background: transparent; border: none;")
            row_layout.addWidget(lbl_name)
            
            p = QFrame()
            p.setFixedSize(85, 24)
            p.setStyleSheet("""
                background-color: #e2ebd5; 
                border: 1px solid #556631; 
                border-radius: 4px;
            """)
            pl = QVBoxLayout(p)
            pl.setContentsMargins(0, 0, 0, 0)
            
            lbl_c = QLabel(f"{count} ящ.")
            lbl_c.setFont(self.font_interface)
            lbl_c.setStyleSheet("color: #314a1a; background: transparent; border: none;")
            lbl_c.setAlignment(Qt.AlignmentFlag.AlignCenter)
            pl.addWidget(lbl_c)
            
            row_layout.addWidget(p)
            self.order_layout.addWidget(row)

            
        # Цикл отрисовки добавленных в заказ ящиков
        for idx, (item, count) in enumerate(self.current_order.items()):
            row = QFrame()
            row.setFixedHeight(36)
            row.setStyleSheet(f"QFrame {{ background-color: {'#141814' if idx % 2 == 0 else 'transparent'}; border: 1px solid transparent; border-radius: 4px; }} QFrame:hover {{ background-color: #1b2e1b; border: 1px solid #84cc16; }}")
            
            row_layout = QHBoxLayout(row)
            row_layout.setContentsMargins(10, 0, 10, 0)
            
            lbl_name = QLabel(f"• {item}")
            lbl_name.setFont(self.font_interface)
            lbl_name.setStyleSheet("color: #e5e7eb; background: transparent;")
            row_layout.addWidget(lbl_name)
            
            p = QFrame()
            p.setFixedSize(85, 24)
            p.setStyleSheet("background-color: #1e291b; border: 1px solid #16a34a; border-radius: 4px;")
            pl = QVBoxLayout(p)
            pl.setContentsMargins(0, 0, 0, 0)
            
            lbl_c = QLabel(f"{count} ящ.")
            lbl_c.setFont(self.font_interface)
            lbl_c.setStyleSheet("color: #a3e635; background: transparent;")
            lbl_c.setAlignment(Qt.AlignmentFlag.AlignCenter)
            pl.addWidget(lbl_c)
            
            row_layout.addWidget(p)
            self.order_layout.addWidget(row)

    def render_dropdown_buttons(self, items_list):
        """Отрисовка контрастных кнопок матрицы предметов под светлую хаки-тему."""
        while self.dropdown_layout.count():
            item = self.dropdown_layout.takeAt(0)
            if item.widget(): 
                item.widget().deleteLater()
                
        for item in items_list:
            btn = QPushButton(f"  {item}")
            btn.setFont(self.font_interface)
            
            # Адаптация под Desert Khaki: тёмный текст, прозрачный фон, оливковый hover сдвиг
            btn.setStyleSheet("""
                QPushButton { 
                    text-align: left; 
                    color: #1b1d1b;            /* Жесткий темно-армейский контрастный текст */
                    background-color: transparent; 
                    border: 1px solid transparent; 
                    padding-left: 6px; 
                    padding-top: 6px;
                    padding-bottom: 6px;
                    border-radius: 4px;
                } 
                QPushButton:hover { 
                    background-color: #4a5c31; /* При наведении заливается глубоким военным зеленым */
                    color: #ffffff;            /* Текст становится кристально белым */
                    border: 1px solid #354222;
                    padding-left: 16px;        /* Эффект тактического отскока вправо */
                }
            """)
            btn.clicked.connect(lambda checked=False, val=item: self.select_dropdown_value(val))
            self.dropdown_layout.addWidget(btn)


    def select_dropdown_value(self, value):
        self.selected_item_name = value
        self.item_btn_selector.setText(value)

    def filter_items(self, text):
        """Интерактивный фильтр предметов по ключевым буквам."""
        q = text.lower().strip()
        if not q:
            self.render_dropdown_buttons(ITEM_OPTIONS)
            return
        f = [i for i in ITEM_OPTIONS if i.lower().startswith(q)] + [i for i in ITEM_OPTIONS if q in i.lower() and not i.lower().startswith(q)]
        self.render_dropdown_buttons(f if f else ["Ничего не найдено"])

    def add_item_to_order(self):
        """Логика добавления выбранной позиции в текущий заказ."""
        item = getattr(self, 'selected_item_name', "Выбрать предмет из матрицы ниже...")
        count = self.count_input.text()
        if item in ["Выбрать предмет из матрицы ниже...", "Ничего не найдено"] or not count.isdigit():
            QMessageBox.warning(self, "ОШИБКА ВВОДА", "Укажите предмет из матрицы и корректное число ящиков!")
            return
        self.current_order[item] = self.current_order.get(item, 0) + int(count)
        self.count_input.clear()
        self.refresh_order_display()

    def clear_order(self):
        self.current_order.clear()
        self.refresh_order_display()
    def load_storage_json(self):
        """Ручной импорт текстового файла логов через диалоговое окно."""
        f, _ = QFileDialog.getOpenFileName(self, "Открыть отчет сканера", "", "Отчеты сканера (*.json *.txt);;Все файлы (*.*)")
        if not f: return
        try:
            parsed = []
            with open(f, "r", encoding="utf-8") as file:
                lines = file.readlines()
                
            for idx, line in enumerate(lines):
                line = line.strip()
                if not line: continue
                if idx == 0 and any(m in line.lower() for m in ["public", "private", "x:", "y:", "valley", "port", "king"]):
                    continue
                    
                if "," in line:
                    parts = line.rsplit(",", 1)
                    item_name = parts[0].strip()
                    count_str = parts[1].strip()
                    if count_str.isdigit():
                        count_val = int(count_str)
                        if count_val > 0:
                            parsed.append({"Name": item_name, "Count": count_val})
                            
            if parsed: 
                self.storage_data = parsed
                self.refresh_storage_display()
                QMessageBox.information(self, "СИНХРОНИЗАЦИЯ", f"Успешно загружено предметов: {len(parsed)}")
            else:
                QMessageBox.warning(self, "ОШИБКА АНАЛИЗА", "На складе нет активных предметов (все позиции равны 0).")
        except Exception as e: 
            QMessageBox.critical(self, "ОШИБКА", f"Сбой парсинга лога:\n{str(e)}")

    def load_storage_clipboard(self):
        """Парсинг лога, скопированного напрямую из буфера обмена."""
        try:
            txt = QApplication.clipboard().text()
            parsed = []
            for line in txt.split('\n'):
                line = line.strip()
                if not line or "," not in line: continue
                parts = line.rsplit(",", 1)
                item_name = parts[0].strip()
                count_str = parts[1].strip()
                if count_str.isdigit() and int(count_str) > 0:
                    parsed.append({"Name": item_name, "Count": int(count_str)})
            if parsed: 
                self.storage_data = parsed
                self.refresh_storage_display()
                QMessageBox.information(self, "БУФЕР ОБМЕНА", f"Данные из буфера успешно загружены!\nПозиций: {len(parsed)}")
        except Exception as e:
            QMessageBox.critical(self, "ОШИБКА БУФЕРА", f"Не удалось распарсить текст из буфера:\n{str(e)}")

    def handle_file_action(self, panel_type, file_format):
        btn = self.btn_mode_left if panel_type == "склад" else self.btn_mode_right
        if btn.isChecked(): 
            QMessageBox.information(self, "ИМПОРТ ДАННЫХ", f"Запущен импорт файлов для панели: {panel_type.upper()}")
        else:
            if file_format == "txt": self.export_text_data(panel_type, "txt")
            elif file_format == "xlsx": self.export_excel_data(panel_type)
            elif file_format == "png": self.export_image_data(panel_type, with_text=True, to_buffer=False)
            elif file_format == "png_buffer": self.export_image_data(panel_type, with_text=True, to_buffer=True)

    def export_text_data(self, mode, ext):
        p, _ = QFileDialog.getSaveFileName(self, "Сохранить рапорт", "", "Text Files (*.txt)")
        if not p: return
        with open(p, "w", encoding="utf-8") as f:
            if mode == "склад":
                f.write("ТАКТИЧЕСКИЙ ОТЧЕТ СКЛАДА:\n")
                for x in self.storage_data: f.write(f"{x['Name']} -> {x['Count']} шт.\n")
            else:
                f.write("ТРЕБУЕМЫЙ ЗАКАЗ СНАБЖЕНИЯ:\n")
                for k, v in self.current_order.items(): f.write(f"{k} -> {v} ящ.\n")
        QMessageBox.information(self, "УСПЕХ", "Рапорт выгружен!")

    def export_excel_data(self, mode):
        p, _ = QFileDialog.getSaveFileName(self, "Сохранить таблицу", "", "Excel Files (*.xlsx)")
        if not p: return
        data = [{"Название": x["Name"], "Количество": x["Count"]} for x in self.storage_data] if mode == "склад" else [{"Название заказа": k, "Количество ящиков": v} for k, v in self.current_order.items()]
        pd.DataFrame(data).to_excel(p, index=False)
        QMessageBox.information(self, "УСПЕХ", "Таблица сформирована!")

    def export_image_data(self, mode, with_text, to_buffer):
        """Разбивка списка предметов на аккуратные страницы и наложение на gray-background.jpg."""
        region, s_type, s_name = "Clanshead Valley", "ПОРТ", "Public"
        current_time_str = datetime.now().strftime("%H-%M_%d.%m.%Y")
        
        target_list = [{"Name": x["Name"], "Count": x["Count"]} for x in self.storage_data] if mode == "склад" else [{"Name": k, "Count": v} for k, v in self.current_order.items()]
            
        if not target_list:
            QMessageBox.warning(self, "ПУСТЫЕ ДАННЫЕ", "Нет элементов для генерации графических страниц!")
            return

        ITEMS_PER_PAGE = 12
        pages_chunks = [target_list[i:i + ITEMS_PER_PAGE] for i in range(0, len(target_list), ITEMS_PER_PAGE)]
        total_pages = len(pages_chunks)

        if to_buffer:
            img = self._render_single_tactical_page(pages_chunks[0], 1, total_pages, region, s_type, s_name)
            import io
            buffer = io.BytesIO()
            img.save(buffer, format="PNG")
            q_pixmap = QPixmap()
            q_pixmap.loadFromData(buffer.getvalue(), "PNG")
            QApplication.clipboard().setPixmap(q_pixmap)
            QMessageBox.information(self, "FAST SHARE", "Первая страница отчета скопирована в буфер обмена Discord через Ctrl+V!")
            return

        base_dir = QFileDialog.getExistingDirectory(self, "Выберите директорию для выгрузки тактической папки страниц")
        if not base_dir: return

        folder_name = f"{current_time_str}_{region}_{s_type}_{s_name}"
        full_output_path = os.path.join(base_dir, folder_name)
        
        if not os.path.exists(full_output_path):
            os.makedirs(full_output_path)

        for page_num, chunk in enumerate(pages_chunks, start=1):
            img = self._render_single_tactical_page(chunk, page_num, total_pages, region, s_type, s_name)
            file_name = f"Стр_{page_num}_из_{total_pages}.png"
            img.save(os.path.join(full_output_path, file_name))

        QMessageBox.information(self, "ПЕЙДЖИНГ ЗАВЕРШЕН", f"Успешно создана тактическая папка:\n{folder_name}\nСтраниц: {total_pages}")

    def _render_single_tactical_page(self, items_chunk, page_num, total_pages, region, s_type, s_name):
        bg_p = get_resource_path(os.path.join("scr", "gray-background.jpg"))
        img = Image.open(bg_p).convert("RGB") if os.path.exists(bg_p) else Image.new("RGB", (650, 1000), color="#2d2d2d")
        img = img.resize((650, 1000), Image.Resampling.LANCZOS)
        draw = ImageDraw.Draw(img)
        try: 
            font_header = ImageFont.truetype("arial.ttf", 20)
            font_body = ImageFont.truetype("arial.ttf", 18)
            font_page = ImageFont.truetype("arial.ttf", 16)
        except: 
            font_header = font_body = font_page = ImageFont.load_default()

        draw.text((40, 30), f"Гекс: {region}", fill="#ffffff", font=font_header)
        draw.text((40, 60), f"Тип: {s_type}", fill="#ffffff", font=font_header)
        draw.text((40, 90), f"Склад: {s_name}", fill="#ffffff", font=font_header)
        draw.text((520, 30), f"Стр. {page_num}/{total_pages}", fill="#60a5fa", font=font_page)
        draw.line([(40, 130), (610, 130)], fill="#4b5563", width=2)

        y_offset = 160
        for x in items_chunk:
            draw.text((40, y_offset), f"•  {x['Name']}", fill="#e5e7eb", font=font_body)
            draw.text((440, y_offset), f"x {x['Count']} (в ящике)", fill="#a3e635", font=font_body)
            y_offset += 65
        return img

    def update_tactical_timers(self):
        """Ежесекундный пересчет времени + обновление счетчиков рисков + сборка цветного HTML конвейера."""
        import random

        # 1. Фоновый отсчет таймеров деспавна складов
        for x in self.timers_list:
            if x["TimeLeft"] > 0: 
                x["TimeLeft"] -= 1

        # Обновление реальной статистики верхних индикаторов Раздела №2
        if hasattr(self, 'lbl_crit_stat'):
            crit = sum(1 for x in self.timers_list if x["TimeLeft"] < 3600)
            warn = sum(1 for x in self.timers_list if 3600 <= x["TimeLeft"] < 86400)
            safe = sum(1 for x in self.timers_list if x["TimeLeft"] >= 86400)
            self.lbl_crit_stat.setText(f"🚨 КРИТИЧЕСКИ (<1ч): {crit} БАЗ")
            self.lbl_warn_stat.setText(f"⚠️ ВНИМАНИЕ (<24ч): {warn} БАЗ")
            self.lbl_safe_stat.setText(f"✅ В БЕЗОПАСНОСТИ (>1д): {safe} БАЗ")

        html_messages = []
        plain_messages = []
        
        # 2. Формируем сообщения для проблемных складов (< 1 дня)
        for x in self.timers_list:
            if x["TimeLeft"] < 86400:
                ts = x["TimeLeft"]
                d, h, m, s_sec = ts // 86400, (ts % 86400) // 3600, (ts % 3600) // 60, ts % 60
                t_str = f"{d}д {h:02d}ч {m:02d}м {s_sec:02d}с" if d > 0 else f"{h:02d}:{m:02d}:{s_sec:02d}"
                
                # Цветовое кодирование: Красный для критических, Оранжевый для обычных алертов
                color_hex = "#ff5555" if ts < 3600 else "#f59e0b"
                status_icon = "🔴 [КРИТИЧЕСКИ]" if ts < 3600 else "🟠 [ВНИМАНИЕ]"
                raw_msg = f"{status_icon} Склад в порту {x['Region']} ({x['Location']}) пропадёт через {t_str}!"
                
                html_messages.append(f"<font color='{color_hex}'>{raw_msg}</font>")
                plain_messages.append(raw_msg)
        
        # 3. Случайный радиоперехват фраз штаба (Шанс 10%) в сочный зеленый цвет
        if self.phrase_hold_seconds > 0:
            self.phrase_hold_seconds -= 1
            if self.active_custom_phrase:
                html_messages.append(f"<font color='#a3e635'>🟢 {self.active_custom_phrase}</font>")
                plain_messages.append(f"🟢 {self.active_custom_phrase}")
        else:
            if random.random() < 0.10:
                self.active_custom_phrase = random.choice(TACTICAL_CUSTOM_PHRASES)
                self.phrase_hold_seconds = 12
                html_messages.append(f"<font color='#a3e635'>🟢 {self.active_custom_phrase}</font>")
                plain_messages.append(f"🟢 {self.active_custom_phrase}")
            else:
                self.active_custom_phrase = ""

        # 4. Склеиваем блоки и дублируем 3 раза для бесшовности конвейера
        if html_messages:
            base_html = "   •   ".join(html_messages) + "   •   "
            base_plain = "   •   ".join(plain_messages) + "   •   "
        else:
            base_html = "<font color='#a3e635'>🟢 ВСЕ СЕКТОРА СНАБЖЕНИЯ В ПОЛНОЙ БЕЗОПАСНОСТИ   •   </font>"
            base_plain = "🟢 ВСЕ СЕКТОРА СНАБЖЕНИЯ В ПОЛНОЙ БЕЗОПАСНОСТИ   •   "

        # Записываем цветной вариант для экрана и чистый вариант для замеров физики
        self.raw_ticker_text = base_html * 3
        self.plain_ticker_text = base_plain * 3
        
        self.refresh_timers_matrix_display()



    def refresh_timers_matrix_display(self):
        """ЛЕГКОВЕСНАЯ ОПЕРАЦИЯ: Безопасное обновление текста времени без нагрузки на систему."""
        if hasattr(self, 'lbl_crit_stat'):
            crit = sum(1 for x in self.timers_list if x["TimeLeft"] < 3600)
            warn = sum(1 for x in self.timers_list if 3600 <= x["TimeLeft"] < 86400)
            safe = sum(1 for x in self.timers_list if x["TimeLeft"] >= 86400)
            self.lbl_crit_stat.setText(f"🚨 КРИТИЧЕСКИ (<1ч): {crit} БАЗ")
            self.lbl_warn_stat.setText(f"⚠️ ВНИМАНИЕ (<24ч): {warn} БАЗ")
            self.lbl_safe_stat.setText(f"✅ В БЕЗОПАСНОСТИ (>1д): {safe} БАЗ")

        # Проверяем, существует ли словарь и не пуст ли он
        if hasattr(self, 'timer_labels') and self.timer_labels:
            for s in self.timers_list:
                if s["ID"] in self.timer_labels:
                    ts = s["TimeLeft"]
                    d, h, m, s_sec = ts // 86400, (ts % 86400) // 3600, (ts % 3600) // 60, ts % 60
                    t_str = f"{d}д {h:02d}ч {m:02d}м {s_sec:02d}с" if d > 0 else f"{h:02d}:{m:02d}:{s_sec:02d}"
                    self.timer_labels[s["ID"]].setText(t_str)


    def animate_ticker(self):
        """ВЕКТОРНЫЙ ДВИЖОК 60 ГЦ: Безошибочный расчет смещения по чистому тексту с выводом цветного HTML."""
        if not hasattr(self, 'raw_ticker_text') or not self.raw_ticker_text:
            return

        # Сдвиг строго по целым пикселям для максимальной четкости букв ClearType
        self.ticker_offset -= 2
        
        # Измеряем точную физическую длину ОДНОЙ ТРЕТИ чистого текста (без учета скрытых тегов кода)
        total_width = self.lbl_ticker_text.fontMetrics().horizontalAdvance(self.plain_ticker_text)
        one_third_width = total_width // 3

        if one_third_width <= 0:
            return

        # Бесшовный сброс без швов и пауз
        if abs(self.ticker_offset) >= one_third_width:
            self.ticker_offset = 0

        # Выводим на экран шикарный цветной HTML рапорт
        self.lbl_ticker_text.setText(self.raw_ticker_text)
        
        # Двигаем текстовый блок по выверенным координатам
        final_x = int(self.sidebar_frame.width() + self.ticker_offset)
        self.lbl_ticker_text.move(final_x, 14)




if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LogisticsStudioApp()
    window.show()
    sys.exit(app.exec())

