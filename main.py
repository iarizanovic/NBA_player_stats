import os
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select

# Get the current date
start_time = datetime.now()
t = start_time.strftime("%Y-%m-%d")  # 2024-03-20

# Find path which doesn't exist
path = f"nba_stat_{t}.csv"
if os.path.exists(path):
    suffix = 1
    while True:
        path = f"nba_stat_{t}_{suffix}.csv"
        if os.path.exists(path):
            suffix += 1
        else:
            break

# Init the file
file = open(path, mode="a", encoding='utf-8')

# Init the selenium
driver = webdriver.Chrome()
driver.get("https://www.nba.com/stats/players/traditional?PerMode=Totals&sort=PTS&dir=-1")
driver.maximize_window()

# Select all players
sel = driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[2]/div[3]/section[2]/div/div[2]/div[2]/div[1]/div[3]/div/label/div/select')
select = Select(sel)
select.select_by_visible_text('All')

# Get the header
header = driver.find_elements(By.XPATH, f'/html/body/div[1]/div[2]/div[2]/div[3]/section[2]/div/div[2]/div[3]/table/thead/tr/th')
data = "index,"
for cell in header:
    long_name = cell.get_attribute('title')
    short_name = cell.text

    # Use long header name if exists
    if len(long_name) > 1:
        data += long_name + ","
    elif len(short_name) > 1:
        data += short_name + ","
    else:
        continue

# Add header in CSV file
file.write(data[:-1] + '\n')

# Get the values
index = 0
while True:
    index += 1
    row = driver.find_elements(By.XPATH, f'/html/body/div[1]/div[2]/div[2]/div[3]/section[2]/div/div[2]/div[3]/table/tbody/tr[{index}]/td')

    # Break if row with specified index doesn't exist
    if not row:
        break

    # Join the values
    data = ""
    for cell in row:
        data += cell.text + ","

    # Add row in CSV file
    file.write(data[:-1] + '\n')

# CLose the file
file.close()

# Print the execution time
print("Execution time:", datetime.now() - start_time)  # Execution time: 0:00:08.309267
