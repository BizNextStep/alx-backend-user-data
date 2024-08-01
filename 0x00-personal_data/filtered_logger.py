#!/usr/bin/env python3
"""
This module contains the filter_datum function for obfuscating sensitive data in log messages.
"""

import re
from typing import List

def filter_datum(fields: List[str], redaction: str, message: str, separator: str) -> str:
    """
    Obfuscates the values of specified fields in a log message.

    Args:
        fields (List[str]): A list of strings representing the fields to obfuscate.
        redaction (str): The string to replace the field values with.
        message (str): The log message containing fields to be obfuscated.
        separator (str): The character that separates fields in the log message.

    Returns:
        str: The obfuscated log message.
    """
    pattern = r'({})=([^{}]+)'.format('|'.join(fields), separator)
    return re.sub(pattern, lambda m: f"{m.group(1)}={redaction}", message)

