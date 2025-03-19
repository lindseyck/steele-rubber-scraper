from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# Set up Chrome WebDriver using WebDriver Manager
options = Options()
options.add_argument("--headless")  # Run in headless mode for efficiency
options.add_argument("--disable-gpu")  # Helps in some headless environments
options.add_argument("--no-sandbox")  # Helps in some environments
options.add_argument("--disable-dev-shm-usage")  # Prevents crashes in Docker/Linux

# Automatically install the correct ChromeDriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

# Navigate to the page
url = "https://www.steelerubber.com/automotive"
driver.get(url)

# Wait for the dropdown to load completely
try:
    wait = WebDriverWait(driver, 10)  # Wait up to 10 seconds
    select_element = wait.until(EC.presence_of_element_located((By.NAME, "make")))
    
    # Once loaded, get all option elements
    make_elements = select_element.find_elements(By.TAG_NAME, "option")

    # Extract text from the elements (skip the first element if it's a placeholder)
    makes = [make.text.strip() for make in make_elements if make.text.strip().lower() != "make"]

    # Replace space with hyphen
    def replace_space_with_hyphen(string_list):
        return [string.replace(" ", "-") for string in string_list]
    
    makes = replace_space_with_hyphen(makes)

    # Drop "Select-Make"
    makes = [make for make in makes if make != "Select-Make"]

    # Print the list of makes
    print(makes)

finally:
    # Close the driver
    driver.quit()
