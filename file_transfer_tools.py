import os
import shutil as sh
import time
import uuid
import datetime

root_paths = []
dest_folder = "./"
extensions = []
timeout = 0
existingFiles = []


def main():
    global root_paths
    global dest_folder
    global extensions
    global timeout
    global existingFiles
    while True:
        root_paths = input("Input path to root folders seperated by semicolon(i.e. "
                           "C:\Downloads);C:\Pictures;D:\Photos;etc...: ").split(";")
        dest_folder = input("Input destination folder(i.e. C:\Destination): ")
        for path in root_paths:
            if not os.path.exists(path):
                print('Invalid root path {0}\n'.format(path))
        else:
            if not os.path.exists(dest_folder):
                print('Invalid destination folder {0}\n'.format(dest_folder))
            else:
                extensions = input(
                    "Enter extension(s) to search for seperated by semicolon(i.e. \".jpg;.tif;.png\"): ").split(";")
                timeout = float(input("Enter timeout in seconds: "))
                break

    while True:
        if len(os.listdir(dest_folder)) == 0:
            print('Traversing {0} {1}...'.format(path, datetime.datetime.now()))
            for dirpath, dnames, fnames in os.walk(path):
                for f in fnames:
                    deal_with_dupes_single(dest_folder, dirpath, extensions, f)
                    break
                break
        for path in root_paths:
            print('Traversing {0} {1}...'.format(path, datetime.datetime.now()))
            for dirpath, dnames, fnames in os.walk(path):
                for f in fnames:
                    deal_with_dupes(dest_folder, dirpath, extensions, f)

        print('End cycle\n')
        time.sleep(timeout)


def deal_with_dupes(dest_folder, dirpath, extensions, f):
    for ext in extensions:
        if f.lower().endswith(ext):
            file_path = os.path.join(dirpath, f)
            size = os.path.getsize(file_path)
            is_found = False
            for destpath, destdnames, destfnames in os.walk(dest_folder):
                for destf in destfnames:
                    if f == destf:
                        is_found = True
                        break
            if not is_found:
                print('Copying file {0}...'.format(f))
                sh.copy(file_path, os.path.join(destpath, f))
                break
            else:
                destf_size = os.path.getsize(os.path.join(destpath, destf))
                if size != destf_size:
                    print('File {0} already exists but a with different size'.format(f))
                    new_name = uuid.uuid4().hex[:6].upper() + ext
                    new_dir_and_name = os.path.join(dirpath, new_name)
                    print('Renaming file {0} to {1}'.format(f, new_name))
                    os.rename(file_path, new_dir_and_name)
                    print('Copying file {0}...'.format(new_name))
                    sh.copy(new_dir_and_name, os.path.join(dest_folder, new_name))
                else:
                    print('File {0} already exists, skipping...'.format(f))
            break

def deal_with_dupes_single(dest_folder, dirpath, extensions, f):
    for ext in extensions:
        if f.lower().endswith(ext):
            file_path = os.path.join(dirpath, f)
            print('Copying file {0}...'.format(f))
            sh.copy(file_path, os.path.join(dest_folder, f))
            return


main()
