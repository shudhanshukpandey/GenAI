import json
import requests
from bs4 import BeautifulSoup
from scratch_agent.tools import tool

BASE_URL = "https://hacker-news.firebaseio.com/v0"

def fetch_item(item_id:int):
    """
    Fetches details of a story by its ID.
    Args:
        item_id(int): The Id of the item to fetch.
    Returns:
        dict: Details of the story.
    """

    url = f"{BASE_URL}/item/{item_id}.json"
    response = requests.get(url)

    return response.json()


def fetch_story_ids(story_type:str='top', limit:int=None):
    """
    Fetches the top story IDs.

    Args:
        story_type: the story type. Defaults to top('topstories.json')
        limit: the limit of stories to be fetched.

    Returns:
        List[int]: A list of top story IDs

    """
    url = f"{BASE_URL}/{story_type}stories.json"

    response = requests.get(url)

    story_ids = response.json()

    if limit:
        story_ids = story_ids[:limit]

    return story_ids


def fetch_text(url:str):
    """
    Fetches the text from a url (if theres text to be fetched). if it fails,
    it will return an informative message to the llm

    Args:
        url: the story url.
    Returns:
        A string representing whether the story text ir an informative error(represented as string)
    """

    try:
        response = requests.get(url)

        if response.status_code==200:

            html_content = response.content
            soup = BeautifulSoup(html_content, 'html.parser')
            text_content = soup.get_text()

            return text_content
        else:
            return f"Unable to fetch content from {url}. Status code ={response.status_code} "
    except Exception as e:
        return f"An error occured: {e}"





@tool
def get_hn_stories(limit: int=5, story_type: str="top"):
    """
    Fetches the top Hacker News Stories Based on the provided parameters.

    Args:
        limit(int): The number of the top stories to retrieve. Default is 10.
        keywords(List[str]): A list of keywords to filter the top storeis.
        story_type(str): The story type

    Returns:
        list[Dict[str,union[str,int]]]: A list of dict containing story_id, title, url and score of the stories.
    """

    if limit:
        story_ids = fetch_story_ids(story_type, limit)

    else:
        story_ids = fetch_story_ids(story_type)

    def fetch_and_filter_stories(story_id):
        return fetch_item(story_id)

    stories = [fetch_and_filter_stories(story_id) for story_id in story_ids]
    formatted_stories = []

    for story in stories:
        story_info = {
            "title":story.get('title'),
             "url":story.get('url'),
             "score":story.get('score'),
             "story_id":story.get('story_id'),
        }
        formatted_stories.append(story_info)

    return formatted_stories[:limit]



@tool
def get_relevant_comments(story_id: int, limit: int=10):
    """
    Get the most relevant comments for a hacker news item

    Args:
        story_id: the id of the hn item
        limit: no of commentsbto retrieve (default to 10)

    Returns:
        A list of dict, each containing comment details
    """
    story =fetch_item(story_id)

    if 'kids' not in story:
        return "this item does not have comments"

    comment_ids = story['kids']

    comment_details = [fetch_item(cid) for cid in comment_ids]
    comment_details.sort(key=lambda coment: coment.get('score', 0), revese=True)

    relevent_comments = comment_details[:limit]
    relevent_comments = [comment['text'] for comment in relevent_comments]

    return json.dumps(relevent_comments)


@tool
def get_story_content(story_url:str):
    """
    gets the content of the story
    Args:
        story_url: url of story
    Returns:
        the content of story
    """
    return fetch_text(story_url)

