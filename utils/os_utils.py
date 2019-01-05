import os
from datetime import datetime
from shutil import copyfile

from utils import constants


def list_files(dir_path, approved_extensions=None, ignore_dirs=None):
    if approved_extensions is None:
        approved_extensions = list()
    if isinstance(approved_extensions, str):
        approved_extensions = [approved_extensions]

    if ignore_dirs is None:
        ignore_dirs = list()
    if isinstance(ignore_dirs, str):
        ignore_dirs = [ignore_dirs]

    approved_files = list()
    for root, dirs, files in os.walk(dir_path):
        for f in files:
            extension = os.path.splitext(f)[1]
            if extension in approved_extensions:
                file_path = os.path.join(root, f)
                # TODO: Verify whether this file in ignore dirs or not. Try to think better way
                dir_name = os.path.basename(os.path.dirname(f))
                if dir_name in ignore_dirs:
                    continue
                approved_files.append(file_path)
    return approved_files


def get_file_name(path):
    base_name = os.path.basename(path)
    file_name = os.path.splitext(base_name)[0]
    return file_name


def get_extension(path):
    return os.path.splitext(path)[1]


def create_writer(path, backup_dir=None):
    if os.path.exists(path):
        if backup_dir is None:
            backup_dir = os.path.join(os.path.dirname(path), constants.DEFAULT_BACKUP_DIR)
        if not os.path.exists(backup_dir):
            os.makedirs(backup_dir)
        time_str = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_file = get_file_name(path) + '_' + time_str + get_extension(path)
        backup_file = os.path.join(backup_dir, backup_file)
        copyfile(path, backup_file)

        os.remove(path)

    return open(path, 'w')


def main():
    # writer = create_writer('../data/english_grammar.txt')
    # print(get_file_name(__file__))
    txt_files = list_files('../..', '.txt')
    for f in txt_files:
        print(f)


if __name__ == '__main__':
    main()
