from fastapi import FastAPI
from pydantic import BaseModel

class Node:
    def __init__(self, car_id, x, y):
        self.id = car_id
        self.x = x
        self.y = y

def create_dist_array(height, width, cars):
    data = []
    for x in range(cars):
        data.append([])
        for i in range(height):
            data[x].append([])
            for _ in range(width):
                data[x][i].append(0)
    return data


def find_path(dist, x, y):
    di = [-1, 1, 0, 0]
    dj = [0, 0, -1, 1]
    path = [[x, y]]
    for d in dist:
        print(d)

    while dist[x][y] != 1:
        print(dist[x][y])
        for d in range(0, 4):
            new_x = x + di[d]
            new_y = y + dj[d]
            if dist[new_x][new_y] == dist[x][y] - 1:
                x = new_x
                y = new_y
                path.append([x, y])
                break
    return path

def find_distribution(encoded_matrix):
    height = len(encoded_matrix)
    width = len(encoded_matrix[0])

    di = [-1, 1, 0, 0]
    dj = [0, 0, -1, 1]

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
        for d in range(0, 4):
            new_top = Node(top.id, top.x + di[d], top.y + dj[d])
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
    Matrix: list[list] = [[]]

class Path(BaseModel):
    CarId: int
    Order: list[int]

@app.post("/distribution/")
async def create_paths(matrix: EncodedMatrix) -> list[Path]:
    print(matrix)
    paths = find_distribution(matrix.Matrix)
    print(paths)
    result = []
    for path in paths:
        result.append(Path(CarId=path[0], Order=path[1]))
    return result
