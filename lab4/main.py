import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button, CheckButtons
from scipy.signal import butter, filtfilt
import matplotlib
matplotlib.use('TkAgg')

# =====================================
# Початкові параметри
# =====================================
INITIAL_PARAMS = {
    "amplitude": 1.0,
    "frequency": 2.0,           # тут frequency інтерпретується як ω
    "phase": 0.0,
    "noise_mean": 0.0,
    "noise_covariance": 0.10,
    "cutoff_frequency": 3.0,
    "show_noise": True
}

# Часова вісь
t = np.linspace(0, 10, 1000)
dt = t[1] - t[0]
sampling_rate = 1 / dt

# Глобальний шум
noise = None

# Запам'ятовування останніх параметрів шуму
last_noise_mean = INITIAL_PARAMS["noise_mean"]
last_noise_covariance = INITIAL_PARAMS["noise_covariance"]


# =====================================
# Основні функції
# =====================================
def harmonic(amplitude, frequency, phase):
    """
    Побудова чистої гармоніки за формулою:
    y(t) = A * sin(ωt + φ)
    """
    return amplitude * np.sin(frequency * t + phase)


def generate_noise(noise_mean, noise_covariance):
    """
    Генерація гаусового шуму.
    noise_mean - середнє значення
    noise_covariance - дисперсія
    """
    std = np.sqrt(noise_covariance)
    return np.random.normal(noise_mean, std, size=t.shape)


def harmonic_with_noise(amplitude, frequency, phase,
                        noise_mean, noise_covariance, show_noise):
    """
    Формує чисту гармоніку та, за потреби, зашумлену.
    Якщо show_noise = False, повертається лише чиста гармоніка.
    """
    clean_signal = harmonic(amplitude, frequency, phase)

    if show_noise:
        noisy_signal = clean_signal + noise
    else:
        noisy_signal = clean_signal.copy()

    return clean_signal, noisy_signal


def lowpass_filter(signal, cutoff_frequency):
    """
    Низькочастотний Butterworth-фільтр.
    """
    nyquist = 0.5 * sampling_rate
    cutoff_frequency = max(0.01, min(cutoff_frequency, nyquist - 0.01))
    normalized_cutoff = cutoff_frequency / nyquist

    b, a = butter(N=4, Wn=normalized_cutoff, btype="low")
    return filtfilt(b, a, signal)


# =====================================
# Початковий шум
# =====================================
noise = generate_noise(
    INITIAL_PARAMS["noise_mean"],
    INITIAL_PARAMS["noise_covariance"]
)

# Початкові сигнали
clean_signal, noisy_signal = harmonic_with_noise(
    INITIAL_PARAMS["amplitude"],
    INITIAL_PARAMS["frequency"],
    INITIAL_PARAMS["phase"],
    INITIAL_PARAMS["noise_mean"],
    INITIAL_PARAMS["noise_covariance"],
    INITIAL_PARAMS["show_noise"]
)
filtered_signal = lowpass_filter(noisy_signal, INITIAL_PARAMS["cutoff_frequency"])


# =====================================
# Створення вікна та графіків
# =====================================
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))
plt.subplots_adjust(left=0.10, bottom=0.34, right=0.80, hspace=0.45)

fig.suptitle("Лабораторна робота №4: Гармоніка з шумом та фільтрацією", fontsize=14)

# Верхній графік: чиста + зашумлена
ax1.set_title("Початковий сигнал")
ax1.set_xlabel("Час")
ax1.set_ylabel("Амплітуда")
ax1.grid(True)

line_clean_1, = ax1.plot(t, clean_signal, label="Чиста гармоніка", color="blue", linewidth=2)
line_noisy_1, = ax1.plot(t, noisy_signal, label="Зашумлена гармоніка", color="orange", alpha=0.8)
ax1.legend(loc="upper right")

# Нижній графік: чиста + відфільтрована
ax2.set_title("Порівняння чистої та відфільтрованої гармоніки")
ax2.set_xlabel("Час")
ax2.set_ylabel("Амплітуда")
ax2.grid(True)

line_clean_2, = ax2.plot(t, clean_signal, label="Чиста гармоніка", color="blue", linewidth=2, linestyle="--")
line_filtered_2, = ax2.plot(t, filtered_signal, label="Відфільтрована гармоніка", color="purple", linewidth=2)
ax2.legend(loc="upper right")


# =====================================
# Інструкція для користувача
# =====================================
instruction_text = (
    "Інструкція:\n"
    "1. Змінюйте параметри гармоніки та шуму за допомогою слайдерів.\n"
    "2. Прапорець Show Noise вмикає або вимикає шум на графіку.\n"
    "3. Cutoff Frequency змінює силу фільтрації сигналу.\n"
    "4. Кнопка Reset повертає початкові параметри.\n"
    "5. Верхній графік показує чисту та зашумлену гармоніку,\n"
    "   нижній — чисту та відфільтровану."
)
fig.text(0.82, 0.72, instruction_text, fontsize=9, va="top",
         bbox=dict(facecolor="white", alpha=0.9))


# =====================================
# Області для слайдерів
# =====================================
ax_amp = plt.axes([0.15, 0.25, 0.55, 0.02])
ax_freq = plt.axes([0.15, 0.22, 0.55, 0.02])
ax_phase = plt.axes([0.15, 0.19, 0.55, 0.02])
ax_noise_mean = plt.axes([0.15, 0.16, 0.55, 0.02])
ax_noise_cov = plt.axes([0.15, 0.13, 0.55, 0.02])
ax_cutoff = plt.axes([0.15, 0.10, 0.55, 0.02])

slider_amp = Slider(ax_amp, "Amplitude", 0.1, 5.0, valinit=INITIAL_PARAMS["amplitude"])
slider_freq = Slider(ax_freq, "Frequency (ω)", 0.1, 10.0, valinit=INITIAL_PARAMS["frequency"])
slider_phase = Slider(ax_phase, "Phase", 0.0, 2 * np.pi, valinit=INITIAL_PARAMS["phase"])
slider_noise_mean = Slider(ax_noise_mean, "Noise Mean", -2.0, 2.0, valinit=INITIAL_PARAMS["noise_mean"])
slider_noise_cov = Slider(ax_noise_cov, "Noise Covariance", 0.01, 1.0, valinit=INITIAL_PARAMS["noise_covariance"])
slider_cutoff = Slider(ax_cutoff, "Cutoff Frequency", 0.1, 20.0, valinit=INITIAL_PARAMS["cutoff_frequency"])


# =====================================
# Checkbox та кнопка
# =====================================
ax_checkbox = plt.axes([0.82, 0.28, 0.14, 0.08])
checkbox = CheckButtons(ax_checkbox, ["Show Noise"], [INITIAL_PARAMS["show_noise"]])

ax_button = plt.axes([0.82, 0.20, 0.12, 0.05])
button_reset = Button(ax_button, "Reset")


# =====================================
# Функція оновлення
# =====================================
def update(_):
    global noise, last_noise_mean, last_noise_covariance

    amplitude = slider_amp.val
    frequency = slider_freq.val
    phase = slider_phase.val
    noise_mean = slider_noise_mean.val
    noise_covariance = slider_noise_cov.val
    cutoff_frequency = slider_cutoff.val
    show_noise = checkbox.get_status()[0]

    # Шум генеруємо заново тільки якщо змінилися параметри шуму
    if noise_mean != last_noise_mean or noise_covariance != last_noise_covariance:
        noise = generate_noise(noise_mean, noise_covariance)
        last_noise_mean = noise_mean
        last_noise_covariance = noise_covariance

    clean_signal, noisy_signal = harmonic_with_noise(
        amplitude, frequency, phase,
        noise_mean, noise_covariance, show_noise
    )

    filtered_signal = lowpass_filter(noisy_signal, cutoff_frequency)

    # Верхній графік
    line_clean_1.set_ydata(clean_signal)
    line_noisy_1.set_ydata(noisy_signal)

    # Нижній графік
    line_clean_2.set_ydata(clean_signal)
    line_filtered_2.set_ydata(filtered_signal)

    fig.canvas.draw_idle()


# =====================================
# Функція скидання
# =====================================
def reset(_):
    global noise, last_noise_mean, last_noise_covariance

    slider_amp.reset()
    slider_freq.reset()
    slider_phase.reset()
    slider_noise_mean.reset()
    slider_noise_cov.reset()
    slider_cutoff.reset()

    current_state = checkbox.get_status()[0]
    if current_state != INITIAL_PARAMS["show_noise"]:
        checkbox.set_active(0)

    noise = generate_noise(
        INITIAL_PARAMS["noise_mean"],
        INITIAL_PARAMS["noise_covariance"]
    )
    last_noise_mean = INITIAL_PARAMS["noise_mean"]
    last_noise_covariance = INITIAL_PARAMS["noise_covariance"]

    update(None)


# =====================================
# Прив'язка подій
# =====================================
slider_amp.on_changed(update)
slider_freq.on_changed(update)
slider_phase.on_changed(update)
slider_noise_mean.on_changed(update)
slider_noise_cov.on_changed(update)
slider_cutoff.on_changed(update)
checkbox.on_clicked(update)
button_reset.on_clicked(reset)


plt.show()