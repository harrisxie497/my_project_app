import os
import glob

# 查找JSON配置文件
config_files = glob.glob('**/delivery_*.json', recursive=True)
print("找到的配置文件:")
for f in config_files:
    print(f"  {f}")
    print(f"  大小: {os.path.getsize(f)} bytes")
