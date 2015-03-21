import requests
import mechanize
from bs4 import BeautifulSoup, Comment
import utility


def open_photo(browser, photo_id, cnt):
    photo_url = "https://www.facebook.com/photo.php?fbid=" + photo_id
    photo_read = browser.open(photo_url).read()
    photo_soup = BeautifulSoup(browser.open(photo_url).read())
    utility.dump("indiv_photo", photo_read, "html")

if __name__ == '__main__':
    username = "prokilerxx@gmail.com"
    password = "facebookhackathontest"
    browser, photos_of = utility.start_browser(username, password)
    # utility.dump("photos_of", photos_of, "html")
    browser, first_photo_id = utility.get_first_photo(browser, photos_of)
    open_photo(browser, first_photo_id, 0)

# import mechanize  #pip install mechanize</p>
# mechanize.Browser()
# br.set_handle_robots(False)
# br.addheaders = [("User-agent","Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.2.13) Gecko/20101206 Ubuntu/10.10 (maverick) Firefox/3.6.13")]
# sign_in = br.open("http://school.dwit.edu.np/login/index.php")  #the login url
# br.select_form(nr = 0) #accessing form by their index. Since we have only one form in this example, nr =0
# br.select_form(name = "form name") # Alternatively you may use this instead of the above line if your form has name attribute available.
# br["username"] = "email/username" #the key "username" is the variable that takes the username/email value
# br["password"] = "password"    #the key "password" is the variable that takes the password value<
# logged_in = br.submit()   #submitting the login credentials
# logincheck = logged_in.read()  #reading the page body that is redirected after successful login
# print logincheck #printing the body of the redirected url after login
# req = br.open("http://school.dwit.edu.np/mod/assign/").read() #accessing other url(s) after login is done this way
