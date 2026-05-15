#include <opencv2/opencv.hpp>
#include "FaceDetector.h"
#include <iostream>

int main()
{
    cv::VideoCapture cap(0);

    if (!cap.isOpened())
    {
        std::cout << "Camera not opened!" << std::endl;
        return -1;
    }

    FaceDetector detector(
        "./deploy.prototxt",
        "./res10_300x300_ssd_iter_140000.caffemodel");

    detector.start();

    cv::Mat frame;

    while (true)
    {
        cap >> frame;

        if (frame.empty())
        {
            break;
        }

        cv::flip(frame, frame, 1);

        detector.submitFrame(frame);

        std::vector<cv::Rect> faces = detector.getFaces();

        for (const auto &face : faces)
        {
            cv::rectangle(frame, face, cv::Scalar(0, 255, 0), 2);
        }

        cv::imshow("Face Detection Threaded Mode", frame);

        char key = static_cast<char>(cv::waitKey(1));

        if (key == 27 || key == 'q')
        {
            break;
        }
    }

    detector.stop();

    cap.release();
    cv::destroyAllWindows();

    return 0;
}