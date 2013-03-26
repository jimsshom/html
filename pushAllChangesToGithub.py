#!/usr/bin/env python
import commands
import time

global added_files
added_files = []
global modified_files
modified_files = []
global deleted_files
deleted_files = []

def proc_shell_cmd(cmd):
    status, output = commands.getstatusoutput(cmd)
    if status != 0:
        raise Exception('cmd=' + cmd + ' ,retCode=' + str(status))
    return output

def is_file_line(line):
    return line.startswith('#\t')

def add_tracked_files(line):
    if line.startswith('#\tdeleted:'):
        deleted_files.append(line[len('#\t')+12:].strip())
    elif line.startswith('#\tmodified:'):
        modified_files.append(line[len('#\t')+12:].strip())

def add_untracked_files(line):
    added_files.append(line[len('#\t'):].strip())

def proc_git_status(status_text):
    lines = status_text.split('\n')
    state = 0#0: not start  1: tracked files  2: untracked files
    for line in lines:
        line = line.strip()
        if line.find('Changes not staged for commit') != -1:
            state = 1
        elif line.find('Untracked files') != -1:
            state = 2
        if is_file_line(line):
            if state == 1:
                add_tracked_files(line)
            elif state == 2:
                add_untracked_files(line)

def get_date_str():
    return time.strftime('%Y%m%d',time.localtime(time.time()))

def generate_github_cmd():
    cmd = []
    for filename in added_files + modified_files:
        cmd.append('git add ' + filename)
    for filename in deleted_files:
        cmd.append('git rm ' + filename)
    cmd.append('git commit -m "by AotuAssist on ' + get_date_str() + '"')
    cmd.append('git push')
    return cmd

try:
    status = proc_shell_cmd('git status')
    print status
    proc_git_status(status)
    cmd_lists = generate_github_cmd()
    for cmd in cmd_lists:
        print proc_shell_cmd(cmd)
except Exception, e:
    print Exception, ":", e
