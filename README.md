# Smart Parking API

Run server locally with:
```python
uvicorn main:app --host 127.0.0.1 --port 8080
```

You can run to check:
```
curl -X POST http://127.0.0.1:8080/distribution/ \
    -H Accept:application/json \
    -H Content-Type:application/json \
    -d '{"matrix": [
                [-2, -2, -2, -2, -2, -2, -2],
                [-2, -1, -1, -1, -1,  1, -2, -2],
                [-2,  2,  0, 0,  0,  0, -1, -2]
                [-2, -1, -1,  1, -1,  0, -1, -2]
                [-2, -2, -2, -2, -1,  2, -1, -2]
                [-2, -2, -2, -2, -2, -2, -2, -2]
            ]
        }' \
```
