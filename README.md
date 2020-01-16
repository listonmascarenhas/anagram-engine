# anagram-engine
The task was to build an anagram engine which would search all the anagrams of that word which is stored in the database. We will be using Google App Engine, Python, Jinja and a NoSQL database.

Methods

1. Main Page:
The get method in main.py initially allows the user to login to the application. If the authentication is successful, the users email address, unique id, word count and anagram count are stored in the NoSQL database. A search functionality is provided on the Main Page which takes in a word from the URL, sorts the word in lexicographical order using the sortWord(string) function imported from class Anagram from anagram.py, and searches if that word and all its anagram are present in the Datastore (NoSQL database). It also retrieves the users word count and anagram count from the Datastore and displays it.   

The post method in main.py checks if the ‘Search’ button is clicked and if clicked sends the input text to the same page through the URL parameter. The parameter is retrieved by the get method in Main Page.

In main.py we also define the application object that is responsible for this application. The routing table is specified in this object.


2. Add Word:
The get method in add.py just renders addword.html.
The post method in add.py checks if the ‘Add Word’ button is clicked and if clicked retrieves the input text from the form. A check is kept seeing if the word is empty or not and if latter, sends it to the function addWord(string) which takes in a string as an argument.

If the ‘Submit File’ button is clicked, the user can take a wordlist through a newline separated text ﬁle in order to populate the dictionary. The words in the file are separated using the ‘\n’ delimiter and stored as a list. The list is passed through a for loop and if the length of the word is greater than or equal to three is sent to the addWord(string) function which takes in a string as an argument. Words less than 3 letters are not allowed.

The addWord(string) function in add.py takes a string as an input. The string which is taken as input is sorted in lexicographical order using the sortWord(string) function imported from the class Anagram from anagram.py. The unique id of the user is concatenated with the sorted word and passed as a key in the Anagram Entity Kind to see if the key exists in the Datastore. If it doesn’t exist, an empty list for storing the input string is created and the input string is appended to the list. Another empty list is created to store the length of words and the length of the input string is appended to the list. The count of the number of words in each key is set to 1. The count of unique anagrams of the current user is retrieved and incremented by 1. The count of the number of words of the current user is incremented by 1. If the key exists, the list of strings with the same key, the list of length of the words and the count of unique anagrams of the current user is retrieved. If the word exists in the retrieved list, the count of the number of words in each key and the number of words of the current user is retrieved from the datastore. If the word doesn’t exist in the retrieved list, the count of the number of words in each key is retrieved from the database and incremented, the input string is appended to the list of strings with the same key, the length of the input string is appended to the list of length of the words, the number of words of the current user is retrieved and incremented by 1. All the values are then put into the datastore.   

3. Sub Anagram:
The get method in subanagram.py just renders subanagram.html.
The post method in subanagram.py checks if the ‘Search’ button is clicked and if clicked retrieves the input text from the form. The string which is taken as input is sorted in lexicographical order using the sortWord(string) function imported from the class Anagram from anagram.py. The string is added to a list and the list is sent to sub_anagram(list,counter) where the counter is initially set to 0. 

sub_anagram(list,count) is a recursive function that creates all unique sub-anagrams of length -1 from the list of input words and appends them to the same input list and the count is incremented. The function breaks out of the recursion when the length of the string is lesser than 3. The list from sub_anagram now contains all unique sub-anagrams of the input text from the form. The list runs through a loop and every word is sorted in lexicographical order using the sortWord(string) function imported from the class Anagram from anagram.py. The unique id of the user is concatenated with the sorted word and passed as a key in the Anagram Entity Kind to see if the key exists in the Datastore. If the key doesn’t exist, anagram_list is retrieved from the datastore and every word in it is appended to list_datastore which is initially blank. list_datastore is sent to subanagram.html and elements in the list are displayed.
4. sortWord(string):
sortWord(string) is a function which takes in a string and returns the string sorted in lexicographical order.

5. app.yaml:
app.yaml is responsible for informing Google App Engine about the runtimes and libraries needed for the application. Python version 2.7 is used as the runtime. We also state that the application is threadsafe so multiple instances can be allowed on the same server. In libraries we state that we will be using Jinja2 running on its latest version. In handlers, we state that all URLs with /css will be redirected to the static directory css. We also state that all other requests will be redirected to the app variable which is defined in main.py. 

Models and data structures

6. MyUser:
myuser.py contains the class MyUser which uses ndb.Model to store the email address, unique id, anagram count(user_anagrams) and word count(user_words) of users. This is possible by importing ndb from google.appengine.ext. email_address is specified as a StringProperty() since an email address is of ASCII format. Anagram count and word count are specified as IntegerProperty() because they are counters and need to be incremented.  

7. Anagram:
myuser.py contains the class Anagram which uses ndb.Model to store a list of words 	with the same anagram, a count of the number of words in the list and a list of the 	length of each word. This is possible by importing ndb from google.appengine.ext. List of 	words(anagram_list) is specified as a StringProperty() with repeated being True because 	of it being a list. A count of the number of words(anagram_count) is specified as an 	IntegerProperty() because it is a counters and needs to be incremented. List for the 	length of each word(anagram_letter_count) is specified as an IntegerProperty() because 	length of the words are integers and repeated is specified as True because of it being a 	list.
