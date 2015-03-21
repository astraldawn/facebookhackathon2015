import requests
import mechanize
from bs4 import BeautifulSoup, Comment
import utility
import pickle
import time
import random


def open_photo(browser, photo_id, self_id):
    print "OPENING PHOTO:", photo_id
    photo_url = "https://www.facebook.com/photo.php?fbid=" + photo_id
    photo_url += "&set=t." + self_id
    photo_read = browser.open(photo_url).read()
    photo_soup = BeautifulSoup(browser.open(photo_url).read())
    # utility.dump("indiv_photo", photo_read, "html")

    # Get all the people tagged - DONE
    # person (dict): (id, realname)
    taggee_list = photo_soup.findAll("a", {"class": "taggee", "data-tag": True})
    people = {}
    for person in taggee_list:
        # print person
        person_id = person['data-tag']
        person_name = person.findAll(text=True)
        people[person_id] = ''.join(person_name)
    # print people

    # Get time of posting
    post_list = photo_soup.findAll("abbr", {"data-utime": True})
    post_time = post_list[0]["data-utime"]

    # Get the next photo
    next_photo_list = photo_soup.findAll("a", {"class": "photoPageNextNav"})
    next_url = next_photo_list[0]["href"]
    next_url = next_url.split("=")
    next_url = next_url[1].split("&")
    next_id = next_url[0]

    return photo_id, post_time, people, next_id

# Stop at 1515109561418


def extract_photos(browser, first_photo_id, self_id, num_photos):
    result = []
    cur_id = first_photo_id
    vis_photos = {}
    for i in range(0, num_photos):
        #Terminate the run at this photo
        # if cur_id == "1665949282124":
        #     break

        if not cur_id in vis_photos.keys():
            vis_photos[cur_id] = 1
            # photo_id, post_time, people, next_id = open_photo(browser, cur_id, self_id)
            try:
                photo_id, post_time, people, next_id = open_photo(browser, cur_id, self_id)
            except:
                print "Crash on", cur_id
                return result
            result.append([photo_id, post_time, people])
            # print photo_id, post_time, people
            cur_id = next_id
            if cur_id == "10152646351363160":
                cur_id = "10152646326648160"
            if cur_id == "10150268535342236":
                cur_id = "249261681767612"
            if cur_id == "10150247183549216":
                cur_id = "10150206609317844"
            if cur_id == "2065343508667":
                cur_id = "10150207478188157"
            if cur_id == "10150221853183048":
                cur_id = "10150221274734756"
            if cur_id == "10150188280185819":
                cur_id = "214625568565272"
            if cur_id == "212428098784304":
                cur_id = "10150549882345104"
            if cur_id == "10150096114610819":
                cur_id = "1758696642184"
            if cur_id == "1541229936774":
                cur_id = "1514900678559"
            if cur_id == "1515177083106":
                cur_id = "481992654572"
            if cur_id =="10150523117650119":
                cur_id = "333600256667087"
            rand_delay = random.randint(1, 5)
            print "Waiting", rand_delay
            time.sleep(rand_delay)
        else:
            break

    return result


if __name__ == '__main__':
    username = "prokilerxx@gmail.com"
    password = "facebookhackathontest"
    self_id = "601910818"
    browser, photos_of = utility.start_browser(username, password)
    # utility.dump("photos_of", photos_of, "html")
    browser, first_photo_id = utility.get_first_photo(browser, photos_of)
    # first_photo_id = "918187591526261"
    # first_photo_id = "10150523117830119"
    first_photo_id = "345744938390"
    data = extract_photos(browser, first_photo_id, self_id, 10000)

    pickle.dump(data, open(self_id + "_data.p", "wb"))

    # Load all the data
    # data_new = pickle.load(open(self_id + "_data.p", "rb"))

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
