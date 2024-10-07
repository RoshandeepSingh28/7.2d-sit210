import speech_recognition as sr
import RPi.GPIO as GPIO
from gtts import gTTS
import os
import time
import tkinter as tk
from tkinter import Label

# Set up GPIO
GPIO.setmode(GPIO.BCM)
LIGHT_PIN = 18
GPIO.setup(LIGHT_PIN, GPIO.OUT)

# Initialize GUI window
root = tk.Tk()
root.title("Smart Light Controller")
root.geometry("400x300")

# Light status label
light_status_label = Label(root, text="Light is OFF", font=("Helvetica", 16))
light_status_label.pack(pady=20)

def speak(text):
    tts = gTTS(text=text, lang='en')
    filename = "voice.mp3"
    tts.save(filename)
    os.system(f"mpg321 {filename}")

def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Please say 'ON' or 'OFF'")
        audio = recognizer.listen(source)
        try:
            command = recognizer.recognize_google(audio).upper()
            print(f"You said: {command}")
            return command
        except sr.UnknownValueError:
            print("Sorry, I did not understand that.")
            return None
        except sr.RequestError:
            print("Could not request results from Google Speech Recognition service.")
            return None

def update_light_status():
    """Function to update the light status label based on GPIO state."""
    if GPIO.input(LIGHT_PIN):
        light_status_label.config(text="Light is ON")
    else:
        light_status_label.config(text="Light is OFF")

def start_voice_command():
    """Triggered when 'Voice Command' button is clicked."""
    command = listen()
    if command == "ON":
        GPIO.output(LIGHT_PIN, GPIO.HIGH)
        speak("Light turned ON")
        light_status_label.config(text="Light is ON")
    elif command == "OFF":
        GPIO.output(LIGHT_PIN, GPIO.LOW)
        speak("Light turned OFF")
        light_status_label.config(text="Light is OFF")

# Button to start voice command
voice_button = tk.Button(root, text="Voice Command", command=start_voice_command, font=("Helvetica", 14), width=15)
voice_button.pack(pady=20)

# Exit button
exit_button = tk.Button(root, text="Exit", command=root.quit, font=("Helvetica", 14), width=10)
exit_button.pack(pady=20)

# Start the GUI loop
root.mainloop()

# Cleanup GPIO when exiting
GPIO.cleanup()
