# rsync-s Documentation

Welcome to the official documentation for `rsync-s`.

## Table of Contents
- [Architecture](#architecture)
- [Implementation Details](#implementation-details)
- [Concurrency Model](#concurrency-model)
- [Command Line Interface](#command-line-interface)
- [Development](#development)
- [Troubleshooting](#troubleshooting)

---

## Architecture

`rsync-s` is designed as a lightweight, high-performance wrapper around the standard `rsync` utility. Rather than re-implementing the complex logic of file delta-transfer, it orchestrates multiple independent `rsync` processes to handle large-scale file transfers in parallel.

### High-Level Flow
1. **Input Parsing**: The CLI parses custom flags (like `--workers`) and separates them from standard `rsync` arguments.
2. **Task Generation**: The source directory is scanned to identify immediate children. Each child is prepared as a single unit of work.
3. **Orchestration**: A process pool manages a set number of worker processes.
4. **Execution**: Each worker executes a standalone `rsync` command for its assigned file/directory.
5. **Aggregation**: The main process monitors worker exit codes and reports success or failure.

---

## Implementation Details

### Language & Tools
- **Language**: Python 3.12+
- **Concurrency**: `multiprocessing` module
- **Testing**: `pytest`
- **Packaging**: `setuptools`

### Core Components
- `rsync_s.main.RsyncSExecutor`: The engine that manages the `multiprocessing.Pool`. It handles the submission of tasks and the collection of exit codes.
- `rsync_s.main.main`: The entry point that handles `argparse` logic and environment validation.

---

## Concurrency Model

`rsync-s` utilizes a **Process-based Concurrency Model**. 

We chose `multiprocessing` over `threading` because:
- **GIL Bypass**: Python's Global Interpreter Lock (GIL) can limit the effectiveness of threads for CPU-bound tasks. While `rsync` itself is an external process, managing hundreds of subprocesses via threads can still encounter overhead in the Python interpreter.
- **Isolation**: Each `rsync` process runs in its own memory space, ensuring that a crash or failure in one worker does not directly affect the main orchestration process.

### Worker Scaling
The number of workers determines how many `rsync` instances can run simultaneously. 
- **Default**: 8 workers.
- **Optimal Setting**: Typically, this should be tuned based on the available network bandwidth and disk I/O capabilities of the source and destination systems.

---

## Command Line Interface

### Basic Usage
```bash
rsync-s [rsync-flags] <source_dir> <destination_dir>
```

### Customizing Workers
```bash
rsync-s --workers 16 -avz /path/to/source /path/to/destination
```

### Flag Compatibility
`rsync-s` is designed to be a transparent pass-through. Any flag not recognized as `--workers` is passed directly to the underlying `rsync` command.

---

## Development

### Setting up the environment
1. Clone the repository.
2. Create a virtual environment: `python3 -m venv venv`
3. Activate the environment: `source venv/bin/activate`
4. Install the package: `pip install .`

### Running Tests
Use `pytest` to run the test suite:
```bash
export PYTHONPATH=$PYTHONPATH:$(pwd)/src
pytest
```

---

## Troubleshooting

### Common Issues
- **Source is not a directory**: `rsync-s` currently expects a directory as the source to allow for granular file-level parallelization.
- **Permission Denied**: Ensure the user running `rsync-s` has read access to the source and write access to the destination.
- **Worker Exhaustion**: If you set `--workers` too high, you may encounter system resource limits (max processes or file descriptors).
