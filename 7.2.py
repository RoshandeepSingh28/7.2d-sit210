import speech_recognition as sr
import RPi.GPIO as GPIO
import time

# Setup for GPIO and LED control
LED_PIN = 18  # Replace with your LED-connected GPIO pin
GPIO.setmode(GPIO.BCM)  # Set the GPIO mode to BCM
GPIO.setup(LED_PIN, GPIO.OUT)  # Set the LED pin as output

def turn_led_on():
  
    GPIO.output(LED_PIN, GPIO.HIGH)  # Set the GPIO pin HIGH to turn the LED on
    print("LED is now ON.")
    time.sleep(0.5)  # Debounce time to avoid multiple triggers

def turn_led_off():
    """Turn the LED OFF."""
    GPIO.output(LED_PIN, GPIO.LOW)  # Set the GPIO pin LOW to turn the LED off
    print("LED is now OFF.")
    time.sleep(0.5)  # Debounce time to avoid multiple triggers

def listen_for_voice_command():
   
    recognizer = sr.Recognizer()  # Initialize the speech recognizer
    microphone = sr.Microphone()  # Initialize the microphone for input

    try:
        with microphone as source:
            print("Adjusting for background noise... Please wait.")
            recognizer.adjust_for_ambient_noise(source)  # Adjust for background noise
            print("Listening for a voice command...")
            audio_input = recognizer.listen(source)  # Capture audio input

            # Recognize speech using Google Speech Recognition and convert to lowercase
            voice_command = recognizer.recognize_google(audio_input).lower()
            print(f"Voice command received: {voice_command}")
            return voice_command

    except sr.UnknownValueError:
        # Handle case where the audio is unintelligible
        print("Sorry, I could not understand the audio.")
    except sr.RequestError:
        # Handle case where the Google API request fails
        print("Could not request results from the speech recognition service.")
    return ""  # Return an empty string if recognition fails

def handle_command(command):
    
    print(f"Processing command: {command}")

    if "light on" in command or "turn on" in command:
        print("Command recognized: Turn LED ON")
        turn_led_on()  # Call the function to turn the LED on
    elif "light off" in command or "turn off" in command:
        print("Command recognized: Turn LED OFF")
        turn_led_off()  # Call the function to turn the LED off
    else:
        # Handle unrecognized commands
        print("Command not recognized. Please say 'light on' or 'light off'.")

if __name__ == "__main__":
    try:
        # Continuous loop to listen for voice commands
        while True:
            voice_command = listen_for_voice_command()  # Listen for a voice command
            if voice_command:  # If a valid command is detected, process it
                handle_command(voice_command)
            time.sleep(1)  # Sleep briefly between commands

    except KeyboardInterrupt:
        # Handle program exit gracefully when interrupted (Ctrl + C)
        print("Exiting program...")

    finally:
        # Cleanup GPIO resources when the program terminates
        GPIO.cleanup()
