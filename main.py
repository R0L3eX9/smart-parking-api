from fastapi import FastAPI
from pydantic import BaseModel

class Node:
    def __init__(self, car_id, x, y):
        self.id = car_id
        self.x = x
        self.y = y

# It creates a 3D array
# D1 represents the car
# D2 represents the height
# D3 represents the width
def create_dist_array(height, width, cars):
    data = []
    for x in range(cars):
        data.append([])
        for i in range(height):
            data[x].append([])
            for _ in range(width):
                data[x][i].append(0)
    return data

def get_direction(direction):
    OX = [-1, 1, 0, 0]
    OY = [0, 0, -1, 1]
    return [OX[direction], OY[direction]]

# Finds the only path between the parking spot located at (x, y) and its according car
def find_path(dist, x, y):
    path = [[x, y]]

    while dist[x][y] != 1:
        for direction in range(0, 4):
            directions = get_direction(direction)
            new_x = x + directions[0]
            new_y = y + directions[1]
            if dist[new_x][new_y] == dist[x][y] - 1:
                x = new_x
                y = new_y
                path.append([x, y])
                break
    return path

def find_distribution(encoded_matrix):
    height = len(encoded_matrix)
    width = len(encoded_matrix[0])

    car_origin = []
    for i in range(0, height):
        for j in range(0, width):
            if encoded_matrix[i][j] == 2:
                car_origin.append([i, j])

    dist = create_dist_array(height, width, len(car_origin))

    queue = []
    cars = 0
    for i in range(0, height):
        for j in range(0, width):
            if encoded_matrix[i][j] == 2:
                dist[cars][i][j] = 1
                node = Node(cars, i, j)
                cars += 1
                queue.append(node)

    paths = []
    while len(queue):
        top = queue[0]
        queue = queue[1:]
        for direction in range(0, 4):
            directions = get_direction(direction)
            new_top = Node(top.id, top.x + directions[0], top.y + directions[1])

            # road
            if encoded_matrix[new_top.x][new_top.y] == 0 and dist[top.id][new_top.x][new_top.y] == 0:
                dist[top.id][new_top.x][new_top.y] = dist[top.id][top.x][top.y] + 1
                queue.append(Node(top.id, new_top.x, new_top.y))

            # parking space found
            if (encoded_matrix[new_top.x][new_top.y] == 1):
                dist[top.id][new_top.x][new_top.y] = dist[top.id][top.x][top.y] + 1
                encoded_matrix[new_top.x][new_top.y] = -1
                paths.append([top.id, find_path(dist[top.id], new_top.x, new_top.y)[::-1]])
    return paths


app = FastAPI()

@app.get("/")
def read_root():
    return {
            "route help": "Make a POST request with the matrix to '/distribution/'",
            "matrix types": "(WALL, USED PARKING SPOT, ROAD, PARKING SPOT, CAR) = (-2, -1, 0, 1, 2)"
           }

class EncodedMatrix(BaseModel):
    Matrix: list[list]

class Path(BaseModel):
    CarId: int
    Order: list[list[int]]

@app.post("/distribution/")
async def create_paths(matrix: EncodedMatrix) -> list[Path]:
    paths = find_distribution(matrix.Matrix)
    result = []
    for path in paths:
        result.append(Path(CarId=path[0], Order=path[1]))
    return result
