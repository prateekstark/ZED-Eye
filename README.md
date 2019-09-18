# Landmark-Recognition

Landmark-Recognition is a C++/Python library for obtaining accurate pose of the robot in case it gets lost in the map.


## Usage
```
roscore
```

```python

python3 human_detection_ros.py # runs the human detection module and publishes the x, y, z coordinates

```
If you are not connected to the robot and just need to check the code, please run

```python
python3 pseudo_publisher.py

```

```python
python3 lanmark_recognition.py save_landmark # To save the landmark in the dictionary

```
```python
python3 lanmark_recognition.py find_camera # To get the camera position if the global coordinates of landmark are present in the dictionary

```


## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.
