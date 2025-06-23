#!/usr/bin/env python3
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import pandas as pd

# All 30 WA community-college institution codes
INSTITUTION_CODES = [
    "WA010","WA020","WA030","WA040","WA050","WA060","WA070","WA080","WA090",
    "WA100","WA110","WA120","WA130","WA140","WA150","WA160","WA170","WA180",
    "WA190","WA200","WA210","WA220","WA230","WA240","WA250","WA260","WA270",
    "WA280","WA290","WA300"
]

# Summer 2025 term code
TERM_CODE = "2255"

def scrape_institution(driver, inst_code):
    url = (
        "https://csprd.ctclink.us/psp/csprd/EMPLOYEE/SA/s/"
        "WEBLIB_HCX_CM.H_CLASS_SEARCH.FieldFormula.IScript_Main"
        f"?institution={inst_code}"
    )
    driver.get(url)
    time.sleep(2)

    # Select term dropdown and choose Summer 2025
    term_sel = driver.find_element(By.NAME, "CLASS_SRCH_WRK2_STRM$0")
    for opt in term_sel.find_elements(By.TAG_NAME, "option"):
        if opt.get_attribute("value") == TERM_CODE:
            opt.click()
            break

    # Submit search
    driver.find_element(By.NAME, "CLASS_SRCH_WRK2_SSR_PB_GO").click()
    time.sleep(5)

    # Parse the results table
    rows = driver.find_elements(
        By.XPATH,
        "//div[@id='win0divAGE_WRK_CLASS_SRCH_RSLT']//table//tr"
    )
    courses = []
    for row in rows[1:]:
        cells = row.find_elements(By.TAG_NAME, "td")
        if len(cells) < 4:
            continue
        courses.append({
            "Institution": inst_code,
            "CRN":        cells[0].text.strip(),
            "Subject":    cells[1].text.strip(),
            "Course":     cells[2].text.strip(),
            "Title":      cells[3].text.strip(),
            # add more fields as desired...
        })
    return courses

def main():
    chrome_opts = Options()
    chrome_opts.add_argument("--headless=new")  # headless mode :contentReference[oaicite:0]{index=0}
    driver = webdriver.Chrome(options=chrome_opts)  # Selenium WebDriver :contentReference[oaicite:1]{index=1}

    all_courses = []
    for code in INSTITUTION_CODES:
        print(f"Scraping {code}…")
        all_courses += scrape_institution(driver, code)

    driver.quit()

    # Save results
    df = pd.DataFrame(all_courses)
    df.to_csv("summer2025_wa_cc_courses.csv", index=False)
    print("Done: summer2025_wa_cc_courses.csv")

if __name__ == "__main__":
    main()
