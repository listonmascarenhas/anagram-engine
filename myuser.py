from google.appengine.ext import ndb

class MyUser(ndb.Model):
    email_address = ndb.StringProperty()
    anagrams = ndb.StringProperty()
    words= ndb.StringProperty()

class Anagram(ndb.Model):
    anagram_list = ndb.StringProperty(repeated = True)
    anagram_count = ndb.IntegerProperty()
    anagram_letter_count = ndb.IntegerProperty(repeated = True)
