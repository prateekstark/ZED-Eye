# Landmark Recognition

This is a C++ library for helping the robot locate its position in case it is lost.

## Installation

```bash
make #compiling the project
```

```bash
make clean #removes the output file (compiled project)
```
## Usage

```python
./landmark-recognition find_camera #for finding the position of the camera in case it is lost.
./landmark-recognition save_landmark #for saving a landmark position.
```
## Landmark Positions
The positions of all the landmarks will be saved in the file landmarks.txt. Edit the file for adding custom landmarks.


## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.
