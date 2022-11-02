from random import randint

# Константы
obstacle_count = 3
target_count = 3
size = 4
# Вспомогательные переменные для DFS
max_queue = -1
queue_counter = -1
dot_counter = 0
finish_found = False
queue_is_not_empty = True
target_remained = target_count
main_neighbours = []
# Временные массивы
used_dots = []
visited_dots = []
queue_dots = []
# Массивы с координатами объектов на поле
agent_dot = []
finish_dot = []
obstacle_dots = []
target_dots = []
# Cловарь объектов на поле
states_dict = {'EMPTY': 0, 'OBSTACLE': 1, 'TARGET': 2, 'FINISH': 3, 'AGENT': 4}
# Список, содержащий значения из словаря по ключу
states_list = list(states_dict.values())


def generate_field(size):
    global agent_dot, finish_dot, obstacle_dots, target_dots
    field = [[states_dict['EMPTY'] for i in range(0, size)] for j in range(0, size)]
    for state in states_list[1:]:
        if state == states_dict['OBSTACLE']:
            random_dots = generate_dots(obstacle_count, size)
            obstacle_dots = random_dots
        elif state == states_dict['TARGET']:
            random_dots = generate_dots(target_count, size)
            target_dots = random_dots
        else:
            random_dots = generate_dots(1, size)
            if state == states_dict['FINISH']:
                finish_dot = random_dots[0]
            elif state == states_dict['AGENT']:
                agent_dot = random_dots[0]
        for dot in random_dots:
            field[dot[0]][dot[1]] = state
    return field


def generate_dots(counter, size):
    global used_dots
    random_dot = []
    random_dots = []
    for i in range(0, counter + 1):
        while dot_is_used(random_dot, used_dots):
            random_dot = [randint(0, size - 1), randint(0, size - 1)]
        used_dots.append(random_dot)
        random_dots.append(random_dot)
    return random_dots[1:]


def dot_is_used(dot, used):
    return True if dot in used else False


def BFS(field, dot, field_size):
    visited_queue_dots = []
    max_queue = -1
    dot_counter = 0
    finish_found = False
    queue_is_not_empty = True
    global visited_dots, queue_dots, target_remained

    print("_______________\r\nBFS statistics\r\n_______________")
    visited_dots.append(dot)
    queue_dots.append(dot)
    while (target_remained > 0 or not finish_found) and queue_is_not_empty:
        dot_counter += 1
        cur_dot = queue_dots.pop(0)
        visited_queue_dots.append(cur_dot)
        print(f"{dot_counter}). dot = {cur_dot}")
        print(f"visited_dots: {visited_queue_dots}")
        print(f"queue: {queue_dots}")
        if field[cur_dot[0]][cur_dot[1]] == states_dict['TARGET']:
            target_remained -= 1
            print(f"target_remained: {target_remained}")
        elif field[cur_dot[0]][cur_dot[1]] == states_dict['FINISH']:
            print(f"finish found")
            finish_found = True
        for neighbour in get_neighbours(cur_dot, field, field_size):
            if neighbour not in visited_dots:
                visited_dots.append(neighbour)
                queue_dots.append(neighbour)
        if len(queue_dots) + len(visited_queue_dots) > max_queue:
            max_queue = len(queue_dots) + len(visited_queue_dots)
        if len(queue_dots) == 0:
            queue_is_not_empty = False
            print(f"Can't complete the task!\r\ntarget_remained: {target_remained}\r\nfinish found: {finish_found}")
    print(f"_______________\r\nBFS_Result\r\n_______________\r\nvisited_dots: {dot_counter}")
    print(f"max_memory_items: {max_queue}\r\n_______________")
    set_globals_to_default()


def DFS(field, dot, field_size):
    global max_queue, queue_counter, dot_counter, finish_found, queue_is_not_empty, target_remained
    counter = 0

    if dot not in visited_dots:
        dot_counter += 1
        visited_dots.append(dot)
        print(f"{dot_counter}). dot = {dot}")
        print(f"visited_dots: {visited_dots})")
        neighbours = get_neighbours(dot, field, field_size)
        for neighbour in neighbours:
            if neighbour not in main_neighbours and neighbour not in visited_dots:
                main_neighbours.insert(counter, neighbour)
                counter += 1
        print(f"main_neighbours: {main_neighbours}")
        if field[dot[0]][dot[1]] == states_dict['TARGET']:
            target_remained -= 1
            print(f"target_remained: {target_remained}")
        elif field[dot[0]][dot[1]] == states_dict['FINISH']:
            print(f"finish found")
            finish_found = True
        if len(main_neighbours) + len(visited_dots) > max_queue:
            max_queue = len(main_neighbours) + len(visited_dots)
        for neighbour in neighbours:
            for neighbour in main_neighbours:
                if target_remained == 0 and finish_found:
                    return dot_counter, max_queue
                main_neighbours.pop(0)
                DFS(field, neighbour, field_size)
    return dot_counter, max_queue


def get_neighbours(dot, field, field_size):
    dot_ins = [[dot[0], dot[1] - 1], [dot[0] - 1, dot[1]], [dot[0], dot[1] + 1], [dot[0] + 1, dot[1]]]
    neighbours = []
    for dot in dot_ins:
        if is_valid_dot(dot, field, field_size):
            neighbours.append(dot)
    return neighbours


def is_valid_dot(dot, field, field_size):
    try:
        if field[dot[0]][dot[1]] == states_dict['OBSTACLE'] or field[dot[0]][dot[1]] == states_dict['AGENT'] or (
                (dot[0] < 0 or dot[0] > field_size) or (dot[1] < 0 or dot[1] > field_size)):
            return False
        elif field[dot[0]][dot[1]] == states_dict['TARGET'] or field[dot[0]][dot[1]] == states_dict['FINISH']:
            return True
    except IndexError:
        return False
    else:
        return True


def set_globals_to_default():
    global used_dots, visited_dots, queue_dots, target_remained, target_count
    used_dots = []
    visited_dots = []
    queue_dots = []
    target_remained = target_count


def print_field(field, size):
    print("Search_Field")
    for i in range(0, size):
        for j in range(0, size):
            if field[i][j] == states_dict['OBSTACLE']:
                print('[■]', end='')
            elif field[i][j] == states_dict['TARGET']:
                print('[x]', end='')
            elif field[i][j] == states_dict['FINISH']:
                print('[V]', end='')
            elif field[i][j] == states_dict['AGENT']:
                print('[A]', end='')
            else:
                print('[ ]', end='')
        print('\r\n', end='')


# Три способа заполнения поля:
# 1).Рандомно сгенерированное поле
# search_field = generate_field(size)
# print(agent_dot)
# print(finish_dot)
# 2).Поле взятое из Методички(Рисунок 3.2)
search_field = [[0, 1, 0, 3], [0, 2, 0, 1], [2, 0, 4, 1], [0, 1, 0, 2]]
# 3).Поле с невозможностью достижения финиша
#search_field = [[0, 1, 1, 3], [0, 2, 0, 1], [2, 0, 4, 0], [0, 1, 0, 2]]
agent_dot = [2, 2]
finish_dot = [0, 3]
print_field(search_field, size)
BFS(search_field, agent_dot, size)
print("_______________\r\nDFS statistics\r\n_______________")
[dot_counter, max_queue] = DFS(search_field, agent_dot, size)
if target_remained > 0 or not finish_found:
    print(f"Can't complete the task!\r\ntarget_remained: {target_remained}\r\nfinish found: {finish_found}")
print(f"_______________\r\nDFS_Result\r\n_______________\r\nvisited_dots: {dot_counter}")
print(f"max_memory_items: {max_queue}\r\n_______________")
set_globals_to_default()
