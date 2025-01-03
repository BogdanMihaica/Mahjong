import subprocess


subprocess.Popen(['start', 'cmd', '/K', "python server.py"], shell=True)
for _ in range(4):
    subprocess.Popen(['start', 'cmd', '/K', "python mahjong.py"], shell=True)
