# FOCALBAT 

## Description 
_focalbat is a comment bot that translates words from English to Irish_

## Project Goal
_to promote Irish by giving the language more exposure on a platfrom comprised of 448k members_<br/><br/>

### **Requirements**
---
* use PRAW to create a reddit instance, get desired subreddit
* get top post of the day
* sort comments by top / best / controversial for example
* store comment (by len ?)
* Use spacy library to POS (part of speech) tag on the comment content
* insert first instance of Noun or Verb or Adjective into teanglann foclóir search (get request)
* if return contains a dictionary entry continue
  * else repeat POS tagging to get next Noun or Verb until dictionary contains entry
* Scrape translation and 1 example from teanglann result
* construct the focal bat response with this data
* if thread top comment contains user focal-bat it has been visited by the bot 
  * do not comment<br/>

### **Tech Used**
* Python
  * Libraries
    * PRAW
    * spacy
    * BeautifulSoup4
