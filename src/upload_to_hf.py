from datasets import Dataset
from huggingface_hub import login
import os
import argparse

# parser = argparse.ArgumentParser()
# parser.add_argument('--token')
# args = parser.parse_args()
print (os.environ.get('HF_TOKEN'))
login(token = os.environ.get('HF_TOKEN'))

# Create a Dataset object from your CSV file
dataset = Dataset.from_csv('./data/counts_dataset.csv')

dataset.push_to_hub("tappyness1/causion")