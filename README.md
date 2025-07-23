# daily-scraper-automation

# 🛠️ ORS NASCO Daily Pricing Scraper & Email Notifier

This Python automation script logs into the ORS NASCO B2B website, scrapes the available quantities of selected products, saves the data to a CSV file, and automatically emails the report to a recipient every morning at 8:00 AM EDT.

---

## 📌 Features

- 🔐 Logs into ORSNasco with provided credentials using Selenium.
- 🔎 Scrapes product availability for a defined list of SKUs.
- 📊 Saves scraped data into a CSV file.
- 📧 Sends the report via email as an attachment using Zoho SMTP.
- ⏰ Can be scheduled to run daily (e.g., via cron or Task Scheduler).

---

## 📂 Project Structure

```
ORSNASCO_Pricing_Scraper/
├── ORSNASCO_Pricing_Daily_Data.csv     # Output CSV report
├── debug_timeout.html                  # Optional: Saved page source for debugging
├── scraper.py                          # Main automation script
├── .env                                # Environment variables (optional)
└── README.md                           # This file
```

---

## ⚙️ Requirements

- Python 3.8+
- Google Chrome installed
- pip packages:
  - `selenium`
  - `webdriver-manager`
  - `beautifulsoup4`
  - `pandas`
  - `python-dotenv` *(optional)*

Install them via:

```bash
pip install selenium webdriver-manager beautifulsoup4 pandas python-dotenv
```

---

## 🔐 Environment Variables

Create a `.env` file or set system environment variables:

```env
EMAIL_USERNAME=your_email@domain.com
EMAIL_PASSWORD=your_secure_password
```

These are used for authenticating with Zoho SMTP.

---

## 🚀 How to Run

```bash
python scraper.py
```

The script will:
1. Open Chrome using Selenium
2. Log into [ORSNASCO login](https://www.orsnasco.com/storefrontCommerce/login.do)
3. Visit product URLs and extract quantity available
4. Save results to `ORSNASCO_Pricing_Daily_Data.csv`
5. Email the CSV file to: `sales@firmindustrial.com`

---

## ⏲️ Daily Automation (8 AM EDT)

### macOS / Linux (using `cron`)

1. Run `crontab -e`
2. Add:

```bash
0 8 * * * /usr/bin/python3 /full/path/to/scraper.py >> /path/to/log.txt 2>&1
```

Ensure your system timezone is set to EDT.

### Windows (using Task Scheduler)

1. Open Task Scheduler
2. Create Basic Task → Trigger: Daily @ 8:00 AM
3. Action: Start a program
   - Program: `python`
   - Arguments: `"C:\path\to\scraper.py"`

---

## 📧 Email Service

- SMTP Server: `smtp.zoho.com`
- Port: `465`
- Authentication: SSL

Make sure the sender email is allowed to send via SMTP (enable 2FA or app password if needed).

---

## 📌 Notes

- The script uses Chrome in headless mode and a temporary user profile for session handling.
- Uses `webdriver-manager` to manage ChromeDriver installation.
- Script is designed to fail gracefully and log issues in the console.

---

## ✅ Sample Output (CSV)

| Products             | Quantity Available |
|----------------------|--------------------|
| FIO-012-11581-070    | 87 DZ              |
| FIO-012-11581-080    | 120 DZ             |
| ...                  | ...                |

---

## 🧑‍💻 Author

**Lakshmi Prabha Ramesh**  
IoT Operations Manager, Python Automation Enthusiast  
---

## 📜 License

This project is private and intended for internal automation at Firm Industrial. Do not distribute or share without permission.
