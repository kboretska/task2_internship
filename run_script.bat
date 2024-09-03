@echo off
set timestamp=%date:~-4%-%date:~-7,2%-%date:~-10,2%_%time:~0,2%-%time:~3,2%
set timestamp=%timestamp: =0%
python C:\Users\kbore\internship\sftp-cluster\srcipt.py > C:\Users\kbore\internship\sftp-cluster\logs\output_%timestamp%.txt 2>&1
