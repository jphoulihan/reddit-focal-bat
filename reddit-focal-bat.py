import os
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

    subreddit = reddit.subreddit("ireland").top("day", limit=1) #retrieves the top submission as limit is 1
    submission_obj = [reddit.submission(id=f'{sub}') for sub in subreddit] # stores the top thread of the day submission object
    
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
        top_comment_body = nlp(f'{submission_obj[0].comments[0].body}') # top comment body processed by spacy nlp

        print(type(top_comment_body))

        word_pos = {token.lemma_ : f'{token.pos_}' for token in top_comment_body } # populating a dictionary with key (lemmatization) value (part of speech) pairs 
        
        print('Top comment from top post of the day, after part of speech word processing: \n')
        print(word_pos)
        print('\n')

        pos_list = ['NOUN', 'VERB', 'PROPN', 'ADJ', 'ADV', 'CCONJ']
        random.shuffle(pos_list) #increase possibility of different results
        

        word, formatted_translated_word, examples_scrape = dict_search(word_pos, pos_list, check_verb) #makes sure the word gets valid dictionary result with examples, returns the word, html page copy and examples 

        searched_word = f'''"{word}"'''

        print('Formatted translation: ',formatted_translated_word)
        print('\n')
        print(f'BÉARLA {word}, GAEILGE {formatted_translated_word}\n')

        raw_example_list = [ex.text for ex in examples_scrape] 
        formatted_example_list = []
        for example_str in raw_example_list:
            for symbol in example_str:
                if ord(symbol) == 187: #phrases begin after right double angle quotes, filter by the ascii value for formatting
                    formatted_example_list.append(example_str[slice(example_str.index(symbol)+1, len(example_str))].strip()) #substring of raw example added to formatted list 

        print('Sentence example list for reply :\n')
        print(formatted_example_list)
        print('\n')

        random_example_sentence = formatted_example_list[random.randrange(len(formatted_example_list))] 
            
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
    formatted_translated_word = ''

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
                break
    
    translation_scrape = soup.find('span', attrs={'class': 'eid trg clickable'})
    translated_word= str(translation_scrape.text).split()
    formatted_translated_word = ' '.join([('' if char in set("mf") else ' ')+char for char in translated_word]).strip() #NEEDS FIXING

    if word_dict.get(word) == 'VERB': formatted_translated_word = check_verb(word, formatted_translated_word)

    return word, formatted_translated_word, examples_scrape


#caveat in dictionary search result, for verbs the first person present conjunction is often returned and not the infinitive, this function should ensure infinitive is returned 
def check_verb(verb, formatted_translated_word):

    verb_infinitive = ''
    page_irish_eng = requests.get(f'https://www.teanglann.ie/en/fgb/{verb}')
    check_soup = BeautifulSoup(page_irish_eng.content, 'html5lib')

    check_translation_scrape = check_soup.find_all('span', attrs={'class': 'head'})

    check_translation_list = [ex.text for ex in check_translation_scrape] 
    irish_eng_list = []
    for s in check_translation_list:
        for symbol in s:
            if ord(symbol) == 187: #phrases begin after right double angle quotes, filter by the ascii value for formatting
                irish_eng_list.append(s[slice(0, s.index(symbol)-1)].strip()) #substring of raw example added to formatted list 
    
    for val in irish_eng_list:
            if val.lower() in formatted_translated_word.lower():
                verb_infinitive = val
            break
    
    return verb_infinitive


if __name__ == "__main__":
    main()






