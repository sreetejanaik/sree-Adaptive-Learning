# Load model directly
import os
import datasets
from pathlib import Path
from transformers import AutoTokenizer, AutoModelForCausalLM

cwd = os.getcwd()
hf_home = os.path.split(cwd)[0]
hf_home = os.path.split(hf_home)[0]
hf_home = os.path.join(hf_home, 'HuggingFace')
#print('hf_home ', hf_home)

datasets.config.DOWNLOADED_DATASETS_PATH = Path(hf_home)
datasets.config.HF_DATASETS_CACHE = Path(hf_home)
#datasets.load_datase(...)

#hf_dir = r"C:\Users\jglossner\OneDrive - Rivier University\HuggingFace"
#os.environ["HUGGINGFACE_HUB_CACHE"] = hf_home
#os.environ["TRANSFORMERS_CACHE"] = hf_home
#os.environ["HF_HOME"] = hf_home

print('environment: ', os.environ['HF_HOME'])

tokenizer = AutoTokenizer.from_pretrained("EleutherAI/llemma_7b")
model = AutoModelForCausalLM.from_pretrained("EleutherAI/llemma_7b")


# Save the downloaded model
# tokenizer.save_pretrained("./your/path/bigscience_t0")
# model.save_pretrained("./your/path/bigscience_t0")
# tokenizer = AutoTokenizer.from_pretrained("./your/path/bigscience_t0")
# model = AutoModel.from_pretrained("./your/path/bigscience_t0")

# Use pretrained model
#os.environ["HF_DATASETS_OFFLINE"] = 1
#os.environ["TRANSFORMERS_OFFLINE"] = 1
#python examples/pytorch/translation/run_translation.py --model_name_or_path google-t5/t5-small --dataset_name wmt16 --dataset_config ro-en ...

