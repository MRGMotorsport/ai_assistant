import os
import subprocess
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
import time


# Description: This function reads a text file and returns all lines in a list with \n written at the end of each entry
def read_txt_file(file_url):

    # Create the full file path by adding .txt

    file_path = os.path.join(file_url + r'.txt')

    # Open the file in write mode

    with open(file_path, 'r') as file:

        contents = file.readlines()

        return contents
    

def kill_edge():
    command = "taskkill /IM msedge.exe /F"
    # Run the command and capture the output
    process = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE)

def kill_ollamas():
    command = "taskkill /IM ollama_llama_server.exe /F"
    # Run the command and capture the output
    process = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE)

def llamas_response(search_query):
    
    # Adapt standalone function
    query = search_query
    query_b_string = query.encode('utf-8')

    # Define the command to run PowerShell and execute the Ollama command
    command = ['powershell', '-NoLogo', '-Command', 'ollama run llama3']

    # Run the command and capture the output
    process = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE)

    # Read the output from the process as a string
    output = process.communicate(input=query_b_string)[0].decode('utf-8').strip()

    return(output)




llamas_prompt = "Please take the following request and provide me with a simple search term for a search engine for the query. I will be using this phrase to google the issue, therefore can you only provide the search term with no more text to explain your reasoning"

llamas_phrase = input("Please type query here: ")

response = llamas_response(llamas_prompt + llamas_phrase)

response_coded = response.replace(" ","+")

print("\n" * 10)
print(response)
print(response_coded)

# Input things








    
# Specify the path to the EdgeDriver executable
edge_driver_path = r"c:\USER_PATH\msedgedriver.exe"

# Create a Service object for EdgeDriver
service = Service(edge_driver_path)

# Setup options to run headless
options = Options()
#options.add_argument("--headless=new")
options.add_argument("--disable-gpu")  # Disable GPU usage
options.add_argument("--no-sandbox")   # Bypass OS security model
options.add_argument("--disable-dev-shm-usage")  # Overcome limited resource problems
options.add_argument("--log-level=3")  # Suppress warnings and info messages

# Initialize the Edge WebDriver in headless mode
driver = webdriver.Edge(service=service, options=options)









# Navigate to the url (e.g., Google)
driver.get("https://www.bing.com/search?q=" + response_coded)


first_search_term = driver.find_element(By.CLASS_NAME , "b_algo")

"""link = first_search_term.find_element(By.TAG_NAME , "href")"""

print(first_search_term.text)

time.sleep(3)


# Locate the anchor ('a') tag within the <li> element by class name or other selectors
link_element = driver.find_element(By.CSS_SELECTOR, '.b_algo a.tilk')

# Scroll to element so can be clicked and close cookies
actions = ActionChains(driver)
actions.move_to_element(link_element).perform()
decline_cookies = driver.find_element(By.ID, "bnp_btn_reject")
decline_cookies.click()

# Click the link
link_element.click()
time.sleep(4)

# Get all info from website

# Extract the entire body content
body_element = driver.find_element(By.TAG_NAME, 'body')

# Get the inner HTML (content) of the body
body_html = body_element.text

kill_edge()

print("\n" * 10)

print(len(body_html))

compressed_text = ' '.join(body_html)

result = llamas_response("please summarise the following consider the users query was " + llamas_phrase + ":" + compressed_text)

kill_ollamas()
print(result)

