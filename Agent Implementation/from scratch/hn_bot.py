
import os
import re
import math
import json
# from google.colab import user_data

from dotenv import load_dotenv
load_dotenv()

from openai import OpenAI

from scratch_agent.react import ReactAgent
from tools import get_hn_stories, get_relevant_comments, get_story_content

def get_hb_bot(api_key:str):
    bot_system_prompt = """ You are the Singularity Incarnation of Hacker News.
    The human will ask you for information about hacker news. If you cant find any information
    about the question asked or the result is incomplete, apologies to the human and ask him if 
    you can help him with something else.

    If the human asks you to show him stories, do it using markdown tables.
    The markdown tables has the following format:

    story_id|title|url|score"""

    agent = ReactAgent(
        system_prompt = bot_system_prompt,
        tools =[get_hn_stories, get_relevant_comments, get_story_content],
        api_key = api_key

    )
    return agent


agent_instance = get_hb_bot(api_key=os.getenv("OPENAI_API_KEY"))

agent_instance.run(user_msg="what are the top stories on hacker news right now?")