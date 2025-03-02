# YouTube通知Discord Bot

このボットは、指定したYouTubeチャンネルに新しい動画が投稿されたときに、Discordサーバーに通知を送信します。

## 機能

- YouTubeチャンネルの新規動画を定期的にチェック
- 新しい動画が見つかるとDiscordに埋め込みメッセージで通知
- サムネイル画像と動画へのリンクを表示

## セットアップ方法

### 必要なもの

1. Discord Bot トークン
2. YouTube Data API キー
3. 通知したいYouTubeチャンネルID
4. 通知を送信するDiscordチャンネルID

### 手順

1. 必要なライブラリをインストール:
   ```
   pip install -r requirements.txt
   ```

2. Discord Botを作成:
   - [Discord Developer Portal](https://discord.com/developers/applications)にアクセス
   - 「New Application」をクリック
   - 「Bot」タブで「Add Bot」をクリック
   - トークンを取得（「Reset Token」をクリックすると表示されます）
   - 「OAuth2」→「URL Generator」で必要な権限を選択（最低限「Send Messages」と「Embed Links」）
   - 生成されたURLを使用してボットをサーバーに招待

3. YouTube API キーを取得:
   - [Google Cloud Console](https://console.cloud.google.com/)にアクセス
   - プロジェクトを作成
   - APIライブラリから「YouTube Data API v3」を有効化
   - 認証情報でAPIキーを作成

4. 設定ファイルの作成:
   - `config.json`を編集し、必要な情報を入力
   - または環境変数を設定（.envファイルも利用可能）

5. ボットを実行:
   ```
   python youtube_discord_bot.py
   ```

## 設定オプション

- `discord_token`: Discordボットのトークン
- `youtube_api_key`: YouTube Data APIのAPIキー
- `youtube_channel_id`: 監視するYouTubeチャンネルのID
- `discord_channel_id`: 通知を送信するDiscordチャンネルのID
- `check_interval`: 新しい動画をチェックする間隔（秒）

## 注意点

- YouTube Data APIには1日のクォータ制限があります（無料で1日10,000ユニット）
- 監視間隔を短くしすぎるとAPIクォータを早く消費する可能性があります
- このボットは常時稼働する環境で実行することをお勧めします（VPSやRaspberry Piなど）

## 無料で利用可能か？

はい、このボットは基本的に無料で利用できます：

- Discord Bot APIは無料で利用可能
- YouTube Data APIは無料枠（1日10,000ユニット）で十分に動作
- ホスティングは自分のPCやRaspberry Piなどで行うことができます
- また、Replit、Heroku、PythonAnywhereなどの無料プランでも動作可能 