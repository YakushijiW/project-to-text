# decode_project.py
import os
import hashlib
import configparser
import argparse
import shutil
from pathlib import Path
import time

def get_sha256(file_path):
    """计算文件的SHA256哈希值"""
    sha256 = hashlib.sha256()
    try:
        with open(file_path, "rb") as f:
            while chunk := f.read(8192):
                sha256.update(chunk)
        return sha256.hexdigest()
    except IOError:
        return None

def decode_project(source_file, output_dir, backup_enabled):
    """
    解码项目文件.
    """
    print("========== 配置信息 ==========")
    print(f"源文件: {source_file}")
    print(f"输出目录: {output_dir}")
    print(f"备份现有文件: {'是' if backup_enabled else '否'}")
    print("==============================")
    print()

    if not os.path.exists(source_file):
        print(f"[错误] 源文件不存在: {source_file}")
        return

    output_path = Path(output_dir)

    # 备份现有文件
    if backup_enabled and output_path.exists() and any(output_path.iterdir()):
        timestamp = time.strftime("%Y-%m-%d_%H-%M-%S")
        backup_dir = output_path.parent / f"{output_path.name}_backup_{timestamp}"
        try:
            shutil.move(str(output_path), str(backup_dir))
            print(f"[信息] 成功备份现有文件到: {backup_dir}")
            output_path.mkdir(parents=True, exist_ok=True)
        except Exception as e:
            print(f"[错误] 备份失败: {e}")
            return
    else:
        output_path.mkdir(parents=True, exist_ok=True)
        
    print("[信息] 开始解析源文件...")
    print()
    
    file_count = 0
    dir_count = 0
    
    DELIMITER = "// =========================================="
    FILE_PREFIX = "// 文件: "
    SHA_PREFIX = "// SHA256: "
    
    files_to_verify = []

    try:
        with open(source_file, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()

        in_header = False
        current_file_path = None
        current_file_content = []

        for line in lines:
            stripped_line = line.strip()

            if stripped_line == DELIMITER:
                if in_header: # 头部结束
                    in_header = False
                    if current_file_path:
                        # 将内容写入文件
                        full_path = output_path / current_file_path
                        full_path.parent.mkdir(parents=True, exist_ok=True)
                        with open(full_path, 'w', encoding='utf-8') as out_f:
                            out_f.writelines(current_file_content)
                        current_file_content = []

                else: # 新文件开始
                    in_header = True
                    current_file_path = None
                continue

            if in_header:
                if line.startswith(FILE_PREFIX):
                    relative_path = line[len(FILE_PREFIX):].strip()
                    current_file_path = Path(relative_path)
                    print(f"[创建] {relative_path}")
                    file_count += 1
                elif line.startswith(SHA_PREFIX):
                    expected_hash = line[len(SHA_PREFIX):].strip()
                    if current_file_path:
                         files_to_verify.append({
                             "path": current_file_path, 
                             "hash": expected_hash
                        })
            elif current_file_path:
                 # 不在头部，是文件内容
                 current_file_content.append(line)


    except Exception as e:
        print(f"[严重错误] 解码过程中发生错误: {e}")
        return

    print()
    print("========== 解码完成 ==========")
    # 目录数可以在验证时统计
    print(f"还原文件数: {file_count}")
    print(f"输出目录: {output_dir}")
    print("==============================")
    print()

    # --- 文件完整性校验 ---
    input("按回车键开始文件完整性校验...")
    print()
    print("[校验] 开始进行文件完整性校验...")
    
    success_count = 0
    failed_count = 0

    for item in files_to_verify:
        relative_path = item['path']
        expected_hash = item['hash']
        full_path = output_path / relative_path

        print(f"[校验中] {relative_path.as_posix()}")
        if not full_path.exists():
            print("   └─ [失败] 文件未找到!")
            failed_count += 1
            continue

        actual_hash = get_sha256(full_path)

        if actual_hash == expected_hash:
            print("   └─ [成功] 哈希匹配")
            success_count += 1
        else:
            print("   └─ [失败] 哈希不匹配!")
            print(f"      ├─ 期望值: {expected_hash}")
            print(f"      └─ 计算值: {actual_hash}")
            failed_count += 1
    
    print()
    print("========== 校验完成 ==========")
    print(f"共校验文件数: {len(files_to_verify)}")
    print(f"成功: {success_count}")
    print(f"失败: {failed_count}")
    print("==============================")

def main():
    config = configparser.ConfigParser()
    config.read('config.ini', encoding='utf-8')
    
    defaults = config['DEFAULT']
    
    parser = argparse.ArgumentParser(description="微信小程序项目文件解码工具 (Python版)")
    parser.add_argument("source_file", nargs="?", default=defaults.get('SOURCE_FILE', 'encoded_project.txt'),
                        help="要解码的源文件 (默认: encoded_project.txt)")
    parser.add_argument("output_dir", nargs="?", default=defaults.get('OUTPUT_DIR', 'decoded_project'),
                        help="解码后输出的目录 (默认: decoded_project)")
    
    args = parser.parse_args()

    backup_str = defaults.get('BACKUP', 'yes').lower()
    backup_enabled = backup_str == 'yes'

    decode_project(args.source_file, args.output_dir, backup_enabled)

if __name__ == "__main__":
    main()