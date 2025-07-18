from transformers import AutoModel, AutoTokenizer

# 加载本地模型
model_path = "./text2vec-base-local"
tokenizer = AutoTokenizer.from_pretrained(model_path)
model = AutoModel.from_pretrained(model_path)

# 验证模型加载成功
print("模型加载成功!")
print(f"Tokenizer: {type(tokenizer)}")
print(f"Model: {type(model)}")