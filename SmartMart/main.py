import os
import sys
import tkinter as tk
from views.login_view import LoginView

def main():
    """Main function to start the application"""
    # Create the main window
    root = tk.Tk()
    
    # Set application icon if available
    try:
        # You can add an icon file in your project
        # root.iconbitmap('icon.ico')
        pass
    except:
        pass
    
    # Initialize the login view
    app = LoginView(root)
    
    # Start the application main loop
    root.mainloop()

if __name__ == "__main__":
    # Add the project root directory to the Python path
    current_dir = os.path.dirname(os.path.abspath(__file__))
    if current_dir not in sys.path:
        sys.path.append(current_dir)
    
    # Start the application
    main() 