# Changelog

All notable changes to the Spider Robot Tutorials are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and entries are grouped by date (the repository does not use version tags).

## 2026-09-12

### Added

- `CHANGELOG.md` (this file) and `AGENTS.md` instructions for AI coding agents, requiring every change to include a changelog entry.
- `requirements.txt` listing the notebook and script dependencies (jupyter, ipympl, numpy, matplotlib, opencv-python, hidapi, pyserial).
- Missing `tutorial_controll_one_leg/README.md` with the series boilerplate and an overview of the folder's files.

### Changed

- Inverse kinematics (`spider_leg.py`, the IK notebook, and the IK tutorial) now use `atan2(y, x)` and compute the horizontal projection `P` with the Pythagorean theorem, so IK works for targets with x ≤ 0 and for legs pointing straight along the Y axis. Verified with forward/inverse round-trip tests; previously such targets returned mirrored angles or crashed.
- Forward kinematics README refers to the actual method name `forward_kinematics_naive` and marks its code block as Python.
- Servo calibration README: corrected the pulse-width-to-angle relationship to 90° per 500 µs to match the notebook, and reworded the `calibration_data` description to match the `Servo.angle()` implementation.
- HID tutorial pseudocode now guards against `read_controller()` returning `None`.
- Root README table of contents: linked the HID tutorial and the one-leg tutorial (previously "TBD").
- `spider_leg.py` and the IK notebook dropped an unused `numpy` import, making the module pure standard library.
- Tools & hardware README copy edits: "XT16S" corrected to "TX16S" and minor grammar.

### Fixed

- Empty TOC link for "Controlling Your Robot Using USB or Bluetooth HID Devices" in the root README.
- Empty Aliexpress link for the soldering iron, odd `image/../media/...` image paths, and a lazy `![Alt text]` in the tools & hardware README.
- Typos: "Artificial Inteligence", "projectiona", "Calculation Proces", "tar4get", "Aliepxress", "touch_treshold", a stray quote, and copy-pasted "Top view" alt texts on side-view images.
- `hardware_controller.py`: copy-pasted `NotImplementedError` messages named the wrong methods, and `receivedValues` was initialized after the reader thread started (race condition).
- `controller.py`: removed unused `vendor_id`/`product_id` parameters from `print_raw_data`.
- `one_leg_controll.ipynb`: removed the broken `project_path_on_rectangle` stub, which returned an undefined variable and was superseded by `project_path_on_plane`.

### Removed

- Obsolete draft `tutorial_tools_hardware_3d_parts_spider_robot/_README.md`, superseded by that folder's README.

## 2026-09-07

### Added

- Catch IT companion-article links to the root README and to each tutorial README.

## 2025-11-24

### Added

- Critical power backfeed safety warning to the tools & hardware tutorial (battery + USB simultaneously), reviewed for technical accuracy in PR #2.
