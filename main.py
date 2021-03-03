from random import choice

script_file = open('script.txt', 'r')
raw_script = script_file.read().replace(' ', '').replace('\n', '')
cube_size = 0
while cube_size * cube_size * 6 < len(raw_script):
    cube_size += 1
raw_script = raw_script + '.' * cube_size * cube_size * 6
script = []
j = 0
for i in range(cube_size * 3):
    if i < cube_size or i >= cube_size * 2:
        script.append(' ' * cube_size + raw_script[j:j+cube_size])
        j += cube_size
    else:
        script.append(raw_script[j:j+cube_size * 4])
        j += cube_size * 4

if True:  # set to True to see script before running
    print()
    for row in script:
        for c in row:
            print(c, end=' ')
        print()
    print()

input_file = open('input.txt', 'r')
inp = input_file.read()
inp_char = 0
memory = [0]
memory_cell = 0
ip_x = cube_size
ip_y = 0
ip_dir = 1  # 0 = up, 1 = right, 2 = down, 3 = left
gravity = 2
ignore = 0
command = '.'

def move(direction):
    global ip_x
    global ip_y
    global ip_dir
    global gravity
    if direction == 0:  # up
        ip_y -= 1
        if ip_x < cube_size and ip_y < cube_size:
            ip_y = ip_x
            ip_x = cube_size
            ip_dir = (ip_dir + 1) % 4
            gravity = (gravity + 1) % 4
        elif ip_x >= cube_size * 3 and ip_y < cube_size:
            ip_x = cube_size * 5 - 1 - ip_x
            ip_y = 0
            ip_dir = (ip_dir + 2) % 4
            gravity = (gravity + 2) % 4
        elif ip_x >= cube_size * 2 and ip_y < cube_size:
            ip_y = cube_size * 3 - 1 - ip_x
            ip_x = cube_size * 2 - 1
            ip_dir = (ip_dir + 3) % 4
            gravity = (gravity + 3) % 4
        elif ip_y < 0:
            ip_x = cube_size * 5 - 1 - ip_x
            ip_y = cube_size
            ip_dir = (ip_dir + 2) % 4
            gravity = (gravity + 2) % 4

    elif direction == 1:  # right
        ip_x += 1
        if ip_x >= cube_size * 2 and ip_y < cube_size:
            ip_x = cube_size * 3 - 1 - ip_y
            ip_y = cube_size
            ip_dir = (ip_dir + 1) % 4
            gravity = (gravity + 1) % 4
        elif ip_x >= cube_size * 2 and ip_y >= cube_size * 2:
            ip_x = ip_y
            ip_y = cube_size * 2 - 1
            ip_dir = (ip_dir + 3) % 4
            gravity = (gravity + 3) % 4
        elif ip_x >= cube_size * 4:
            ip_x = 0

    elif direction == 2:  # down
        ip_y += 1
        if ip_x < cube_size and ip_y >= cube_size * 2:
            ip_y = cube_size * 3 - 1 - ip_x
            ip_x = cube_size
            ip_dir = (ip_dir + 3) % 4
            gravity = (gravity + 3) % 4
        elif ip_x >= cube_size * 3 and ip_y >= cube_size * 2:
            ip_x = cube_size * 5 - 1 - ip_x
            ip_y = cube_size * 3 - 1
            ip_dir = (ip_dir + 2) % 4
            gravity = (gravity + 2) % 4
        elif ip_x >= cube_size * 2 and ip_y >= cube_size * 2:
            ip_y = ip_x
            ip_x = cube_size * 2 - 1
            ip_dir = (ip_dir + 1) % 4
            gravity = (gravity + 1) % 4
        elif ip_y >= cube_size * 3:
            ip_x = cube_size * 5 - 1 - ip_x
            ip_y = cube_size * 2 - 1
            ip_dir = (ip_dir + 2) % 4
            gravity = (gravity + 2) % 4

    elif direction == 3:  # left
        ip_x -= 1
        if ip_x < cube_size and ip_y < cube_size:
            ip_x = ip_y
            ip_y = cube_size
            ip_dir = (ip_dir + 3) % 4
            gravity = (gravity + 3) % 4
        elif ip_x < cube_size and ip_y >= cube_size * 2:
            ip_x = cube_size * 3 - 1 - ip_y
            ip_y = cube_size * 2 - 1
            ip_dir = (ip_dir + 1) % 4
            gravity = (gravity + 1) % 4
        elif ip_x < 0:
            ip_x = cube_size * 4 - 1

space = False

while True:
    if ignore > 0:
        ignore -= 1
    command = script[ip_y][ip_x]
    carried = False
    if ignore == 0:
        if command == '@':
            break
        elif command == '^':
            if gravity % 2 == 1:
                ip_dir = 0
            elif gravity == 2:
                carried = True
        elif command == '>':
            if gravity % 2 == 0:
                ip_dir = 1
            elif gravity == 3:
                carried = True
        elif command == 'v':
            if gravity % 2 == 1:
                ip_dir = 2
            elif gravity == 0:
                carried = True
        elif command == '<':
            if gravity % 2 == 0:
                ip_dir = 3
            elif gravity == 1:
                carried = True
        elif command == '?':
            if gravity % 2 == 0:
                ip_dir = choice([1, 3])
            else:
                ip_dir = choice([0, 2])
        elif command == '+':
            memory[memory_cell] += 1
        elif command == '-':
            memory[memory_cell] -= 1
        elif command == '(':
            if memory_cell == 0:
                memory.insert(0, 0)
            else:
                memory_cell -= 1
        elif command == ')':
            memory_cell += 1
            if memory_cell == len(memory):
                memory.append(0)
        elif command == '*':
            if space:
                print(' ', end='', flush=True)
            print(chr(memory[memory_cell]), end='', flush=True)
            space = False
        elif command == '=':
            if space:
                print(' ', end='', flush=True)
            print(memory[memory_cell], end='', flush=True)
            space = True
        elif command == ',':
            if inp_char < len(inp):
                memory[memory_cell] = ord(inp[inp_char])
                inp_char += 1
            else:
                memory[memory_cell] = 0

        elif command == ';':  # not consistent with MarioLANG like I planned
            get_num = ''
            if inp_char < len(inp):
                if inp[inp_char] == ' ':
                    inp_char += 1
            while inp[inp_char] in '0123456789':
                get_num = get_num + inp[inp_char]
                inp_char += 1
                if inp_char >= len(inp):
                    break
            if inp_char < len(inp):
                if inp[inp_char] == ' ':
                    inp_char += 1
            try:
                memory[memory_cell] = int(get_num)
            except:
                pass

        elif command == '!':
            if memory[memory_cell] == 0:
                ignore = 2
        elif command == '$':
            if memory[memory_cell] != 0:
                ignore = 2
    if ignore > 0 and command not in '@^>v<?+-()*=,;!':
        ignore = 2
    if carried:
        move(ip_dir)
    else:
        move(gravity)
        if script[ip_y][ip_x] == '#':
            move((gravity + 2) % 4)
            move(ip_dir)
