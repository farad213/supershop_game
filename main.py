from playwright.sync_api import sync_playwright
import csv, os.path, time
from datetime import datetime

url = "https://www.supershop.hu/nyerjen"
start_time = 10


def stored_inputs():
    with open("config.csv", "r", newline="") as f:
        file = csv.reader(f, delimiter=",")
        temp = [row for row in file]
        if temp:
            return temp
        else:
            return "Config file is empty."


def main(inputs):
    assert isinstance(inputs, list)
    assert isinstance(inputs[0], list)

    with sync_playwright() as playwright:

        chromium = playwright.chromium
        browser = chromium.launch(headless=False, slow_mo=500)
        page = browser.new_page()

        for data in inputs:
            page.goto(url)

            # handling cookies and popups
            page.click('//*[@id="__next"]/div[2]/div/div[1]/div/div/div/div/div[1]/div')
            page.click('//*[@id="__next"]/div[3]/div/div/div[2]/div[2]/div[1]/button/div/div')
            page.click('//*[@id="__next"]/div[3]/div/div/div[2]/div[2]/div[2]/button/div/div')

            page.fill('//*[@id="__next"]/div[2]/div/div[4]/div[3]/div[1]/div/div/div[2]/div[1]/div[2]/div/div/input',
                      data[0])
            page.fill('//*[@id="__next"]/div[2]/div/div[4]/div[3]/div[1]/div/div/div[2]/div[2]/div[2]/div/div/input',
                      data[1])
            page.fill('//*[@id="__next"]/div[2]/div/div[4]/div[3]/div[1]/div/div/div[2]/div[3]/div[2]/div/div/input',
                      data[2])
            page.click('//*[@id="__next"]/div[2]/div/div[4]/div[3]/div[2]/div/div/div/div/label/div[1]/div')
            page.click('//*[@id="__next"]/div[2]/div/div[4]/div[3]/div[2]/div/div/div/button')
            try:
                page.click('//*[@id="__next"]/div[2]/div/div[4]/div[1]/div[2]/div[2]/button')
                page.wait_for_timeout(10000)
                page.screenshot(path=os.path.join("screenshots", data[1].split("@")[0]))
            except:
                pass


if __name__ == "__main__":
    inputs = stored_inputs()

    while True:
        now = datetime.now()
        current_minutes = int(now.strftime("%M"))
        current_hour_minutes = now.strftime("%H:%M")
        if current_minutes == start_time:
            main(inputs=inputs)
        else:
            if current_minutes < start_time:
                until_next_session = start_time - current_minutes

            else: # current_minutes > start_time
                until_next_session = 60 - current_minutes + start_time
            print(f'Current time: {current_hour_minutes}\n'
                  f'Next session in {until_next_session} minutes')
        time.sleep(50)



