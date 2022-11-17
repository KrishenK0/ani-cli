# from selenium.webdriver.chrome.options import Options
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

import requests, vlc

options = ChromeOptions()
headers = {
    "Accept": "*/*",
    "Accept-Encoding": "identity;q:1, *;q:0",
    "Accept-Language": "fr-FR,fr;q:0.7",
    "Cache-Control": "no-cache",
    "DNT": "1",
    "Pragma": "no-cache",
    "Referer": "https://dood.pm/",
    "Sec-Fetch-Dest": "video",
    "Sec-Fetch-Mode": "no-cors",
    "Sec-Fetch-Site": "cross-site",
    "Sec-GPC": "1",
    "sec-ch-ua": '"Brave";v="107", "Chromium";v="107", "Not=A?Brand";v="24"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
}
# options.headless = True
# chrome_options.add_argument("--headless")

driver = Chrome(options=options)

# Browser goes to google.com
driver.get("http://mavanimes.cc/code-geass-fukkatsu-no-lelouch-film-01-vostfr")

wait = WebDriverWait(driver, 10)
element = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'btn-robot')))
element.click()

# print(driver.find_element(By.TAG_NAME, 'body').text)
# elements = driver.find_element('btn-robot')

# .click()

# print(driver.text)

wait = WebDriverWait(driver, 20).until(EC.frame_to_be_available_and_switch_to_it(
    (By.CSS_SELECTOR, 'body > div.container.mx-auto.mt-6 > article > div > h3 > div:nth-child(1) > iframe')))
element = WebDriverWait(driver, 20).until(EC.presence_of_element_located(
    (By.TAG_NAME, 'video')))

url = element.get_attribute('src')
print(element)
print(driver.page_source)
print(url)

if url:
    print('[!] Send request (%s)' % url[:50])
    Instance = vlc.Instance()
    player = Instance.media_player_new()
    Media = Instance.media_new('master.mp4')

    Media.add_option("sout=#rtp{mux=ts,ttl=10,port=10000,sdp=rtsp://:10000/test.sdp}")
    Media.add_option("--no-sout-all")
    Media.add_option("--sout-keep")
    Media.get_mrl()
    player.set_media(Media)
    player.play()

    with open('master.mp4', 'wb') as f:
        with requests.get(url, headers=headers, stream=True) as r:
            total_length = r.headers['Content-length']
            print('total: ', total_length)
            for chunk in r.iter_content(chunk_size=1024):
                print(chunk)
                f.write(chunk)

            print(r.status_code)


driver.quit()
# video_player_html5_api


# https://re511lo.dood.video/u5kj7hnaplflsdgge5fvspcpld6pn4qkfdn7jsln4iyqwhd63dbl4zg3zufa/yxqjcyti44~d1oELq8g7A?token=gfoy5s1a5bdiwrln9yudgv7y&expiry=1668714983568
