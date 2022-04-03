from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
from fake_useragent import UserAgent
import requests
import json
from types import SimpleNamespace


def main():
    ua = UserAgent(cache=False)
    HEADERS = {
        'User-Agent': ua.random
    }
    options = webdriver.ChromeOptions()
    options.add_argument('window-size=1900,1000')
    driver = webdriver.Chrome(chrome_options=options)
    APIkey = "CapMonster API key"
    url = "https://www.google.com/recaptcha/api2/demo"

    driver.get(url)
    sleep(5)

    sitekey = driver.find_element_by_xpath('//*[@id="recaptcha-demo"]').get_attribute("data-sitekey")
    response = requests.post('https://api.capmonster.cloud/createTask', json={
        "clientKey": APIkey,
        "task":
            {
                "type": "NoCaptchaTaskProxyless",
                "websiteURL": url,
                "websiteKey": sitekey
            }
    }, headers=HEADERS).text
    x = json.loads(response, object_hook=lambda d: SimpleNamespace(**d))
    print("Answer", response)

    result = requests.post('https://api.capmonster.cloud/getTaskResult/', json={
        "clientKey": APIkey,
        "taskId": x.taskId
    }, headers=HEADERS).text
    y = json.loads(result, object_hook=lambda d: SimpleNamespace(**d))
    while y.status != "ready":
        sleep(1)
        result = requests.post('https://api.capmonster.cloud/getTaskResult/', json={
            "clientKey": APIkey,
            "taskId": x.taskId
        }, headers=HEADERS).text
        print("Result While", result)
        y = json.loads(result, object_hook=lambda d: SimpleNamespace(**d))

    answer = y.solution.gRecaptchaResponse
    wirte_token_js = f'document.getElementById("g-recaptcha-response").innerHTML="{answer}";'
    submit_js = 'document.getElementById("recaptcha-demo-form").submit();'
    driver.execute_script(wirte_token_js)
    sleep(3)
    driver.execute_script(submit_js)
    sleep(10)


if __name__ == "__main__":
    main()
