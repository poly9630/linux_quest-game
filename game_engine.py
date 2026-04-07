"""
Linux Quest – Game Engine
Adapted from the CLI version for web/Flask usage.
"""
import random
import time

# ─────────────────────────────────────────────
#  Game Data
# ─────────────────────────────────────────────
LEVELS = {
    1: {
        "name": "File Navigation",
        "icon": "🌱",
        "tier": "Beginner",
        "description": "Learn to move around the filesystem",
        "xp_reward": 100,
        "questions": [
            {
                "type": "mcq",
                "question": "Which command lists files in the current directory?",
                "choices": ["ls", "cd", "pwd", "cat"],
                "answer": "ls",
                "explanation": "`ls` lists directory contents. Add `-la` for hidden files and details."
            },
            {
                "type": "mcq",
                "question": "Which command prints the current working directory?",
                "choices": ["cd", "pwd", "ls", "echo"],
                "answer": "pwd",
                "explanation": "`pwd` stands for Print Working Directory."
            },
            {
                "type": "fill",
                "question": "Type the command to change to the home directory:",
                "answer": "cd ~",
                "alt_answers": ["cd", "cd ~/", "cd $HOME"],
                "explanation": "`cd ~` or just `cd` takes you to your home directory."
            },
            {
                "type": "fill",
                "question": "Type the command to go UP one directory level:",
                "answer": "cd ..",
                "alt_answers": ["cd.."],
                "explanation": "`cd ..` moves to the parent directory."
            },
            {
                "type": "mcq",
                "question": "Which flag shows HIDDEN files with `ls`?",
                "choices": ["-h", "-a", "-l", "-r"],
                "answer": "-a",
                "explanation": "`ls -a` shows all files including hidden ones (starting with `.`)."
            },
        ]
    },
    2: {
        "name": "File Management",
        "icon": "🌿",
        "tier": "Beginner",
        "description": "Create, copy, move, and delete files",
        "xp_reward": 150,
        "questions": [
            {
                "type": "mcq",
                "question": "Which command creates an empty file?",
                "choices": ["mkdir", "touch", "create", "new"],
                "answer": "touch",
                "explanation": "`touch filename` creates an empty file or updates its timestamps."
            },
            {
                "type": "mcq",
                "question": "Which command creates a new directory?",
                "choices": ["touch", "newdir", "mkdir", "create"],
                "answer": "mkdir",
                "explanation": "`mkdir dirname` creates a new directory."
            },
            {
                "type": "fill",
                "question": "Type the command to copy 'file.txt' to 'backup.txt':",
                "answer": "cp file.txt backup.txt",
                "alt_answers": [],
                "explanation": "`cp source destination` copies files."
            },
            {
                "type": "fill",
                "question": "Type the command to MOVE (rename) 'old.txt' to 'new.txt':",
                "answer": "mv old.txt new.txt",
                "alt_answers": [],
                "explanation": "`mv` moves or renames files."
            },
            {
                "type": "mcq",
                "question": "Which command removes an EMPTY directory?",
                "choices": ["rm", "rmdir", "del", "remove"],
                "answer": "rmdir",
                "explanation": "`rmdir` removes empty directories. Use `rm -rf` for non-empty (carefully!)."
            },
            {
                "type": "mcq",
                "question": "Which command removes a file?",
                "choices": ["del", "erase", "rm", "unlink"],
                "answer": "rm",
                "explanation": "`rm filename` removes a file permanently (no recycle bin!)."
            },
        ]
    },
    3: {
        "name": "File Content",
        "icon": "🌲",
        "tier": "Intermediate",
        "description": "View and search file content",
        "xp_reward": 200,
        "questions": [
            {
                "type": "mcq",
                "question": "Which command shows the content of a file?",
                "choices": ["show", "cat", "read", "open"],
                "answer": "cat",
                "explanation": "`cat` concatenates and displays file content."
            },
            {
                "type": "mcq",
                "question": "Which command shows file content one screen at a time?",
                "choices": ["cat", "less", "view", "page"],
                "answer": "less",
                "explanation": "`less` allows scrolling through files. Press `q` to quit."
            },
            {
                "type": "mcq",
                "question": "Which command shows the FIRST 10 lines of a file?",
                "choices": ["start", "top", "head", "first"],
                "answer": "head",
                "explanation": "`head file.txt` shows the first 10 lines. Use `-n 20` for 20 lines."
            },
            {
                "type": "mcq",
                "question": "Which command shows the LAST 10 lines of a file?",
                "choices": ["end", "bottom", "tail", "last"],
                "answer": "tail",
                "explanation": "`tail file.txt` shows the last 10 lines. `-f` follows live updates!"
            },
            {
                "type": "fill",
                "question": "Type the command to search for 'error' inside 'log.txt':",
                "answer": "grep error log.txt",
                "alt_answers": ["grep 'error' log.txt"],
                "explanation": "`grep pattern file` searches for text patterns in files."
            },
            {
                "type": "mcq",
                "question": "Which flag makes `grep` case-INSENSITIVE?",
                "choices": ["-c", "-n", "-i", "-v"],
                "answer": "-i",
                "explanation": "`grep -i` ignores upper/lowercase differences."
            },
        ]
    },
    4: {
        "name": "Permissions & Ownership",
        "icon": "🔥",
        "tier": "Intermediate",
        "description": "Control who can read, write, and execute files",
        "xp_reward": 250,
        "questions": [
            {
                "type": "mcq",
                "question": "Which command changes file permissions?",
                "choices": ["chown", "chmod", "chperm", "access"],
                "answer": "chmod",
                "explanation": "`chmod` changes the access permissions of files."
            },
            {
                "type": "mcq",
                "question": "Which command changes file OWNERSHIP?",
                "choices": ["chmod", "chown", "chgrp", "own"],
                "answer": "chown",
                "explanation": "`chown user:group file` changes ownership."
            },
            {
                "type": "mcq",
                "question": "In `ls -l`, what does `rwxr-xr--` mean for the OWNER?",
                "choices": [
                    "Read only",
                    "Read and write only",
                    "Read, write, and execute",
                    "Execute only"
                ],
                "answer": "Read, write, and execute",
                "explanation": "The first 3 chars (rwx) = owner permissions. r=read, w=write, x=execute."
            },
            {
                "type": "mcq",
                "question": "What numeric permission gives EVERYONE full access (read+write+execute)?",
                "choices": ["644", "755", "777", "600"],
                "answer": "777",
                "explanation": "7 = 4+2+1 (r+w+x). `chmod 777` gives full access to all — use carefully!"
            },
            {
                "type": "fill",
                "question": "Type the command to make 'script.sh' executable for the owner only:",
                "answer": "chmod u+x script.sh",
                "alt_answers": ["chmod 700 script.sh", "chmod 744 script.sh"],
                "explanation": "`u+x` adds execute permission for the user (owner)."
            },
        ]
    },
    5: {
        "name": "Processes & System",
        "icon": "⚡",
        "tier": "Advanced",
        "description": "Manage running processes and system info",
        "xp_reward": 300,
        "questions": [
            {
                "type": "mcq",
                "question": "Which command shows all running processes?",
                "choices": ["jobs", "ps aux", "run", "tasks"],
                "answer": "ps aux",
                "explanation": "`ps aux` shows all processes with CPU/memory usage."
            },
            {
                "type": "mcq",
                "question": "Which command provides a live/interactive process viewer?",
                "choices": ["ps", "top", "list", "proc"],
                "answer": "top",
                "explanation": "`top` (or `htop`) shows a dynamic real-time view of processes."
            },
            {
                "type": "fill",
                "question": "Type the command to kill a process with PID 1234:",
                "answer": "kill 1234",
                "alt_answers": ["kill -9 1234"],
                "explanation": "`kill PID` sends SIGTERM. `kill -9 PID` forces immediate termination."
            },
            {
                "type": "mcq",
                "question": "Which command shows disk usage of the filesystem?",
                "choices": ["du", "df -h", "disk", "space"],
                "answer": "df -h",
                "explanation": "`df -h` shows disk space in human-readable format."
            },
            {
                "type": "mcq",
                "question": "Which command shows memory usage?",
                "choices": ["mem", "free -h", "ram", "memory"],
                "answer": "free -h",
                "explanation": "`free -h` shows RAM and swap usage in human-readable format."
            },
            {
                "type": "mcq",
                "question": "Which symbol runs a command in the BACKGROUND?",
                "choices": ["#", "$", "&", "@"],
                "answer": "&",
                "explanation": "Appending `&` runs a command in the background: `sleep 60 &`"
            },
        ]
    },
}

COMMAND_REFERENCE = {
    "Navigation":    ["ls", "cd", "pwd", "tree"],
    "Files":         ["touch", "mkdir", "cp", "mv", "rm", "rmdir"],
    "Content":       ["cat", "less", "more", "head", "tail", "grep", "wc"],
    "Permissions":   ["chmod", "chown", "chgrp", "umask"],
    "Processes":     ["ps", "top", "htop", "kill", "jobs", "bg", "fg"],
    "Networking":    ["ping", "curl", "wget", "ssh", "scp", "netstat"],
    "System":        ["df", "du", "free", "uname", "uptime", "who", "whoami"],
    "Pipe/Redirect": ["| (pipe)", "> (overwrite)", ">> (append)", "< (input)"],
}

XP_THRESHOLDS = [0, 200, 500, 900, 1400, 2000]
RANK_NAMES = ["Newbie", "Script Kiddie", "Shell Wizard", "Kernel Hacker", "Sysadmin", "Linux Master"]


def get_level_info():
    """Return level metadata for the frontend."""
    result = {}
    for num, data in LEVELS.items():
        result[num] = {
            "name": data["name"],
            "icon": data["icon"],
            "tier": data["tier"],
            "description": data["description"],
            "xp_reward": data["xp_reward"],
            "total_questions": len(data["questions"]),
        }
    return result


def get_questions_for_level(level_num):
    """Return shuffled questions for a level."""
    questions = LEVELS[level_num]["questions"][:]
    random.shuffle(questions)
    return questions


def get_random_questions(n=10):
    """Return n random questions from all levels."""
    all_q = []
    for data in LEVELS.values():
        all_q.extend(data["questions"])
    return random.sample(all_q, min(n, len(all_q)))


def check_answer(question, user_answer):
    """
    Returns (is_correct, correct_answer, explanation).
    """
    correct = question["answer"]
    alts = question.get("alt_answers", [])
    ua = user_answer.strip()
    is_correct = (ua == correct) or (ua in alts)
    return is_correct, correct, question["explanation"]


def compute_xp_level(xp):
    """Return (player_level, rank_name, xp_to_next, progress_pct)."""
    lvl = sum(1 for t in XP_THRESHOLDS if xp >= t)
    lvl = min(lvl, len(XP_THRESHOLDS))
    rank = RANK_NAMES[min(lvl - 1, len(RANK_NAMES) - 1)]
    if lvl < len(XP_THRESHOLDS):
        xp_curr = XP_THRESHOLDS[lvl - 1]
        xp_next = XP_THRESHOLDS[lvl]
        progress = int((xp - xp_curr) / (xp_next - xp_curr) * 100)
        to_next = xp_next - xp
    else:
        progress = 100
        to_next = 0
    return lvl, rank, to_next, progress
