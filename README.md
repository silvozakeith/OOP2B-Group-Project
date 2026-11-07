# PrintSync

PrintSync is a desktop order management application built with Python and PyQt6. It provides an order submission interface, live price calculator, job status tracker, and rate configuration panel.

## File Structure

- `main.py` - Application entry point and window container.
- `user_screen.py` - Order entry form, specification selectors, and price calculation panel.
- `admin_screen.py` - Order management queue dashboard and base pricing editor.
- `dialogs.py` - Custom dialog windows for order confirmations, alerts, and status changes.
- `data_manager.py` - Data persistence layer for order histories and rate rules.
- `style.qss` - Application-wide QSS stylesheet.

## 🛠️ Tech Stack

- **Language:** Python 3.x
- **GUI Framework:** PyQt6 (Qt Style Sheets)
- **Storage Layer:** Local File Persistence (`data_manager.py`)
- **Binary Packager:** PyInstaller

## 👨‍💻 Author & Course Info

* **Developer:** Keith Nicole B. Silvoza (CPE21S4)
* **Course:** CPE 009B - Object-Oriented Programming 2
* **Instructor:** Engr. Jimlord M. Quejado
* **Institution:** Technological Institute of the Philippines (TIP) - Quezon City[cite: 8, 22]
