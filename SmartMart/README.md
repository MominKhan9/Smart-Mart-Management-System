# Smart Mart Management System

A desktop application for managing a retail store with admin and cashier roles.

## Features

- **Admin Panel**:
  - Manage cashiers (add, update, delete)
  - Manage product categories and products
  - Control product inventory

- **Cashier Panel**:
  - Browse products by category
  - Add products to cart
  - Process payments (cash or card with 10% discount)
  - Generate bills

## Architecture

This application is built using the MVC (Model-View-Controller) architecture:

- **Models**: Handle data operations and file I/O
- **Views**: Implement the GUI using Tkinter
- **Controllers**: Contain business logic

## Installation

### Requirements

- Python 3.6 or higher
- Tkinter (usually comes with Python)

### Steps

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/smart-mart.git
   cd smart-mart
   ```

2. Install required packages:
   ```
   pip install -r requirements.txt
   ```

3. Run the application:
   ```
   python SmartMart/main.py
   ```

## Default Login Credentials

### Admin
- Username: admin
- Password: admin123

### Cashiers
- Username: cashier1, Password: pass123
- Username: cashier2, Password: pass456
- Username: cashier3, Password: pass789

## Running Tests

Run the test suite using pytest:
```
pytest SmartMart/tests/
```

## Building Executable

To create a standalone executable:
```
pyinstaller --onefile --windowed SmartMart/main.py
```

The executable will be created in the `dist` directory.

## Project Structure

```
SmartMart/
├── models/           # Data models
├── views/            # UI components
├── controllers/      # Business logic
├── data/             # Data files
├── tests/            # Unit tests
├── main.py           # Application entry point
└── requirements.txt  # Dependencies
```

## License

[MIT License](LICENSE) 