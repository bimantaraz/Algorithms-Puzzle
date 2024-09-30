import pygame
import random
import time
import heapq 
import timeit  

# Warna
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
ORANGE = (255, 165, 0)
GRAY = (128, 128, 128)

# Ukuran grid dan blok
GRID_SIZE = 30
BLOCK_SIZE = 20 

# Representasi grid
WALL = '#'
PATH = ' '
START = 'S'
EXIT = 'E'

def create_grid_with_path(size, wall_percentage):
    grid = [[PATH for _ in range(size)] for _ in range(size)]

    # Buat jalur acak
    current_pos = (0, 0)
    path = [current_pos]

    while current_pos != (size-1, size-1):
        x, y = current_pos
        if x < size - 1 and random.random() > 0.5:
            current_pos = (x + 1, y)
        elif y < size - 1:
            current_pos = (x, y + 1)
        else:
            current_pos = (x + 1, y)

        path.append(current_pos)

    for i in range(size):
        for j in range(size):
            if (i, j) not in path and random.random() < wall_percentage:
                grid[i][j] = WALL

    return grid

# Algoritma DFS 
def dfs(grid, start, exit_point, screen, color):
    stack = [start]
    visited = set()  
    path = []  

    while stack:
        x, y = stack.pop()
        
        draw_block(screen, x, y, color)
        pygame.display.update()
        time.sleep(0.01)

        if (x, y) == exit_point:
            path.append((x, y))
            return path
        
        if (x, y) in visited:
            continue
        
        visited.add((x, y))
        path.append((x, y))
        
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            new_x, new_y = x + dx, y + dy
            if (0 <= new_x < len(grid) and  
                0 <= new_y < len(grid[0]) and 
                grid[new_x][new_y] != WALL and  
                (new_x, new_y) not in visited): 
                stack.append((new_x, new_y))

    return None

# Algoritma A*
def a_star(grid, start, exit_point, screen, color):
    def heuristic(a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1]) 

    open_list = []
    heapq.heappush(open_list, (0, start, [start])) 
    g_score = {start: 0}
    visited = set()

    while open_list:
        _, (x, y), path = heapq.heappop(open_list)

        draw_block(screen, x, y, BLUE)
        pygame.display.update()
        time.sleep(0.01)

        if (x, y) == exit_point:
            return path

        if (x, y) in visited:
            continue

        visited.add((x, y))

        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            new_x, new_y = x + dx, y + dy
            if 0 <= new_x < len(grid) and 0 <= new_y < len(grid[0]) and grid[new_x][new_y] != WALL:
                tentative_g_score = g_score[(x, y)] + 1
                if (new_x, new_y) not in g_score or tentative_g_score < g_score[(new_x, new_y)]:
                    g_score[(new_x, new_y)] = tentative_g_score
                    f_score = tentative_g_score + heuristic((new_x, new_y), exit_point)
                    heapq.heappush(open_list, (f_score, (new_x, new_y), path + [(new_x, new_y)]))

    return None


def draw_grid(screen, grid):
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            color = WHITE
            if grid[i][j] == WALL:
                color = BLACK
            elif grid[i][j] == START:
                color = GREEN
            elif grid[i][j] == EXIT:
                color = GREEN
            draw_block(screen, i, j, color)

def draw_block(screen, i, j, color):
    pygame.draw.rect(screen, color, (j * BLOCK_SIZE, i * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
    pygame.draw.rect(screen, BLACK, (j * BLOCK_SIZE, i * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 1)

def draw_fastest_path(screen, path):
    for (x, y) in path:
        draw_block(screen, x, y, GRAY)
        pygame.display.update()
        time.sleep(0.01)

# Main function
def main():
    pygame.init()

    screen_dfs = pygame.display.set_mode((GRID_SIZE * BLOCK_SIZE, GRID_SIZE * BLOCK_SIZE))
    screen_astar = pygame.display.set_mode((GRID_SIZE * BLOCK_SIZE, GRID_SIZE * BLOCK_SIZE))

    pygame.display.set_caption("AI Puzzle Solver - DFS vs A*")

    grid = create_grid_with_path(GRID_SIZE, 0.3)

    start = (0, 0)
    exit_point = (GRID_SIZE-1, GRID_SIZE-1)
    grid[start[0]][start[1]] = START
    grid[exit_point[0]][exit_point[1]] = EXIT

    # Gambar grid awal untuk kedua algoritma
    screen_dfs.fill(WHITE)
    draw_grid(screen_dfs, grid)
    pygame.display.update()

    screen_astar.fill(WHITE)
    draw_grid(screen_astar, grid)
    pygame.display.update()

    # Jalankan DFS
    start_time_dfs = timeit.default_timer()
    path_dfs = dfs(grid, start, exit_point, screen_dfs, ORANGE)
    time_dfs = timeit.default_timer() - start_time_dfs

    # Jalankan A*
    start_time_astar = timeit.default_timer()
    path_astar = a_star(grid, start, exit_point, screen_astar, BLUE)
    time_astar = timeit.default_timer() - start_time_astar

    if path_dfs is not None and path_astar is not None:
        fastest_path = path_dfs if len(path_dfs) < len(path_astar) else path_astar
        draw_fastest_path(screen_dfs, fastest_path)
        draw_fastest_path(screen_astar, fastest_path)

    if time_dfs < time_astar:
        print("Algorima DFS lebih cepat menemukan jalur:")
        for step in path_dfs:
            print(step)
    else:
        print("Algoritma A* lebih cepat menemukan jalur:")
        for step in path_astar:
            print(step)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

    pygame.quit()

if __name__ == "__main__":
    main()
