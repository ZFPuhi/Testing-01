import time
import random
from plyer import notification

# Define the list of messages
messages = [
    "Message 1: Remember to take a sip of water!",
    "Message 2: Stay hydrated, folks!",
    "Message 3: Don't forget to drink some water.",
    "Message 4: Hydration is key to staying healthy!",
    "Message 5: Keep a water bottle handy!",
    "Message 6: Time for a water break!",
    "Message 7: Water is essential for your body!",
    "Message 8: Have you had your glass of water yet?",
    "Message 9: Drink water to keep your energy up!",
    "Message 10: Water is life. Drink up!"
]

# Track the last displayed message index
last_message_index = -1

def remind_to_drink_water():
    global last_message_index
    
    while True:
        # Select a random message
        random_index = random.randint(0, len(messages) - 1)
        
        # Ensure the selected message is different from the last one
        while random_index == last_message_index:
            random_index = random.randint(0, len(messages) - 1)
        
        # Display the selected message
        notification.notify(
            title="Stay Hydrated!",
            message=messages[random_index],
            app_name="Water Reminder",
            toast=True  # Display as a toast notification with an "Okay" button
        )
        
        # Update the last displayed message index
        last_message_index = random_index
        
        # Wait for an hour
        time.sleep(3600)  # 3600 seconds = 1 hour

if __name__ == "__main__":
    remind_to_drink_water()
