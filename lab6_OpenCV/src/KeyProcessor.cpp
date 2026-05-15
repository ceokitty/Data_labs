#include "KeyProcessor.hpp"

void KeyProcessor::processKey(int key) {
    switch (key) {
        case 27: // ESC
        case 'q':
            running = false;
            break;

        case '0':
            currentMode = Mode::NORMAL;
            break;

        case '1':
            currentMode = Mode::INVERT;
            break;

        case '2':
            currentMode = Mode::GRAY;
            break;

        case '3':
            currentMode = Mode::BLUR;
            break;

        case '4':
            currentMode = Mode::CANNY;
            break;

        case '5':
            currentMode = Mode::SOBEL;
            break;

        case '6':
            currentMode = Mode::BINARY;
            break;

        default:
            break;
    }
}

KeyProcessor::Mode KeyProcessor::getMode() const {
    return currentMode;
}

bool KeyProcessor::isRunning() const {
    return running;
}