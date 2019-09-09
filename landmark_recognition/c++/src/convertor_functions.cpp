#include<iostream>
#include<stdlib.h>
#include<cmath>
#include<fstream>
#include<string>
#include<cstring>
#include<sstream>
#include "../include/stdc++.h"

using namespace std;

class coordinate{
    public:
        float x,y,z;
        int frameID = 0;
};

coordinate globalCameraCoordinate(coordinate pointGlobalCoordinate, coordinate pointLocalCoordinate, float theta){
  coordinate mapGlobalCoordinate;
  mapGlobalCoordinate.x = pointGlobalCoordinate.x - pointLocalCoordinate.x*(cos(theta)) + pointLocalCoordinate.y*(sin(theta));
  mapGlobalCoordinate.y = pointGlobalCoordinate.y - pointLocalCoordinate.x*(sin(theta)) - pointLocalCoordinate.y*(cos(theta));
  mapGlobalCoordinate.z = pointGlobalCoordinate.z - pointLocalCoordinate.z;
  return mapGlobalCoordinate;
  // We notice that:
    //  let a point be (x,y,z) for a particular origin, now if the point is made the origin then the coordinate of origin becomes (-x,-y,-z)
}

float getTheta(coordinate pointGlobalCoordinate1, coordinate pointGlobalCoordinate2, coordinate pointLocalCoordinate1, coordinate pointLocalCoordinate2){
  float sin_theta_num = (((pointLocalCoordinate1.x - pointLocalCoordinate2.x)*(pointGlobalCoordinate1.y - pointGlobalCoordinate2.y)) - ((pointGlobalCoordinate1.x - pointGlobalCoordinate2.x)*(pointLocalCoordinate1.y - pointLocalCoordinate2.y)));
  float sin_theta_den = ((pointLocalCoordinate1.x - pointLocalCoordinate2.x)*(pointLocalCoordinate1.x - pointLocalCoordinate2.x)) + ((pointLocalCoordinate1.y - pointGlobalCoordinate2.y)*(pointLocalCoordinate1.y - pointGlobalCoordinate2.y));
  float sin_theta = sin_theta_num/sin_theta_den;
  return asin(sin_theta);
}


vector<float> extractCoordinate(string line){
  char tempLine[line.size()+1];
  strcpy(tempLine, line.c_str());
  string tempNum = "";
  int tempCount = 0;
  int i = 0;
  vector<float> returnCoordinate;
  while(tempCount < 3){
    tempNum = tempNum + tempLine[i];
    if(tempLine[i] == ' '){
      returnCoordinate.push_back(atof(tempNum.c_str()));
      tempNum = "";
      tempCount++;
    }
    i++;
  }
  return returnCoordinate;
}


coordinate getLandmarkCoordinate(string landmarkName){
  ifstream inFile;
  coordinate returnCoordinate;
  returnCoordinate.x = 0;
  size_t found;
  returnCoordinate.y = 0;
  returnCoordinate.z = 0;
  inFile.open("landmarks.txt");
  if(inFile.is_open()){
    string line;
    while(getline(inFile, line)){
      found = line.find(landmarkName);
      // char *token = strtok(str, " ");
      if(found != string::npos){
        istringstream iss(line);
        int count = 0;
        vector<float> tempCoordinate = extractCoordinate(line);
        returnCoordinate.x = tempCoordinate.at(0);
        returnCoordinate.y = tempCoordinate.at(1);
        returnCoordinate.z = tempCoordinate.at(2);

      }
    }
    inFile.close();
  }
  return returnCoordinate;
}


bool isLandmarkPresent(string landmarkName){
  ifstream inFile;
  inFile.open("landmarks.txt");
  size_t found;
  if(inFile.is_open()){
    string line;
    while(getline(inFile, line)){
      found = line.find(landmarkName);
      if(found != string::npos){
        return true;
      }
    }
    return false;
  }
}

coordinate CameraToMap(coordinate globalCameraCoordinate, coordinate pointLocalCoordinate, float theta){

    coordinate pointGlobalCoordinate;
    pointGlobalCoordinate.x = globalCameraCoordinate.x + ((pointLocalCoordinate.x*cos(theta)) - (pointLocalCoordinate.y*sin(theta)));
    pointGlobalCoordinate.y = globalCameraCoordinate.y + ((pointLocalCoordinate.x*sin(theta)) + (pointLocalCoordinate.y*cos(theta)));
    pointGlobalCoordinate.z = globalCameraCoordinate.z + pointLocalCoordinate.z;
    return pointGlobalCoordinate;

}
