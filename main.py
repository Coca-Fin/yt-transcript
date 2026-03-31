from os import makedirs
from os.path import (dirname, exists)
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.proxies import WebshareProxyConfig

YT_API = YouTubeTranscriptApi()

def get_text(video_id:str, language:str):

    result = YT_API.list(video_id)\
                        .find_transcript(language)\
                        .fetch().to_raw_data()  
    text = ''
    for i in result:
        text += i['text']+'\n'
    return text

def get_text_translated(video_id:str, language:str, translate:str) -> str:
    
    result = YT_API.list(video_id)\
                        .find_transcript(language)\
                        .translate(translate)\
                        .fetch().to_raw_data()
    text = ''
    for i in result:
        text += i['text']+'\n'
    return text

def save(text:str, path='transcript.txt') -> None:
    '''
    Check path and write transcript to .txt
    Args:
        path (str): path to save directory file
    '''
    directory = dirname(path)
    
    if directory and not exists(directory):
        makedirs(directory, exist_ok=True)
    
    with open(path, 'w', encoding='utf-8') as file:
        file.write(text)

def load_params(path:str) -> dict:
    '''
    Args:
        path (str): path to .ini file
    '''
    settings = {}
    try:
        with open(path, 'r', encoding='utf-8') as file:
            for line in file:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue

                if '=' in line:
                    key, value = line.split('=', 1)
                    key = key.strip()
                    value = value.strip()
                settings[key] = value
    except FileNotFoundError:
        with open(path, 'w', encoding='utf-8') as file:
            _text = 'languages = en\ntranslate = ru\ndirectory = transcripts/' 
            file.write(_text)
        settings = load_params(path)
    except Exception as e:
        print(e)

    return settings



while True:
    languages, translate, path = load_params('settings.ini').values()
    video_id = input('video id: ')
    name = input('name of transcript: ') + '.txt'
    languages = languages.split(',')
    path = path + name    
    try:
        if translate == '':
            text = get_text(video_id, languages)
        else:
            text = get_text_translated(video_id, languages, translate)
        save(text, path)
    except Exception as e:
        print('get_text error:', e)
    input("\n\nsomthing' happened :)\n")
