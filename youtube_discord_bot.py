import os
import discord
from discord.ext import tasks
import googleapiclient.discovery
import datetime
import json
from dotenv import load_dotenv

# .envファイルを読み込む
load_dotenv()

# 設定ファイルを読み込むか、環境変数から設定を取得
try:
    with open('config.json', 'r') as f:
        config = json.load(f)
    DISCORD_TOKEN = config.get('discord_token')
    YOUTUBE_API_KEY = config.get('youtube_api_key')
    YOUTUBE_CHANNEL_ID = config.get('youtube_channel_id')
    DISCORD_CHANNEL_ID = int(config.get('discord_channel_id'))
    CHECK_INTERVAL = int(config.get('check_interval', 3600))  # デフォルトは1時間ごと
except FileNotFoundError:
    DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
    YOUTUBE_API_KEY = os.getenv('YOUTUBE_API_KEY')
    YOUTUBE_CHANNEL_ID = os.getenv('YOUTUBE_CHANNEL_ID')
    DISCORD_CHANNEL_ID = int(os.getenv('DISCORD_CHANNEL_ID'))
    CHECK_INTERVAL = int(os.getenv('CHECK_INTERVAL', 3600))  # デフォルトは1時間ごと

# 最後にチェックした時間を保存するファイル
LAST_CHECK_FILE = 'last_check.txt'

# Discordクライアントの設定
intents = discord.Intents.default()
client = discord.Client(intents=intents)

# YouTubeのAPIクライアントを初期化
youtube = googleapiclient.discovery.build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)

def get_latest_videos(channel_id, published_after=None):
    """指定されたチャンネルから新しい動画を取得する"""
    request = youtube.search().list(
        part="snippet",
        channelId=channel_id,
        maxResults=5,
        order="date",
        type="video",
        publishedAfter=published_after
    )
    response = request.execute()
    
    videos = []
    for item in response.get('items', []):
        video_id = item['id']['videoId']
        title = item['snippet']['title']
        published_at = item['snippet']['publishedAt']
        thumbnail = item['snippet']['thumbnails']['high']['url']
        
        videos.append({
            'id': video_id,
            'title': title,
            'published_at': published_at,
            'thumbnail': thumbnail,
            'url': f'https://www.youtube.com/watch?v={video_id}'
        })
    
    return videos

def save_last_check_time():
    """最後にチェックした時間を保存する"""
    now = datetime.datetime.utcnow().isoformat() + 'Z'
    with open(LAST_CHECK_FILE, 'w') as f:
        f.write(now)
    return now

def get_last_check_time():
    """最後にチェックした時間を取得する"""
    try:
        with open(LAST_CHECK_FILE, 'r') as f:
            return f.read().strip()
    except FileNotFoundError:
        # ファイルが存在しない場合、現在時刻を保存して返す
        return save_last_check_time()

def get_latest_videos_force(channel_id, max_results=1):
    """指定されたチャンネルから最新の動画を取得する（publishedAfterなし）"""
    request = youtube.search().list(
        part="snippet",
        channelId=channel_id,
        maxResults=max_results,
        order="date",
        type="video"
        # publishedAfterパラメータを指定しない
    )
    response = request.execute()
    
    videos = []
    for item in response.get('items', []):
        video_id = item['id']['videoId']
        title = item['snippet']['title']
        published_at = item['snippet']['publishedAt']
        thumbnail = item['snippet']['thumbnails']['high']['url']
        
        videos.append({
            'id': video_id,
            'title': title,
            'published_at': published_at,
            'thumbnail': thumbnail,
            'url': f'https://www.youtube.com/watch?v={video_id}'
        })
    
    return videos

@client.event
async def on_ready():
    """ボットが起動したときに呼ばれる"""
    print(f'{client.user} としてログインしました')
    check_new_videos.start()

@tasks.loop(seconds=CHECK_INTERVAL)
async def check_new_videos():
    """定期的に新しい動画をチェックする"""
    try:
        last_check_time = get_last_check_time()
        new_videos = get_latest_videos(YOUTUBE_CHANNEL_ID, last_check_time)
        
        channel = client.get_channel(DISCORD_CHANNEL_ID)
        if not channel:
            print(f"エラー: Discord チャンネル ID {DISCORD_CHANNEL_ID} が見つかりません")
            return

        for video in new_videos:
            embed = discord.Embed(
                title=video['title'],
                url=video['url'],
                description="新しい動画が投稿されました！",
                color=0xFF0000  # YouTube赤
            )
            embed.set_image(url=video['thumbnail'])
            embed.set_footer(text=f"投稿日時: {video['published_at']}")
            
            await channel.send(embed=embed)
            print(f"通知を送信しました: {video['title']}")
        
        # 新しい最終チェック時間を保存
        save_last_check_time()
        
    except Exception as e:
        print(f"エラーが発生しました: {e}")

@check_new_videos.before_loop
async def before_check():
    """タスクを開始する前にDiscordへの接続を待つ"""
    await client.wait_until_ready()

# ボットを実行
if __name__ == "__main__":
    client.run(DISCORD_TOKEN) 