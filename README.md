# PrintPad 

Control your Klipper-based 3D printer with a gamepad. Move axes, manage filament, control fans and lights — all without touching your computer.

**Tested on:** Elegoo Neptune 4 (should work on any Klipper printer with Moonraker)

---

## Requirements

- Python 3
- A Klipper printer running **Moonraker** (for the HTTP API)
- A gamepad/joystick connected to your PC

Install dependencies:

```bash
pip install pygame requests
```

---

## Setup

1. Open `printpad.py` and change the IP address to your printer's IP:

```python
url = "http://192.168.0.128/printer/gcode/script"
```

2. Connect your gamepad, then run:

```bash
python printpad.py
```

---

## Controls

### Movement (Left & Right Sticks)
| Input | Action |
|---|---|
| Left stick ← / → | Move X axis |
| Left stick ↑ / ↓ | Move Y axis |
| Right stick ↑ / ↓ | Move Z axis |

### D-Pad
| Input | Action |
|---|---|
| D-pad ↑ | Fan speed up (+25) |
| D-pad ↓ | Fan speed down (-25) |

### Buttons
| Button | Action |
|---|---|
| Button 0 (A/Cross) | Toggle big light |
| Button 1 (B/Circle) | Toggle model light |
| Button 6 (LT/L2) | Unload filament |
| Button 7 (RT/R2) | Load filament |
| Button 8 (Select) | Preheat for PLA (bed 65°C, nozzle 170°C) |
| Button 9 | Disable motors (M84) |
| Button 10 | Home all axes (G28) |
| **LT + RT together** | **Emergency stop & shutdown** |

### Emergency Shutdown (LT + RT)
Turns off heaters, fan, and disables motors. Also exits the program.

---

## Configuration

At the top of the script you can tweak these values:

```python
filament_load = 50      # How many mm to load/unload
filament_speed = 150    # Filament move speed (mm/min)
AXIS_THRESHOLD = 0.5    # Stick deadzone (0.0–1.0)
MOVE_INTERVAL = 0.2     # Seconds between move commands
```

---

## Notes

- Button numbers may vary depending on your gamepad model. If controls feel wrong, run `pygame`'s joystick test to remap them.
- The printer connection uses Moonraker's `/printer/gcode/script` endpoint — make sure Moonraker is running and accessible on your network.
- If the printer is unreachable, the script prints a warning and keeps running.
