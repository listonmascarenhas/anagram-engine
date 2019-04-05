import webapp2
import jinja2
import os

from google.appengine.ext import ndb
from google.appengine.api import users

from myuser import MyUser
from myuser import Anagram
from myuser import sortWord
JINJA_ENVIRONMENT = jinja2.Environment(
    loader = jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions = ['jinja2.ext.autoescape'],
    autoescape = True
)

class AddWord(webapp2.RequestHandler):
    global addWord
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'

        template = JINJA_ENVIRONMENT.get_template('addword.html')
        self.response.write(template.render())


    def post(self):
        self.response.headers['Content-Type'] = 'text/html'
        action = self.request.get('button')
        template = JINJA_ENVIRONMENT.get_template('addword.html')
        error = ''
        if action =='Add word' :
            add_word = self.request.get('add_word')
            if add_word != '':
                addWord(add_word)
            else:
                error = 'Cannot input empty string'
            template_values={'error':error}
            self.response.write(template.render(template_values))

        elif action == 'Submit':
            file = self.request.POST['file']
            if file != '':
                new_words=file.value.split('\n')
                for add_word in new_words:
                    if(len(add_word)>3):
                        addWord(add_word.rstrip())
            else :
                error = 'Choose a file to upload'
            template_values={'error':error}
            self.response.write(template.render(template_values))
        elif action == 'Back':
            self.redirect('/')

    def addWord(add_word):
        user = users.get_current_user()
        myuser_key = ndb.Key('MyUser',user.user_id())
        my_user = myuser_key.get()
        sorted_word = sortWord(add_word)
        user_key_word = user.user_id() + sorted_word
        anagram_key = ndb.Key('Anagram',user_key_word)
        anagram = anagram_key.get()
        if anagram==None:
            anagram_list = []
            anagram_letter_count = []
            anagram_list.append(add_word)
            anagram_letter_count.append(len(add_word))
            count = 1
            user_anagrams = my_user.user_anagrams + 1
            user_words = my_user.user_words + 1

        else:
            anagram_list = anagram.anagram_list
            anagram_letter_count = anagram.anagram_letter_count
            user_anagrams = my_user.user_anagrams

            if  add_word  in anagram_list:
                count = anagram.anagram_count
                user_words = my_user.user_words

            else:
                count = anagram.anagram_count + 1
                anagram_list.append(add_word)
                anagram_letter_count.append(len(add_word))
                user_words = my_user.user_words +    1

        anagram = Anagram(id = user_key_word ,anagram_count=count, anagram_list = anagram_list,anagram_letter_count = anagram_letter_count)
        my_user = MyUser( id = user.user_id(), user_words = user_words, user_anagrams= user_anagrams,email_address=user.email())
        anagram.put()
        my_user.put()
