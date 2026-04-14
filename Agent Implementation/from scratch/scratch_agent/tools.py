
import os
import json
import re
from dataclasses import dataclass
from typing import Callable
from openai import OpenAI

# from google.colab import userdata

def get_fn_signature(fn:Callable)->dict:
    """
    Generates the signature for a given function

    Args:
        fn(Callable): The function whose signature needs to be extracted.

    Returns:
        dict: A dictionary containing the function's name, description, and parameter types.
    """
    fn_signature = {
        "name": fn.__name__,
        "description": fn.__doc__,
        "parameters":{"properties":{}}
    }

    schema = {
        k:{"type":v.__name__} for k,v in fn.__annotations__.items() if k!='return'
    }

    fn_signature['parameters']['properties'] = schema
    return fn_signature


def validate_arguments(tool_call:dict, tool_signature:dict)->dict:
    """
    Validates and converts argument in the input dict to match the expected types.

    Args:
        tool_call(dict): A dict containing the arguments passed to the tool.
        tool_signature(dict): The expected function signature and parameter types.

    Returns:
        dict: The tool call dict with arguments converted to the correct types if necessary.

    """

    properties = tool_signature['parameters']['properties']

    # TODO: This is overly simplified but enough for simple tools

    type_mapping = {
        'int':int,
        'str':str,
        'bool':bool,
        'float':float
    }

    for arg_name, arg_value in tool_call['arguments'].items():
        expected_type = properties[arg_name].get('type')

        if not isinstance(arg_value, type_mapping[expected_type]):
            tool_call['arguments'][arg_name] = type_mapping[expected_type](arg_value)

    return tool_call


class Tool:
    """
    A class representing a tool that wraps a callable and its signature.

    Attributes:
        name(str): The name of the tool(function)
        fn(Callable): The function that the tool represents.
        fn_signature(str): json String representing the fn signature.
    """

    def __init__(self, name:str, fn:Callable, fn_signature:str):
        self.name = name
        self.fn = fn
        self.fn_signature = fn_signature

    def __str__(self):
        return self.fn_signature

    def run(self, **kwargs):
        """
        Executes the tool(function) with provided arguments.

        Args:
            **kwargs: Keyword arguments passed to the function.

        Returns:
            The result of the function.
        """

        return self.fn(**kwargs)


def tool(fn:Callable):
    """
    A decorator that wraps a function into tool object.
    Args:
        fn(Callable): The function to be wrapped.

    Returns:
        Tool: A Tool object containing the function, its name, and signature.

    """

    def wrapper():
        fn_signature = get_fn_signature(fn)

        return Tool(
            name=fn_signature.get('name'), fn=fn, fn_signature=json.dumps(fn_signature)
        )
    return wrapper()
