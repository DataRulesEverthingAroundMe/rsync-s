import argparse
import subprocess
import multiprocessing
import logging
import sys
import os
import shutil
from typing import List

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=sys.stderr
)
logger = logging.getLogger("rsync-s")

class RsyncSExecutor:
    """
    Handles the parallel execution of rsync processes.
    """
    def __init__(self, workers: int):
        self.workers = workers

    def _run_single_rsync(self, cmd: List[str]) -> int:
        """Executes one rsync command."""
        try:
            # Use subprocess.run for synchronous execution within the worker
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode != 0:
                logger.error(f"Rsync error (exit {result.returncode}): {result.stderr.strip()}")
            return result.returncode
        except Exception as e:
            logger.error(f"Unexpected error in worker: {e}")
            return 1

    def execute(self, base_cmd: List[str], file_list: List[str], destination: str) -> int:
        """
        Executes rsync for each file in parallel.
        base_cmd: The rsync command + flags (e.g., ['rsync', '-avz'])
        file_list: List of source files to copy
        destination: The target directory
        """
        if not file_list:
            logger.warning("No files to sync.")
            return 0

        # Prepare the tasks: for each file, construct the full rsync command
        # We must ensure the destination is treated as a directory
        tasks = []
        for src_file in file_list:
            # Construct: rsync [flags] [src_file] [destination]
            tasks.append(base_cmd + [src_file, destination])

        logger.info(f"Syncing {len(file_list)} files using {self.workers} workers.")
        
        # Use a Process Pool to manage workers
        with multiprocessing.Pool(processes=self.workers) as pool:
            results = pool.map(self._run_single_rsync, tasks)

        # If any rsync command failed, return a non-zero exit code
        if any(r != 0 for r in results):
            return 1
        return 0

def main():
    # 1. Parse custom --workers flag
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--workers", type=int, default=8)
    
    # We use parse_known_args to separate our flag from the rsync flags
    args, unknown = parser.parse_known_args()

    if not unknown:
        print("Usage: rsync-s [--workers N] [rsync flags] <source_dir> <destination>")
        sys.exit(1)

    # 2. Validate rsync arguments
    # Expected: [rsync_flags] <source_dir> <destination>
    # Note: This implementation assumes <source_dir> is a directory 
    # and we are parallelizing its top-level contents.
    
    if len(unknown) < 2:
        print("Error: rsync requires at least a source and a destination.")
        sys.exit(1)

    # The last two arguments are source and destination
    destination = unknown[-1]
    source_dir = unknown[-2]
    rsync_flags = unknown[:-2]

    # 3. Verify source exists
    if not os.path.isdir(source_dir):
        print(f"Error: Source '{source_dir}' is not a directory.")
        sys.exit(1)

    # 4. Gather files to sync
    # We'll sync the immediate children of the source directory to maintain 
    # compatibility with how rsync handles directory contents.
    try:
        # Get all files and directories in the source
        items = os.listdir(source_dir)
        # To be safe and simple, we build absolute paths
        file_paths = [os.path.join(source_dir, item) for item in items]
    except Exception as e:
        print(f"Error accessing source directory: {e}")
        sys.exit(1)

    # 5. Execute
    base_rsync_cmd = ["rsync"] + rsync_flags
    executor = RsyncSExecutor(workers=args.workers)
    
    exit_code = executor.execute(base_rsync_cmd, file_paths, destination)
    sys.exit(exit_code)

if __name__ == "__main__":
    main()
