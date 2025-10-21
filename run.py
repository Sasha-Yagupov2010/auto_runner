import os
import subprocess
import requests

filename = ""
github_raw_url = ""

with open("data.txt", 'r', encoding='utf-8') as f:
    filename = f.readline().strip()
    github_raw_url = f.readline().strip()+filename
    

def file_exists(filepath):
    return os.path.isfile(filepath)

def get_remote_file_content(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        print(f"Не удалось получить файл с GitHub: {response.status_code}")
        return None

def main():
    remote_content = get_remote_file_content(github_raw_url)

    if remote_content is None:
        print("Не удалось получить содержимое удаленного файла.")
        return

    local_content = None
    if file_exists(filename):
        with open(filename, 'r', encoding='utf-8') as f:
            local_content = f.read()

        if local_content != remote_content:
            # Обновляем файл
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(remote_content)
            print(f"{filename} обновлен из GitHub.")
    else:
        # Файл отсутствует, создаем
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(remote_content)

    # Запускаем файл в отдельном окне
    subprocess.Popen(
        ["python", filename],
        creationflags=subprocess.CREATE_NEW_CONSOLE
    )

if __name__ == "__main__":
    main()