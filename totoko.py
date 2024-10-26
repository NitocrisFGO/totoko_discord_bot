import asyncio
import os
from datetime import date
import random

import discord
from discord.ext import commands


# 将music_base_list转换为music_dictionary
def txt_to_dict(file_path):
    result_dict = {}

    # 逐行读取文件内容
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            # 去除行尾的换行符，并按空格分隔键和值
            parts = line.strip().split(maxsplit=1)

            # 确保每行都有键和值
            if len(parts) == 2:
                key, value = parts
                result_dict[key] = value
            else:
                print(f"格式错误：'{line}'")

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
hello_text_list = ['哟~你好，魔法少女托托子竭诚为您服务。还有，是中国人就说你好。', '欸嘿，今天是 ' + str(today) + ' 过的怎么样啊？']
play_test_list = ['哦，在这停顿！ ', '阿伟，又在听音乐了，休息一下好不好。 ', '让我看看你在听什么？ ', '这首歌我还挺喜欢的，品味不错。 ']
file_path = 'music_base_list'
play_list = []
play_model = '列表循环'
current_song_index = 0
music_dictionary = txt_to_dict(file_path)

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


# 播放下一首音乐
async def play_next(ctx, current_song_index):

    if play_model == '列表循环':
        # 如果已经到播放列表的末尾，重置索引以循环播放
        if current_song_index >= len(play_list):
            current_song_index = 0

    # 获取当前要播放的音乐文件
    music_name = play_list[current_song_index]
    music_dic_name = music_dictionary[music_name]
    file_name = 'musics/' + music_dic_name + '.mp3'

    # 播放音乐并设置回调
    ctx.voice_client.play(discord.FFmpegPCMAudio(file_name, **FFMPEG_OPTIONS))
    current_song_index += 1
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
@bot.command(name='leave', help='让机器人离开语音频道')
async def leave(ctx):
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
        await ctx.send('拜~润咯')
    else:
        await ctx.send('额，离开哪儿啊？我不到啊，滴滴哒滴滴嘟。')


# 播放 music database 中的音频
@bot.command(name='play', help='播放来自咱音乐存储库中的音乐。用法: !play <音乐名>')
async def play(ctx, music_name):

    if not await ensure_voice(ctx):
        return

    music_dic_name = music_dictionary[music_name]

    file_name = 'musics/' + music_dic_name + '.mp3'
    voice_client = ctx.voice_client

    if not os.path.isfile(file_name):
        print(file_name)
        await ctx.send(f'额，暂时不会这首: {music_name} ， 要不你找尼托帮你找找看？')
        return

    # voice_client.play(discord.FFmpegPCMAudio(file_name, **FFMPEG_OPTIONS))

    # play_text = random.choice(play_test_list)
    if voice_client.is_playing():
        play_list.append(music_name)
        await ctx.send(music_name + " 加入列表成功！")
    else:
        await ctx.send(music_name + "原声，启动！")
        play_list.append(music_name)
        current_song_index = len(play_list) - 1
        await play_next(ctx, current_song_index)

# # 随机播放 music database 中的音频
# @bot.command(name='random_play', help='那肯定是随机播放咯，这都看不懂吗？')
# async def random_play(ctx, music_name):
#
#     if not await ensure_voice(ctx):
#         return
#
#     music_dic_name = music_dictionary[music_name]
#
#     file_name = 'musics/' + music_dic_name + '.mp3'
#     voice_client = ctx.voice_client
#
#     if not os.path.isfile(file_name):
#         print(file_name)
#         await ctx.send(f'额，暂时不会这首: {music_name} ， 要不你找尼托帮你找找看？')
#         return
#
#     voice_client.play(discord.FFmpegPCMAudio(file_name, **FFMPEG_OPTIONS))
#
#     play_text = random.choice(play_test_list)
#     await ctx.send(play_text + music_name)


# 输出音乐列表
@bot.command(name='music_list', help='查找音乐列表')
async def music_list(ctx):
    await ctx.send('Emmm, 我找找看啊，都有哪些呢？')
    await asyncio.sleep(3)
    music_list_str = '\n'.join(music_dictionary.keys())
    await ctx.send(f"音乐列表：\n{music_list_str}")


@bot.command(name='play_list', help='看看你的歌单！')
async def music_list(ctx):
    await ctx.send('是放完了，还是没放完，这是一个问题')
    await asyncio.sleep(3)
    await ctx.send(f"播放列表：\n{play_list}")
    await ctx.send(f"你现在播放到：\n{play_list[current_song_index]}")


# 停止播放音乐
@bot.command(name='stop', help='停止当前播放的音乐')
async def stop(ctx):
    if ctx.voice_client:
        ctx.voice_client.stop()
        await ctx.send('停止播放音乐喵~')
    else:
        await ctx.send('咱寻思咱也没有唱歌呀。')


@bot.command(name='continue', help='继续播放没放完的捏')
async def continue_play(ctx):

    if not await ensure_voice(ctx):
        return

    if ctx.voice_client:
        await ctx.send('没暂停继续什么继续，笨蛋。')
    else:
        await play_next(ctx, current_song_index)
        await ctx.send('继续继续！接着奏乐接着舞。')


# 启动机器人
bot.run('MTI5OTU1MzExOTA4ODE1MjYwOA.G7gtNl.-olG9jwYGTGpnvH0M2DoVpDv6jabyjnVWV5law')

