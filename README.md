# Space Know pyClient

This is a tool to fetch imagery and perform analysis using SpaceKnow platform.

## Requirements
- Python 3.7
- Libraries in requirements.txt

```
pip install -r /path/to/requirements.txt
```

## Running
Modify files in input folder to suit your neeeds. Then simply run the main.py script with your SpaceKnow account login

```
python3 main.py -u [your-username] -p [your-password]
```

## Notes
- Imagery tiles are downloaded but not stitched together
- No support for paginated responses
- Output the actual number of cars from the Analysis task
- JWT Token is now regenerated with each login. Instead, the session should be reused.