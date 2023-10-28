# Smart Parking API

Make sure you have all the required packages:
```
pip install -r requirements.txt
```
this will install:
- fastapi
- uvicorn

Run server locally with:
```python
uvicorn main:app --host 127.0.0.1 --port 8080
```

You can make a POST request to the endpoint : "/distribution/"
```
curl -X POST http://127.0.0.1:8080/distribution/ \
    -H Accept:application/json \
    -H Content-Type:application/json \
    -d '{"Matrix" :[
                [-2, -2, -2, -2, -2, -2, -2],
                [-2, -1, -1, -1, -1,  1, -2, -2],
                [-2,  2,  0, 0,  0,  0, -1, -2],
                [-2, -1, -1,  1, -1,  0, -1, -2],
                [-2, -2, -2, -2, -1,  2, -1, -2],
                [-2, -2, -2, -2, -2, -2, -2, -2],
        ]}'
```

Codes:
- "-2" means that the area is blocked
- "-1" means that the parking spot is occupied
- "0" means that the this is a road
- "1" means that the area is a parking spot
- "2" means that the this is a car

