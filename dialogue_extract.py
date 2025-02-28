import json
import re
import os
import requests


def extract_dialogue(chapter, txt_name):
    """
       提取特定章节的对话内容。
       通过检测 "＠" 或 "？" 来判断是否需要提取对话，并去除无关内容。
       """
    is_extract = False
    dialogue_path = './scripts/' + chapter + '/unextract'
    extract_path = './scripts/' + chapter + '/extract'

    os.makedirs(extract_path, exist_ok=True)

    # open the .txt file
    with open(dialogue_path + '/' + txt_name + '.txt', 'r', encoding='utf-8') as file:
        with open(extract_path + '/' + txt_name + '_extracted.txt', 'w', encoding='utf-8') as extracted_file:

            for line in file:

                if "＠" in line or "？" in line:
                    is_extract = True

                if not line.strip() or is_bracketed_content(line):
                    is_extract = False

                if is_extract:
                    clean_line = clean_dialogue(line)
                    if clean_line.strip():
                        extracted_file.write(clean_line)


def extract_character_dialogue(chapter, txt_name):
    """
       提取特定章节的对话内容。
       通过检测 "＠" 或 "？" 来判断是否需要提取对话，并去除无关内容。
       """
    is_extract = False
    dialogue_path = './scripts/' + chapter + '/unextract'
    extract_path = './scripts/' + chapter + '/extract'

    os.makedirs(extract_path, exist_ok=True)

    # open the .txt file
    with open(dialogue_path + '/' + txt_name + '.txt', 'r', encoding='utf-8') as file:
        with open(extract_path + '/' + txt_name + '_extracted.txt', 'w', encoding='utf-8') as extracted_file:

            for line in file:

                if not is_bracketed_content(line):
                    clean_line = clean_dialogue(line)
                    if clean_line.strip():
                        extracted_file.write(clean_line)


def clean_dialogue(text):
    """
       清理对话文本，去除无关标记。
       """
    if text[0] == "？":
        text = re.sub(r'\d+：', '', text[1:])
        text = "＠我\n" + text
    clean_text = text.replace('[k]', '')
    clean_text = clean_text.replace('[r]', '')
    clean_text = re.sub(r'[^\w\s]*\[\s*line\s*3\s*\]', '', clean_text)
    clean_text = re.sub(r'[^\w\s]*\[\s*line\s*2\s*\]', '', clean_text)
    clean_text = re.sub(r'[^\w\s]*\[\s*line\s*1\s*\]', '', clean_text)
    clean_text = re.sub(r'[^\w\s]*\[\s*%1\s*\]', '', clean_text)
    return clean_text


def download_dialogue(json_name):
    """
        下载对话数据，并保存到本地文件。
        """
    chapter_path = './scripts/' + json_name + '.json'
    save_path = './scripts/' + json_name
    os.makedirs(save_path, exist_ok=True)
    os.makedirs(save_path + '/unextract', exist_ok=True)

    with open(chapter_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
        spots = data.get("spots", [])
        for spot in spots:
            quests = spot.get("quests", [])
            for quest in quests:
                quest_name = quest.get("name", "Unknown")
                # print(f"Quest Name: {quest_name}")
                phase_scripts = quest.get("phaseScripts", [])
                for phase in phase_scripts:
                    phase_number = phase.get("phase", "Unknown Phase")
                    scripts = phase.get("scripts", [])
                    for script in scripts:
                        script_link = script.get("script", "No Link")
                        # print(f"  Phase {phase_number} Script: {script_link}")
                        try:
                            response = requests.get(script_link)

                            # check whether the http request is success
                            response.raise_for_status()

                            # write content into local file
                            quest_name = quest_name.replace(" ", "")
                            quest_name = quest_name.replace("/", "_")
                            dialogue_path = save_path + '/unextract/' + quest_name + '_' + str(phase_number) + '.txt'
                            with open(dialogue_path, 'w', encoding='utf-8') as dialogue:
                                dialogue.write(response.text)

                        except requests.exceptions.RequestException as e:
                            print(f"下载失败：{e}")
                        except Exception as e:
                            print(f"保存文件时发生错误：{e}")


def extract_data():
    """
        遍历 scripts 目录下的所有章节，提取并处理对话内容。
        """
    folder_path = "./scripts"

    # get all filenames in the folder
    try:
        file_names = os.listdir(folder_path)

        # remove folder name
        file_names = [f for f in file_names if os.path.isfile(os.path.join(folder_path, f))]

        file_names = [os.path.splitext(file_name)[0] for file_name in file_names]

        for file_name in file_names:

            download_dialogue(file_name)

            dialogue_path = './scripts/' + file_name + '/unextract'
            dialogue_names = os.listdir(dialogue_path)

            # remove folder name
            dialogue_names = [f for f in dialogue_names if os.path.isfile(os.path.join(dialogue_path, f))]

            dialogue_names = [os.path.splitext(dialogue_name)[0] for dialogue_name in dialogue_names]

            for dialogue_name in dialogue_names:
                extract_dialogue(file_name, dialogue_name)

    except FileNotFoundError:
        print(f"文件夹未找到：{folder_path}")
    except PermissionError:
        print(f"没有权限访问该文件夹：{folder_path}")
    except Exception as e:
        print(f"发生错误：{e}")


def extract_role_dialogue(chapter, role):
    """
        提取特定章节中特定角色的对话。
        """
    count = 0
    sameCharact = 1
    firstCharact = 1
    lastCharact = ''
    thisCharact = ''
    lastDialogue = ''
    thisDialogue = ''
    isExtract = False
    question = ''
    reply = ''
    questionList = []
    replyList = []

    dialogue_path = './scripts/' + chapter + '/extract'

    dialogues = os.listdir(dialogue_path)

    for dialogue in dialogues:
        with open(dialogue_path + '/' + dialogue, 'r', encoding='utf-8') as file:
            for line in file:
                if line.strip():

                    if "＠" in line:

                        if not firstCharact:
                            if thisCharact in line:
                                sameCharact = 1
                            else:
                                sameCharact = 0

                        if not firstCharact and sameCharact == 0:

                            if role in thisCharact:
                                questionList.append(lastDialogue)
                                replyList.append(thisDialogue)
                                count += 1

                            lastCharact = thisCharact
                            lastDialogue = thisDialogue
                            thisDialogue = ''
                            sameCharact = 1

                        thisCharact = line

                    else:

                        if not is_bracketed_content(line):
                            clean_line = line.rstrip("\n")

                            thisDialogue = thisDialogue + clean_line

                            firstCharact = 0

            if role in thisCharact:
                questionList.append(lastDialogue)
                replyList.append(thisDialogue)
                count += 1

    return questionList, replyList


def add_data(chapter, role, dataFileName):
    """
        将提取的对话数据添加到 JSON 文件中。
        """

    questionList, replyList = extract_role_dialogue(chapter, role)

    for i in range(len(questionList)):

        new_data = {
            "role": "user",
            "content": questionList[i],
            "response": replyList[i]
        }

        # read origin json file
        try:
            with open(dataFileName, "r", encoding="utf-8") as file:
                data = json.load(file)  #
        except FileNotFoundError:
            print("文件不存在")
            return

        data.append(new_data)

        # save json file
        with open(dataFileName, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

    print("章节，人物： " + chapter + ", " + role + "\n 已添加到 " + dataFileName)


def is_bracketed_content(line):
    """
        检查文本是否是括号内容，例如 [背景音]。
        """
    pattern = r'^\[.*\]$'
    return bool(re.match(pattern, line))


def list_json_files():
    folder_path = "./scripts"

    try:
        # 获取 scripts 文件夹下所有文件
        file_names = os.listdir(folder_path)

        # 过滤出 .json 文件
        json_files = [f for f in file_names if f.endswith('.json')]

        # 打印 JSON 文件名
        for json_file in json_files:
            print(json_file)

    except FileNotFoundError:
        print(f"文件夹未找到：{folder_path}")
    except PermissionError:
        print(f"没有权限访问该文件夹：{folder_path}")
    except Exception as e:
        print(f"发生错误：{e}")


if __name__ == '__main__':
    """
        主程序运行逻辑，提供用户操作选择。
        """
    print("Software on, please select operate Type")
    print("Operate 1 : Download and extract dialogue")
    print("Operate 2 : Add dialogue to data")
    print("Operate 3 : List all name for .json file")
    print("Operate 4 : Extract character script")
    print("Operate 5 : Close software")
    isOpen = 1
    while isOpen == 1:
        operate = input()
        if operate == '1':
            print("Downloading.")
            extract_data()
            print("Complete.")
        if operate == '2':

            print(" Please enter Chapter name: 1 for all chapters")
            chapter = input()
            print(" Please enter Role name: ")
            role = input()
            print(" Please enter Data File: ")
            dataFileName = input()

            if chapter == '1':
                try:
                    # 获取 scripts 目录下的所有文件，并筛选出文件夹
                    folders = [f for f in os.listdir("./scripts") if os.path.isdir(os.path.join("./scripts", f))]
                    for folder in folders:
                        add_data(folder, role, dataFileName)
                except FileNotFoundError:
                    print(f"错误：目录 ./scripts 未找到。")
                except PermissionError:
                    print(f"错误：没有权限访问 ./scripts。")
                except Exception as e:
                    print(f"发生错误：{e}")
            print("Complete.")
        if operate == '3':
            list_json_files()
        if operate == '4':
            print(" Please enter character file name: ")
            characterFileName = input()
            extract_character_dialogue("character_script", characterFileName)
            print("Complete.")
        if operate == '5':
            print("Close software")
            isOpen = 0


