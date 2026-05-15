#include "Display.hpp"

void Display::show(const std::string& windowName, const cv::Mat& frame) {
    cv::imshow(windowName, frame);
}