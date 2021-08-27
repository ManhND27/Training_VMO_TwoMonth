import requests

header = {
    "authority": "www.vulnerabilitycenter.com",
    "sec-ch-ua": "\" Not A;Brand\";v=\"99\", \"Chromium\";v=\"91\", \"Google Chrome\";v=\"91\"",
    "x-gwt-module-base": "https://www.vulnerabilitycenter.com/svc/svc/",
    "x-gwt-permutation": "938A4411868A979D515A5CE34BBE59F8",
    "sec-ch-ua-mobile": "?0",
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 Safari/537.36",
    "cookie_string" : "JSESSIONID=1CC719D39466FCA3C60E7592BEAC22F0; SESS9ab004767f41bf8781a9a80db17b50c6=90mdbc9bi7ffeqlkan6aoi8475; d-a8e6=2afa44f7-9a02-4f79-9569-f03f72ef83df; __utmz=66189737.1626662324.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); _mkto_trk=id:440-MPQ-510&token:_mch-vulnerabilitycenter.com-1626662324339-98950; OptanonAlertBoxClosed=2021-07-19T02:55:04.552Z; has_js=1; s-9da4=4fef12a7-a209-4eca-8dd8-2dd6b22e9b0f; __utma=66189737.538287118.1626662324.1626662324.1626687780.2; __utmc=66189737; __utmt=1; OptanonConsent=landingPath=NotLandingPage&datestamp=Mon+Jul+19+2021+16%3A52%3A13+GMT%2B0700+(Indochina+Time)&version=3.6.28&groups=1%3A1%2C2%3A1%2C3%3A1%2C4%3A1%2C0_162101%3A1%2C0_162100%3A1%2C0_162099%3A1%2C0_162105%3A1%2C0_162104%3A1%2C0_162103%3A1%2C0_162102%3A1%2C0_162109%3A1%2C0_162108%3A1%2C0_162107%3A1%2C0_162106%3A1%2C0_162113%3A1%2C0_162112%3A1%2C0_162111%3A1%2C0_162110%3A1&AwaitingReconsent=false; __utmb=66189737.4.10.1626687780",
    "content-type": "text/x-gwt-rpc; charset=UTF-8",
    "accept": "*/*",
    "origin": "https://www.vulnerabilitycenter.com",
    "sec-fetch-site": "same-origin",
    "sec-fetch-mode": "cors",
    "sec-fetch-dest": "empty",
    "referer": "https://www.vulnerabilitycenter.com/svc/SVC.html",
    "accept-language": "en-US,en;q=0.9"
}

url = 'https://www.vulnerabilitycenter.com/#home'
reponse = requests.get(url)
print(reponse)
