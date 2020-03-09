#include<sl/Camera.hpp>
using namespace std;
using namespace sl;





vector<float> getDistance(sl::Mat point_cloud, int i, int j){
	point_cloud.getValue(i,j,&point3D);
	float x = point3D.x;
	float y = point3D.y;
	float z = point3D.z;
	float color = point3D.w;
	vector<int> answer;
	answer.push_back(x);
	answer.push_back(y);
	answer.push_back(z);
	return answer;
}






int main(int argc, char **argv){
	Camera zed;
	InitParameters initParameters;
    initParameters.depth_mode = DEPTH_MODE_ULTRA;
    initParameters.coordinate_system = COORDINATE_SYSTEM_RIGHT_HANDED_Y_UP;
    if(argc > 1 && string(argv[1]).find(".svo"))
        initParameters.svo_input_filename = argv[1];

    // Open the camera
    ERROR_CODE zed_error = zed.open(initParameters);

    if(zed_error != SUCCESS) {// Quit if an error occurred
        cout << zed_error << endl;
        zed.close();
        return 1;
    }

    Resolution resolution = zed.getResolution();
    CameraParameters camera_parameters = zed.getCameraInformation().calibration_parameters.left_cam;

    // Allocation of 4 channels of float on GPU
    Mat point_cloud(resolution, MAT_TYPE_32F_C4, MEM_GPU);

    // Main Loop
    while(viewer.isAvailable()) {
        if(zed.grab() == SUCCESS){
            zed.retrieveMeasure(point_cloud, MEASURE_XYZRGBA, MEM_GPU);
            getDistance(point_cloud, 1, 2);
        } 
        else sleep_ms(1);
    }
    // free allocated memory before closing the ZED
    point_cloud.free();

    // close the ZED
    zed.close();

    return 0;
}