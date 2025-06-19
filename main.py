import tkinter as tk
from tkinter import messagebox
import threading
import sqlite3

# Database Initialization
def initialize_database():
    """Initialize the database with tables and sample data."""
    conn = sqlite3.connect('movie_booking_system.db')
    cursor = conn.cursor()

    # Create halls table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS halls (
        hall_id INTEGER PRIMARY KEY AUTOINCREMENT,
        hall_name TEXT UNIQUE NOT NULL,
        total_seats INTEGER NOT NULL
    )
    ''')

    # Create bookings table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS bookings (
        booking_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_name TEXT NOT NULL,
        hall_id INTEGER NOT NULL,
        seat_number INTEGER NOT NULL,
        FOREIGN KEY (hall_id) REFERENCES halls(hall_id)
    )
    ''')

    # Insert sample halls if not already present
    cursor.execute('SELECT COUNT(*) FROM halls')
    if cursor.fetchone()[0] == 0:
        cursor.executemany('INSERT INTO halls (hall_name, total_seats) VALUES (?, ?)', [
            ('Hall A', 10),
            ('Hall B', 15),
            ('Hall C', 20)
        ])

    conn.commit()
    conn.close()

# Movie Booking System Class
class MovieBookingSystem:
    def __init__(self, master, num_users):
        self.master = master
        self.num_users = num_users

        # Lock to prevent double-booking
        self.lock = threading.Lock()

        # Start threads for user booking windows
        self.create_user_threads()

    def create_user_threads(self):
        """Create threads for each user and start them."""
        for user_num in range(self.num_users):
            threading.Thread(target=self.show_halls, args=(user_num + 1,)).start()

    def show_halls(self, user_num):
        """Display the available halls and allow booking."""
        user_window = tk.Toplevel(self.master)
        user_window.title(f"User {user_num} - Select a Hall")
        user_window.geometry("600x400")

        halls = self.get_halls_from_db()

        for i, hall in enumerate(halls):
            hall_name = hall[0]
            total_seats = hall[1]
            hall_button = tk.Button(user_window, text=f"{hall_name} - {total_seats} Seats",
                                    command=lambda i=i: self.show_seats(user_num, halls[i], user_window))
            hall_button.grid(row=i, column=0, padx=10, pady=10, sticky="w")

    def show_seats(self, user_num, hall, user_window):
        """Show the seats for a selected hall, indicating booked seats."""
        hall_name, total_seats = hall
        hall_window = tk.Toplevel(user_window)
        hall_window.title(f"User {user_num} - {hall_name}")
        hall_window.geometry("600x400")

        # Get booked seats from the database
        booked_seats = self.get_booked_seats(hall_name)

        for seat in range(1, total_seats + 1):
            if seat in booked_seats:
                seat_button = tk.Button(hall_window, text=f"Seat {seat} - Booked",
                                        state=tk.DISABLED, bg="red", fg="white")
            else:
                seat_button = tk.Button(hall_window, text=f"Seat {seat}",
                                        command=lambda seat=seat: self.book_ticket(user_num, hall, seat, hall_window))
            seat_button.grid(row=(seat - 1) // 5, column=(seat - 1) % 5, padx=5, pady=5)

    def get_booked_seats(self, hall_name):
        """Fetch the list of booked seats for a specific hall."""
        conn = sqlite3.connect('movie_booking_system.db')
        cursor = conn.cursor()

        # Get the hall_id for the hall_name
        cursor.execute('SELECT hall_id FROM halls WHERE hall_name = ?', (hall_name,))
        result = cursor.fetchone()
        if not result:
            conn.close()
            return []

        hall_id = result[0]

        # Get all booked seat numbers for the hall
        cursor.execute('SELECT seat_number FROM bookings WHERE hall_id = ?', (hall_id,))
        booked_seats = [row[0] for row in cursor.fetchall()]

        conn.close()
        return booked_seats

    def book_ticket(self, user_num, hall, seat, hall_window):
        """Attempt to book the seat."""
        with self.lock:
            hall_name, _ = hall

            success = self.insert_booking_into_db(user_num, hall_name, seat)

            if success:
                messagebox.showinfo("Booking Successful", f"User {user_num} successfully booked seat {seat} in {hall_name}!")
                hall_window.destroy()
            else:
                messagebox.showerror("Booking Failed", "Seat already booked or invalid. Please try another.")

    def insert_booking_into_db(self, user_num, hall_name, seat_number):
        """Insert the booking information into the database."""
        try:
            conn = sqlite3.connect('movie_booking_system.db')
            cursor = conn.cursor()

            # Ensure the hall exists and seat is available
            cursor.execute('SELECT hall_id FROM halls WHERE hall_name = ?', (hall_name,))
            result = cursor.fetchone()
            if not result:
                conn.close()
                return False

            hall_id = result[0]

            # Check if the seat is already booked
            cursor.execute('SELECT 1 FROM bookings WHERE hall_id = ? AND seat_number = ?', (hall_id, seat_number))
            if cursor.fetchone():
                conn.close()
                return False

            # Insert the booking
            cursor.execute('INSERT INTO bookings (user_name, hall_id, seat_number) VALUES (?, ?, ?)',
                           (f"User {user_num}", hall_id, seat_number))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print("Error inserting booking:", e)
            return False

    def get_halls_from_db(self):
        """Get available halls from the database."""
        conn = sqlite3.connect('movie_booking_system.db')
        cursor = conn.cursor()

        cursor.execute('SELECT hall_name, total_seats FROM halls')
        halls = cursor.fetchall()

        conn.close()
        return halls

# Main Function
def start_booking_system():
    try:
        num_users = int(user_input.get())
        if num_users > 0:
            MovieBookingSystem(root, num_users)
        else:
            messagebox.showerror("Invalid Input", "Number of users must be greater than 0.")
    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter a valid number.")

# Initialize the database
initialize_database()

# Create main input window
root = tk.Tk()
root.title("Movie Ticket Booking System")
root.geometry("400x200")

tk.Label(root, text="Enter Number of Users:").pack(pady=10)
user_input = tk.Entry(root)
user_input.pack(pady=10)

start_button = tk.Button(root, text="Start Booking", command=start_booking_system)
start_button.pack(pady=10)

root.mainloop()