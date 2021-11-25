# FOCAL-BAT 

## Description 
_focal-bat is a personalized word of the day comment bot_<br/><br/>
_this comment bot responds to users and translates a word they used in their comment from English to Irish_

## Project Goal
_to promote Irish by giving the language more exposure on a forum for Ireland, comprised of 448k members_<br/><br/>

### **Requirements**
---
* use PRAW to create a reddit instance, get desired subreddit
* get top post of the day
* get top comment in that post
* store comment
* Use natural language processing to get POS (part of speech) on the comment content
* insert first instance of Noun or Verb or Adjective etc. into teanglann foclóir (dictionary) search (get request)
* if return contains a dictionary entry continue
  * else repeat POS tagging to get next Noun or Verb etc. until the dictionary yields a result
* if the word pos is VERB search in Irish to English dictionary to ensure the infinitive is returned
* Use web scraping to get the dictionary result content
* construct the focal bat response with this data
  * response composed of:
    * translation
    * sample phrase
    * link to dictionary result page
* if the top post of the day already contains a focal-bat response it has been visited by the bot 
  * do not comment<br/>

### **Tech Used**
* Python
  * Libraries
    * PRAW
    * spacy
    * BeautifulSoup4
