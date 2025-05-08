from selenium import webdriver
from selenium.webdriver.common.by import By

# Configure Selenium WebDriver
driver = webdriver.Chrome()  # Ensure you have ChromeDriver installed
driver.get("https://www.breakingpoint.gg/match/93849/Atlanta-FaZe-vs-Carolina-Royal-Ravens-at-CDL-Minor-1-Tournament-2025")

# Wait for the content to load
driver.implicitly_wait(10)

print(driver.title)
table = driver.find_element(By.CLASS_NAME, "mantine-Table-table")  # Adjust based on class name

print(table)


rows = table.find_elements(By.TAG_NAME, "tr")


# Extract and print data
for row in rows:
    cells = row.find_elements(By.TAG_NAME, "td")  # Find all cells in the row
    data = [cell.text for cell in cells if cell.text.strip()]  # Extract text, ignoring empty cells
    if data:  # Only print rows with actual data
        print(data)
driver.quit()
