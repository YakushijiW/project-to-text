# encode_project.py
import os
import hashlib
import configparser
import argparse
from pathlib import Path

def get_sha256(file_path):
    """计算文件的SHA256哈希值"""
    sha256 = hashlib.sha256()
    try:
        with open(file_path, "rb") as f:
            while chunk := f.read(8192):
                sha256.update(chunk)
        return sha256.hexdigest()
    except IOError as e:
        print(f"  [错误] 无法读取文件以计算哈希: {file_path} - {e}")
        return None

def encode_project(target_dir, output_file, file_types, exclude_dirs):
    """
    编码项目文件.
    """
    print("========== 配置信息 ==========")
    print(f"目标目录: {target_dir}")
    print(f"输出文件: {output_file}")
    print(f"文件类型: {', '.join(file_types)}")
    print(f"排除目录: {', '.join(exclude_dirs)}")
    print("==============================")
    print()

    if not os.path.isdir(target_dir):
        print(f"[错误] 目标目录不存在: {target_dir}")
        return

    # 删除已存在的输出文件
    if os.path.exists(output_file):
        os.remove(output_file)
        print(f"[信息] 已删除旧文件: {output_file}")

    file_count = 0
    error_count = 0
    
    # 规范化排除目录为路径对象
    exclude_paths = {Path(target_dir, d).resolve() for d in exclude_dirs}

    print("[信息] 开始搜索并处理文件...")
    print()
    
    # 使用 Path.glob 查找所有文件
    target_path_obj = Path(target_dir)

    all_files = []
    for ext in file_types:
        all_files.extend(target_path_obj.rglob(f'*.{ext}'))
        
    for file_path_obj in all_files:
        try:
            # 检查是否应排除
            if any(p in file_path_obj.resolve().parents for p in exclude_paths):
                continue
            
            relative_path = file_path_obj.relative_to(target_path_obj).as_posix()
            print(f"[找到] {relative_path}")

            file_hash = get_sha256(file_path_obj)
            if not file_hash:
                error_count += 1
                continue

            with open(output_file, 'a', encoding='utf-8') as out_f:
                out_f.write("\n")
                out_f.write("// ==========================================\n")
                out_f.write(f"// 文件: {relative_path}\n")
                out_f.write(f"// SHA256: {file_hash}\n")
                out_f.write("// ==========================================\n")
                out_f.write("\n")

                try:
                    with open(file_path_obj, 'r', encoding='utf-8', errors='ignore') as in_f:
                        out_f.write(in_f.read())
                    file_count += 1
                except Exception as e:
                    print(f"  [警告] 无法读取文件内容: {relative_path} - {e}")
                    error_count += 1
        except Exception as e:
            print(f"  [严重错误] 处理文件时发生未知错误: {file_path_obj} - {e}")
            error_count += 1

    print()
    print("========== 处理完成 ==========")
    print(f"成功处理文件数: {file_count}")
    print(f"遇到错误数: {error_count}")
    print(f"输出文件已生成: {output_file}")
    print("==============================")


def main():
    config = configparser.ConfigParser()
    config.read('config.ini', encoding='utf-8')
    
    defaults = config['DEFAULT']

    parser = argparse.ArgumentParser(description="微信小程序项目文件编码工具 (Python版)")
    parser.add_argument("target_dir", nargs="?", default=defaults.get('TARGET_DIR', '.'),
                        help="要编码的小程序项目目录 (默认: 当前目录)")
    parser.add_argument("output_file", nargs="?", default=defaults.get('OUTPUT_FILE', 'encoded_project.txt'),
                        help="编码后输出的单个文件名 (默认: encoded_project.txt)")
    
    args = parser.parse_args()

    file_types = defaults.get('FILE_TYPES', 'wxml js wxss wxs json').split()
    exclude_dirs = defaults.get('EXCLUDE_DIRS', 'node_modules dist build .git unpackage').split()

    encode_project(args.target_dir, args.output_file, file_types, exclude_dirs)

if __name__ == "__main__":
    main()