import time
import requests
import os
from selenium import webdriver
from selenium.webdriver.common.by import By

# GitHub Secrets theke Token gulo nebe
TELEGRAM_BOT_TOKEN = os.getenv('8824526553:AAE8bc3CEDVL1VDqq114s12a8w5OJcXLc2E')
TELEGRAM_CHAT_ID = os.getenv('5038339761')

# Multiple Keywords (DevOps, SRE, Cloud, Kubernetes) + 4 Years Exp + Any Location
NAUKRI_URL = "https://www.naukri.com/devops-or-sre-or-cloud-engineer-or-kubernetes-jobs?experience=4&sort=date" 

FOUNDIT_URL = "https://www.foundit.in/srp?query=DevOps%20OR%20SRE%20OR%20Cloud%20OR%20Kubernetes&experience=4&sort=1"

LINKEDIN_URL = "https://www.linkedin.com/jobs/search/?keywords=DevOps%20OR%20SRE%20OR%20Cloud%20OR%20Kubernetes&location=India&f_E=3%2C4&f_TPR=r86400&sortBy=DD"

def send_telegram_message(platform, title, link):
    message = f"🚨 New Job on {platform}!\n\n💼 {title}\n🔗 {link}"
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    requests.post(url, data={'chat_id': TELEGRAM_CHAT_ID, 'text': message})

def setup_browser():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36")
    return webdriver.Chrome(options=options)

def check_jobs(driver):
    # --- Check Naukri ---
    try:
        driver.get(NAUKRI_URL)
        time.sleep(5)
        jobs = driver.find_elements(By.CSS_SELECTOR, "a.title")[:2]
        for job in jobs:
            send_telegram_message("Naukri", job.text, job.get_attribute('href'))
    except: pass

    # --- Check Foundit ---
    try:
        driver.get(FOUNDIT_URL)
        time.sleep(5)
        jobs = driver.find_elements(By.CSS_SELECTOR, ".jobTitle a")[:2]
        for job in jobs:
            send_telegram_message("Foundit", job.text, job.get_attribute('href'))
    except: pass

    # --- Check LinkedIn ---
    try:
        driver.get(LINKEDIN_URL)
        time.sleep(5)
        jobs = driver.find_elements(By.CSS_SELECTOR, ".base-search-card__title")[:2]
        links = driver.find_elements(By.CSS_SELECTOR, ".base-card__full-link")[:2]
        for job, link in zip(jobs, links):
            clean_link = link.get_attribute('href').split('?')[0]
            send_telegram_message("LinkedIn", job.text.strip(), clean_link)
    except: pass

if __name__ == "__main__":
    driver = setup_browser()
    check_jobs(driver)
    driver.quit() # Kaaj sesh hole browser close kore debe