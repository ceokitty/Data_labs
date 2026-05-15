#include "CameraProvider.hpp"

CameraProvider::CameraProvider(int cameraIndex) {
    camera.open(cameraIndex);
}

bool CameraProvider::isOpened() const {
    return camera.isOpened();
}

cv::Mat CameraProvider::getFrame() {
    cv::Mat frame;
    camera >> frame;
    return frame;
}