from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pytest

# Define a function to start the Dash app
def start_dash_app():
    from app import app  # Replace 'your_dash_app_file' with the name of your Dash app file
    app.run_server(port=8050, debug=False)  # Run the Dash app on a specific port

# Define test functions for each condition
def test_header_present():
    driver = webdriver.Chrome()  # Initialize the Chrome WebDriver
    driver.get('http://localhost:8050')  # Open the Dash app in the WebDriver
    time.sleep(1)  # Wait for the page to load

    # Find the header element and assert its presence and text
    header = driver.find_element(By.ID, 'header')
    assert header.text == 'MORSEL SALES REPORT'

    driver.quit()  # Close the WebDriver

def test_visualization_present():
    driver = webdriver.Chrome()
    driver.get('http://localhost:8050')
    time.sleep(1)

    # Find the visualization element and assert its presence
    visualization = driver.find_element(By.ID, 'pink-morsel-line')
    assert visualization.tag_name == 'div'

    driver.quit()

def test_region_picker_present():
    driver = webdriver.Chrome()
    driver.get('http://localhost:8050')
    time.sleep(1)

    # Find the region picker element and assert its presence
    region_picker = driver.find_element(By.ID, 'Region')
    assert region_picker.tag_name == 'div'

    driver.quit()

# Run the tests
if __name__ == '__main__':
    start_dash_app()  # Start the Dash app
    pytest.main([__file__, '-v'])  # Run the tests
