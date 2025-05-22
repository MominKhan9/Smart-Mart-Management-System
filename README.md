# 🛒 Smart Mart Management System

A desktop-based retail management system built with **Python** and **Tkinter** using the **MVC architecture**. This project supports both **Admin** and **Cashier** roles with separate interfaces and file-based data storage.

---

## 📌 Project Overview

Smart Mart is a GUI-based mini retail system that allows an admin to manage products and cashiers, and enables cashiers to handle billing and payments. The system is designed with a clean, modular architecture and stores all data in `.txt` files for simplicity.

---

## 🚀 Features

### 🔐 Admin Panel
- Hardcoded login from `admin.txt`
- Manage 5 product categories (with at least 10 products each)
- Add, update, and delete cashier accounts
- View existing cashiers
- Manage product stock

### 💼 Cashier Panel
- Login using credentials from `cashiers.txt`
- Browse categories and add products to cart
- Generate bills with two payment methods:
  - **Cash**: no discount
  - **Card**: 10% discount applied
- Save paid bill totals to `bills.txt` (e.g., `Bill 1: 2500`)

---

## 🧱 Project Structure (MVC)

SmartMart/
├── models/ # Data handling and file I/O
├── views/ # Tkinter GUI components
├── controllers/ # Business logic and coordination
├── data/ # .txt files for data storage
├── tests/ # Unit tests (PyTest)
├── main.py # Entry point
└── README.md


---

## 💾 Data Files

| File Name     | Purpose                          |
|---------------|----------------------------------|
| `admin.txt`   | Stores hardcoded admin login     |
| `cashiers.txt`| List of cashier accounts         |
| `products.txt`| Categories and product inventory |
| `bills.txt`   | Final total of each bill         |

---

## ⚙️ Technologies Used

- **Python 3**
- **Tkinter** (for GUI)
- **PyTest** (for unit testing)
- **PyInstaller** (to create `.exe` file)
- **PlantUML** (for UML diagrams)
- **draw.io / GanttProject** (planning visuals)

---

## 🧪 Testing

- Unit tests written using **PyTest**
- Covers file I/O, billing logic, and login validation
- All test results available in `/tests`

---

## 📦 Deployment

- Packaged into a `.exe` file using **PyInstaller**
- Run the application via:
  ```bash
  python main.py
