import json

# 读取配置文件
with open('delivery_file_definitions_config.json', 'r', encoding='utf-8') as f:
    config = json.load(f)

# 美化打印
print(json.dumps(config, indent=2, ensure_ascii=False))
