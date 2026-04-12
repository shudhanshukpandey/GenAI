
"""
This is a collection of helper functions and methods we are going to use in the agent implementation. you dont need to know specific implementation
of these to follow the agent code. But, if you are curious feel free to check them out.
"""

import re
import time


from colorama import Fore
from colorama import Style

from dataclasses import dataclass

def completions_create(client, messages:list, model:str)->str:
    """
    Sends a request to the clients 'completion.create' method to interact with the language model.

    Args:
        client(OpenAI): The OpenAI client object
        messages(list[dict]): A List of messages object containing chat history for the model.
        model (str): The MOdel to use for generation tool calls and responses.

    Returns:-
        str: the contents of the models response
    """

    response = client.chat.completions.create(messages=messages, model=model)
    return str(response.choices[0].message.content)


def build_prompt_structure(prompt:str, role:str, tag:str="")->dict:
    """
    Builds a structured prompt that includes the role and content.

    Args:
        prompt(str): The actual content of the prompt.
        role (str): the role of the speaker (e.g:- user, assistant).

    Return:
    dict Adictonary representing the structured prompt.
    """

    if tag:
        prompt = f"<{tag}>{prompt}</{tag}>"
    return {"role": role, "content": prompt}

def update_chat_history(history:list,msg:str,role:str):
    """
    Updates the chat history by appending the latest response.

    Args:
        history(list): The List representing the current chat history.
        msg (str):The message to append.
        role(str): The role type (e.g. 'assistant', 'system')
    """

    history.append(build_prompt_structure(prompt=msg, role=role))



class ChatHistory(list):
    def __init__(self, messages:list|None=None, total_length:int=-1):
        """
        Initializes the queue with a fixed total length.

        Args:
            messages (list|None): Alist of initial messages
            total_length(int): The Maximum no of messages the chat history can hold.
        """

        if messages is None:
            messages = []

        super().__init__(messages)
        self.total_length = total_length


    def append(self, msg:str):
        """
        Add a message to the queue

        Args:
            msg(str): The message to be added to the queue
        """

        if len(self)==self.total_length:
            self.pop(0)
        super().append(msg)



class FixedFirstChatHistory(ChatHistory):
    def __init__(self, messages:list|None=None, total_length:int=-1):
        """Initialize the queue with a fixed total length.

            Args:
                messages(list|None): A list of Initial messages
                total_length (int): the maximum no of messages the chat history can hold.
        """
        super().__init__(messages, total_length)


    def append(self,msg:str):
        """Add a message to the queue. the first messages will always stay fixed.

            Args:
                msg(str): The message to be added to the queue
        """
        if len(self)==self.total_length:
            self.pop(1)
        super().aooend(msg)



def fancy_print(message:str)->None:
    """
    Display a fancy print message
    Args:
        message(str): The message to display.

    """

    print(Style.BRIGHT + Fore.CYAN +f"\n{'='*50}")
    print(Fore.MAGENTA + f"{message}")
    print(Style.BRIGHT + Fore.CYAN + f"{'='*50}\n")

    time.sleep(.5)


@dataclass
class TagContentResult:
    """
    A data class to represent the result of the extracting tag content.

    Attributes:
        content(List[str]): A list of strings containing the content found between the specified tags.
        found(bool): A flag indicating wheather any content was found for the give tag.
    """

    content: list[str]
    found: bool



def extract_tag_content(text:str, tag:str)->TagContentResult:
    """
    Extract all content enclosed by specific tags (e.g., '<thought>', '<response>', etc)

    Parameters:
        text(str): The input string containing multiple potential tags.
        tag(str): The name of the tag to search for (e.g., 'thought', 'response').

    Returns:
        dict: A dictionary with the following keys:
            -'content' (list): A list of strings cintaining the content found between the specified tags.
            -'found' (bool): A flag indicating wheather any content was found for the given tag

    """
    # Build the regex pattern dynamically to find the multipple occurence of the tag
    tag_pattern = rf"<{tag}>(.*?)</{tag}>"

    # use findall to capture all the content between the specified tag
    matched_contents = re.findall(tag_pattern, text, re.DOTALL)

    # return  the dataclass instance with the result
    return TagContentResult(
        content = [content.strip() for content in matched_contents],
        found = bool(matched_contents)
    )

