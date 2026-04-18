# 🔧 Real-Time Hardware Validator for Linux (Python)

A real-time hardware validation and diagnostic tool developed in Python, designed to monitor system performance and simulate industrial testing processes.

---

## 🚀 Overview

This project is a modular hardware validation system that performs real-time diagnostics on key system components such as CPU, RAM, storage, and temperature.

It also includes a stress testing mechanism to evaluate system thermal performance and reliability under load.

The tool generates structured reports in both console and JSON formats, making it suitable for system monitoring, validation, and testing environments.

---

## ⚙️ Features

- CPU identification and validation  
- RAM capacity verification  
- Disk usage monitoring  
- Real-time temperature analysis  
- CPU stress testing  
- Structured report generation (table + JSON)  
- Modular and scalable architecture  

---

## 🧠 How It Works

The system runs a series of automated tests:

1. Detects CPU model and validates configuration  
2. Measures total RAM and compares with expected values  
3. Monitors disk usage and flags critical levels  
4. Reads system temperature using available sensors  
5. Executes a CPU stress test and evaluates thermal behavior  
6. Logs all results into a structured report  

---

## 🖥️ Technologies Used

- Python 3  
- psutil (system monitoring)  
- subprocess (system command execution)  
- tabulate (report visualization)  
- JSON (data export)  

---

## ▶️ Usage

Run the script:

```bash
python hardware_validator.py
