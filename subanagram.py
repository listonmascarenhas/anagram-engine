import webapp2
import jinja2
import os
import logging

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
            def sub_anagram(blank,count):

                if len(blank[count])<=3:
                    return blank
                else:
                    word = list(blank[count])
                    if count is 0:
                        del blank[count]
                    for i in word[:]:
                        temp_list = word[:]
                        temp_list.remove(i)
                        reduced_word = ''.join(temp_list)
                        logging.info(str(count)+':::'+i+':::'+reduced_word)
                        if reduced_word not in blank:
                            blank.append(reduced_word)
                    count = count+1
                    return sub_anagram(blank,count)
            word = self.request.get('search_word')
            word = sortWord(word)
            blank = [word]
            sub_anagram(blank,0)
            template_values = {
                'blank': blank
            }
            template = JINJA_ENVIRONMENT.get_template('subanagram.html')
            self.response.write(template.render(template_values))
