#include "./convertor_functions.cpp"
int main(int argc, char const *argv[]){
  try{
    if(argc == 2){
      string action(argv[1]);
      string action1 = "save_landmark";
      string action2 = "find_camera";
      // cout<<action<<endl;
      try{
        if(action.compare(action1) == 0){
          float x = 1;
          float y = 1;
          float z = 1;
          float self_x = 1;
          float self_y = 2;
          float self_z = 3;
          float theta = 0.5;
          string objectName = "KUKA Robot";
          coordinate pointLocalCoordinate;
          pointLocalCoordinate.frameID = 1;
          coordinate globalCameraCoordinate;
          pointLocalCoordinate.x = x;
          pointLocalCoordinate.y = y;
          pointLocalCoordinate.z = z;
          globalCameraCoordinate.x = self_x;
          globalCameraCoordinate.y = self_y;
          globalCameraCoordinate.z = self_z;
          coordinate pointGlobalCoordinate;
          pointGlobalCoordinate = CameraToMap(globalCameraCoordinate, pointLocalCoordinate, theta);
          cout<<"Do you want to save the landmark to file?"<<endl;
          string input_answer;
          cin>>input_answer;
          string answer_type1 = "yes";
          string answer_type2 = "no";
          if(input_answer.compare(answer_type1) == 0){
            string tempWrite = to_string(pointGlobalCoordinate.x) + " " + to_string(pointGlobalCoordinate.y) + " " + to_string(pointGlobalCoordinate.z) + " " + objectName +"\n";
            ofstream myfile;
            myfile.open("landmarks.txt", ios_base::app);
            myfile<<tempWrite;
            myfile.close();
          }

        }
        else if(action.compare(action2) == 0){
          float localx = 1;
          float localy = 2;
          float localz = 3;
          float theta = 0.7;
          coordinate landmarkLocalCoordinate;
          landmarkLocalCoordinate.frameID = 1;
          landmarkLocalCoordinate.x = localx;
          landmarkLocalCoordinate.z = localz;
          landmarkLocalCoordinate.y = localy;
          string landmarkName = "KUKA Robot";
          try{
            if(isLandmarkPresent(landmarkName)){
              coordinate globalLandmarkCoordinate = getLandmarkCoordinate(landmarkName);
              coordinate cameraCoordinate = globalCameraCoordinate(globalLandmarkCoordinate, landmarkLocalCoordinate, theta);
              cout<<"x:"<<cameraCoordinate.x<<" y:"<<cameraCoordinate.y<<" z:"<<cameraCoordinate.z<<endl;
            }
            else{
              throw "landmark information not present!";
            }

          }
          catch(const char* errorMessage){
            cerr<<errorMessage<<endl;
          }

        }
        else{
          throw "wrongArguments";
        }

      }
      catch(const char* wrongArguments){
        cerr<<wrongArguments<<endl;
      }
    }
    else{
      throw "Wrong Arguments";
    }

  }
  catch(const char* wrongArgument){
    cerr<<wrongArgument<<endl;
  }
  return 0;
}
