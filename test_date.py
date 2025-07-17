filename1 = "video_anime_20250717_181836.mp4"
filename2 = "video_seedance_20250717_185303.mp4"

def parse_date(filename):
    try:
        parts = filename.split('_')
        print(f"Filename: {filename}")
        print(f"Parts: {parts}")
        if len(parts) >= 4:
            date_part = parts[2]  # 20250717
            time_part = parts[3].split('.')[0]  # 181836
            print(f"Date part: {date_part}")
            print(f"Time part: {time_part}")
            date_str = f"{date_part[:4]}-{date_part[4:6]}-{date_part[6:8]}T{time_part[:2]}:{time_part[2:4]}:{time_part[4:6]}"
            print(f"Result: {date_str}")
            return date_str
        else:
            print("Not enough parts")
            return None
    except Exception as e:
        print(f"Error: {e}")
        return None

print("=== TEST 1 ===")
parse_date(filename1)
print("\n=== TEST 2 ===")
parse_date(filename2)
