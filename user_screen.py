import os
from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QLabel, QLineEdit, QSpinBox, QCheckBox, QPushButton, 
    QButtonGroup, QFrame
)


import data_manager
from dialogs import ConfirmOrderDialog, CustomAlertDialog




class UserOrderWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PrintSync - User Screen")
        self.selected_color = "B&W"
        self.selected_size = "Short"
        self.prices = data_manager.load_prices()


        self.init_ui()


        # Timer to auto-update prices if admin changes rates
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.reload_prices)
        self.timer.start(3000)


    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)


        # Header Bar
        header = QFrame()
        header.setObjectName("header_bar")
        h_layout = QHBoxLayout(header)
        h_layout.setContentsMargins(14, 8, 14, 8)


        title_box = QVBoxLayout()
        title_box.setSpacing(0)
        t = QLabel("PrintSync")
        t.setObjectName("brand_title")
        sub = QLabel("User Screen")
        sub.setObjectName("brand_subtitle")
        title_box.addWidget(t)
        title_box.addWidget(sub)


        h_layout.addLayout(title_box)
        h_layout.addStretch()
        main_layout.addWidget(header)


        # Content Area
        content = QWidget()
        root = QHBoxLayout(content)
        root.setContentsMargins(16, 16, 16, 16)
        root.setSpacing(16)


        # Left Column Card Panel
        left_panel = QFrame()
        left_panel.setObjectName("card_panel")
        left_layout = QVBoxLayout(left_panel)
        left_layout.setSpacing(10)


        title_box_card = QVBoxLayout()
        title_box_card.setSpacing(1)
        lbl_title = QLabel("Customer Information")
        lbl_title.setObjectName("card_title")
        lbl_sub = QLabel("Enter client details and preferred contact channel.")
        lbl_sub.setObjectName("card_subtitle")
        title_box_card.addWidget(lbl_title)
        title_box_card.addWidget(lbl_sub)
        left_layout.addLayout(title_box_card)


        self.txt_name = QLineEdit()
        self.txt_name.setPlaceholderText("e.g. Juan Dela Cruz")


        self.txt_phone = QLineEdit()
        self.txt_phone.setPlaceholderText("0917-XXX-XXXX")


        self.txt_account = QLineEdit()
        self.txt_account.setPlaceholderText("Email address or FB username")


        row_info = QHBoxLayout()
        row_info.setSpacing(10)


        col_name = QVBoxLayout()
        col_name.setSpacing(2)
        col_name.addWidget(self._label("Customer Name *"))
        col_name.addWidget(self.txt_name)


        col_phone = QVBoxLayout()
        col_phone.setSpacing(2)
        col_phone.addWidget(self._label("Contact Number"))
        col_phone.addWidget(self.txt_phone)


        row_info.addLayout(col_name, 1)
        row_info.addLayout(col_phone, 1)
        left_layout.addLayout(row_info)


        col_acc = QVBoxLayout()
        col_acc.setSpacing(2)
        col_acc.addWidget(self._label("Email / FB Account"))
        col_acc.addWidget(self.txt_account)
        left_layout.addLayout(col_acc)


        left_layout.addWidget(self._label("File Submission Source"))
        source_row = QHBoxLayout()
        source_row.setSpacing(8)


        self.source_group = QButtonGroup(self)
        self.btn_gmail = QPushButton("●  Gmail / Email")
        self.btn_fb = QPushButton("●  Facebook / Messenger")


        for btn in (self.btn_gmail, self.btn_fb):
            btn.setCheckable(True)
            btn.setObjectName("grid_option_btn")
            self.source_group.addButton(btn)
            source_row.addWidget(btn, 1)


        self.source_group.buttonClicked.connect(self._update_styles)
        self.btn_gmail.setChecked(True)
        left_layout.addLayout(source_row)


        spec_box = QVBoxLayout()
        spec_box.setSpacing(1)
        lbl_spec_title = QLabel("Print Specifications")
        lbl_spec_title.setObjectName("card_title")
        lbl_spec_sub = QLabel("Select paper size, color options, and add-on services.")
        lbl_spec_sub.setObjectName("card_subtitle")
        spec_box.addWidget(lbl_spec_title)
        spec_box.addWidget(lbl_spec_sub)
        left_layout.addLayout(spec_box)


        left_layout.addWidget(self._label("Color Mode"))
        color_row = QHBoxLayout()
        color_row.setSpacing(8)
        self.color_group = QButtonGroup(self)
        self.btn_bw = QPushButton()
        self.btn_color = QPushButton()


        for btn in (self.btn_bw, self.btn_color):
            btn.setCheckable(True)
            btn.setObjectName("grid_option_btn")
            self.color_group.addButton(btn)
            color_row.addWidget(btn, 1)


        self.color_group.buttonClicked.connect(self._on_color_changed)
        self.btn_bw.setChecked(True)
        left_layout.addLayout(color_row)


        left_layout.addWidget(self._label("Paper Size"))
        size_row = QHBoxLayout()
        size_row.setSpacing(8)
        self.size_group = QButtonGroup(self)
        self.btn_short = QPushButton()
        self.btn_legal = QPushButton()


        for btn in (self.btn_short, self.btn_legal):
            btn.setCheckable(True)
            btn.setObjectName("grid_option_btn")
            self.size_group.addButton(btn)
            size_row.addWidget(btn, 1)


        self.size_group.buttonClicked.connect(self._on_size_changed)
        self.btn_short.setChecked(True)
        left_layout.addLayout(size_row)


        stepper_row = QHBoxLayout()
        stepper_row.setSpacing(10)


        self.spin_pages = QSpinBox()
        self.spin_pages.setRange(1, 1000)
        self.spin_pages.setValue(10)
        self.spin_pages.valueChanged.connect(self.calculate_total)


        self.spin_copies = QSpinBox()
        self.spin_copies.setRange(1, 100)
        self.spin_copies.setValue(1)
        self.spin_copies.valueChanged.connect(self.calculate_total)


        col_p = QVBoxLayout()
        col_p.setSpacing(2)
        col_p.addWidget(self._label("Total Pages"))
        col_p.addWidget(self.spin_pages)


        col_c = QVBoxLayout()
        col_c.setSpacing(2)
        col_c.addWidget(self._label("Number of Copies"))
        col_c.addWidget(self.spin_copies)


        stepper_row.addLayout(col_p, 1)
        stepper_row.addLayout(col_c, 1)
        left_layout.addLayout(stepper_row)


        left_layout.addWidget(self._label("Add-on Services"))
        addons_row = QHBoxLayout()
        addons_row.setSpacing(8)


        box_bind = QFrame()
        box_bind.setObjectName("addon_box")
        l_bind = QVBoxLayout(box_bind)
        l_bind.setContentsMargins(8, 8, 8, 8)
        self.chk_binding = QCheckBox("Book Binding")
        self.chk_binding.toggled.connect(self.calculate_total)
        self.lbl_bind_sub = QLabel("+₱30.00 / copy")
        self.lbl_bind_sub.setStyleSheet("color: #64748b; font-size: 10px;")
        l_bind.addWidget(self.chk_binding)
        l_bind.addWidget(self.lbl_bind_sub)


        box_lam = QFrame()
        box_lam.setObjectName("addon_box")
        l_lam = QVBoxLayout(box_lam)
        l_lam.setContentsMargins(8, 8, 8, 8)
        self.chk_lamination = QCheckBox("Lamination")
        self.chk_lamination.toggled.connect(self.calculate_total)
        self.lbl_lam_sub = QLabel("+₱15.00 / copy")
        self.lbl_lam_sub.setStyleSheet("color: #64748b; font-size: 10px;")
        l_lam.addWidget(self.chk_lamination)
        l_lam.addWidget(self.lbl_lam_sub)


        addons_row.addWidget(box_bind, 1)
        addons_row.addWidget(box_lam, 1)
        left_layout.addLayout(addons_row)


        root.addWidget(left_panel, 3)


        # Right Summary Panel
        right_panel = QFrame()
        right_panel.setObjectName("card_panel")
        right_layout = QVBoxLayout(right_panel)
        right_layout.setSpacing(12)


        header_rec = QHBoxLayout()
        lbl_rec_title = QLabel("ORDER SUMMARY")
        lbl_rec_title.setStyleSheet("font-size: 11px; font-weight: 800; color: #0f172a;")


        lbl_badge = QLabel("Live Calculator")
        lbl_badge.setStyleSheet("background-color: #eff6ff; color: #2563eb; font-size: 9px; font-weight: 700; border-radius: 8px; padding: 2px 6px;")


        header_rec.addWidget(lbl_rec_title)
        header_rec.addStretch()
        header_rec.addWidget(lbl_badge)
        right_layout.addLayout(header_rec)


        self.lbl_breakdown = QLabel()
        self.lbl_breakdown.setStyleSheet("color: #475569; font-family: monospace; font-size: 11px; line-height: 1.6;")
        right_layout.addWidget(self.lbl_breakdown)


        total_box = QFrame()
        total_box.setStyleSheet("background-color: #ecfdf5; border: 1px solid #a7f3d0; border-radius: 6px; padding: 12px;")
        tb_layout = QHBoxLayout(total_box)
        tb_layout.setContentsMargins(10, 10, 10, 10)


        t_left = QVBoxLayout()
        t_left.setSpacing(0)
        lbl_t1 = QLabel("TOTAL AMOUNT")
        lbl_t1.setStyleSheet("font-size: 10px; font-weight: 700; color: #047857;")
        lbl_t2 = QLabel("Incl. all taxes & fees")
        lbl_t2.setStyleSheet("font-size: 9px; color: #059669;")
        t_left.addWidget(lbl_t1)
        t_left.addWidget(lbl_t2)


        self.lbl_total = QLabel("₱0.00")
        self.lbl_total.setStyleSheet("font-size: 22px; font-weight: 800; color: #047857;")


        tb_layout.addLayout(t_left)
        tb_layout.addStretch()
        tb_layout.addWidget(self.lbl_total)
        right_layout.addWidget(total_box)


        self.btn_submit = QPushButton("✓  Place Order into Queue")
        self.btn_submit.setObjectName("primary_action_btn")
        self.btn_submit.clicked.connect(self.place_order)
        right_layout.addWidget(self.btn_submit)


        right_layout.addStretch()
        root.addWidget(right_panel, 2)


        main_layout.addWidget(content, 1)


        self.update_price_labels()


    def _label(self, text: str) -> QLabel:
        lbl = QLabel(text)
        lbl.setObjectName("field_label")
        return lbl


    def _update_styles(self):
        for btn in self.source_group.buttons() + self.color_group.buttons() + self.size_group.buttons():
            btn.setProperty("checked", btn.isChecked())
            btn.style().unpolish(btn)
            btn.style().polish(btn)


    def _on_color_changed(self, button):
        self.selected_color = "Full Color" if button == self.btn_color else "B&W"
        self._update_styles()
        self.calculate_total()


    def _on_size_changed(self, button):
        self.selected_size = "Long (Folio)" if button == self.btn_legal else "Short (Letter)"
        self._update_styles()
        self.calculate_total()


    def reload_prices(self):
        self.prices = data_manager.load_prices()
        self.update_price_labels()


    def update_price_labels(self):
        p = self.prices
        self.btn_bw.setText(f"Black && White\n₱{p['bw']:.2f}/pg")
        self.btn_color.setText(f"Full Color\n₱{p['color']:.2f}/pg")
        self.btn_short.setText(f"Short (Letter)\n₱{p['paper']:.2f}/pg")
        self.btn_legal.setText(f"Long (Folio)\n₱{p['legal']:.2f}/pg")
        self.lbl_bind_sub.setText(f"+₱{p['binding']:.2f} / copy")
        self.lbl_lam_sub.setText(f"+₱{p['lamination']:.2f} / copy")
        self._update_styles()
        self.calculate_total()


    def calculate_total(self) -> float:
        prices = self.prices
        paper_cost = prices['legal'] if "Long" in self.selected_size else prices['paper']
        print_cost = prices['color'] if self.selected_color == "Full Color" else prices['bw']


        pages = self.spin_pages.value()
        copies = self.spin_copies.value()


        base_paper_total = pages * paper_cost
        color_total = pages * print_cost


        addon_cost = 0.00
        addons_list = []
        if self.chk_binding.isChecked():
            addon_cost += prices['binding']
            addons_list.append("Binding")
        if self.chk_lamination.isChecked():
            addon_cost += prices['lamination']
            addons_list.append("Lamination")


        subtotal_per_copy = base_paper_total + color_total + addon_cost
        total_price = subtotal_per_copy * copies


        addons_str = ", ".join(addons_list) if addons_list else "None"


        self.lbl_breakdown.setText(
            f"Paper ({self.selected_size}):\n  {pages} pgs × ₱{paper_cost:.2f} = ₱{base_paper_total:.2f}\n\n"
            f"Color Mode ({self.selected_color}):\n  {pages} pgs × ₱{print_cost:.2f} = ₱{color_total:.2f}\n\n"
            f"Add-ons:\n  {addons_str} (₱{addon_cost:.2f})\n\n"
            f"Print Multiplier:\n  ₱{subtotal_per_copy:.2f} × {copies} copy"
        )
        self.lbl_total.setText(f"₱{total_price:.2f}")
        return total_price


    def place_order(self):
        name = self.txt_name.text().strip()
        phone = self.txt_phone.text().strip()
        account = self.txt_account.text().strip()
        selected_btn = self.source_group.checkedButton()
        source = "Gmail" if "Gmail" in (selected_btn.text() if selected_btn else "") else "Messenger"


        if not name:
            CustomAlertDialog("Missing Info", "Please enter the customer name.", self).exec()
            return


        if not ConfirmOrderDialog(name, phone, source, self).exec():
            return


        orders = data_manager.load_orders()
        order_id = "ORD-" + str(1001 + len(orders))


        pages = self.spin_pages.value()
        copies = self.spin_copies.value()
        extras = [text for text, box in (("Binding", self.chk_binding), ("Lamination", self.chk_lamination)) if box.isChecked()]
        job = f"{pages} pgs × {copies} copy • {self.selected_color} ({self.selected_size})"
        if extras:
            job += f" • Addons: {', '.join(extras)}"


        order = {
            "id": order_id,
            "name": name,
            "phone": phone,
            "account": account,
            "source": source,
            "job": job,
            "amount": self.calculate_total(),
            "status": "Pending",
        }


        data_manager.add_order(order)
        CustomAlertDialog("Order Placed", f"Order {order_id} submitted to queue.", self).exec()


        for box in (self.txt_name, self.txt_phone, self.txt_account):
            box.clear()




# Compatibility Alias
UserOrderView = UserOrderWindow
