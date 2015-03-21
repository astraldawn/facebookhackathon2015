import requests
import mechanize
from bs4 import BeautifulSoup, Comment

def start_browser(username, password):
    print "UTILITY: Start browser"
    browser = mechanize.Browser()
    browser.set_handle_robots(False)
    browser.addheaders = [('User-agent', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.101 Safari/537.36')]
    sign_in = browser.open("https://www.facebook.com/login.php")
    browser.select_form(nr=0)
    browser.form['email'] = username
    browser.form['pass'] = password
    response = browser.submit()

    # Loads all the photos_of a person
    photos = browser.open("https://www.facebook.com/chuyong/photos_of").read()
    print "UTILITY: Browser load success"
    return browser, photos

def dump(name, object, type):
    print "UTILITY:", "Dumping", name, "to file"
    f = open(name + ".txt", "w")
    if type == "html":
        soup = BeautifulSoup(object)
        soup.encode('utf-8')
        f.write(soup.prettify('latin1'))
    else:
        f.write(object)
    f.close()

def get_first_photo(browser, photos_of):
    print "UTILITY: Getting first photo"
    photos_soup = BeautifulSoup(photos_of)
    comments = photos_soup.findAll(text=lambda text:isinstance(text, Comment))
    final_id = 0
    for k in comments:
        comment_soup = BeautifulSoup(k)
        photo_id = comment_soup.findAll('div', attrs={"data-fbid": True})
        if len(photo_id) > 0:
            final_id = photo_id[0]["data-fbid"]

    return browser, final_id

def print_html(object):
    object.encode('utf-8')
    print object.prettify('latin1')

if __name__ == '__main__':
    pass
