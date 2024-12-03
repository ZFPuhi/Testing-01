import pyautogui
import pygetwindow as gw
import time

def list_open_windows():
    titles = gw.getAllTitles()
    for i, title in enumerate(titles):
        print(f"{i + 1}: {title}")
    return titles

def select_window(titles):
    while True:
        try:
            selection = int(input("Select the number corresponding to the target window: "))
            if 1 <= selection <= len(titles):
                selected_title = titles[selection - 1]
                print(f"You selected: {selected_title}")
                return selected_title
            else:
                print("Invalid selection. Please select a valid number.")
        except ValueError:
            print("Invalid input. Please enter a number.")

def confirm_selection(title):
    while True:
        confirmation = input(f"Is '{title}' the correct program? (yes/no): ").strip().lower()
        if confirmation in ['yes', 'y']:
            return True
        elif confirmation in ['no', 'n']:
            return False
        else:
            print("Please enter 'yes', 'y', 'no', or 'n'.")

# Function to get the center of the window
def get_window_center(window):
    left, top, right, bottom = window.left, window.top, window.right, window.bottom
    center_x = left + (right - left) // 2
    center_y = top + (bottom - top) // 2
    return center_x, center_y

# Main function to perform the click
def perform_click(selected_title):
    click_count = 0
    while True:
        # Find the window by title
        windows = gw.getWindowsWithTitle(selected_title)
        if windows:
            window = windows[0]

            # Bring the window to the foreground
            window.restore()
            window.activate()
            time.sleep(1)  # Wait a bit to ensure the window is in the foreground

            # Locate the reference image and click on it
            try:
                # Adding confidence parameter for better matching
                location = pyautogui.locateCenterOnScreen('reference.png', confidence=0.8)
                if location:
                    pyautogui.click(location.x, location.y)
                    click_count += 1
                    print(f"Click {click_count} sent to '{selected_title}' at ({location.x}, {location.y})")
                else:
                    print("Reference image not found on screen.")
            except Exception as e:
                print(f"An error occurred: {e}")

            # Minimize the window again (optional)
            window.minimize()

        # Wait for 30 seconds before the next click
        time.sleep(30)

# Run the main function
if __name__ == "__main__":
    print("Looking for the 'Banana' program...")

    banana_window = None
    all_titles = list_open_windows()

    for title in all_titles:
        if 'Banana' in title:
            banana_window = title
            break

    if banana_window and confirm_selection(banana_window):
        perform_click(banana_window)
    else:
        print("Listing all open windows:")
        selected_title = select_window(all_titles)
        perform_click(selected_title)
