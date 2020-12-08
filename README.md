# Super Smash Bros Electric
Detect damage in a video feed played by OBS from the game. It detect the damage by template matching the percent score of each player.

## Install
`npm i` will install all you need for the python script and the nodeJS test server

You can install only python dependency with `pip install -r requirements.txt`

## OBS Setup
First you need to setup obs:
1. use a 1920x1080 canvas
2. right click on the preview and open a `Windowed Projector (Preview)`
3. make sur to maximise the `Windowed Projector (Preview)` to fullscreen
4. In `win_capture.py` make sur that the name in `FindWindow` setting is the same has your preview
5. optional: you can disable the obs preview for better performance

## Run Python Script
`npm start` or `python win_capture.py`

## Run test server
`npm run serve`