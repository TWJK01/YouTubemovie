import yt_dlp
import os

def fetch_long_videos(urls):
    ydl_opts = {
        'extract_flat': True, 
        'quiet': True,
        # 這裡過濾 20 分鐘 (1200秒) 以上的影片
        'match_filter': yt_dlp.utils.match_filter_func("duration > 1200"),
    }
    
    all_results = []
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        for channel_url in urls:
            try:
                target = channel_url if "/videos" in channel_url else f"{channel_url}/videos"
                info = ydl.extract_info(target, download=False)
                if 'entries' in info:
                    for entry in info['entries']:
                        if entry:
                            title = entry.get('title', '')
                            video_url = f"https://www.youtube.com/watch?v={entry.get('id')}"
                            lang_tag = "[國語]" if "國語" in title else ""
                            all_results.append(f"{title}{lang_tag},{video_url}")
            except Exception as e:
                print(f"Error: {e}")
    return all_results

if __name__ == "__main__":
    channel_list = [
        "https://www.youtube.com/@8-hkmovie",
        "https://www.youtube.com/@chnclassic"
    ]
    
    final_data = fetch_long_videos(channel_list)
    
    # 統一檔名為 movie_links.txt
    with open("movie_links.txt", "w", encoding="utf-8") as f:
        for line in final_data:
            f.write(line + "\n")
    
    # 確認檔案已產生
    if os.path.exists("movie_links.txt"):
        print("File movie_links.txt created successfully.")
