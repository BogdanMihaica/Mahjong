import subprocess

subprocess.Popen(['start', 'cmd', '/K', "python server.py"], shell=True)
for i in range(4):
    subprocess.Popen(['start', 'cmd', '/K', f"python mahjong.py"], shell=True)
