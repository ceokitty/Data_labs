#pragma once

class KeyProcessor {
public:
    enum class Mode {
        NORMAL,
        INVERT,
        GRAY,
        BLUR,
        CANNY,
        SOBEL,
        BINARY
    };

private:
    Mode currentMode = Mode::NORMAL;
    bool running = true;

public:
    void processKey(int key);

    Mode getMode() const;
    bool isRunning() const;
};