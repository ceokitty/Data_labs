#pragma once

#include <opencv2/opencv.hpp>
#include <string>

class Display {
public:
    static void show(const std::string& windowName, const cv::Mat& frame);
};