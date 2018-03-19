from bs4 import BeautifulSoup
from selenium import webdriver
import datetime
import pandas as pd
import time


class RiceQuant:

    def __init__(self):
        self._url = 'https://www.ricequant.com/notification/pt/2593359?entryDate=%s&startTime=%s&endTime=%s'
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        self.driver = webdriver.Chrome(chrome_options=options)

    def Login(self, username, pwd):
        self.username = username
        self.pwd = pwd

    def GetData(self, dt):
        datestr = dt.date().strftime('%Y%m%d')
        hour = dt.time().hour
        minutes = dt.time().minute
        hour_1 = (dt - datetime.timedelta(seconds = 60)).time().hour
        min_1 = (dt - datetime.timedelta(seconds = 60)).time().minute
        startTime = str(hour_1) + str(min_1).zfill(2) + '00000'
        endTime = str(hour) + str(minutes).zfill(2) + '00000'
        url = self._url % (datestr, startTime, endTime)
        self.driver.get(url)
        time.sleep(4)

        usernames = self.driver.find_elements_by_xpath("//input[@name='newusername'] [@type='text']")
        for user in usernames:
            try:
                self.driver.execute_script("arguments[0].style.visibility = 'visible';", user)
                user.clear()
                user.send_keys(self.username)
            except:
                pass

        pwds = self.driver.find_elements_by_xpath("//input[@name='password'] [@type='password']")

        for pwd in pwds:
            try:
                self.driver.execute_script("arguments[0].style.visibility = 'visible';", pwd)
                pwd.clear()
                pwd.send_keys(self.pwd)
            except:
                pass

        submit = self.driver.find_element_by_xpath("//input[@value='登录'] [@type='submit']")
        self.driver.execute_script("arguments[0].style.visibility = 'visible';", submit)
        submit.submit()
        time.sleep(8)
        html = self.driver.page_source
        soup = BeautifulSoup(html, 'lxml')
        table = soup.find('table')
        data = pd.read_html(str(table))[0]
        return data


if __name__ == "__main__":
    dt = datetime.datetime(2018,3,9,23,00,00)
    rq = RiceQuant()
    rq.Login('15950076835', 'ljh121005783')
    data = rq.GetData(dt)
    print(data)