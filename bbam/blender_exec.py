import sys
import re
import subprocess

def build_extension(src, dst, blender_executable_path):

    command = [
        blender_executable_path,
        '--command', 'extension', 'build',
        '--source-dir', src,
        '--output-filepath', dst,
    ]
    result = subprocess.run(command, capture_output=True, text=True)
    return result

def get_build_file(build_result):
    match = re.search(r'created: "([^"]+)"', build_result.stdout)
    if match:
        return match.group(1)
    return None

def validate_extension(path, blender_executable_path):
    validate_command = [
        blender_executable_path,
        '--command', 'extension', 'validate', 
        path,
    ]
    subprocess.run(validate_command)