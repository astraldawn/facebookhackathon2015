import facebook
import pickle

# Change access token
graph = facebook.GraphAPI(access_token='CAACEdEose0cBAGGiyQGOrcBMwuiqaQzc4snjt4QYbOWxreo7sE1iNiwd3bEi9bdY0FkOtR0zR6FPkQVwqviF7FSPB5pdLPF8AawmvshG1gaf2zVghh4U2K5wdpdYnLwlz2LR4OLIRF6LeMZCWmnmgmcqrfgIF6lwJR3cbH1UYVvuEeAgV5nVQvCQvC4iwpALL97fZCRkzsW4jygSyg')

def load_profile():
    photos = graph.get_object(id="me/photos", limit=1000)
    print len(photos['data'])
    result = []
    cnt = 0
    for photo in photos['data']:
        cnt += 1
        people = {}
        print "FROM", photo['from']
        people[photo['from']['id']] = photo['from']['name']
        print "TAG", photo['tags']
        print "ID", photo['id']
        print "CREATED", photo['created_time'], len(photos['data']), cnt
        for taggee in photo['tags']['data']:
            if 'id' in taggee.keys():
                people[taggee['id']] = taggee['name']
        result.append((photo['id'], photo['created_time'], people))

    # Change the file name here
    pickle.dump(result, open("mark_data.p", "wb"))
    #data = pickle.load(open("mark_data.p", "rb"))
    #print data

if __name__ == '__main__':
    load_profile()
