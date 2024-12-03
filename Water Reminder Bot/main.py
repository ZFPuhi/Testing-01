import time
import random
import pygame
import os
from plyer import notification

# Initialize pygame mixer
pygame.mixer.init()

# Define the list of regular messages
regular_messages = [
    "Remember to take a sip of water!",
    "Stay hydrated, folks!",
    "Don't forget to drink some water.",
    "Hydration is key to staying healthy!",
    "Keep a water bottle handy!",
    "Time for a water break!",
    "Water is essential for your body!",
    "Have you had your glass of water yet?",
    "Drink water to keep your energy up!",
    "Water is life. Drink up!"
]

# Define the list of funny messages
funny_messages = [
    "Water you waiting for? Hydrate now and be cooler than a cucumber!",
    "Sip happens! Keep calm and hydrate on.",
    "Don't be a shriveled raisin! Drink water and stay juicy.",
    "Hydration station, coming through! Grab a glass and join the party.",
    "Water: the original energy drink. Take a swig and power up!",
    "Don't let dehydration turn you into a wilted lettuce leaf. Drink up and stay crisp!",
    "H2-Oh yeah! Hydration is the key to unlocking your full potential.",
    "Stay hydrated, my friends. Because nobody likes a raisin with legs.",
    "Warning: Dehydration may lead to a case of the grumpies. Keep your spirits up with water!",
    "Hydrate like your life depends on it... because it kinda does! Stay hydrated, stay awesome."
]

def remind_to_drink_water():
    while True:
        # Randomly select a message
        message = random.choice(regular_messages + funny_messages)
        
        # Display the selected message
        notification.notify(
            title="Stay Hydrated!",
            message=message,
            app_name="Water Reminder",
            toast=True  # Display as a toast notification with an "Okay" button
        )
        
        # Play the sound
        play_sound("water.mp3")
        
        # Wait for an hour
        time.sleep(3600)  # 3600 seconds = 1 hour

def play_sound(sound_file):
    # Check if the sound file exists in the current directory
    if os.path.exists(sound_file):
        pygame.mixer.music.load(sound_file)
        pygame.mixer.music.play()
        # Wait for the sound to finish playing
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
    else:
        print("Sound file not found.")

if __name__ == "__main__":
    remind_to_drink_water()