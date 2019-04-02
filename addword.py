import webapp2
import jinja2
import os

from google.appengine.ext import ndb
from google.appengine.api import users

from myuser import MyUser
from myuser import Anagram
JINJA_ENVIRONMENT = jinja2.Environment(
    loader = jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions = ['jinja2.ext.autoescape'],
    autoescape = True
)

class AddWord(webapp2.RequestHandler):

    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        template = JINJA_ENVIRONMENT.get_template('addword.html')
        self.response.write(template.render())

    def post(self):
        self.response.headers['Content-Type'] = 'text/html'
        action = self.request.get('button')
        if action =='Add word' :
            add_word = self.request.get('add_word')
            user = users.get_current_user()
            myuser_key = ndb.Key('MyUser',user.user_id())
            my_user = myuser_key.get()
            sorted_word = ''.join(sorted(add_word))
            user_key_word = user.user_id()+sorted_word
            anagram_key = ndb.Key('Anagram',user_key_word)
            anagram = anagram_key.get()
            if anagram==None:
                anagram_list = []
                anagram_letter_count = []
                anagram_list.append(add_word)
                anagram_letter_count.append(len(add_word))
                count = 1

            else:
                anagram_list = anagram.anagram_list
                anagram_letter_count = anagram.anagram_letter_count
                if not word  in anagram_list:
                anagram_list.append(add_word)
                anagram_letter_count.append(len(add_word))
                count = anagram.anagram_count+1

            anagram = Anagram(id = user_key_word ,anagram_count=count, anagram_list = anagram_list,anagram_letter_count = anagram_letter_count)
            anagram.put()
            my_user.put()
            self.redirect('/addWord')
