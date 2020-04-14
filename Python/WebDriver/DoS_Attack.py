from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

i = 1
options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument("use-fake-ui-for-media-stream")
driver = webdriver.Chrome("chromedriver.exe",chrome_options=options)
driver.set_window_size(800, 920)

def newDriver():
    #driver.get("https://127.0.0.1/tempurl/?aid=39woJnrTG&uid=session%s"%str(i))
    url = "https://127.0.0.1/tempurl/?aid=39woJnrTG&uid=session%s"%str(i)
    #url = "https://127.0.0.1/tempurl/?aid=39woJnrTG&uid=session%s"%"Test-W00D0001"
    driver.execute_script("window.open('%s','_blank');"%url)
    time.sleep(2)
    url = "https://127.0.0.1/tempurl/?aid=39woJnrTG&uid=session%s"%str(i)
    #url = "https://127.0.0.1/tempurl/?aid=39woJnrTG&uid=session%s"%"Test-W00D0001"
    driver.execute_script("window.open('%s','_blank');"%url)
    driver.switch_to.window(driver.window_handles[i])
    driver.execute_script("var iframe = document.getElementById('page-displayer'); var btn = iframe.contentWindow.document.getElementById('btnConnect'); btn.click();")
    time.sleep(2)
    driver.switch_to.window(driver.window_handles[i+1])
    driver.execute_script("var iframe = document.getElementById('page-displayer'); var btn = iframe.contentWindow.document.getElementById('btnConnect'); btn.click();")

while True:

    newDriver()
    i = i + 1
    time.sleep(5)