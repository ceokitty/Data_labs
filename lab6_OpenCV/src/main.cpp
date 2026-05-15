#include <iostream>

#include "CameraProvider.hpp"
#include "Display.hpp"
#include "FrameProcessor.hpp"
#include "KeyProcessor.hpp"

int main() {

    CameraProvider camera;

    if (!camera.isOpened()) {
        std::cerr << "Camera not opened!" << std::endl;
        return -1;
    }

    FrameProcessor processor;
    KeyProcessor keyProcessor;

    while (keyProcessor.isRunning()) {

        cv::Mat frame = camera.getFrame();

        if (frame.empty()) {
            std::cerr << "Empty frame!" << std::endl;
            break;
        }

        cv::Mat processedFrame =
                processor.process(frame, keyProcessor.getMode());

        Display::show("OpenCV Lab", processedFrame);

        int key = cv::waitKey(30);

        keyProcessor.processKey(key);
    }

    cv::destroyAllWindows();

    return 0;
}