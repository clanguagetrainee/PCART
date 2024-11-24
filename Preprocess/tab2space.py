import os

# 函数：递归处理目录
def process_directory(directory):
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".py"):
                file_path=os.path.join(root, file)
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
                modified_content = content.replace("\t"," "*4)
                with open(file_path, "w", encoding="utf-8")as f:
                    f.write(modified_content)

target_dir="../Copy"

# 开始处理目录
process_directory(target_dir)
