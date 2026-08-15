import pandas as pd
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

csvInput = input("Enter the path to the CSV file: ")

# Load CSV
df = pd.read_csv(csvInput)

# Open Chrome
driver = webdriver.Chrome()
driver.get("https://messages.google.com/web/")

input("Scan QR code and press ENTER...")


failed_clients = []

for index, row in df.iterrows():
    phone = input(f"Enter the column name for phone number in the CSV file for client '{row.get('Client', row.get('Name', 'Unknown'))}': ")
    client = input(f"Enter the column name for client name in the CSV file for client '{row.get('Client', row.get('Name', 'Unknown'))}': ")

    try:
        # Click Start Chat
        driver.get("https://messages.google.com/web/conversations/new")
        time.sleep(3)

        # Enter phone number
        input_box = driver.find_element(By.TAG_NAME, "input")
        input_box.send_keys(phone)
        time.sleep(2)
        input_box.send_keys(Keys.ENTER)

        time.sleep(2)

        # Enter message
        message_box = driver.find_element(By.TAG_NAME, "textarea")
       
        # Ask user for message, use default if left blank, ensure formatting is correct
        user_message = input("Enter the message to send: ")
        

        for i, line in enumerate(user_message.split('\n')):
            if i > 0:
                message_box.send_keys(Keys.SHIFT, Keys.ENTER)
            message_box.send_keys(line)
 

        # Send message
        message_box.send_keys(Keys.ENTER)

        print(f"Sent to {client} ({phone})")
    except Exception as e:
        print(f"Failed to send to {client} ({phone}): {e}")
        failed_clients.append({
            "Client": client,
            "Phone": phone,
            "Error": str(e),
        })

    time.sleep(8)  # delay to avoid spam detection

if failed_clients:
    failed_df = pd.DataFrame(failed_clients)
    failed_df.to_csv("failed_clients.csv", index=False)
    print(f"Saved {len(failed_clients)} failed sends to failed_clients.csv")
else:
    print("No failed sends.")
