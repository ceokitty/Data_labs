#include "FaceDetector.h"
#include <chrono>

FaceDetector::FaceDetector(const std::string &prototxtPath, const std::string &modelPath)
{
    net = cv::dnn::readNetFromCaffe(prototxtPath, modelPath);
    running = false;
}

FaceDetector::~FaceDetector()
{
    stop();
}

void FaceDetector::start()
{
    running = true;
    worker = std::thread(&FaceDetector::processLoop, this);
}

void FaceDetector::stop()
{
    running = false;
    if (worker.joinable())
    {
        worker.join();
    }
}

void FaceDetector::submitFrame(const cv::Mat &frame)
{
    std::lock_guard<std::mutex> lock(frameMutex);
    latestFrame = frame.clone();
    hasNewFrame = true;
}

std::vector<cv::Rect> FaceDetector::getFaces()
{
    std::lock_guard<std::mutex> lock(facesMutex);
    return faces;
}

void FaceDetector::processLoop()
{
    while (running)
    {
        cv::Mat frameToProcess;
        {
            std::lock_guard<std::mutex> lock(frameMutex);
            if (!hasNewFrame || latestFrame.empty())
            {
                continue;
            }
            frameToProcess = latestFrame.clone();
            hasNewFrame = false;
        }

        int frameWidth = frameToProcess.cols;
        int frameHeight = frameToProcess.rows;

        cv::Mat blob = cv::dnn::blobFromImage(
            frameToProcess,
            1.0,
            cv::Size(300, 300),
            cv::Scalar(104.0, 177.0, 123.0));

        net.setInput(blob);
        std::this_thread::sleep_for(std::chrono::milliseconds(500));
        cv::Mat detections = net.forward();

        cv::Mat detectionMat(
            detections.size[2],
            detections.size[3],
            CV_32F,
            detections.ptr<float>());

        std::vector<cv::Rect> detectedFaces;

        for (int i = 0; i < detectionMat.rows; i++)
        {
            float confidence = detectionMat.at<float>(i, 2);
            if (confidence > 0.5)
            {
                int x1 = static_cast<int>(detectionMat.at<float>(i, 3) * frameWidth);
                int y1 = static_cast<int>(detectionMat.at<float>(i, 4) * frameHeight);
                int x2 = static_cast<int>(detectionMat.at<float>(i, 5) * frameWidth);
                int y2 = static_cast<int>(detectionMat.at<float>(i, 6) * frameHeight);
                detectedFaces.emplace_back(cv::Point(x1, y1), cv::Point(x2, y2));
            }
        }

        {
            std::lock_guard<std::mutex> lock(facesMutex);
            faces = detectedFaces;
        }
    }
}