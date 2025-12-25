import yt_dlp
import os

def fetch_classified_videos(urls):
    ydl_opts = {
        'extract_flat': True, 
        'quiet': True,
        # 篩選 20 分鐘 (1200秒) 以上的影片
        'match_filter': yt_dlp.utils.match_filter_func("duration > 1200"),
    }
    
    mandarin_list = []
    cantonese_list = []
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        for channel_url in urls:
            try:
                # 自動補上 /videos 確保抓取影片分頁
                target = channel_url if "/videos" in channel_url else f"{channel_url}/videos"
                info = ydl.extract_info(target, download=False)
                
                if 'entries' in info:
                    for entry in info['entries']:
                        if not entry: continue
                        
                        title = entry.get('title', '')
                        video_url = f"https://www.youtube.com/watch?v={entry.get('id')}"
                        
                        # 根據標題判斷語言分類
                        if "國語" in title:
                            mandarin_list.append(f"{title},{video_url}")
                        elif "粵語" in title:
                            cantonese_list.append(f"{title},{video_url}")
            except Exception as e:
                print(f"Error processing {channel_url}: {e}")
                
    return mandarin_list, cantonese_list

if __name__ == "__main__":
    # 您可以根據需求在此清單加入多個頻道網址
    channels = [
        "https://www.youtube.com/@8-hkmovie"
    ]
    
    m_list, c_list = fetch_classified_videos(channels)
    
    with open("movie_links.txt", "w", encoding="utf-8") as f:
        # --- 輸出國語部分 ---
        if m_list:
            f.write("國語,#genre#\n")
            for item in m_list:
                f.write(item + "\n")
            f.write("\n") # 區隔空行
        
        # --- 輸出粵語部分 ---
        if c_list:
            f.write("粵語,#genre#\n")
            for item in c_list:
                f.write(item + "\n")
            f.write("\n")
                
    print("檔案已依照指定格式產生：movie_links.txt")
