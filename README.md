# ChromeDinoBot
Chrome Dino game bot using only image processing.

# Usage
Run the script with a chrome window and a `chrome://dino` tab open. 
*The current code is optimized for a 1000 x 750 px chrome window.*

To end the script, open a new tab or close the chrome window.

# Built Using
- Python
- OpenCV

# How It Works
A screenshot is captured of the game area. The screenshot is positioned such that bumps and high birds would not be detected.
<p>
  <img src="https://i.imgur.com/FlkMlEA.png">
</p>
<p>
  <em style="display: block">High Birds and Bumps</em>
</p>

<p>
  <img src="https://i.imgur.com/Q2qw4vz.jpg">
</p>
<p>
  <em style="display: block">Original Screenshot</em>
</p>

The screenshot is then converted into a complete black and white image. This is done so that it is easier to detect obstacles during the change of day cycles.
<p>
  <img src="https://i.imgur.com/OXnUHEI.jpg">
</p>
<p>
  <em style="display: block">Day Black and White Image</em>
</p>

The black and white images are then passed through a canny edge detector to grab the edges from the image.
<p>
  <img src="https://i.imgur.com/V8leUqp.jpg">
</p>
<p>
  <em style="display: block">Canny Edge</em>
</p>

From the edges, next the contours are found. The contours are found so that the bounding box and the center points can be found.
<p>
  <img src="https://i.imgur.com/kuRzhV3.jpg">
</p>
<p>
  <em style="display: block">Bounding Box</em>
</p>

After detecting the obstacle, the position of the obstacle is known. By using the distance between the obstacle and the dino, rules for jump and duck can be created.

An initial distance is set but as the game speeds up, this distance must increase. By using an equation for growth over time, the distance can be adjusted and leveled of as a function of time. If the distance between the obstacle and the dino meets the requirements, a control is selected.

The y position is also taken into consideration. If the y position is at head height, the dino needs to duck. After a control is selected, loop through again.

# Future Plans
- Add sliders to easily adjust frame size

