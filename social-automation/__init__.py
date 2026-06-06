#!/usr/bin/env python3
"""
Social Media Automation Package
Automates cross-platform content distribution for blog posts
"""

__version__ = "1.0.0"
__author__ = "Victor Kipruto Rop"

from dispatcher import SocialDispatcher
from formatter import ContentFormatter
from linkedin import LinkedInPoster
from twitter import TwitterPoster
from devto import DevtoPoster
from medium import MediumPoster
from telegram import TelegramPoster

__all__ = [
    "SocialDispatcher",
    "ContentFormatter",
    "LinkedInPoster",
    "TwitterPoster",
    "DevtoPoster",
    "MediumPoster",
    "TelegramPoster"
]
