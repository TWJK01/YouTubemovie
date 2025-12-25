import yt_dlp

def fetch_long_videos(urls):
    # 設定過濾條件：長度大於 1200 秒 (20分鐘)
    # 格式設定：只抓取資訊，不下載影片
    ydl_opts = {
        'extract_flat': True, 
        'quiet': True,
        'match_filter': yt_dlp.utils.match_filter_func("duration > 1200"),
    }
    
    all_results = []
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        for channel_url in urls:
            print(f"正在分析頻道: {channel_url}")
            try:
                # 確保抓取影片分頁
                target = channel_url if "/videos" in channel_url else f"{channel_url}/videos"
                
                # 取得影片資訊
                info = ydl.extract_info(target, download=False)
                
                if 'entries' in info:
                    for entry in info['entries']:
                        # 只有符合 match_filter 的影片會出現在這裡
                        if entry:
                            title = entry.get('title', '')
                            video_url = f"https://www.youtube.com/watch?v={entry.get('id')}"
                            
                            # 判斷標題語言（國語、粵語等）
                            lang_tag = ""
                            if "國語" in title: lang_tag = "[國語]"
                            elif "粵語" in title: lang_tag = "[粵語]"
                            
                            all_results.append(f"{title}{lang_tag},{video_url}")
                            
            except Exception as e:
                print(f"跳過頻道 {channel_url}，原因: {e}")
                
    return all_results

if __name__ == "__main__":
    # 在此清單中加入你想要抓取的所有頻道網址
    channel_list = [
        "https://www.youtube.com/@8-hkmovie",
        "https://www.youtube.com/@chnclassice"

    ]
    
    final_data = fetch_long_videos(channel_list)
    
    # 儲存結果
    with open("long_movies.txt", "w", encoding="utf-8") as f:
        for line in final_data:
            f.write(line + "\n")
            
    print(f"任務完成！已篩選出 {len(final_data)} 部 20 分鐘以上的影片。")
