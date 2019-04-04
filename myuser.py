from google.appengine.ext import ndb

class MyUser(ndb.Model):
    email_address = ndb.StringProperty()
    user_anagrams = ndb.IntegerProperty()
    user_words= ndb.IntegerProperty()



class Anagram(ndb.Model):
    anagram_list = ndb.StringProperty(repeated = True)
    anagram_count = ndb.IntegerProperty()
    anagram_letter_count = ndb.IntegerProperty(repeated = True)
    global sortWord
    def sortWord(string):
        return ''.join(sorted(string))
