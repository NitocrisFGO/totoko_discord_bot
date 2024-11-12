import os
import shutil
from mutagen.easyid3 import EasyID3  # 确保你已经安装 mutagen


def get_base_list(file_path):
    base_list = []
    # 逐行读取文件内容
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            base_list.append(line)
    return base_list


def add_one_music(file_name):
    # 确保源文件存在
    if os.path.exists(file_name):
        # 定义文件路径
        base_file = 'music_base_list.txt'
        destination_folder = 'musics'

        # 创建 musics 文件夹（如果不存在）
        if not os.path.exists(destination_folder):
            os.makedirs(destination_folder)

        print("正在处理文件： " + file_name)

        # 尝试读取文件标题
        try:
            audio = EasyID3(file_name)
            title = audio.get('title', [None])[0]  # 获取歌曲标题，如果没有则返回 None
        except Exception as e:
            print("无法读取标题，需手动输入。")
            title = None

        # 如果无法读取标题，则让用户输入
        if title is None:
            user_input = input("请输入歌曲名，如果有其他语言名字并且想添加中文名，用；分割：" + '\n')
            title = user_input

        if title in base_list:
            print("已经有这首歌了。 歌名： " + title)
            return

        # 将用户输入写入 base_line_file 的末尾
        with open(base_file, 'a', encoding='utf-8') as f:
            f.write('\n' + title)

        # 计算文件行数
        with open(base_file, 'r', encoding='utf-8') as f:
            line_count = sum(1 for line in f)

        # 重命名文件，并移动到 musics 文件夹中
        new_filename = f"{line_count}.mp3"
        destination_path = os.path.join(destination_folder, new_filename)

        shutil.move(file_name, destination_path)
    else:
        print(f"文件 {file_name} 不存在。")


def add_all_music():
    # 定义待处理的文件夹
    wait_list_folder = 'wait_list'

    # 检查文件夹是否存在
    if not os.path.exists(wait_list_folder):
        print(f"文件夹 {wait_list_folder} 不存在。")
        return

    # 遍历 wait_list 文件夹中的所有文件
    for file_name in os.listdir(wait_list_folder):
        # 检查文件是否以 .mp3 结尾
        if file_name.endswith('.mp3'):
            # 调用 add_one_music 函数并传入文件名
            add_one_music('wait_list/' + file_name)


if __name__ == '__main__':
    base_list = get_base_list('music_base_list.txt')
    print("请选择将歌曲加入数据库的模式")
    print("1为仅加入一首歌，请将音乐拖动入根目录或给出该文件相对于根目录的路径")
    print("2为加入一个歌曲列表，请将多个音乐文件拖入wait_list中")
    model_input = input()
    if model_input == '1':
        file_name = input("您已选择模式1，请给出音乐名或给出该文件相对于根目录的路径" + '\n')
        add_one_music(file_name)
    if model_input == '2':
        add_all_music()
