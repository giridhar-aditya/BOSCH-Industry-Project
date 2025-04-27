
# C++ to Rust Code Converter (BOSCH MOU Project)

## Overview
This project, developed under an MOU with **BOSCH**, aims to build a **C++ to Rust code converter** using two approaches:
- **Custom Transformer-Based Deep Learning Model**
- **Hybrid Rule-Based System (Regex + Pattern Matching)**

The solution targets automated, reliable, and scalable migration of industrial C++ codebases to safe, modern Rust code.

## Approaches

### 1. AI-Based Model (Custom Transformer)
- Implements a **custom Transformer architecture**, built from scratch (no external pre-trained models).
- Specialized **tokenizers for C++ and Rust** handle keywords, operators, punctuation, and unknowns (`<var>`, `<num>`, `<str>`).
- Trained on curated parallel C++-Rust code pairs.
- Handles complex language translation tasks including variable mappings, structure reordering, and idiomatic Rust generation.

### 2. Rule-Based Converter (Regex + Pattern Matching)
- Uses a **combination of regular expressions and `for`-loop-based pattern scanning**.
- Accurately converts:
  - Loops (`for`, `while`)
  - Conditional statements (`if-else`)
  - I/O operations (`cin`, `cout`)
  - Classes, structs, enums, switch-cases
  - Memory management constructs (`new`, `delete`)
- Focuses on fast, deterministic conversion for well-understood patterns.

## Project Structure
```
cpp-to-rust-converter/
├── ai_model/
│   ├── SASTRA_Code_Converter_DL.py  # Custom Transformer model code
├── rule_based/
│   ├── sastra.py                    # Regex and pattern-matching converter
├── dataset/                         # Parallel C++ and Rust datasets
├── examples/                        # Example input and output files
├── README.md                        # Project description (this file)
└── requirements.txt                 # Python libraries needed
```

## How to Run

### Rule-Based Conversion
```bash
cd rule_based
python sastra.py input.cpp output.rs
```

### AI-Based Conversion
Train the model:
```bash
cd ai_model
python SASTRA_Code_Converter_DL.py
```
Use the trained model for translation (custom inference script required).

*Detailed steps for training, validation, and inference are documented inside the `ai_model/` folder.*

## Technologies Used
- **Python**
- **PyTorch** (Custom Transformer Model)
- **Regex + Procedural Parsing** (Rule-Based Converter)
- **C++ and Rust** programming languages (source and target)
- **TQDM, NumPy, Torch Datasets**

## Contributions
This project is part of an academic-industry collaboration with **BOSCH Global Software Technologies**, addressing the growing need for **automated legacy code migration** from C++ to Rust in critical software systems.

## License
Proprietary — © 2025 BOSCH and **SASTRA University**.
