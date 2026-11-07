from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
    QComboBox, QFrame, QFormLayout
)




class ConfirmOrderDialog(QDialog):
    def __init__(self, customer_name: str, phone: str, source: str, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Confirm Order Submission")
        self.setMinimumWidth(320)
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(14, 14, 14, 14)
        layout.setSpacing(10)
        
        title = QLabel("Confirm Order Details")
        title.setStyleSheet("font-size: 15px; font-weight: bold; color: #0f172a;")
        layout.addWidget(title)
        
        card = QFrame()
        card.setStyleSheet("background-color: #f8fafc; border: 1px solid #cbd5e1; border-radius: 6px; padding: 10px;")
        card_layout = QFormLayout(card)
        card_layout.setSpacing(6)
        
        card_layout.addRow(self._label("Customer Name:"), self._val_label(customer_name))
        card_layout.addRow(self._label("Contact Number:"), self._val_label(phone if phone else "N/A"))
        card_layout.addRow(self._label("File Source:"), self._val_label(source))
        
        layout.addWidget(card)
        
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(8)
        
        btn_cancel = QPushButton("Cancel")
        btn_cancel.setStyleSheet("background-color: #f1f5f9; color: #475569; font-weight: 600; border-radius: 6px; padding: 6px 12px;")
        btn_cancel.clicked.connect(self.reject)
        
        btn_confirm = QPushButton("Confirm && Submit")
        btn_confirm.setStyleSheet("background-color: #2563eb; color: #ffffff; font-weight: bold; border-radius: 6px; padding: 6px 12px;")
        btn_confirm.clicked.connect(self.accept)
        
        btn_layout.addWidget(btn_cancel)
        btn_layout.addWidget(btn_confirm)
        layout.addLayout(btn_layout)


    def _label(self, text: str) -> QLabel:
        lbl = QLabel(text)
        lbl.setStyleSheet("font-size: 11px; font-weight: 600; color: #64748b;")
        return lbl


    def _val_label(self, text: str) -> QLabel:
        lbl = QLabel(text)
        lbl.setStyleSheet("font-size: 11px; font-weight: 600; color: #0f172a;")
        return lbl




class CustomAlertDialog(QDialog):
    def __init__(self, title_text: str, message_text: str, parent=None):
        super().__init__(parent)
        self.setWindowTitle(title_text)
        self.setMinimumWidth(280)
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(14, 14, 14, 14)
        layout.setSpacing(10)
        
        lbl_title = QLabel(title_text)
        lbl_title.setStyleSheet("font-size: 14px; font-weight: bold; color: #0f172a;")
        layout.addWidget(lbl_title)
        
        lbl_msg = QLabel(message_text)
        lbl_msg.setWordWrap(True)
        lbl_msg.setStyleSheet("color: #475569; font-size: 11px; line-height: 1.3;")
        layout.addWidget(lbl_msg)
        
        btn_ok = QPushButton("OK")
        btn_ok.setStyleSheet("background-color: #2563eb; color: #ffffff; font-weight: bold; border-radius: 6px; padding: 6px 12px;")
        btn_ok.clicked.connect(self.accept)
        layout.addWidget(btn_ok)




class UpdateStatusDialog(QDialog):
    def __init__(self, order_id: str, current_status: str = "Pending", parent=None):
        super().__init__(parent)
        self.setWindowTitle(f"Update Order {order_id}")
        self.setMinimumWidth(300)
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(14, 14, 14, 14)
        layout.setSpacing(10)
        
        title = QLabel(f"Order #{order_id}")
        title.setStyleSheet("font-size: 14px; font-weight: bold; color: #0f172a;")
        layout.addWidget(title)
        
        form = QFormLayout()
        lbl_status = QLabel("Set Status:")
        lbl_status.setStyleSheet("font-size: 11px; font-weight: 600; color: #64748b;")
        
        self.combo_status = QComboBox()
        self.combo_status.addItems(["Pending", "Printing", "Ready for Pickup", "Completed", "Cancelled"])
        self.combo_status.setCurrentText(current_status)
        self.combo_status.setStyleSheet("background-color: #ffffff; color: #0f172a; padding: 5px; border: 1px solid #cbd5e1; border-radius: 6px; font-size: 11px;")
        
        form.addRow(lbl_status, self.combo_status)
        layout.addLayout(form)
        
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(8)
        
        btn_cancel = QPushButton("Cancel")
        btn_cancel.setStyleSheet("background-color: #f1f5f9; color: #475569; font-weight: 600; border-radius: 6px; padding: 6px 12px;")
        btn_cancel.clicked.connect(self.reject)
        
        btn_save = QPushButton("Save")
        btn_save.setStyleSheet("background-color: #2563eb; color: #ffffff; font-weight: bold; border-radius: 6px; padding: 6px 12px;")
        btn_save.clicked.connect(self.accept)
        
        btn_layout.addWidget(btn_cancel)
        btn_layout.addWidget(btn_save)
        layout.addLayout(btn_layout)


    def get_selected_status(self) -> str:
        return self.combo_status.currentText()