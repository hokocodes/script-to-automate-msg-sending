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

message_text = """Message from Tina Agency of Texas, your tax return was rejected.
\n\n
来自德克萨斯州 Tina 机构的消息：您的报税申请已被拒绝。
\n\n
Tin nhắn từ Tina Agency Texas: Hồ sơ khai thuế của bạn đã bị từ chối.
\n\n
Reject Code:\n
Please verify your full legal name (as on your Social Security card) OR your SSN so we can fix and resubmit your return."""
failed_clients = []

for index, row in df.iterrows():
    phone = str(row['Phone'])
    client = row.get('Client', row.get('Name', 'Unknown'))

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
        message_box.send_keys(message_text)

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
