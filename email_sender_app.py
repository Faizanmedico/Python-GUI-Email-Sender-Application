
import tkinter as tk
from tkinter import messagebox, simpledialog
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import ssl # For explicit context creation (optional, but good practice)

# --- Configuration (Gmail example) ---
# You might need to change this if you're using a different email provider
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587 # TLS port

class EmailSenderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Python Email Sender")
        self.root.geometry("600x650")
        self.root.resizable(False, False)
        self.root.config(bg="#e0f7fa") # Light blue-green background

        self.create_widgets()

    def create_widgets(self):
        # Frame for input fields
        input_frame = tk.Frame(self.root, bg="#ffffff", padx=20, pady=20, bd=2, relief="groove")
        input_frame.pack(pady=30, padx=30, fill="both", expand=True)

        # Title
        tk.Label(input_frame, text="Send Email", font=("Arial", 24, "bold"), fg="#4a148c", bg="white").pack(pady=10)

        # Sender Email
        tk.Label(input_frame, text="Your Email:", font=("Arial", 12), bg="white").pack(anchor="w", pady=(10, 0))
        self.sender_email_entry = tk.Entry(input_frame, width=50, font=("Arial", 12), bd=1, relief="solid")
        self.sender_email_entry.pack(pady=5, ipadx=5, ipady=5)
        # Optional: Pre-fill for convenience during testing
        # self.sender_email_entry.insert(0, "your_email@example.com") # REMEMBER TO REMOVE FOR PRODUCTION!

        # Recipient Email
        tk.Label(input_frame, text="Recipient Email:", font=("Arial", 12), bg="white").pack(anchor="w", pady=(10, 0))
        self.recipient_email_entry = tk.Entry(input_frame, width=50, font=("Arial", 12), bd=1, relief="solid")
        self.recipient_email_entry.pack(pady=5, ipadx=5, ipady=5)

        # Subject
        tk.Label(input_frame, text="Subject:", font=("Arial", 12), bg="white").pack(anchor="w", pady=(10, 0))
        self.subject_entry = tk.Entry(input_frame, width=50, font=("Arial", 12), bd=1, relief="solid")
        self.subject_entry.pack(pady=5, ipadx=5, ipady=5)

        # Message
        tk.Label(input_frame, text="Message:", font=("Arial", 12), bg="white").pack(anchor="w", pady=(10, 0))
        self.message_text = tk.Text(input_frame, width=50, height=10, font=("Arial", 12), bd=1, relief="solid")
        self.message_text.pack(pady=5, ipadx=5, ipady=5)

        # Send Button
        self.send_button = tk.Button(input_frame, text="Send Email", command=self.send_email,
                                     font=("Arial", 14, "bold"), bg="#4CAF50", fg="white",
                                     padx=20, pady=10, relief="raised", cursor="hand2")
        self.send_button.pack(pady=20)

        # Status Label
        self.status_label = tk.Label(self.root, text="", font=("Arial", 10), bg="#e0f7fa", fg="#d32f2f")
        self.status_label.pack(pady=10)

    def send_email(self):
        sender_email = self.sender_email_entry.get()
        recipient_email = self.recipient_email_entry.get()
        subject = self.subject_entry.get()
        message_body = self.message_text.get("1.0", tk.END).strip() # Get text from Text widget

        # --- Input Validation ---
        if not sender_email or not recipient_email or not subject or not message_body:
            messagebox.showerror("Error", "All fields are required!")
            self.status_label.config(text="Please fill in all fields.")
            return

        # Prompt for password securely
        # This will show a separate dialog for the password
        sender_password = simpledialog.askstring("Password", "Enter your email password (App Password for Gmail):", show='*')
        if not sender_password:
            self.status_label.config(text="Email sending cancelled. Password not provided.")
            return

        self.status_label.config(text="Attempting to send email...")
        self.root.update_idletasks() # Update GUI immediately to show status

        try:
            # Create a multipart message and set headers
            msg = MIMEMultipart()
            msg['From'] = sender_email
            msg['To'] = recipient_email
            msg['Subject'] = subject

            # Add body to email
            msg.attach(MIMEText(message_body, 'plain'))

            # Create a default SSL context for security
            context = ssl.create_default_context()

            # Connect to the SMTP server
            # Use smtplib.SMTP_SSL for port 465 (SMTPS) or smtplib.SMTP for port 587 (TLS)
            with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
                server.starttls(context=context) # Secure the connection with TLS
                server.login(sender_email, sender_password)
                server.send_message(msg)

            messagebox.showinfo("Success", "Email sent successfully!")
            self.status_label.config(text="Email sent successfully!")

            # Clear recipient, subject, and message fields after successful send
            self.recipient_email_entry.delete(0, tk.END)
            self.subject_entry.delete(0, tk.END)
            self.message_text.delete("1.0", tk.END)
            # self.sender_email_entry.delete(0, tk.END) # Option to clear sender too

        except smtplib.SMTPAuthenticationError:
            messagebox.showerror("Authentication Error",
                                 "Failed to log in. Please check your email and password (or App Password for Gmail if 2FA is on).")
            self.status_label.config(text="Authentication failed.")
        except smtplib.SMTPConnectError:
            messagebox.showerror("Connection Error",
                                 "Could not connect to the SMTP server. Check your internet connection or server settings.")
            self.status_label.config(text="Connection error.")
        except smtplib.SMTPServerDisconnected:
            messagebox.showerror("Server Disconnected",
                                 "The SMTP server unexpectedly disconnected. Try again.")
            self.status_label.config(text="Server disconnected.")
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred:\n{e}")
            self.status_label.config(text=f"Error: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = EmailSenderApp(root)
    root.mainloop()