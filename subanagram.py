import webapp2
import jinja2
import os
import logging

from google.appengine.api import users
from google.appengine.ext import ndb

from myuser import MyUser
from myuser import Anagram
from myuser import sortWord

from  myuser import sortWord
JINJA_ENVIRONMENT = jinja2.Environment(
    loader = jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions = ['jinja2.ext.autoescape'],
    autoescape = True
)

class SubAnagram(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        template = JINJA_ENVIRONMENT.get_template('subanagram.html')
        self.response.write(template.render())

    def post(self):
        self.response.headers['Content-Type'] = 'text/html'
        action = self.request.get('button')
        if action == 'Search':
            def sub_anagram(all_sub_anagrams_list,count):

                if len(all_sub_anagrams_list[count])<=3:
                    return all_sub_anagrams_list
                else:
                    word = list(all_sub_anagrams_list[count])
                    for i in word[:]:
                        temp_list = word[:]
                        temp_list.remove(i)
                        reduced_word = ''.join(temp_list)
                        if reduced_word not in all_sub_anagrams_list:
                            all_sub_anagrams_list.append(reduced_word)
                    count = count+1
                    return sub_anagram(all_sub_anagrams_list,count)
            word = self.request.get('search_word')
            word = sortWord(word)
            all_sub_anagrams_list = [word]
            sub_anagram(all_sub_anagrams_list,0)

            list_datastore = []
            user = users.get_current_user()
            myuser_key = ndb.Key('MyUser',user.user_id())
            my_user = myuser_key.get()

            for sub in all_sub_anagrams_list:
                sorted_word = sortWord(sub)
                user_key_word = user.user_id() + sorted_word
                anagram_key = ndb.Key('Anagram',user_key_word)
                anagram = anagram_key.get()
                logging.info(user_key_word)
                if anagram != None:
                    anagram_list=anagram.anagram_list
                    for word in anagram_list:
                        list_datastore.append(word)

            template_values = {
                'all_sub_anagrams_list': list_datastore
            }
            template = JINJA_ENVIRONMENT.get_template('subanagram.html')
            self.response.write(template.render(template_values))

        elif action == 'Back':
            self.redirect('/')
