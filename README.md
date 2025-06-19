===============================
Movie Ticket Booking System 🎟️
===============================

📌 DESCRIPTION
--------------
This is a desktop-based Cinema Ticket Booking System built using **Python** and **Tkinter** for the graphical user interface, and **SQLite** as the backend database. The system simulates multiple users selecting halls and booking movie seats in real time.

It provides a simple but functional representation of a booking system where:
- Users choose a cinema hall.
- Available seats are displayed.
- Users can book a seat if it hasn’t already been taken.

This application is a great introduction to GUI programming, database integration, and handling concurrency using threads in Python.

🚀 FEATURES
-----------
✔️ Simple graphical interface using Tkinter  
✔️ Displays available cinema halls and number of seats  
✔️ Real-time seat availability tracking  
✔️ Prevents double booking using thread locks  
✔️ Multi-user simulation with dynamic window creation  
✔️ Booking confirmation and error alerts using pop-up messages  
✔️ Auto-creation and initialization of a SQLite database  
✔️ Sample data insertion for quick setup

⚠️ REQUIREMENTS
---------------
Before running the program, ensure that:
1. You have **Python 3.x** installed on your machine.
2. The **Tkinter** library is installed (comes by default with most Python installations).
3. Your system supports **SQLite** (comes built-in with Python).
4. Any antivirus or system restrictions that block file-based databases are disabled.

🗃️ NOTE:
--------
This program **uses a database (SQLite)** to store hall and booking information.
You **must allow the program to create and write to a file** named:
    `movie_booking_system.db`

If your environment blocks database creation (like some online IDEs or restricted OS setups), the program will not work correctly.

📦 HOW TO RUN
-------------
1. Download or clone this repository.
2. Make sure all files are in the same folder.
3. Open a terminal or command prompt in that folder.
4. Run the app with:
    ```bash
    python your_filename.py
    ```
5. Enter the number of users (simulated), and enjoy the booking interface.

📁 FILES
--------
- `your_filename.py`  — main Python script
- `movie_booking_system.db` — SQLite database (auto-created)

👨‍💻 AUTHOR
-----------
Developed by [Your Name]
Feel free to customize, expand, or improve the project!
