import re
import sys

def search_vid_pid_chunked(exe_path):
    pattern = re.compile(b'VID_([0-9A-F]{4})&PID_([0-9A-F]{4})', re.IGNORECASE)
    
    try:
        with open(exe_path, 'rb') as file:
            chunk_size = 4096
            overlap = len(max(pattern.patterns, key=len)) - 1
            prev_chunk = b''
            matches = []

            while True:
                chunk = file.read(chunk_size)
                if not chunk:
                    break

                data_to_scan = prev_chunk + chunk
                found_matches = pattern.findall(data_to_scan)
                matches.extend(found_matches)
                prev_chunk = chunk[-overlap:]

            if matches:
                for match in matches:
                    print("Found VID: {} and PID: {}".format(match[0].decode(), match[1].decode()))
            else:
                print("No VID and PID found in the file.")
    except IOError:
        print("Error: File cannot be opened. Please check the file path.")

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python script_name.py path_to_your_executable.exe")
    else:
        search_vid_pid_chunked(sys.argv[1])
