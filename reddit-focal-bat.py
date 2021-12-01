import os
import sys
import praw
import spacy
import random
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv

load_dotenv()
ID = os.getenv('CLIENT_ID')
SECRET = os.getenv('CLIENT_SECRET')
PASSWORD = os.getenv('PASSWORD')

nlp = spacy.load('en_core_web_sm')

def main():

    reddit = praw.Reddit(
        user_agent= "Comment Extraction (by u/USERNAME)",
        client_id= ID,
        client_secret= SECRET,
        username= "focal-bat",
        password= PASSWORD
    )

    subreddit = reddit.subreddit("botwatch").top("year", limit=1) #retrieves the top submission as limit is 1
    submission_obj = [reddit.submission(id=f'{sub}') for sub in subreddit] # stores the top thread of the day submission object
    
    if  len(submission_obj) == 0:
        sys.exit('No Thread found, exiting program')
    elif len(submission_obj[0].comments) == 0:
         sys.exit('Thread contains 0 comments, exiting program')
    
    parent = reddit.comment(f'{submission_obj[0].comments[0]}')
    parent.refresh()
    parent.replies.replace_more()
    child_comments = parent.replies.list() # all top comment replies converted to list

    #wrapping algorithm in a loop which checks if the bot has already replied, if bot username is found in child comments break, else reply
    for reply in child_comments:
        if reply.author == 'focal-bat':
            print('focal-bat reply FOUND in',len(child_comments),'replies, program exited')
            break
    else:
        print('\nfocal-bat reply NOT FOUND in',len(child_comments),'replies, continuing program...\n')

        top_comment_author = f'u/{submission_obj[0].comments[0].author}'
        top_comment_body = nlp(f'{submission_obj[0].comments[0].body}')
        word_pos_dict = {token.lemma_ : f'{token.pos_}' for token in top_comment_body } # populating a dictionary with key (lemmatization) value (part of speech) pairs 
        pos_list = ['NOUN', 'VERB', 'PROPN', 'ADJ', 'ADV', 'CCONJ']
        
        confirm_comment_has_pos = [True for pos in pos_list if pos in word_pos_dict.values()]
        if confirm_comment_has_pos.count(True) < 2: sys.exit('Not enough parts of speech in comment for dictionary search, exiting program')
        
        random.shuffle(pos_list) #increase possibility of different results

        word, formatted_translated_word, examples_scrape = dict_search(word_pos_dict, pos_list, check_verb) #makes sure the word gets valid dictionary result with examples, returns the word, html page copy and examples 
        
        raw_example_list = [ex.text for ex in examples_scrape] 
        formatted_example_list = []
        for example_str in raw_example_list:
            for symbol in example_str:
                if ord(symbol) == 187: #phrases begin after right double angle quotes, filter by the ascii value for formatting
                    formatted_example_list.append(example_str[slice(example_str.index(symbol)+1, len(example_str))].strip()) #substring of raw example added to formatted list 

        print(formatted_example_list)

        random_example_sentence = formatted_example_list[random.randrange(len(formatted_example_list))]
            
        searched_word = f'''"{word}"'''
        reply = f'{top_comment_author}, seo duit an focal {searched_word} as gaeilge: {formatted_translated_word}'
        example = f'Sampla gaolmhara (Related example): {random_example_sentence}'
        search_further = f'https://www.teanglann.ie/en/eid/{word}'
    
        print('focal_bat reply: \n')
        print(f'{reply}\n{example}\nLike to learn more? Go on, go on, go on...{search_further}')
        lb='\n\n'

        #reply for reddit
        focal_bat_reply = f'{reply}{lb}{example}{lb}Like to learn more? Go on, go on, go on... {search_further}'
        #parent.reply(focal_bat_reply)


#checks if word is in part of speech list and ensures word returns an accurate translation and example phrases from online dictionary
def dict_search(word_dict, pos_list, check_verb):

    word_search_fail = ['ireland', 'Ireland', 'Irish', 'irish'] 
    for word, pos in word_dict.items():
            if pos in pos_list:
                if word in word_search_fail:
                    continue
                page_eng_to_irish = requests.get(f'https://www.teanglann.ie/en/eid/{word}') # Getting page_eng_irish HTML through request
                soup = BeautifulSoup(page_eng_to_irish.content, 'html5lib')
                examples_scrape = soup.find_all('div', attrs={'class': 'ex'}, limit=20) #get example phrases here, if none add word to fail list
                if len(word) <= 2 or soup.find('div', attrs={'class': 'nojoy'}) or len(examples_scrape) == 0:
                    word_search_fail.append(word)
                    continue
                translation_scrape = soup.find('span', attrs={'class': 'eid trg clickable'})
                translated_word_list = translation_scrape.text.split()
                stopwords = ['m', 'f']
                nogender_translated_word_list = [w for w in translated_word_list if w not in stopwords]
                translated_word = " ".join(nogender_translated_word_list)
                
                if word.lower() == translated_word.lower(): #handle the ocassion that english and irish are same word
                    word_search_fail.append(word)
                    continue
                break

    if word_dict.get(word) == 'VERB': 
        translated_word = check_verb(word, translated_word)
    
    return word, translated_word, examples_scrape


#caveat in dictionary search result, for verbs the first person present conjunction is often returned and not the infinitive, this function should ensure infinitive is returned 
def check_verb(verb, formatted_translated_word):

    page_irish_eng = requests.get(f'https://www.teanglann.ie/en/fgb/{verb}')
    check_soup = BeautifulSoup(page_irish_eng.content, 'html5lib')

    check_translation_scrape = check_soup.find_all('span', attrs={'class': 'head'})

    check_translation_list = [trans.text for trans in check_translation_scrape] 
    irish_eng_list = []
    for s in check_translation_list:
        for symbol in s:
            if ord(symbol) == 187: #irish translated result comes before this symbol, use as end marker for substring
                irish_eng_list.append(s[slice(0, s.index(symbol)-1)].strip()) #substring of raw example added to formatted list 

    for verb_infinitive in irish_eng_list:
            if verb_infinitive.lower() in formatted_translated_word.lower(): #eliminates the conjugated suffix
                return verb_infinitive
            else:
                return formatted_translated_word    
    

if __name__ == "__main__":
    main()






