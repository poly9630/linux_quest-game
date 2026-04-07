from flask import Flask, render_template, jsonify, request, session
import json, random, time, os

app = Flask(__name__)
app.secret_key = os.urandom(24)

LEVELS = {
    1: {
        "name": "File Navigation",
        "icon": "🌱",
        "tier": "Beginner",
        "description": "Learn to move around the filesystem",
        "xp_reward": 100,
        "questions": [
            {"type":"mcq","question":"Which command lists files in the current directory?","choices":["ls","cd","pwd","cat"],"answer":"ls","explanation":"`ls` lists directory contents. Add `-la` for details and hidden files."},
            {"type":"mcq","question":"Which command prints the current working directory?","choices":["cd","pwd","ls","echo"],"answer":"pwd","explanation":"`pwd` stands for Print Working Directory — it shows exactly where you are."},
            {"type":"fill","question":"Type the command to change to the home directory:","answer":"cd ~","alt_answers":["cd","cd ~/","cd $HOME"],"explanation":"`cd ~` or just `cd` takes you to your home directory."},
            {"type":"fill","question":"Type the command to go UP one directory level:","answer":"cd ..","alt_answers":["cd.."],"explanation":"`cd ..` moves to the parent directory."},
            {"type":"mcq","question":"Which flag shows HIDDEN files with `ls`?","choices":["-h","-a","-l","-r"],"answer":"-a","explanation":"`ls -a` shows all files including hidden ones (starting with `.`)."},
        ]
    },
    2: {
        "name": "File Management",
        "icon": "🌿",
        "tier": "Beginner",
        "description": "Create, copy, move, and delete files",
        "xp_reward": 150,
        "questions": [
            {"type":"mcq","question":"Which command creates an empty file?","choices":["mkdir","touch","create","new"],"answer":"touch","explanation":"`touch filename` creates an empty file or updates timestamps."},
            {"type":"mcq","question":"Which command creates a new directory?","choices":["touch","newdir","mkdir","create"],"answer":"mkdir","explanation":"`mkdir dirname` creates a new directory."},
            {"type":"fill","question":"Type the command to copy 'file.txt' to 'backup.txt':","answer":"cp file.txt backup.txt","alt_answers":[],"explanation":"`cp source destination` copies files."},
            {"type":"fill","question":"Type the command to MOVE (rename) 'old.txt' to 'new.txt':","answer":"mv old.txt new.txt","alt_answers":[],"explanation":"`mv` moves or renames files."},
            {"type":"mcq","question":"Which command removes an EMPTY directory?","choices":["rm","rmdir","del","remove"],"answer":"rmdir","explanation":"`rmdir` removes empty directories. Use `rm -rf` for non-empty (carefully!)."},
            {"type":"mcq","question":"Which command removes a file?","choices":["del","erase","rm","unlink"],"answer":"rm","explanation":"`rm filename` removes a file permanently — no recycle bin!"},
        ]
    },
    3: {
        "name": "File Content",
        "icon": "🌲",
        "tier": "Intermediate",
        "description": "View and search file content",
        "xp_reward": 200,
        "questions": [
            {"type":"mcq","question":"Which command shows the content of a file?","choices":["show","cat","read","open"],"answer":"cat","explanation":"`cat` concatenates and displays file content."},
            {"type":"mcq","question":"Which command shows file content one screen at a time?","choices":["cat","less","view","page"],"answer":"less","explanation":"`less` allows scrolling through files. Press `q` to quit."},
            {"type":"mcq","question":"Which command shows the FIRST 10 lines of a file?","choices":["start","top","head","first"],"answer":"head","explanation":"`head file.txt` shows the first 10 lines. Use `-n 20` for 20 lines."},
            {"type":"mcq","question":"Which command shows the LAST 10 lines of a file?","choices":["end","bottom","tail","last"],"answer":"tail","explanation":"`tail file.txt` shows the last 10 lines. `-f` follows live updates!"},
            {"type":"fill","question":"Type the command to search for 'error' inside 'log.txt':","answer":"grep error log.txt","alt_answers":["grep 'error' log.txt"],"explanation":"`grep pattern file` searches for text patterns in files."},
            {"type":"mcq","question":"Which flag makes `grep` case-INSENSITIVE?","choices":["-c","-n","-i","-v"],"answer":"-i","explanation":"`grep -i` ignores upper/lowercase differences."},
        ]
    },
    4: {
        "name": "Permissions & Ownership",
        "icon": "🔥",
        "tier": "Intermediate",
        "description": "Control who can read, write, and execute files",
        "xp_reward": 250,
        "questions": [
            {"type":"mcq","question":"Which command changes file permissions?","choices":["chown","chmod","chperm","access"],"answer":"chmod","explanation":"`chmod` changes the access permissions of files."},
            {"type":"mcq","question":"Which command changes file OWNERSHIP?","choices":["chmod","chown","chgrp","own"],"answer":"chown","explanation":"`chown user:group file` changes ownership."},
            {"type":"mcq","question":"In `ls -l`, what does `rwxr-xr--` mean for the OWNER?","choices":["Read only","Read and write only","Read, write, and execute","Execute only"],"answer":"Read, write, and execute","explanation":"The first 3 chars (rwx) = owner permissions. r=read, w=write, x=execute."},
            {"type":"mcq","question":"What numeric permission gives EVERYONE full access (read+write+execute)?","choices":["644","755","777","600"],"answer":"777","explanation":"7 = 4+2+1 (r+w+x). `chmod 777` gives full access to all — use carefully!"},
            {"type":"fill","question":"Type the command to make 'script.sh' executable for the owner only:","answer":"chmod u+x script.sh","alt_answers":["chmod 700 script.sh","chmod 744 script.sh"],"explanation":"`u+x` adds execute permission for the user (owner)."},
        ]
    },
    5: {
        "name": "Processes & System",
        "icon": "⚡",
        "tier": "Advanced",
        "description": "Manage running processes and system info",
        "xp_reward": 300,
        "questions": [
            {"type":"mcq","question":"Which command shows all running processes?","choices":["jobs","ps aux","run","tasks"],"answer":"ps aux","explanation":"`ps aux` shows all processes with CPU/memory usage."},
            {"type":"mcq","question":"Which command provides a live/interactive process viewer?","choices":["ps","top","list","proc"],"answer":"top","explanation":"`top` (or `htop`) shows a dynamic real-time view of processes."},
            {"type":"fill","question":"Type the command to kill a process with PID 1234:","answer":"kill 1234","alt_answers":["kill -9 1234"],"explanation":"`kill PID` sends SIGTERM. `kill -9 PID` forces immediate termination."},
            {"type":"mcq","question":"Which command shows disk usage of the filesystem?","choices":["du","df -h","disk","space"],"answer":"df -h","explanation":"`df -h` shows disk space in human-readable format."},
            {"type":"mcq","question":"Which command shows memory usage?","choices":["mem","free -h","ram","memory"],"answer":"free -h","explanation":"`free -h` shows RAM and swap usage in human-readable format."},
            {"type":"mcq","question":"Which symbol runs a command in the BACKGROUND?","choices":["#","$","&","@"],"answer":"&","explanation":"Appending `&` runs a command in the background: `sleep 60 &`"},
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

def get_state():
    return session.get('state', {
        'name': 'Penguin', 'xp': 0, 'level': 1, 'lives': 3,
        'streak': 0, 'max_streak': 0, 'correct': 0, 'wrong': 0,
        'badges': [], 'start_time': time.time(),
        'current_level': None, 'questions': [], 'q_index': 0,
        'level_correct': 0, 'mode': None,
    })

def save_state(s):
    session['state'] = s

def calc_level(xp):
    thresholds = [0, 200, 500, 900, 1400, 2000]
    return sum(1 for t in thresholds if xp >= t)

def accuracy(s):
    total = s['correct'] + s['wrong']
    return round(s['correct'] / total * 100, 1) if total > 0 else 0.0

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/start', methods=['POST'])
def start():
    data = request.json
    s = {
        'name': data.get('name', 'Penguin') or 'Penguin',
        'xp': 0, 'level': 1, 'lives': 3, 'streak': 0,
        'max_streak': 0, 'correct': 0, 'wrong': 0, 'badges': [],
        'start_time': time.time(), 'current_level': None,
        'questions': [], 'q_index': 0, 'level_correct': 0, 'mode': None,
    }
    save_state(s)
    return jsonify({'ok': True, 'state': s})

@app.route('/api/state')
def state():
    s = get_state()
    s['accuracy'] = accuracy(s)
    return jsonify(s)

@app.route('/api/levels')
def levels():
    out = {}
    for k, v in LEVELS.items():
        out[k] = {
            'name': v['name'], 'icon': v['icon'], 'tier': v['tier'],
            'description': v['description'], 'xp_reward': v['xp_reward'],
            'question_count': len(v['questions'])
        }
    return jsonify(out)

@app.route('/api/start_mode', methods=['POST'])
def start_mode():
    s = get_state()
    data = request.json
    mode = data.get('mode')
    s['mode'] = mode
    s['lives'] = 3
    s['streak'] = 0
    s['q_index'] = 0
    s['level_correct'] = 0

    if mode == 'story':
        s['current_level'] = 1
        qs = LEVELS[1]['questions'][:]
        random.shuffle(qs)
        s['questions'] = qs
    elif mode == 'quiz':
        all_q = []
        for lv in LEVELS.values():
            all_q.extend(lv['questions'])
        s['questions'] = random.sample(all_q, min(10, len(all_q)))
    elif mode == 'survival':
        all_q = []
        for lv in LEVELS.values():
            all_q.extend(lv['questions'])
        random.shuffle(all_q)
        s['questions'] = all_q

    save_state(s)
    return jsonify({'ok': True, 'total': len(s['questions']),
                    'level': s.get('current_level'), 'mode': mode})

@app.route('/api/question')
def question():
    s = get_state()
    qs = s['questions']
    idx = s['q_index']

    if s['lives'] <= 0:
        return jsonify({'done': True, 'reason': 'no_lives'})
    if idx >= len(qs):
        return jsonify({'done': True, 'reason': 'complete'})

    q = dict(qs[idx])
    choices = q.get('choices', [])
    if choices:
        shuffled = choices[:]
        random.shuffle(shuffled)
        q['shuffled_choices'] = shuffled

    return jsonify({
        'done': False,
        'question': q,
        'index': idx,
        'total': len(qs),
        'mode': s['mode'],
        'level': s.get('current_level'),
        'lives': s['lives'],
        'streak': s['streak'],
        'xp': s['xp'],
    })

@app.route('/api/answer', methods=['POST'])
def answer():
    s = get_state()
    data = request.json
    user_ans = (data.get('answer') or '').strip()
    qs = s['questions']
    idx = s['q_index']

    if idx >= len(qs):
        return jsonify({'error': 'No question'}), 400

    q = qs[idx]
    correct = q['answer']
    alts = q.get('alt_answers', [])
    is_correct = (user_ans == correct or user_ans in alts)

    badge_earned = None
    level_up = False
    level_complete = None

    if is_correct:
        s['correct'] += 1
        s['streak'] += 1
        s['max_streak'] = max(s['streak'], s['max_streak'])
        bonus = s['streak'] >= 3
        gained = int(20 * 1.5) if bonus else 20
        s['xp'] += gained
        s['level_correct'] = s.get('level_correct', 0) + 1
    else:
        s['wrong'] += 1
        s['streak'] = 0
        s['lives'] -= 1
        gained = 0
        bonus = False

    old_level = s['level']
    s['level'] = calc_level(s['xp'])
    level_up = s['level'] > old_level

    s['q_index'] += 1
    next_done = s['lives'] <= 0 or s['q_index'] >= len(qs)

    # Story mode: level transition
    if s['mode'] == 'story' and s['q_index'] >= len(qs):
        cur = s['current_level']
        total_q = len(qs)
        passing = s['level_correct'] >= total_q * 0.6
        if passing:
            s['xp'] += LEVELS[cur]['xp_reward']
            badge_name = LEVELS[cur]['name'] + " Master"
            if badge_name not in s['badges']:
                s['badges'].append(badge_name)
                badge_earned = badge_name
        level_complete = {'level': cur, 'passing': passing,
                          'correct': s['level_correct'], 'total': total_q,
                          'xp_reward': LEVELS[cur]['xp_reward'] if passing else 0}

        # Advance to next level
        next_lv = cur + 1
        if next_lv in LEVELS:
            s['current_level'] = next_lv
            nqs = LEVELS[next_lv]['questions'][:]
            random.shuffle(nqs)
            s['questions'] = nqs
            s['q_index'] = 0
            s['level_correct'] = 0
            next_done = False
        else:
            # All done
            if 'Linux Quest Champion' not in s['badges']:
                s['badges'].append('Linux Quest Champion')
            next_done = True

    # Survival badges
    if s['mode'] == 'survival' and next_done:
        if s['correct'] >= 10 and 'Survival Expert' not in s['badges']:
            s['badges'].append('Survival Expert')
            badge_earned = 'Survival Expert'

    save_state(s)
    return jsonify({
        'correct': is_correct,
        'answer': correct,
        'explanation': q['explanation'],
        'xp_gained': gained,
        'bonus': bonus,
        'streak': s['streak'],
        'lives': s['lives'],
        'xp': s['xp'],
        'player_level': s['level'],
        'level_up': level_up,
        'badge_earned': badge_earned,
        'level_complete': level_complete,
        'done': next_done,
        'accuracy': accuracy(s),
    })

@app.route('/api/stats')
def stats():
    s = get_state()
    elapsed = int(time.time() - s.get('start_time', time.time()))
    return jsonify({
        'name': s['name'], 'xp': s['xp'], 'level': s['level'],
        'correct': s['correct'], 'wrong': s['wrong'],
        'accuracy': accuracy(s), 'max_streak': s['max_streak'],
        'badges': s['badges'],
        'time': f"{elapsed // 60}m {elapsed % 60}s"
    })

@app.route('/api/reference')
def reference():
    return jsonify(COMMAND_REFERENCE)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
