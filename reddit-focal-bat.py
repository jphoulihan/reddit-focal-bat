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
USERNAME = os.getenv('USERNAME')

nlp = spacy.load('en_core_web_sm')

def main():


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
            print('focal_bat response FOUND in',len(child_comments),'replies, program exited')
            break
    else:
        print('\nfocal_bat response NOT FOUND in',len(child_comments),'replies, continuing program...\n')
        top_comment_author = 'u/'+str(sub_obj[0].comments[0].author)
        top_comment_body = nlp(f'{sub_obj[0].comments[0].body}') # top comment body processed by spacy nlp
        # test_string_body = nlp('there was a teleporting thingamajig in the ufo, I shudda chucked it in the fryer, yesterday')

        word_pos = {}
        #test string loop
        # for token in test_string_body:
        for token in top_comment_body:
            word_pos[token.lemma_] = f'{token.pos_}' # populating a dictionary with key (lemmatization) value (part of speech) pairs 
        
        print('Top comment from top post of the day, after part of speech word processing: \n')
        print(word_pos)
        print('\n')

        #if soup page.content has div class 'nojoy' append the searched word to fail list, move to next word_pos translation search
        word_searched_fail = [] 
        pos_list = ['NOUN', 'VERB', 'PROPN', 'ADJ', 'ADV', 'CCONJ', 'DET']

        print(pos_list)
        random.shuffle(pos_list)
        print(pos_list)
        print('\n')

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
        translated_word = str(translation_scrape.text.partition(' ')[0])

        print(f'BÉARLA {word}, GAEILGE {translated_word}\n')

        raw_example_list = [ex.text for ex in examples_scrape] 
        formatted_example_list = []
        for example_str in raw_example_list:
            for symbol in example_str:
                if ord(symbol) == 187:
                    new_str = slice(example_str.index(symbol)+1, len(example_str))
                    formatted_example_list.append(example_str[new_str].strip())

        print('Sentence example list for response :\n')
        print(formatted_example_list)
        print('\n')

        random_example_sentence = formatted_example_list[random.randrange(len(formatted_example_list))] 
            
        response = str(top_comment_author)+', seo duit an focal '+searched_word+' as gaeilge: '+translated_word
        example = f'Mar shampla: {random_example_sentence}'
        search_further = f'https://www.teanglann.ie/en/eid/{word}'
    
        print('focal_bat response: \n')
        print(response+'\n'+example+'\nLike to learn more? Go on, go on, go on...', search_further)
        
    
if __name__ == "__main__":
    main()






