# from imp import reload
# from requests_html import HTMLSession
# session = HTMLSession()


# script = """
#     () => {
#          setTimeout(function(){
#             document.querySelectorAll("button.btn-robot")[0].click();
#         }, 3000);
#     }
# """

# r = session.get(
#     'http://mavanimes.cc/code-geass-fukkatsu-no-lelouch-film-01-vostfr')


# r.html.render(sleep=10, script=script, reload=False)
# print(r.html.html)


# from selenium.webdriver.chrome.options import Options
from selenium.webdriver import Chrome, ChromeOptions

options = ChromeOptions()
options.headless = True
# chrome_options.add_argument("--headless")

driver = Chrome(options=options)

driver.get("http://mavanimes.cc/code-geass-fukkatsu-no-lelouch-film-01-vostfr") #Browser goes to google.com
print(driver)

elements = driver.find_element_by_class_name('btn-robot')

for element in elements:
    print(element.text)
    # .click()

# print(driver.text)

driver.quit()