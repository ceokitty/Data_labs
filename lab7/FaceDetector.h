#ifndef FACE_DETECTOR_H
#define FACE_DETECTOR_H

#include <opencv2/opencv.hpp>
#include <opencv2/dnn.hpp>
#include <thread>
#include <mutex>
#include <atomic>
#include <vector>

class FaceDetector
{
private:
    cv::dnn::Net net;
    std::thread worker;
    std::mutex frameMutex;
    std::mutex facesMutex;
    std::atomic<bool> running;
    cv::Mat latestFrame;
    bool hasNewFrame = false;
    std::vector<cv::Rect> faces;
    void processLoop();

public:
    FaceDetector(const std::string &prototxtPath, const std::string &modelPath);
    ~FaceDetector();
    void start();
    void stop();
    void submitFrame(const cv::Mat &frame);
    std::vector<cv::Rect> getFaces();
};

#endif