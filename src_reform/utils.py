import json
import pickle
from argparse import Namespace
from transformers import AutoModel, AutoTokenizer
import torch

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

def download_models():
    print("正在下载Luotuo-Bert")
    # Import our models. The package will take care of downloading the models automatically
    model_args = Namespace(do_mlm=None, pooler_type="cls", temp=0.05, mlp_only_train=False,
                            init_embeddings_model=None)
    model_name = "silk-road/luotuo-bert"

    model = AutoModel.from_pretrained(model_name, trust_remote_code=True, model_args=model_args).to(device)
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    print("Luotuo-Bert下载完毕")
    return model, tokenizer

def load_models():
    model_path = "luotuo-bert"  # 替换为你保存模型的路径
    print("正在加载luotuo-Bert")
    tokenizer = AutoTokenizer.from_pretrained(model_path)
    model_args = Namespace(do_mlm=None, pooler_type="cls", temp=0.05, mlp_only_train=False, init_embeddings_model=None)
    model = AutoModel.from_pretrained(model_path, trust_remote_code=True, model_args=model_args)
    print("Luotuo-Bert加载完毕")
    return model, tokenizer

def get_embedding(model, tokenizer, texts):
    # tokenizer = AutoTokenizer.from_pretrained("silk-road/luotuo-bert")
    # str or strList
    texts = texts if isinstance(texts, list) else [texts]
    # 截断
    for i in range(len(texts)):
        if len(texts[i]) > 510:
            texts[i] = texts[i][:510]
    # Tokenize the texts_source
    inputs = tokenizer(texts, padding=True, truncation=False, return_tensors="pt")
    inputs = inputs.to(device)
    # Extract the embeddings
    # Get the embeddings
    with torch.no_grad():
        embeddings = model(**inputs, output_hidden_states=True, return_dict=True, sent_emb=True).pooler_output
    print(embeddings.size())
    return embeddings[0] if len(texts) == 1 else embeddings


def pkl_to_json(filename):
    with open(filename, 'rb') as f, open(filename[:-3]+'jsonl', 'w+', encoding='utf-8') as f2:
        data = pickle.load(f)
        for k, v in data.items():
            if isinstance(v, torch.Tensor):
                v = v.numpy().tolist()
            item = {k:v}
            json.dump(item, f2, ensure_ascii=False)
            f2.write('\n')


def check(fileName):
    with open(fileName, 'rb') as f:
        print(pickle.load(f))


# check('../characters/liyunlong/pkl/dict_text.pkl')
