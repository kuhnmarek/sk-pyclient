# Space Know pyClient

This is a tool to fetch imagery and perform analysis using SpaceKnow platform (https://docs.spaceknow.com/)

## Requirements
- SpaceKnow account (https://analytics.spaceknow.com/)
- Python 3.7
- Libraries in requirements.txt

```
pip install -r /path/to/requirements.txt
```

## Running
1) Navigate to the */input* folder and define your imagery, date range and area of interest (GeoJSON) in *imagery-request.json*. If you use some non-default authentication method, modify *login.json* accordingly.
2) Then simply run the main.py script with your SpaceKnow account credentials

```
python3 main.py -u [your-username] -p [your-password]
```

## Notes
- Imagery tiles are downloaded but not stitched together
- No support for paginated responses
- Output from the Analysis task is currently not presented to the user in any intuitive way.
- JWT Token is now regenerated with each login. Instead, the session should be reused.uld be reused.
- Not tested with insufficient credit (need to allocate manually at https://analytics.spaceknow.com/)

