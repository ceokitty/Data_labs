#include "FrameProcessor.hpp"

cv::Mat FrameProcessor::process(const cv::Mat& frame, KeyProcessor::Mode mode) {

    cv::Mat result = frame.clone();

    switch (mode) {

        case KeyProcessor::Mode::NORMAL:
            break;

        case KeyProcessor::Mode::INVERT:
            cv::bitwise_not(frame, result);
            break;

        case KeyProcessor::Mode::GRAY:
            cv::cvtColor(frame, result, cv::COLOR_BGR2GRAY);
            break;

        case KeyProcessor::Mode::BLUR:
            cv::GaussianBlur(frame, result, cv::Size(15, 15), 0);
            break;

        case KeyProcessor::Mode::CANNY: {
            cv::Mat gray;
            cv::cvtColor(frame, gray, cv::COLOR_BGR2GRAY);
            cv::Canny(gray, result, 100, 200);
            break;
        }

        case KeyProcessor::Mode::SOBEL: {
            cv::Mat gray;
            cv::Mat sobel;

            cv::cvtColor(frame, gray, cv::COLOR_BGR2GRAY);

            cv::Sobel(gray, sobel, CV_8U, 1, 1);

            result = sobel;
            break;
        }

        case KeyProcessor::Mode::BINARY: {
            cv::Mat gray;

            cv::cvtColor(frame, gray, cv::COLOR_BGR2GRAY);

            cv::threshold(gray, result, 128, 255, cv::THRESH_BINARY);
            break;
        }
    }

    return result;
}