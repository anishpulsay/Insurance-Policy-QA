import os
import glob
from dotenv import load_dotenv
from pathlib import Path
import gradio as gr
from openai import OpenAI
from langchain_community.document_loaders import DirectoryLoader, TextLoader
load_dotenv(override=True)
openai_api_key = os.getenv("OPENAI_API_KEY")

MODEL = "gpt-4o-mini"
openai = OpenAI()
knowledge = {}
filenames = glob.glob("data/knowledge-base/*.md")
for filename in filenames:
    with open(filename, "r",encoding ="utf-8") as file:
        knowledge[filename] = file.read()
for filename in filenames:
    doc_type = os.path.basename(filename) 
    loader = DirectoryLoader(filename glob="**/*.md", loader_cls=TextLoader, loader_kwargs={'encoding': 'utf-8'})












