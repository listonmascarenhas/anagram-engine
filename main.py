import webapp2
import jinja2
import os
from google.appengine.ext import ndb
from google.appengine.api import users

from myuser import MyUser
from addword import AddWord
from myuser import sortWord
from subanagram import SubAnagram

JINJA_ENVIRONMENT = jinja2.Environment(
    loader = jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions = ['jinja2.ext.autoescape'],
    autoescape = True
)

class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        url = ''
        url_string = ''
        list = ''
        user=users.get_current_user()

        if user:
            url = users.create_logout_url(self.request.uri)
            url_string = 'logout'

            myuser_key = ndb.Key('MyUser',user.user_id())
            myuser = myuser_key.get()
            if myuser == None:
                myuser = MyUser(id=user.user_id() ,email_address=user.email(), user_anagrams=0, user_words=0)
                myuser.put()

            search_word=self.request.get('word')
            if search_word != '':
                search_word =sortWord(search_word)
                user_key_word = user.user_id()+search_word
                anagram_key = ndb.Key('Anagram',user_key_word)
                anagram=anagram_key.get()
                if anagram != None:
                    list = anagram.anagram_list
                else:
                    list = []
            else:
                list = []
            user_words = myuser.user_words
            user_anagrams=myuser.user_anagrams

        else:
            url = users.create_login_url(self.request.uri)
            url_string = 'login'
            user_words = ''
            user_anagrams = ''
        template_values = {
            'url': url,
            'url_string':url_string,
            'user': user,
            'list' : list,
            'user_words' : user_words,
            'user_anagrams' : user_anagrams,
        }
        template = JINJA_ENVIRONMENT.get_template('main.html')
        self.response.write(template.render(template_values))

    def post(self):
        self.response.headers['Content-Type'] = 'text/html'
        search_button=self.request.get('search_button')
        if search_button == 'Search':
            search_word=self.request.get('search_word')
            self.redirect('/?word='+search_word)
app = webapp2.WSGIApplication([
    ('/',MainPage),
    ('/addWord',AddWord),
    ('/subAnagram',SubAnagram)
], debug =True)
