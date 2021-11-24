from re import S
import requests
import spacy
import praw
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os

load_dotenv()

nlp = spacy.load('en_core_web_sm')

def main():

    ID = os.getenv('CLIENT_ID')
    SECRET = os.getenv('CLIENT_SECRET')
    USERNAME = os.getenv('USERNAME')

    reddit = praw.Reddit(
        user_agent= "Comment Extraction (by u/USERNAME)",
        client_id= ID,
        client_secret= SECRET,
        username= "focal-bat",
        password= USERNAME
    )

    sub_obj = [] # stores the top thread of the day submission object
    subreddit = reddit.subreddit("ireland").top("week", limit=1) #retrieves the top submission as limit is 1

    for submission in subreddit:
        sub_obj.append(reddit.submission(id=f'{submission}'))

    parent = reddit.comment(f'{sub_obj[0].comments[0]}')
    parent.refresh()
    parent.replies.replace_more()
    child_comments = parent.replies.list() # all top comment replies converted to list

    #wrapping algorithm in a loop which checks if the bot has already replied, if bot username is found in child comments, break else reply
    for reply in child_comments:
        if reply.author == 'focal_bat':
            print('focal_bat response FOUND in',len(child_comments),'replies')
            break
    else:
        print('focal_bat response NOT FOUND in',len(child_comments),'replies\n')
        top_comment_author = 'u/'+str(sub_obj[0].comments[0].author)
        top_comment_body = nlp(f'{sub_obj[0].comments[0].body}') # top comment body processed by spacy nlp
        test_string_body = nlp('there was a teleporting gadget in the ufo in the garden, yesterday')

        word_pos = {}
        pos_list = ['NOUN', 'VERB', 'PROPN', 'ADJ']
        #test string loop
        # for token in test_string_body:
        for token in top_comment_body:
            word_pos[token.lemma_] = f'{token.pos_}' # populating a dictionary with key (lemmatization) value (part of speech) pairs 
        
        print(word_pos)

        #if soup page.content has div class 'nojoy' append the searched word to fail list
        word_searched_fail = [] 
        for word, pos in word_pos.items():
            if pos in pos_list:
                if word in word_searched_fail:
                    continue
                searched_word = f'''"{word}"''' #qoutationed string which will form part of response
                page = requests.get(f'https://www.teanglann.ie/en/eid/{word}') # Getting page HTML through request
                soup = BeautifulSoup(page.content, 'html5lib') # Parsing content using beautifulsoup
                if soup.find('div', attrs={'class': 'nojoy'}):
                    word_searched_fail.append(word)
                    continue
                break
            
            
        translation_scrape = soup.find('span', attrs={'class': 'eid trg clickable'})
        examples_scrape = soup.find_all('div', attrs={'class': 'ex'}, limit=10)

        translation = str(translation_scrape.text.partition(' ')[0])
        # print(type(translation))
        print(translation.lower())

        

        raw_example_list = [ex.text for ex in examples_scrape]
        
        for count, value in enumerate(raw_example_list):
            print(count, value.strip())
        
        for i in raw_example_list:
            for j in i:
                if translation.lower() in j:
                    print(j)
                    break
            
        response = str(top_comment_author)+', seo duit an focal '+searched_word+' as gaeilge: '+translation_scrape.text.partition(' ')[0]
        search_further = f'https://www.teanglann.ie/en/eid/{word}'
    
        print('focal_bat repsonse: \n')
        print(response+'\nLike to learn more? Go on, go on, go on...', search_further)
        
    
if __name__ == "__main__":
    main()






