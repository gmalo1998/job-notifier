import time
import requests
import os
from selenium import webdriver
from selenium.webdriver.common.by import By

# GitHub Secrets theke Token gulo nebe
TELEGRAM_BOT_TOKEN = os.getenv('8824526553:AAE8bc3CEDVL1VDqq114s12a8w5OJcXLc2E')
TELEGRAM_CHAT_ID = os.getenv('5038339761')

if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
    print("ERROR: Telegram Token or Chat ID is missing in Secrets!", flush=True)
    sys.exit(1)

# গত ৭২ ঘণ্টার (3 Days) জব লিঙ্কগুলো
NAUKRI_URL = "https://www.naukri.com/devops-or-sre-or-cloud-engineer-or-kubernetes-jobs?experience=4&sort=date&jobAge=3" 
FOUNDIT_URL = "https://www.foundit.in/srp?query=DevOps%20OR%20SRE%20OR%20Cloud%20OR%20Kubernetes&experience=4&sort=1"
LINKEDIN_URL = "https://www.linkedin.com/jobs/search/?keywords=DevOps%20OR%20SRE%20OR%20Cloud%20OR%20Kubernetes&location=India&f_E=3%2C4&f_TPR=r259200&sortBy=DD"

def send_telegram_message(platform, title, link):
    message = f"🚨 New Job on {platform}!\n\n💼 {title}\n🔗 {link}"
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    try:
        response = requests.post(url, data={'chat_id': TELEGRAM_CHAT_ID, 'text': message})
        print(f"[{platform}] Telegram status: {response.status_code} - {response.text}", flush=True)
    except Exception as e:
        print(f"[{platform}] Telegram Error: {e}", flush=True)

def setup_browser():
    print("Setting up Chrome browser...", flush=True)
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36")
    return webdriver.Chrome(options=options)

def check_jobs(driver):
    print("\nChecking Naukri...", flush=True)
    try:
        driver.get(NAUKRI_URL)
        time.sleep(10)
        jobs = driver.find_elements(By.CSS_SELECTOR, "a.title")[:2]
        print(f"Found {len(jobs)} jobs on Naukri.", flush=True)
        for job in jobs:
            send_telegram_message("Naukri", job.text, job.get_attribute('href'))
    except Exception as e: 
        print(f"Naukri Error: {e}", flush=True)

    print("\nChecking Foundit...", flush=True)
    try:
        driver.get(FOUNDIT_URL)
        time.sleep(10)
        jobs = driver.find_elements(By.CSS_SELECTOR, ".jobTitle a")[:2]
        print(f"Found {len(jobs)} jobs on Foundit.", flush=True)
        for job in jobs:
            send_telegram_message("Foundit", job.text, job.get_attribute('href'))
    except Exception as e: 
        print(f"Foundit Error: {e}", flush=True)

    print("\nChecking LinkedIn...", flush=True)
    try:
        driver.get(LINKEDIN_URL)
        time.sleep(10)
        jobs = driver.find_elements(By.CSS_SELECTOR, ".base-search-card__title")[:2]
        links = driver.find_elements(By.CSS_SELECTOR, ".base-card__full-link")[:2]
        print(f"Found {len(jobs)} jobs on LinkedIn.", flush=True)
        for job, link in zip(jobs, links):
            clean_link = link.get_attribute('href').split('?')[0]
            send_telegram_message("LinkedIn", job.text.strip(), clean_link)
    except Exception as e: 
        print(f"LinkedIn Error: {e}", flush=True)

if __name__ == "__main__":
    driver = setup_browser()
    check_jobs(driver)
    driver.quit()
    print("\n--- JOB CHECK COMPLETED ---", flush=True)
