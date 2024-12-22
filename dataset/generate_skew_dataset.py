def insert_reads(input_file_path, output_file_path):
    try:
        with open(input_file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()

        new_lines = []
        count = 0
        for index, line in enumerate(lines):
            new_lines.append(line)
            count += 1
            if count == 3:
                read_str = " read " * 50
                new_lines.append(read_str + '\n')
                count = 0

        with open(output_file_path, 'w', encoding='utf-8') as file:
            file.writelines(new_lines)
    except FileNotFoundError:
        print(f"输入的文件路径 {input_file_path} 或 {output_file_path} 不存在，请检查后重新输入。")
    except UnicodeDecodeError:
        print(f"文件编码格式可能不正确，请确保 {input_file_path} 文件使用的是utf-8编码。")
    except Exception as e:
        print(f"出现未知错误: {e}")


if __name__ == "__main__":
    input_file_path = "dataset.txt"
    output_file_path = "skew_dataset.txt"
    insert_reads(input_file_path, output_file_path)
    print("插入操作已完成，内容已写入新文件")