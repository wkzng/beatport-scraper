from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
from enum import Enum
from typing import Union


import traceback
import json
import os
import re



class ExecutionStatus(int, Enum):
    SUCCESS = 200
    FAILURE = 400
    MISSING_URL = 401
    INVALID_URL = 402




def is_valid_beatport_url(url:str) -> bool:
    """ Checks if a URL is a valid Beatport URL.
        Args:
            url (str): The URL to check.
        Returns:
            bool: True if the URL is a valid Beatport URL, False otherwise.
    """
    # Define the pattern for a valid Beatport URL
    #pattern = r"^https?://(?:www\.)?beatport\.com/(?:track|release|artist)/[a-zA-Z0-9_-]+$"
    pattern = r"^https?://(?:www\.)?beatport\.com/(?:track|release|artist)/[a-zA-Z0-9-_/]+/\d+$"
    # Use regular expression to match the URL
    return bool(re.match(pattern, url))



def extract_lofi_url(html_content:str) -> Union[None, str]:
    """ Checks if a URL is a valid Beatport URL.
        Args:
            url (str): The URL to check.
        Returns:
            bool: True if the URL is a valid Beatport URL, False otherwise.
    """
    try:
        # Parse HTML and get script tag content
        soup = BeautifulSoup(html_content, 'html.parser')
        script_tag = soup.find('script', id='__NEXT_DATA__')
        
        if not script_tag:
            raise ValueError("Could not find script tag with id '__NEXT_DATA__'")
        
        # Define pattern to match "sample_url":"<url ending with LOFI.mp3>"
        pattern = r'"sample_url"\s*:\s*"([^"]*?LOFI\.mp3)"'
        
        # Search for the pattern in the script content
        match = re.search(pattern, script_tag.string, re.IGNORECASE)
        
        if match:
            return match.group(1)  # Return the captured URL
        return None
    except:
        message = traceback.format_exc()
        print(message)
        return None



def extract_audio_metadata(url: str) -> dict:
    """ Fetch the Beatport audio data from url """
    try :
        #parse the beatport url
        req = Request(url=url, headers={'user-agent':'tcProc'})
        res = urlopen(req)
        soup = BeautifulSoup(res, "lxml")       
 
        #extract the download url and thumbnail
        results = {
            #"audio_url" : "twitter:player:stream",
            "image_url" : "twitter:image",
            "title" : "twitter:title",
        }
        for k, v in results.items():
            tags = soup.find_all("meta", {"name":v})
            results[k] = tags[0].get("content", None) if tags else None

        html = soup.prettify("utf-8")
        results["audio_url"] = extract_lofi_url(html)

        results["platform"] = "beatport"
        results["url"] = url
        return {"status":ExecutionStatus.SUCCESS, "data":results}
    except Exception as e:
        message = traceback.format_exc()
        print(url, message)
        return {"status":ExecutionStatus.FAILURE, 'message':"The track might be unavailable at this time or has been removed from beatport."}



def main(event:dict, context:dict):
    url = event.get("url")
    if not url:
        return {
            "status":ExecutionStatus.MISSING_URL, 
            'message':f"Input event is missing a 'url' key"
        }
    elif not is_valid_beatport_url(url):
        print(url)
        return {
            "status":ExecutionStatus.INVALID_URL, 
            'message':f"Input url is not a valid beatport url. For information, valid audio track typically starts with https://www.beatport.com/track/"
        }
    return extract_audio_metadata(url)



if __name__ == '__main__':
    from pprint import pprint

    url = "https://www.beatport.com/track/never-get-enough/15766697"
    url = "https://www.beatport.com/track/junin-shane-robinson-remix/7226500"
    #url = "https://www.beatport.com/track/causality/17017979"
    #url = "https://www.beatport.com/track/paraglider/16797299"
    #url = "https://www.beatport.com/track/kumnyama/15777212"
    #url = "https://www.youtube.com/watch?v=die1U9GMrfs&ab_channel=TheG%CE%94mesWePl%CE%94y"
    #url = "https://www.youtube.com/watch?v=7oxGkCXX5KA&ab_channel=X-Sound"
    #url = "https://www.beatport.com/track/it-goes-like-nanana/17839150"
    #url = "AD"

    event = {"url":url}
    r = main(event, context=None)
    pprint(r)

 