# Global
import logging
# Transcript
import os
import numpy
import time
import whisper
import speech_recognition
import soundfile
import torch
import re
import unidecode
import openai
import json
import subprocess
import pymongo
from llama_cpp import Llama
from termcolor import colored
from queue import Queue
from datetime import datetime
from typing import List

