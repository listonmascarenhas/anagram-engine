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
        # def sub_anagram(word,length,blank):
        #     if len(word)<3:
        #         return blank
        #     else:
        #         for i in word[:]:
        #             list = word[:]
        #             list.remove(i)
        #             reduced_word = ''.join(list)
        #             logging.info('yo'+reduced_word)
        #             blank.append(reduced_word)
        #         return sub_anagram(list,length,blank)

        def sub_anagram(blank,count):

            if len(blank[count])<=3:
                if count ==20:
                    return blank
            else:
                word = list(blank[count])
                for i in word[:]:
                    temp_list = word[:]
                    temp_list.remove(i)
                    reduced_word = ''.join(temp_list)
                    logging.info(str(count)+':::'+i+':::'+reduced_word)
                    if reduced_word not in blank:
                        blank.append(reduced_word)
                count = count+1
                return sub_anagram(blank,count)
        self.response.headers['Content-Type'] = 'text/html'
        template = JINJA_ENVIRONMENT.get_template('subanagram.html')
        word = 'glare'
        word = sortWord(word)
        #word = sorted(word)
        blank = [word]
        # for i in word[:]:
        #     list = word[:]
        #     list.remove(i)
        #sub_anagram(word,len(word),blank)
        sub_anagram(blank,0)
        self.response.write(blank)
