import argparse
import csv
import os
import re
import sys
import subprocess

def parse_time(time_str):
    """Parse time strings in various formats to seconds"""
    # Normalize separators and decimal points
    normalized = time_str.replace(',', '.').replace(';', ':')
    parts = re.split(r'[:]', normalized)
    
    if not parts:
        return 0.0
    
    try:
        # Convert parts to floats
        time_parts = [float(part) for part in parts]
    except ValueError:
        raise ValueError(f"Invalid time format: {time_str}")
    
    if len(time_parts) == 3:  # HH:MM:SS
        return time_parts[0]*3600 + time_parts[1]*60 + time_parts[2]
    elif len(time_parts) == 2:  # MM:SS
        return time_parts[0]*60 + time_parts[1]
    elif len(time_parts) == 1:  # SS
        return time_parts[0]
    else:
        raise ValueError(f"Unsupported time format: {time_str}")

def extract_audio_segment(video_path, start, end, output_file, audio_format, bitrate, ffmpeg_path='ffmpeg'):
    """Extract audio segment using FFmpeg"""
    # Map formats to FFmpeg codecs
    codec_map = {
        'mp3': 'libmp3lame',
        'm4a': 'aac',
        'wav': 'pcm_s16le'
    }
    
    if audio_format not in codec_map:
        raise ValueError(f"Unsupported audio format: {audio_format}")
    
    # Construct FFmpeg command
    cmd = [
        ffmpeg_path,
        '-ss', str(start),
        '-to', str(end),
        '-i', video_path,
        '-vn',              # Disable video
        '-acodec', codec_map[audio_format],
        '-b:a', bitrate,
        '-y',               # Overwrite output
        output_file
    ]
    
    # Run FFmpeg command
    result = subprocess.run(
        cmd, 
        stdout=subprocess.PIPE, 
        stderr=subprocess.PIPE,
        text=True
    )
    
    if result.returncode != 0:
        error_msg = result.stderr.split('error')[-1][:200]
        raise RuntimeError(f"FFmpeg error: {error_msg}")

def main():
    parser = argparse.ArgumentParser(
        description='Extract audio segments from video files (MP4, WebM, MOV, etc.)',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument('video', help='Input video file path')
    parser.add_argument('csv', help='CSV file with segment timestamps')
    parser.add_argument('-o', '--output-dir', default='./audio_segments', 
                        help='Output directory for audio files')
    parser.add_argument('-f', '--format', choices=['mp3', 'm4a', 'wav'], default='mp3',
                        help='Output audio format')
    parser.add_argument('--start-col', type=int, default=0, 
                        help='Column index (0-based) for start time')
    parser.add_argument('--end-col', type=int, default=1, 
                        help='Column index (0-based) for end time')
    parser.add_argument('--name-col', type=int, default=None,
                        help='Column index (0-based) for custom segment names')
    parser.add_argument('--no-header', action='store_true',
                        help='CSV has no header row')
    parser.add_argument('--bitrate', default='192k',
                        help='Audio bitrate (e.g., 128k, 192k, 256k)')
    parser.add_argument('--ffmpeg-path', default='ffmpeg',
                        help='Path to FFmpeg executable')
    
    args = parser.parse_args()
    
    # Create output directory
    os.makedirs(args.output_dir, exist_ok=True)
    
    # Validate columns
    if args.start_col == args.end_col:
        sys.exit("Error: Start and end columns must be different")
    
    if args.name_col is not None and args.name_col in (args.start_col, args.end_col):
        sys.exit("Error: Name column conflicts with time columns")
    
    # Check FFmpeg installation
    try:
        subprocess.run(
            [args.ffmpeg_path, '-version'],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=True
        )
    except Exception as e:
        sys.exit(f"FFmpeg not found: {e}\nInstall with: sudo apt install ffmpeg")
    
    # Read CSV segments
    segments = []
    with open(args.csv, 'r', encoding='utf-8-sig') as f:
        reader = csv.reader(f)
        if not args.no_header:
            next(reader)  # Skip header row
        
        for row_idx, row in enumerate(reader, start=1):
            if len(row) <= max(args.start_col, args.end_col):
                print(f"Warning: Row {row_idx} has insufficient columns - skipping")
                continue
            
            try:
                start_time = parse_time(row[args.start_col])
                end_time = parse_time(row[args.end_col])
                
                if end_time <= start_time:
                    print(f"Warning: Row {row_idx} has end time before start time - skipping")
                    continue
                
                # Get custom name if available
                segment_name = None
                if args.name_col is not None and len(row) > args.name_col:
                    segment_name = row[args.name_col].strip()
                
                segments.append((start_time, end_time, segment_name))
            except ValueError as e:
                print(f"Error processing row {row_idx}: {e} - skipping")
    
    if not segments:
        sys.exit("No valid segments found in CSV file")
    
    # Process segments
    base_name = os.path.splitext(os.path.basename(args.video))[0]
    success_count = 0
    
    for i, (start, end, name) in enumerate(segments, start=1):
        try:
            # Generate output filename
            if name:
                safe_name = re.sub(r'[\\/*?:"<>|]', "_", name)
                output_file = os.path.join(args.output_dir, f"{safe_name}.{args.format}")
            else:
                output_file = os.path.join(args.output_dir, f"{base_name}_segment_{i}.{args.format}")
            
            print(f"Extracting segment {i}: {start:.2f}s to {end:.2f}s")
            
            # Extract using FFmpeg
            extract_audio_segment(
                args.video,
                start,
                end,
                output_file,
                args.format,
                args.bitrate,
                args.ffmpeg_path
            )
            
            print(f"Created: {output_file}")
            success_count += 1
        except Exception as e:
            print(f"Error processing segment {i}: {e}")
    
    print(f"\nSuccessfully extracted {success_count}/{len(segments)} segments")

if __name__ == '__main__':
    main()