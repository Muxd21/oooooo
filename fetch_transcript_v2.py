import yt_dlp
import sys
import json
import os

def fetch_transcript(url, output_file=None):
    ydl_opts = {
        'skip_download': True,
        'writesubtitles': True,
        'writeautomaticsub': True,
        'subtitleslangs': ['en'],
        'outtmpl': '%(id)s.%(ext)s',
        'quiet': True,
        'no_warnings': True,
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(url, download=True)
            video_id = info['id']
            title = info['title']
            
            vtt_file = f"{video_id}.en.vtt"
            if not os.path.exists(vtt_file):
                # Try auto-generated
                vtt_file = f"{video_id}.en.vtt"
                # If still not there, try different formats?
                pass
            
            if os.path.exists(vtt_file):
                with open(vtt_file, 'r', encoding='utf-8') as f:
                    vtt_content = f.read()
                
                # Simple cleanup of VTT
                lines = []
                for line in vtt_content.split('\n'):
                    if '-->' in line or line.strip() == '' or line.isdigit() or line.startswith('WEBVTT'):
                        continue
                    # Remove timestamps like <00:00:00.000>
                    line = line.replace('<', '[').replace('>', ']') # Placeholder
                    lines.append(line.strip())
                
                transcript = ' '.join(lines)
                
                # Cleanup files
                if os.path.exists(vtt_file):
                    os.remove(vtt_file)
                
                final_text = f"# {title}\n\n{transcript}"
                
                if output_file:
                    with open(output_file, 'w', encoding='utf-8') as f:
                        f.write(final_text)
                    return f"Saved to {output_file}"
                return final_text
            else:
                return "Error: Could not find transcript."
                
        except Exception as e:
            return f"Error: {str(e)}"

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python fetch_transcript_v2.py <URL>")
        sys.exit(1)
    
    print(fetch_transcript(sys.argv[1]))
