# Free Open Source Hydratation Notification Script
Made it so that I can stay Hydrated when working hard on projects.

<p><h2>How to automatically start the script on Windows.</p></h2>

Steps Required:
<p>1. Press Win + R to open the Run dialog.</p>
<p>2. Type shell:startup and press Enter. This will open the Startup folder.</p>
<p>3. Create a shortcut to your Python script in this folder. Right-click on the script, select "Create shortcut," and then drag the shortcut into the Startup folder.</p>

<p><h2>How to automatically start the script on MacOS.</p></h2>

Steps Required:
<p>1. Open System Preferences and go to Users & Groups.</p>
<p>2. Select your user account and go to the "Login Items" tab.</p>
<p>3. Click the "+" button and add your Python script to the list.</p>

<p><h2>How to automatically start the script on Linux.</p></h2>

Steps Required:
<p>1. Open a terminal.</p>
<p>2. Type crontab -e and press Enter. This will open the crontab file in your default text editor (usually Nano).</p>
<p>3. At the bottom of the file, add a line to execute your script at boot. For example:<br>
@reboot /path/to/python /path/to/your/script.py
<br>Replace /path/to/python with the path to your Python interpreter and /path/to/your/script.py with the path to your script.</p>
<p>4. Save and exit the crontab file. In Nano, you can do this by pressing Ctrl + X, then Y to confirm, and then `Enter`.</p>

## If you encounter any issues such as ModuleNotFoundError: No module named 'plyer':
<p>In such cases you should simply run `pip install plyer`</p>