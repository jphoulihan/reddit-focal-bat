# **FOCAL-BAT** 

## **Description** 
_focal-bat is a 'word of the day' comment bot_<br/><br/>

## **Project Goal**
The idea spawned from an interest in forum board reply bots, natural language processing and a love for languages. The goal of this project is to promote the Irish language by giving it more exposure on a forum for Ireland, comprised of 448k members. With only 4% of the population using Irish on a daily basis it needs the exposure. By piggybacking on Reddits' voting system, I take the top comment of the top post of the day and directly reply to it with a personalized Irish word of the day. With this approach I maximize the number of users that will see my bot and therefore read a bit of Irish and potentially go a bit deeper and click the attached link.<br/><br/>

### **Tech Used**
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
  
  ### Libraries
   * praw
   * spacy
   * beautifulsoup4
   * html5lib<br/><br/>

### **Features**
focal-bat ensures a reliable translation by using the nlp library's tokenization and lammetization. Creating a dictionary (hash map) from a user's comment it removes any duplicate words, where key is a word and value is a token. It checks both English to Irish and Irish to English dictionary entries to ensure the best translation is selected for a response. After scraping and formatting the results it constructs a reply. A related phrase and a link to the dictionary entry is also included in the reply. The reply is addressed to the author of the comment.<br/><br/>

### **Sample Console Output**

![alt text](focal-console.png "samp console output")<br/><br><br/><br/>


### **In App Response**

![alt text](reddit-response-example.png "in app response")<br/><br/>


### **To Run This Project**

This script was developed in a Python virtual environment 

```
$ git clone https://github.com/jphoulihan/reddit-focal-bat.git
```

```
$ python3 -m venv <insert-directory-name>
```
```
$ <your-directory-name>/bin/activate
```
```
$ pip install praw
```
```
$ pip install spacy
```
```
$ pip install beautifulsoup4
```
```
$ pip install html5lib
```
<br/><br/>

### **Register Reddit App**
This project requires the developer to register a reddit app. After which they will receive a personal use script id and a secret. These along with the redditor's username and password are to be used in the creation of a Reddit instance, example below 

On the reddit app the client_id can be found under personal use script


![alt text](reddit-instance.png "reddit instance")<br/><br/>

## Learning Outcomes
* Consume data with API wrapper
* Autofill and run HTTP request
* NLP tokenization and lammetization
* Web scraping
* Traversing the DOM
* Parse HTML 
* Format text response 
* Script automation
<br/>

## Future Development

### Create A Year Retrospective
* Stream all replies from focal-bat at year's end
* Create ranked lists of replies
    * Rank by upvotes
    * Rank by word most translated
* Include original author in lists

### Use NLP to categorize responses
* What type of words were most translated? 
    * Verbs, Nouns, Adjectives etc.<br/><br/><br/><br/>

## Created by

- [John Houlihan](https://github.com/jphoulihan "Visit John's GitHub")<br/><br/>

## License

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

