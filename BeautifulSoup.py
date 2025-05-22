import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
options = webdriver.ChromeOptions()
options.add_argument("--headless")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
url = "https://rera.odisha.gov.in/projects/project-list"
driver.get(url)
time.sleep(5)
projects_data = []

for i in range(6):
    cards = driver.find_elements(By.CSS_SELECTOR, "table tbody tr")
    if i < len(cards):
        try:
            view_buttons = driver.find_elements(By.LINK_TEXT, "View Details")
            driver.execute_script("arguments[0].click();", view_buttons[i])
            time.sleep(3)

            soup = BeautifulSoup(driver.page_source, "html.parser")
            details = soup.find("div", class_="project-detail")
            rera_no = details.find("label", string="Rera Regd. No").find_next_sibling().text.strip()
            project_name = details.find("label", string="Project Name").find_next_sibling().text.strip()
            promoter_tab = driver.find_element(By.LINK_TEXT, "Promoter Details")
            driver.execute_script("arguments[0].click();", promoter_tab)
            time.sleep(2)

            soup = BeautifulSoup(driver.page_source, "html.parser")
            promoter_section = soup.find("div", class_="tab-pane active")

            company_name = promoter_section.find("label", string="Company Name").find_next_sibling().text.strip()
            address = promoter_section.find("label", string="Registered Office Address").find_next_sibling().text.strip()
            gst_no = promoter_section.find("label", string="GST No.").find_next_sibling().text.strip()

            projects_data.append({
                "Rera Regd. No": rera_no,
                "Project Name": project_name,
                "Promoter Name": company_name,
                "Promoter Address": address,
                "GST No.": gst_no
            })

            driver.back()
            time.sleep(3)

        except Exception as e:
            print(f"Error with project {i+1}: {e}")
            driver.back()
            time.sleep(3)

driver.quit()
df = pd.DataFrame(projects_data)
print(df)
df.to_csv("rera_projects.csv", index=False)
