import yt_dlp
import os

def fetch_classified_videos(urls):
    ydl_opts = {
        'extract_flat': True, 
        'quiet': True,
        'match_filter': yt_dlp.utils.match_filter_func("duration > 1200"), # 20分鐘以上
    }
    
    mandarin_list = []
    cantonese_list = []
    other_list = []
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        for channel_url in urls:
            try:
                target = channel_url if "/videos" in channel_url else f"{channel_url}/videos"
                info = ydl.extract_info(target, download=False)
                if 'entries' in info:
                    for entry in info['entries']:
                        if not entry: continue
                        
                        title = entry.get('title', '')
                        video_url = f"https://www.youtube.com/watch?v={entry.get('id')}"
                        
                        # 根據關鍵字分類並格式化
                        if "國語" in title:
                            mandarin_list.append(f"國語,#genre# {title},{video_url}")
                        elif "粵語" in title:
                            cantonese_list.append(f"粵語,#genre# {title},{video_url}")
                        else:
                            other_list.append(f"其他,#genre# {title},{video_url}")
            except Exception as e:
                print(f"Error skipping {channel_url}: {e}")
                
    return mandarin_list, cantonese_list, other_list

if __name__ == "__main__":
    channels = [
        "https://www.youtube.com/@8-hkmovie"
    ]
    
    m_list, c_list, o_list = fetch_classified_videos(channels)
    
    with open("movie_links.txt", "w", encoding="utf-8") as f:
        # 先寫入國語
        f.write("=== 國語電影 ===\n")
        for line in m_list:
            f.write(line + "\n")
        
        # 再寫入粵語
        f.write("\n=== 粵語電影 ===\n")
        for line in c_list:
            f.write(line + "\n")
            
        # 其他（未標註語言的）
        if o_list:
            f.write("\n=== 其他 ===\n")
            for line in o_list:
                f.write(line + "\n")
                
    print("分類抓取完成！")
