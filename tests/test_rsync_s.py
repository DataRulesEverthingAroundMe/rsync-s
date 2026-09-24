import sys
import os
import subprocess
import pytest
import tempfile
from rsync_s.main import RsyncSExecutor

@pytest.fixture
def sync_env():
    """Creates a source and destination directory for testing."""
    with tempfile.TemporaryDirectory() as src_dir, \
         tempfile.TemporaryDirectory() as dest_dir:
        
        # Create some dummy files in src
        for i in range(20):
            with open(os.path.join(src_dir, f"file_{i}.txt"), "w") as f:
                f.write(f"Content for file {i}")
        
        yield src_dir, dest_dir

def test_rsync_s_basic_sync(sync_env):
    """Tests if rsync-s actually copies files."""
    src_dir, dest_dir = sync_env
    executor = RsyncSExecutor(workers=4)
    
    # base_cmd: ['rsync', '-a']
    # files: [src/file_0, src/file_1, ...]
    # destination: dest
    src_files = [os.path.join(src_dir, f) for f in os.listdir(src_dir)]
    exit_code = executor.execute(["rsync", "-a"], src_files, dest_dir)
    
    assert exit_code == 0
    # Verify files exist in destination
    dest_files = os.listdir(dest_dir)
    assert len(dest_files) == 20

def test_rsync_s_with_flags(sync_env):
    """Tests if rsync-s respects rsync flags (e.g., -v)."""
    src_dir, dest_dir = sync_env
    executor = RsyncSExecutor(workers=2)
    src_files = [os.path.join(src_dir, f) for f in os.listdir(src_dir)]
    
    # Using -v (verbose)
    exit_code = executor.execute(["rsync", "-av"], src_files, dest_dir)
    assert exit_code == 0
    assert len(os.listdir(dest_dir)) == 20

def test_rsync_s_worker_config():
    """Verifies the executor accepts different worker counts."""
    # This is a unit test for the executor object
    executor = RsyncSExecutor(workers=16)
    assert executor.workers == 16

def test_rsync_s_command_line_integration(sync_env, monkeypatch):
    """Tests the CLI wrapper with subprocess."""
    src_dir, dest_dir = sync_env
    
    # We need to simulate the installed command. 
    # Since it's not installed, we'll call the script via python.
    # We'll use 'python3 -m rsync_s.main'
    
    # Test case 1: Basic usage via CLI
    # Note: rsync-s [flags] source dest
    # In our implementation: rsync-s --workers 4 /src /dest
    # The script takes 'unknown' (which would be ['--workers', '4', '/src', '/dest'])
    # and splits it.
    
    # Because we are testing the actual CLI parsing:
    # Command: python3 -m rsync_s.main --workers 2 /tmp/src /tmp/dest
    
    # Construct the command
    cmd = [
        sys.executable, "-m", "rsync_s.main", 
        "--workers", "2", 
        src_dir, 
        dest_dir
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    assert result.returncode == 0
    assert len(os.listdir(dest_dir)) == 20

def test_rsync_s_invalid_source(sync_env):
    """Tests behavior with non-existent source."""
    src_dir, dest_dir = sync_env
    cmd = [
        sys.executable, "-m", "rsync_s.main", 
        "--workers", "2", 
        "/non/existent/path", 
        dest_dir
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    assert result.returncode != 0
    assert "Error: Source" in result.stderr or "Error" in result.stdout
