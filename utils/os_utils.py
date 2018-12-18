import os


def list_files(dir_path, approved_extensions):
    approved_files = list()
    for root, dirs, files in os.walk(dir_path):
        for f in files:
            extension = os.path.splitext(f)[1]
            if extension in approved_extensions:
                file_path = os.path.join(root, f)
                approved_files.append(file_path)
    return approved_files


def get_file_name(path):
    base_name = os.path.basename(path)
    file_name = os.path.splitext(base_name)[0]
    return file_name


def main():
    print(get_file_name(__file__))


if __name__ == '__main__':
    main()
