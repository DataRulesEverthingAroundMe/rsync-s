# rsync-s

A high-performance, multi-threaded wrapper for the standard `rsync` utility.

`rsync-s` enhances the traditional single-threaded `rsync` by providing parallel execution of file transfers, significantly increasing throughput for large numbers of files.

## Features

- **Multi-threading**: Uses a configurable number of worker processes to run multiple `rsync` instances in parallel.
- **Full Compatibility**: Inherits all standard `rsync` flags and arguments.
- **Easy Configuration**: Use `--workers <N>` to specify the number of concurrent workers. Defaults to 8.

## Installation

```bash
pip install .
```

## Usage

Standard `rsync` usage:
```bash
rsync-s -avz /src/ /dest/
```

With custom worker count:
```bash
rsync-s --workers 16 -avz /src/ /dest/
```

## License

MIT
