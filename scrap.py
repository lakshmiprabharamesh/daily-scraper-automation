from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from bs4 import BeautifulSoup
import pandas as pd
import smtplib 
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import os 
import tempfile


csv_path = "/Users/connectiot/Desktop/lramesh/automated_python/ORSNASCO_Pricing_Daily_Data.csv"
def send_email(csv_path):
    sender_email = os.getenv("EMAIL_USERNAME")
    receiver_email = "sales@firmindustrial.com"
    password =os.getenv("EMAIL_PASSWORD")

    subject="ORS Nasco Daily Report"
    body="Attached is the ORS NASCO daily csv report."

    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = receiver_email
    msg["Subject"]=subject


    msg.attach(MIMEText(body,"plain"))

    with open(csv_path,"rb") as f:
        part=MIMEApplication(f.read(),Name=os.path.basename(csv_path))
    part["Content-Disposition"] = f'attachment; filename="{os.path.basename(csv_path)}"'
    msg.attach(part)


    with smtplib.SMTP_SSL('smtp.zoho.com', 465) as server:
        server.login(sender_email, password)
        server.send_message(msg)

    print("Email sent successfully!")

user_data_dir = tempfile.mkdtemp()
options = Options()
options.add_argument("--headless=new")
options.add_argument(f"--user-data-dir={user_data_dir}")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/114.0.0.0 Safari/537.36")

service = Service(ChromeDriverManager().install())

driver = webdriver.Chrome(service=service,options=options)

driver.get("https://www.orsnasco.com/storefrontCommerce/login.do")

time.sleep(2)

with open("debug_timeout.html", "w", encoding="utf-8") as f:
    f.write(driver.page_source)

wait = WebDriverWait(driver, 15)

user_name_input = wait.until(EC.presence_of_element_located((By.NAME, "usr_name")))
password_input = wait.until(EC.presence_of_element_located((By.NAME, "usr_password")))
button_click = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,'input[type="submit"][value="Sign In"]')))

user_name_input.send_keys("lakshmi.prabha@firmindustrial.com")
password_input.send_keys("SaiSaibaba@8080")
button_click.click()

time.sleep(5)

print("Logged in.Current page title:",driver.title)

urls_to_scrap = [
    "https://www.orsnasco.com/storefrontCommerce/itemDetail.do?item-id=396654&order-quantity=1&item-index=0&customer-item=012-11581-070&order-uom=DZ&warehouse-id=13&item-number=012-11581-070",
    "https://www.orsnasco.com/storefrontCommerce/itemDetail.do?item-id=396655&order-quantity=1&item-index=0&customer-item=012-11581-080&order-uom=DZ&warehouse-id=13&item-number=012-11581-080",
    "https://www.orsnasco.com/storefrontCommerce/itemDetail.do?item-id=396656&order-quantity=1&item-index=0&customer-item=012-11581-090&order-uom=DZ&warehouse-id=13&item-number=012-11581-090",
    "https://www.orsnasco.com/storefrontCommerce/itemDetail.do?item-id=409476&order-quantity=1&item-index=0&customer-item=978-104500&order-uom=CA&warehouse-id=13&item-number=978-104500",
    "https://www.orsnasco.com/storefrontCommerce/itemDetail.do?item-id=409477&order-quantity=1&item-index=0&customer-item=978-104503&order-uom=CA&warehouse-id=13&item-number=978-104503",
    "https://www.orsnasco.com/storefrontCommerce/itemDetail.do?item-id=409478&order-quantity=1&item-index=0&customer-item=978-104570&order-uom=CA&warehouse-id=13&item-number=978-104570",
    "https://www.orsnasco.com/storefrontCommerce/itemDetail.do?item-id=144368&order-quantity=1&item-index=0&customer-item=012-92-500-6.5-7&order-uom=BX&warehouse-id=13&item-number=012-92-500-6.5-7",
    "https://www.orsnasco.com/storefrontCommerce/itemDetail.do?item-id=144369&order-quantity=1&item-index=0&customer-item=012-92-500-7.5-8&order-uom=BX&warehouse-id=13&item-number=012-92-500-7.5-8",
    "https://www.orsnasco.com/storefrontCommerce/itemDetail.do?item-id=144370&order-quantity=1&item-index=0&customer-item=012-92-500-8.5-9&order-uom=BX&warehouse-id=13&item-number=012-92-500-8.5-9",
    "https://www.orsnasco.com/storefrontCommerce/itemDetail.do?item-id=144371&order-quantity=1&item-index=0&customer-item=012-92-500-9.5-10&order-uom=BX&warehouse-id=13&item-number=012-92-500-9.5-10"
]

all_data=[]

for url in urls_to_scrap:
    driver.get(url)
    time.sleep(3)

    soup = BeautifulSoup(driver.page_source,"html.parser")

    tables = []
    tables=soup.find_all("table")
    first_table= tables[0]

    rows = []
    td_list=[]

    rows=first_table.find_all("tr")
    Eleventh_row = rows[11]
    td_list =Eleventh_row.find_all("td")
    data_value = td_list[1].get_text()
    all_data.append(data_value)

products= ["FIO-012-11581-070","FIO-012-11581-080","FIO-012-11581-090","FIO-978-104500","FIO-978-104503","FIO-978-104570","FIO-012-92-500-6.5-7","FIO-012-92-500-7.5-8",
"FIO-012-92-500-8.5-9","FIO-012-92-500-9.5-10"]

d = {
    "Products" :products,
    "Quantity Available":all_data
}

df =pd.DataFrame(data=d)
df.to_csv("ORSNASCO_Pricing_Daily_Data.csv",index=False)
print("All pages scraped and saved to orsnasco_daily_data.csv")
send_email("ORSNASCO_Pricing_Daily_Data.csv")
driver.quit()

