#!/usr/bin/env python3
""" A module containing functions for filtering logs """
import re
from typing import List

def filter_datum(
        fields: List[str], redaction: str, message: str, separator: str) -> str:
    """ Filters a log line """
    extract, replace = (patterns['extract'], patterns['replace'])
    return re.sub(extract(fields, separator), replace(redaction), message)
