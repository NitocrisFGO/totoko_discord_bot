import asyncio
import os
import time
from datetime import date
import random

import discord
from discord.ext import commands


# 将music_base_list转换为music_dictionary
def txt_to_dict(file_path):
    result_dict = {}

    # 逐行读取文件内容
    with open(file_path, 'r', encoding='utf-8') as file:
        temp = 1
        for line in file:
            # 去除行尾的换行符，并按空格分隔键和值
            parts = line.strip().split("；")
            base_list.append(line)
            # 确保每行都有值
            if len(parts) != 0:
                # 对于每个值，都分配同一首歌的歌曲编号
                for part in parts:
                    # print(part)
                    result_dict[part] = temp
            else:
                print(f"格式错误：'{line}'")
            temp += 1

    return result_dict


# 创建 Bot 实例，设置命令前缀为 !
intents = discord.Intents.default()
intents.message_content = True  # 确保机器人可以读取消息内容
intents.members = True  # 确保可以访问服务器成员信息
bot = commands.Bot(command_prefix='!', intents=intents)
today = date.today()
FFMPEG_OPTIONS = {
    'options': '-vn'
}

file_path = 'music_base_list.txt'
base_list = []
music_dictionary = txt_to_dict(file_path)
allow_play = False

seed = int(time.time() * 1000) ^ os.getpid() ^ random.randint(0, 100000)
random.seed(seed)

hello_text_list = ['哟~你好，魔法少女托托子竭诚为您服务。还有，是中国人就说你好。', '欸嘿，今天是 ' + str(today) + ' 过的怎么样啊？'
                   , '天气真好， 今天来一首 ' + random.choice(base_list) + ' 怎么样？']
play_test_list = ['哦，在这停顿！ ', '阿伟，又在听音乐了，休息一下好不好。 ', '让我看看你在听什么？ ', '这首歌我还挺喜欢的，品味不错。 ']

rps_lose_text = ["略~欺负人，真不行吧？", "不准走！再来！再来！", "你作弊了对吧，你作弊了对吧？", "不可能！我不承认！", "🙃",
                 "哎，也就在石头剪刀布中能赢赢托托子了。", "这不去打个石头剪刀布的世界联赛我是不认可的，什么？阴阳？我才没有阴阳你。",
                 '欺负托托子的，你去和狗一桌。', "嘛~嘛~算你比较厉害"]
rps_win_text = ["哎，杂鱼就是杂鱼，一边呆着去吧~", "去~去~你去抓只螃蟹和他玩吧。不过注意不要出布，因为你会输",
                "打游戏会存在一直输的情况，所以，心情就很烦躁，凭什么自己会一直输，明明自己已经很努力了，但还是输了，所以，就会不断地责怪自己，然后就很不开心，很压抑，因此，应该怎么办？",
                "玩原神玩的，🤣", "你有试过和蚂蚁比举重吗？", "噗~如果我道歉，你会好受些吗？", "菜，就多练，输不起就别玩。接下来的忘了",
                "托托子是石头剪刀布界最高的山，最长的河，输给咱是很正常的。",
                "https://baike.baidu.com/item/%E8%BC%95%E5%BA%A6%E5%BC%B1%E6%99%BA/4265374"]

play_list = []
play_model = '列表循环'

current_song_list = []
current_song_index = 0

print(music_dictionary)


# 让机器人加入用户所在的语音频道
async def ensure_voice(ctx):
    # 检查机器人是否已连接到语音频道
    if not ctx.voice_client:
        if ctx.author.voice:  # 检查用户是否在语音频道
            await ctx.author.voice.channel.connect()
            await ctx.send("在哪在哪？ 我来咯！" + str(ctx.author.voice.channel))
        else:
            await ctx.send("要不你先开个房再叫咱？")
            return False
    return True


def check_current_list(current_song_list):
    if len(current_song_list) >= 11:
        current_song_list.pop(0)


# 播放下一首音乐
async def play_next(ctx, current_song_index):

    if not allow_play:
        return

    current_song_list.append(current_song_index)
    check_current_list(current_song_list)

    # 如果已经到播放列表的末尾，重置索引以循环播放
    if play_model == '列表循环':
        if current_song_index >= len(play_list):
            current_song_index = 0

    # 获取当前要播放的音乐文件
    music_name = play_list[current_song_index]
    music_dic_name = music_dictionary[music_name]
    file_name = 'musics/' + str(music_dic_name) + '.mp3'

    if play_model == '随机播放':
        while current_song_index in current_song_list:
            current_song_index = random.randint(0, len(play_list) - 1)
    else:
        current_song_index += 1

    # 播放音乐并设置回调
    ctx.voice_client.play(
        discord.FFmpegPCMAudio(file_name),
        after=lambda e: asyncio.run_coroutine_threadsafe(play_next(ctx, current_song_index), bot.loop)
    )

    play_text = random.choice(play_test_list)
    await ctx.send(play_text + music_name)


# 启动时的事件
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} ({bot.user.id})')
    print('------')


# 一个简单的测试命令，用户可以输入 !hello，机器人会回应
@bot.command(name='hello', help='这么想让我和你问好吗？')
async def hello(ctx):
    hello_random_index = random.randint(0, len(hello_text_list) - 1)
    await ctx.send(hello_text_list[hello_random_index])


# 让机器人加入用户所在的语音频道
@bot.command(name='join', help='让托托子加入语音频道')
async def join(ctx):
    if ctx.author.voice:
        channel = ctx.author.voice.channel
        await channel.connect()
        await ctx.send(f'{channel}， 咱降临咯！')
    else:
        await ctx.send('不是，哥们儿，你自己先加个频道再和咱约会啊。')


# 让机器人离开语音频道
@bot.command(name='leave', help='真的假的，想把我踢出去吗？')
async def leave(ctx):

    global current_song_index
    global play_list

    if ctx.voice_client:
        await ctx.voice_client.disconnect()
        current_song_index = 0
        play_list = []
        await ctx.send('拜~润咯')
    else:
        await ctx.send('额，离开哪儿啊？我不到啊，滴滴哒滴滴嘟。')


# 播放 music database 中的音频
@bot.command(name='play', help='播放来自咱音乐存储库中的音乐。用法: !play <音乐名>')
async def play(ctx, music_name):
    global current_song_index
    global allow_play
    if not await ensure_voice(ctx):
        return

    if music_name in music_dictionary:
        music_dic_name = music_dictionary[music_name]
    else:
        await ctx.send(f'额，暂时不会这首: {music_name} ， 要不你找尼托帮你找找看？')
        return

    # file_name = 'musics/' + music_dic_name + '.mp3'
    voice_client = ctx.voice_client

    # if not os.path.isfile(file_name):
    #     print(file_name)
    #     await ctx.send(f'额，暂时不会这首: {music_name} ， 要不你找尼托帮你找找看？')
    #     return

    # voice_client.play(discord.FFmpegPCMAudio(file_name, **FFMPEG_OPTIONS))

    # play_text = random.choice(play_test_list)
    if voice_client.is_playing():
        play_list.append(music_name)
        await ctx.send(music_name + " 加入列表成功！")
    else:
        allow_play = True
        await ctx.send(music_name + "原声，启动！")
        play_list.append(music_name)
        current_song_index = len(play_list) - 1
        await play_next(ctx, current_song_index)


# 随机播放 music database 中的音频
@bot.command(name='random_play', help='那肯定是随机播放咯，这都看不懂吗？')
async def random_play(ctx):
    global current_song_index
    global play_model
    global allow_play

    play_model = '随机播放'

    if not await ensure_voice(ctx):
        return

    play_list.clear()
    play_list.extend(music_dictionary.keys())
    random.shuffle(play_list)

    current_song_index = random.randint(0, len(play_list) - 1)
    print('随机数是：' + str(current_song_index))

    voice_client = ctx.voice_client

    if voice_client.is_playing():
        await ctx.send("接下来该尝试刺激点的了哦~")
    else:
        allow_play = True
        await ctx.send("陌生的城市坐公交，每一站都是惊喜捏。")
        await play_next(ctx, current_song_index)


# 全部播放 music database 中的音频
@bot.command(name='all_play', help='全都给我来一遍！')
async def all_play(ctx):

    global current_song_index
    global allow_play
    global play_model

    if not await ensure_voice(ctx):
        return

    play_model = '列表循环'

    play_list.clear()
    current_song_index = 0
    play_list.extend(music_dictionary.keys())

    voice_client = ctx.voice_client

    if voice_client.is_playing():
        await ctx.send("从零开始的播放列表。")
    else:
        allow_play = True
        await ctx.send("我们重新战斗吧，神龙凯欧，奥鹰格特，岩豹烈伽，冰龟罗克，赤蛇蒙洛，悍狼尼尔，天熊雷赫，肉蛋葱鸡。")
        await play_next(ctx, current_song_index)


# 全部播放 music database 中的音频
@bot.command(name='search', help='查找歌名捏。')
async def search_music(ctx):
    await ctx.send("想找什么？")

    def check(message):
        # 确保消息来自相同的用户且在同一频道中
        return message.author == ctx.author and message.channel == ctx.channel

    try:
        # 等待用户输入，有效输入时返回消息对象，超时为 30 秒
        message = await bot.wait_for("message", timeout=30.0, check=check)
        search_word = message.content
        result = []
        for music in base_list:
            if search_word in music:
                result.append(music)
        if len(result) == 0:
            await ctx.send("没有找到，哥们儿。")
        else:
            await ctx.send(f'你看看也没有你喜欢的： \n' + ''.join(result))
    except asyncio.TimeoutError:
        # 如果用户没有在 30 秒内作出选择
        await ctx.send(f"{ctx.author.mention}，似了？")


# 输出音乐列表
@bot.command(name='music_list', help='打开咱的百宝袋')
async def music_list(ctx):
    await ctx.send('Emmm, 我找找看啊，都有哪些呢？')
    await asyncio.sleep(1)
    chunk_size = 50
    for i in range(0, len(base_list), chunk_size):
        chunk = base_list[i:i + chunk_size]
        await ctx.send("".join(chunk))


@bot.command(name='play_list', help='看看你的歌单！')
async def music_play_list(ctx):
    await ctx.send('是放完了，还是没放完，这是一个问题')
    await asyncio.sleep(1)
    await ctx.send(f"播放列表：\n{play_list}")
    await ctx.send(f"你现在播放到：\n{play_list[current_song_index]}")


# 停止播放音乐
@bot.command(name='stop', help='太吵了！闭嘴！')
async def stop(ctx):

    global allow_play

    if ctx.voice_client:

        allow_play = False

        ctx.voice_client.stop()

        # 强制结束 FFmpeg 进程
        if ctx.voice_client.is_playing():
            await ctx.voice_client.disconnect()
            await ctx.voice_client.connect()

        await ctx.send('停止播放音乐喵~')
    else:

        await ctx.send('咱寻思咱也没有唱歌呀。')


@bot.command(name='continue', help='继续播放没放完的捏')
async def continue_play(ctx):

    global allow_play

    if not await ensure_voice(ctx):
        return

    if allow_play is True:
        await ctx.send('没暂停继续什么继续，笨蛋。')
    else:

        allow_play = True
        await ctx.send('继续继续！接着奏乐接着舞。')
        await play_next(ctx, current_song_index)


@bot.command(name='skip', help='老板唱K你切歌')
async def skip_play(ctx):

    global current_song_index
    global allow_play

    if not await ensure_voice(ctx):
        return

    if ctx.voice_client:

        await ctx.send('切歌，切歌！不爱听这个。')

        if play_model == "列表循环":
            current_song_index += 1
        elif play_model == "随机播放":
            current_song_index = random.randint(0, len(play_list) - 1)

        allow_play = False

        ctx.voice_client.stop()

        while ctx.voice_client.is_playing():
            await asyncio.sleep(0.1)

        allow_play = True

        await play_next(ctx, current_song_index)
    else:
        await ctx.send('没放呢，切不了一点。')


@bot.command(name='rps', help='想和托托子来一次石头剪刀布吗？')
async def rps(ctx):
    # 定义合法的选择
    choices = ["石头", "剪刀", "布"]

    await ctx.send(f"{ctx.author.mention}，石头~剪刀~布！快出快出，放心，托托子绝对不会作弊的。")

    # 使用 `wait_for` 来等待用户的输入
    def check(message):

        # 确保消息来自相同的用户且在同一频道中
        return message.author == ctx.author and message.channel == ctx.channel and message.content in choices

    try:

        # 等待用户输入，有效输入时返回消息对象，超时为 30 秒
        message = await bot.wait_for("message", timeout=30.0, check=check)

        user_choice = message.content

        # 机器人随机选择
        bot_choice = random.choice(choices)

        # 发送双方选择
        await ctx.send(f"就决定是你了： {bot_choice}")

        # 判断游戏结果
        if user_choice == bot_choice:
            await ctx.send("平局！再来一局？")

        elif (user_choice == "石头" and bot_choice == "剪刀") or \
                (user_choice == "剪刀" and bot_choice == "布") or \
                (user_choice == "布" and bot_choice == "石头"):

            await ctx.send(random.choice(rps_lose_text))

        else:

            await ctx.send(random.choice(rps_win_text))

    except asyncio.TimeoutError:
        # 如果用户没有在 30 秒内作出选择
        await ctx.send(f"{ctx.author.mention}，不是，哥们儿，不玩就别狗叫。")


# 启动机器人
bot.run('MTI5OTU1MzExOTA4ODE1MjYwOA.GgzRBr.J2uWpHXPDx0o3ezDbhGIZCV-kEeAlgPx8TiWek')

