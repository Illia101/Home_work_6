import sys
import pathlib 
import os
import shutil
import zipfile
import tarfile
import gzip


IMAGES = []
AUDIO = []
VIDEO = []
DOCUMENTS = []
ARCHIVES = []
FOLDERS = []
UNKNOWN = []
REGISTERED_EXTENSIONS = {
    'JPEG': IMAGES,
    'PNG': IMAGES,
    'JPG': IMAGES,
    'SVG': IMAGES,
    'AVI': VIDEO,
    'MP4': VIDEO,
    'MOV': VIDEO,
    'MKV': VIDEO,
    'DOC': DOCUMENTS,
    'DOCX': DOCUMENTS,
    'TXT': DOCUMENTS,
    'XLSX': DOCUMENTS,
    'PPTX': DOCUMENTS,
    'PDF': DOCUMENTS,
    'MP3': AUDIO,
    'OGG': AUDIO,
    'WAV': AUDIO,
    'AMR': AUDIO,
    'ZIP': ARCHIVES,
    'GZ': ARCHIVES,
    'TAR': ARCHIVES,
}

CYRILLIC_SYMBOLS = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ"
TRANSLATION = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
               "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "ya", "je", "i", "ji", "g")

TRANS = {}
for c, l in zip(CYRILLIC_SYMBOLS, TRANSLATION):
        TRANS[ord(c)] = l
        TRANS[ord(c.upper())] = l.upper()
    


def normalize(name):
    result = name.translate(TRANS)
    # print(type(result))
    strink = ''

    for res in result:
        if res.isalnum():
            strink += res
        else:
            strink += '_'
             
    return strink

def split_extension(file_name: str):

    # name, extension = file_name.split('.')
    
    # return  extension
    if '.' in file_name:
        name, extension = file_name.split('.', 1)
        return extension.lower()
    else:
        return None
              





path = 'D:\\Home_work_1\\motloh'    
def new_scan(path):
   
    for i in os.listdir(path):
        file_or_dir = path + '\\' + i
        if os.path.isfile(file_or_dir):
            extension = split_extension(file_or_dir)
            if extension in ['jpg', 'jpeg', 'png']:
                IMAGES.append(file_or_dir)
            elif extension in ['avi', 'mp4', 'mov', 'mkv']:
                VIDEO.append(file_or_dir)
            elif extension in ['doc', 'docx', 'txt', 'pdf', 'xlsx', 'pptx']:
                DOCUMENTS.append(file_or_dir)
            elif extension in ['mp3', 'ogg', 'wav', 'amr']:
                AUDIO.append(file_or_dir)
            elif extension in 'zip':
                with zipfile.ZipFile(file_or_dir, 'r') as zip_ref:
                    ARCHIVES.append(zip_ref)
            elif extension in 'tar':
                with tarfile.open(file_or_dir, 'r') as tar_ref:
                    ARCHIVES.append(tar_ref)
            elif extension in 'gz':
                with gzip.open(file_or_dir, 'rb') as gz_ref:
                    ARCHIVES.append(gz_ref)


            else:
                UNKNOWN.append(file_or_dir)
        
        if os.path.isdir(file_or_dir):
            len_folder = os.listdir(file_or_dir)
            if len(len_folder) == 0:
                os.rmdir(file_or_dir)
            elif os.path.isdir(file_or_dir) and i in ["archives", "video", "audio", "documents", "images"]:
                continue
            else:       
               FOLDERS.append(file_or_dir)
               new_scan(file_or_dir)


            


new_scan(path)
print('Фото:', IMAGES)
print('Документи:', DOCUMENTS) 
print('Відео:' , VIDEO)
print('Музика:' , AUDIO)
print('Архіви:' , ARCHIVES)
print('Папки:', FOLDERS)
print('Невідомі файли:' , UNKNOWN)




def move_files(file_list, destination_folder):
    for file_path in file_list:
        if os.path.exists(file_path):
            file_name = os.path.basename(file_path)
            name, extension = os.path.splitext(file_name)
            normalized_name = normalize(name)
            new_file_name = normalized_name + extension
            new_file_path = os.path.join(destination_folder, new_file_name)
            try:
                shutil.move(file_path, new_file_path)
                print(f"Файл {file_path} переміщено до {new_file_path}")
            except Exception as e:
                print(f"Помилка під час переміщення файлу {file_path}: {str(e)}")
        else:
            print(f"Файл {file_path} не існує")

def move_folders(folder_list, destination_folder):
    for folder_path in folder_list:
        if os.path.exists(folder_path):
            folder_name = os.path.basename(folder_path)
            normalized_name = normalize(folder_name)
            new_folder_path = os.path.join(destination_folder, normalized_name)
            try:
                shutil.move(folder_path, new_folder_path)
                print(f"Папку {folder_path} переміщено до {new_folder_path}")
            except Exception as e:
                print(f"Помилка під час переміщення папки {folder_path}: {str(e)}")

        else:
            print(f"Папка {folder_path} не існує")




move_files(IMAGES, r'D:\Home_work_1\images')


move_files(AUDIO, r'D:\Home_work_1\audios')


move_files(VIDEO, r'D:\Home_work_1\video')


move_files(DOCUMENTS, r'D:\Home_work_1\documents')

move_files(UNKNOWN, r'D:\Home_work_1\UNKNOWN')

move_folders(FOLDERS, r'D:\Home_work_1\Folders')

# if __name__ == "__main__":
#     path = sys.argv[1]
#     # print(path)
#     arg = pathlib.Path(path)
#     # scan(arg.absolute())
#     # main(arg.absolute())
#     # name, extension = split_extension('ОПИС!@.txt')
    

    
#     # print(normalize(name))
#     # print(name, extension)
    