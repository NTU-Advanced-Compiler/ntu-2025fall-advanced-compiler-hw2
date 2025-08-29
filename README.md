# Homework 2: DCE and LVN for Bril

## Overview

In this assignment, you will implement a local Dead Code Elimination (DCE) pass for the Bril intermediate representation (IR). The objective is to remove redundant instructions within basic blocks and then integrate DCE with Local Value Numbering (LVN) to further reduce dynamic instruction count. You will assess the impact of these transformations using the brili interpreter, comparing dynamic instruction counts before and after the passes are applied.

## Prerequisites

- Python 3.7+
- Bril toolchain

## Getting Started

1. Clone the repository:
   ```bash
   git clone --recursive <url-of-your-forked-repo>
   ```

2. Navigate to the homework directory:
   ```bash
   cd <homework-directory>
   ```

## Project Structure
```
homework-directory/
├── src/
│   ├── form_blocks.py
│   ├── local_dce.py
│   ├── lvn.py
│   └── util.py.py
├── tests/
│   ├── local_dce/
│   │   ├── testcase_1.bril
│   │   └── [additional test cases]
│   └── lvn+local_dce/
│       ├── testcase_5.bril
│       └── [additional test cases]
├── bril/
├── install_bril.sh
├── run_testcase.sh
└── README.md
```


## Implementation Tasks

1. Remove instructions that are never served as arguments of other instructions (`trivial_dce_pass` in `local_dce.py`)
2. Delete instructions that is unused before next assignment  (`drop_killed_local` in `local_dce.py`)


## Running and Testing

1. To generate the form after transformations:
```bash
# DCE only
bril2json < [path_to_testcase] | python3 ./src/local_dce.py | bril2txt > output.bril

# Combine DCE with LVN
bril2json < [path_to_testcase] | python3 ./src/lvn.py | python3 ./src/local_dce.py | bril2txt > output.bril
```
2. To check the dynamic instruction count:
```bash
#  Original program
bril2json < [path_to_testcase] | brili -p

# DCE only
bril2json < [path_to_testcase] | python3 ./src/local_dce.py | brili -p

# Combine DCE with LVN
bril2json < [path_to_testcase] | python3 ./src/lvn.py | python3 ./src/local_dce.py | brili -p
```
3. To check if the dynamic instruction count pass the threshold 
```bash
# DCE only
bash run_testcase.sh [path_to_testcase] [path_to_corresponding_threshold_file] local_dce

# Combine DCE with LVN
bash run_testcase.sh [path_to_testcase] [path_to_corresponding_threshold_file] lvn+local_dce

```


## Submission Instructions

1. Implement all required functionalities in the `src/` directory.
2. Test your implementation thoroughly.
3. Commit and push your changes:
   ```bash
   git add src/ 
   git commit -m "Completed Homework 2"
   git push origin main
   ```
4. Verify that the GitHub Actions workflow passes all tests.

## Do and Don't

- You are allowed to modify any part of the starter code within the src/ directory, except for is_ssa.py, to suit your approach. While the current structure serves as a guideline, ensuring the driver script functions properly is key for grading.
- Make sure you have a solid understanding of the algorithm before starting your implementation.
- Ensure your student ID is correctly entered in the student_id.txt file before submission.
- DO NOT modify the src/is_ssa.py file or anything outside the src/ directory except student_id.txt. Any such changes will be considered cheating.

## Additional Resources

- Engineering a Compiler
- [Bril Language Reference](https://capra.cs.cornell.edu/bril/lang/index.html)
- Course lecture notes on DCE and LVN
