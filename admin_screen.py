from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QLabel, QLineEdit, QComboBox, QTableWidget, QFrame, QTableWidgetItem,
    QHeaderView, QSpinBox, QPushButton, QStackedWidget
)


import data_manager
from dialogs import UpdateStatusDialog, CustomAlertDialog




class AdminDashboardView(QWidget):
    COLUMNS = ["ORDER ID", "CUSTOMER INFO", "SPECIFICATIONS", "SOURCE", "AMOUNT", "STATUS", "ACTION"]


    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.init_ui()


    def init_ui(self):
        admin_layout = QVBoxLayout(self)
        admin_layout.setContentsMargins(14, 14, 14, 14)
        admin_layout.setSpacing(10)


        metrics_layout = QHBoxLayout()
        metrics_layout.setSpacing(10)


        card_sales, self.label_sales = self._create_metric_card("SALES TODAY", "₱0.00")
        card_orders, self.label_orders = self._create_metric_card("TOTAL ORDERS", "0")
        card_jobs, self.label_jobs = self._create_metric_card("OPEN JOBS", "0")


        metrics_layout.addWidget(card_sales)
        metrics_layout.addWidget(card_orders)
        metrics_layout.addWidget(card_jobs)


        table_panel = QFrame()
        table_panel.setObjectName("card_panel")
        tp_layout = QVBoxLayout(table_panel)
        tp_layout.setContentsMargins(10, 10, 10, 10)
        tp_layout.setSpacing(8)


        filter_layout = QHBoxLayout()
        filter_layout.setSpacing(8)


        self.txt_search = QLineEdit()
        self.txt_search.setPlaceholderText("Search name or order ID...")


        self.combo_filter = QComboBox()
        self.combo_filter.addItems(["All Statuses", "Pending", "Printing", "Ready for Pickup", "Completed", "Cancelled"])
        self.combo_filter.setStyleSheet("background-color: #ffffff; border: 1px solid #cbd5e1; border-radius: 6px; padding: 4px 8px; font-size: 11px;")


        filter_layout.addWidget(self.txt_search, 1)
        filter_layout.addWidget(QLabel("Filter:"))
        filter_layout.addWidget(self.combo_filter)


        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels(self.COLUMNS)


        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.txt_search.textChanged.connect(self.refresh_table)
        self.combo_filter.currentIndexChanged.connect(self.refresh_table)
        self.table.cellClicked.connect(self.cell_clicked)


        tp_layout.addLayout(filter_layout)
        tp_layout.addWidget(self.table)


        admin_layout.addLayout(metrics_layout)
        admin_layout.addWidget(table_panel)


    def _create_metric_card(self, title: str, initial_val: str) -> tuple[QFrame, QLabel]:
        card = QFrame()
        card.setObjectName("metric_card")
        layout = QVBoxLayout(card)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(2)


        lbl_title = QLabel(title)
        lbl_title.setStyleSheet("font-size: 10px; font-weight: 800; color: #64748b; letter-spacing: 0.5px;")


        lbl_val = QLabel(initial_val)
        lbl_val.setStyleSheet("font-size: 18px; font-weight: 800; color: #0f172a;")


        layout.addWidget(lbl_title)
        layout.addWidget(lbl_val)
        return card, lbl_val


    def refresh_table(self):
        search = self.txt_search.text().strip().lower()
        status = self.combo_filter.currentText()
        self.table.setRowCount(0)
        sales = 0.0
        open_jobs = 0


        orders = data_manager.load_orders()


        for order in orders:
            if order["status"] != "Cancelled":
                sales += order["amount"]
            if order["status"] not in ("Completed", "Cancelled"):
                open_jobs += 1


            matches_search = search in order["name"].lower() or search in order["id"].lower()
            matches_status = status == "All Statuses" or order["status"] == status


            if matches_search and matches_status:
                row = self.table.rowCount()
                self.table.insertRow(row)
                customer = f"{order['name']}\n{order['phone']}"
                cells = [
                    order["id"],
                    customer,
                    order["job"],
                    order["source"],
                    f"₱{order['amount']:.2f}",
                    order["status"],
                    "Update"
                ]
                for column, text in enumerate(cells):
                    item = QTableWidgetItem(text)
                    if column == 6:
                        item.setForeground(Qt.GlobalColor.blue)
                    self.table.setItem(row, column, item)


        self.table.resizeRowsToContents()
        self.label_sales.setText(f"₱{sales:.2f}")
        self.label_orders.setText(str(len(orders)))
        self.label_jobs.setText(str(open_jobs))


    def cell_clicked(self, row: int, column: int):
        if column == 6:
            item = self.table.item(row, 0)
            if item:
                self.update_status(item.text())


    def update_status(self, order_id: str):
        orders = data_manager.load_orders()
        for order in orders:
            if order["id"] == order_id:
                dialog = UpdateStatusDialog(order_id, order["status"], self)
                if dialog.exec() == 1:
                    data_manager.update_order_status(order_id, dialog.get_selected_status())
                    self.refresh_table()




class PriceSettingsView(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.init_ui()


    def init_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(14, 14, 14, 14)
        root.setAlignment(Qt.AlignmentFlag.AlignCenter)


        form_card = QFrame()
        form_card.setObjectName("card_panel")
        form_card.setFixedWidth(440)


        layout = QVBoxLayout(form_card)
        layout.setSpacing(12)


        title_box = QVBoxLayout()
        title_box.setSpacing(1)
        lbl_t = QLabel("Base Pricing Settings")
        lbl_t.setObjectName("card_title")
        lbl_s = QLabel("Update print rates and fees. Changes take effect instantly.")
        lbl_s.setObjectName("card_subtitle")
        title_box.addWidget(lbl_t)
        title_box.addWidget(lbl_s)
        layout.addLayout(title_box)


        prices = data_manager.load_prices()
        self.spin_bw = self._create_spin(prices['bw'])
        self.spin_color = self._create_spin(prices['color'])
        self.spin_paper = self._create_spin(prices['paper'])
        self.spin_legal = self._create_spin(prices['legal'])
        self.spin_binding = self._create_spin(prices['binding'])
        self.spin_lamination = self._create_spin(prices['lamination'])


        row1 = QHBoxLayout()
        row1.addWidget(self._col("B&&W Rate per Page (₱)", self.spin_bw))
        row1.addWidget(self._col("Color Rate per Page (₱)", self.spin_color))


        row2 = QHBoxLayout()
        row2.addWidget(self._col("Short Paper Rate (₱)", self.spin_paper))
        row2.addWidget(self._col("Long Paper Rate (₱)", self.spin_legal))


        row3 = QHBoxLayout()
        row3.addWidget(self._col("Book Binding Fee (₱)", self.spin_binding))
        row3.addWidget(self._col("Lamination Fee (₱)", self.spin_lamination))


        layout.addLayout(row1)
        layout.addLayout(row2)
        layout.addLayout(row3)


        btn_save = QPushButton("Save && Update Rates")
        btn_save.setObjectName("primary_action_btn")
        btn_save.clicked.connect(self.save_prices)


        layout.addWidget(btn_save)
        root.addWidget(form_card)


    def _col(self, title: str, widget: QWidget) -> QWidget:
        box = QWidget()
        l = QVBoxLayout(box)
        l.setContentsMargins(0, 0, 0, 0)
        l.setSpacing(2)
        lbl = QLabel(title)
        lbl.setObjectName("field_label")
        l.addWidget(lbl)
        l.addWidget(widget)
        return box


    def _create_spin(self, val: float) -> QSpinBox:
        spin = QSpinBox()
        spin.setRange(0, 999)
        spin.setValue(int(val))
        return spin


    def save_prices(self):
        new_prices = {
            'bw': float(self.spin_bw.value()),
            'color': float(self.spin_color.value()),
            'paper': float(self.spin_paper.value()),
            'legal': float(self.spin_legal.value()),
            'photo_paper': 25.0,
            'binding': float(self.spin_binding.value()),
            'lamination': float(self.spin_lamination.value()),
        }
        data_manager.save_prices(new_prices)
        CustomAlertDialog("Prices Saved", "Rates successfully updated.", self).exec()
        self.main_window.switch_tab(0)




class AdminWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PrintSync - Admin Screen")
        self.init_ui()


        # Timer to auto-refresh queue table
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.queue_view.refresh_table)
        self.timer.start(2000)


    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)


        header = QFrame()
        header.setObjectName("header_bar")
        h_layout = QHBoxLayout(header)
        h_layout.setContentsMargins(14, 8, 14, 8)


        title_box = QVBoxLayout()
        title_box.setSpacing(0)
        t = QLabel("PrintSync")
        t.setObjectName("brand_title")
        sub = QLabel("Admin Screen")
        sub.setObjectName("brand_subtitle")
        title_box.addWidget(t)
        title_box.addWidget(sub)


        nav_layout = QHBoxLayout()
        nav_layout.setSpacing(6)


        self.btn_nav_queue = QPushButton("Order Queue")
        self.btn_nav_rates = QPushButton("Price Rates")


        self.nav_buttons = [self.btn_nav_queue, self.btn_nav_rates]


        for index, btn in enumerate(self.nav_buttons):
            btn.setObjectName("top_nav_btn")
            btn.clicked.connect(lambda _, idx=index: self.switch_tab(idx))
            nav_layout.addWidget(btn)


        h_layout.addLayout(title_box)
        h_layout.addStretch()
        h_layout.addLayout(nav_layout)
        main_layout.addWidget(header)


        self.stack = QStackedWidget()
        self.queue_view = AdminDashboardView(self)
        self.rates_view = PriceSettingsView(self)


        self.stack.addWidget(self.queue_view)
        self.stack.addWidget(self.rates_view)


        main_layout.addWidget(self.stack, 1)


        self.switch_tab(0)


    def switch_tab(self, index: int):
        self.stack.setCurrentIndex(index)
        for i, btn in enumerate(self.nav_buttons):
            btn.setProperty("active", i == index)
            btn.style().unpolish(btn)
            btn.style().polish(btn)


        if index == 0:
            self.queue_view.refresh_table()