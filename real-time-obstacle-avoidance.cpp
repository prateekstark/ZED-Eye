#include<sl/Camera.hpp>
using namespace std;
using namespace sl;

bool isPointInRegionOfInterest(int x, int y){

}

int main(int argc, char **argv) {

    Camera zed;
    InitParameters init_params;
    init_params.depth_mode = DEPTH_MODE_PERFORMANCE; // Use PERFORMANCE depth mode
    init_params.coordinate_units = UNIT_MILLIMETER; // Use millimeter units (for depth measurements)
    ERROR_CODE err = zed.open(init_params);
    if (err != SUCCESS){
        exit(-1);
    }
    RuntimeParameters runtime_parameters;
    runtime_parameters.sensing_mode = SENSING_MODE_STANDARD; // Use STANDARD sensing mode
    int i = 0;
    sl::Mat image, depth, point_cloud;
    sl::float4 point_cloud_value;
    while(true){
        if (zed.grab(runtime_parameters) == SUCCESS) {
            zed.retrieveImage(image, VIEW_LEFT);
            zed.retrieveMeasure(depth, MEASURE_DEPTH);
            zed.retrieveMeasure(point_cloud, MEASURE_XYZRGBA);

            for (int x=0;x<image.getWidth();x++){
                for(int y=0;y<image.getHeight();y++){
                    if(isPointInRegionOfInterest(x, y)){
                        point_cloud.getValue(x, y, &point_cloud_value);
                        float distance = sqrt(point_cloud_value.x * point_cloud_value.x + point_cloud_value.y * point_cloud_value.y + point_cloud_value.z * point_cloud_value.z);
                        printf("Distance to Camera at (%d, %d): %f mm\n", x, y, distance);
                        cout << "Do something!" << endl;
                    }
                }
            }
        }
    }

    zed.close();
    return 0;
}