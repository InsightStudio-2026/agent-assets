#!/usr/bin/env python3
"""
Server Lifecycle Manager (Windows-optimized)

This script starts one or more servers, waits for their ports to open, 
executes a test command (e.g. Playwright scripts), and guarantees 
the clean destruction of all server process trees afterwards.

Optimized specifically for Windows 11 to solve the persistent orphan process 
issue (where 'npm run dev' leaves Node zombies locking ports like 5173/3000).

Usage:
    # Single server
    python with_server.py --server "npm run dev" --port 5173 -- python test_flow.py

    # Multiple servers (Frontend + Backend)
    python with_server.py \
      --server "cd backend && python app.py" --port 5000 \
      --server "cd frontend && npm run dev" --port 5173 \
      -- python run_tests.py
"""

import subprocess
import socket
import time
import sys
import argparse
import platform


def is_port_open(port, timeout=30):
    """Poll localhost:port to verify if the server is ready."""
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            with socket.create_connection(('127.0.0.1', port), timeout=1):
                return True
        except (socket.error, ConnectionRefusedError):
            time.sleep(0.5)
    return False


def terminate_process_tree(process):
    """
    Safely and aggressively clean up process tree.
    Uses Windows 'taskkill' to wipe the whole tree (/T) including Node.js orphans.
    """
    if process.poll() is not None:
        return  # Process already exited

    is_windows = platform.system() == "Windows"
    pid = process.pid

    if is_windows:
        try:
            # Taskkill /F /T kills the specified PID and all its child processes (the entire tree).
            # This is essential in Windows when running shell=True (kills cmd.exe + node.exe).
            subprocess.run(
                ["taskkill", "/F", "/T", "/PID", str(pid)],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                check=False,
            )
        except (OSError, subprocess.SubprocessError):
            # Fallback if taskkill fails
            try:
                process.terminate()
                process.wait(timeout=2)
            except subprocess.TimeoutExpired:
                process.kill()
    else:
        # Unix/macOS cleanup
        try:
            process.terminate()
            process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            process.kill()
            process.wait()


def main():
    """启动服务器、执行测试命令、清理服务器进程树。"""
    parser = argparse.ArgumentParser(
        description='Run custom automation commands with server lifecycle management'
    )
    parser.add_argument(
        '--server', action='append', dest='servers', required=True,
        help='Command to launch a server (can repeat)'
    )
    parser.add_argument(
        '--port', action='append', dest='ports', type=int, required=True,
        help='Port of the server (must match --server count)'
    )
    parser.add_argument(
        '--timeout', type=int, default=30,
        help='Max timeout in seconds to wait for port (default: 30)'
    )
    parser.add_argument(
        'command', nargs=argparse.REMAINDER,
        help='The test execution command to run'
    )

    args = parser.parse_args()

    # Strip '--' helper if present
    if args.command and args.command[0] == '--':
        args.command = args.command[1:]

    if not args.command:
        print("Error: No test or execution command specified.", file=sys.stderr)
        sys.exit(1)

    if len(args.servers) != len(args.ports):
        print("Error: Number of --server and --port parameters must match.", file=sys.stderr)
        sys.exit(1)

    servers = [{'cmd': cmd, 'port': port} for cmd, port in zip(args.servers, args.ports)]
    server_processes = []

    try:
        # 1. Start all servers in parallel
        for i, svr in enumerate(servers):
            print(f"[{i+1}/{len(servers)}] Starting background server: {svr['cmd']}")

            # Use shell=True to support multi-commands (like cd x && npm dev)
            proc = subprocess.Popen(
                svr['cmd'],
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            server_processes.append(proc)

            print(f"Waiting for local port {svr['port']} to open...")
            if not is_port_open(svr['port'], timeout=args.timeout):
                raise RuntimeError(
                    f"Server on port {svr['port']} did not start within "
                    f"{args.timeout}s timeout boundary."
                )
            print(f"Port {svr['port']} is open and healthy.")

        print("\nAll servers are active and ready. Running test suite...")

        # 2. Run the actual automated execution command
        print(f"Executing target command: {' '.join(args.command)}\n" + "="*50)
        run_result = subprocess.run(args.command, check=False)
        print("="*50 + "\nTarget command finished.")
        sys.exit(run_result.returncode)

    except (RuntimeError, OSError, subprocess.SubprocessError) as e:
        print(f"\nRuntime Failure: {e}", file=sys.stderr)
        sys.exit(1)

    finally:
        # 3. Clean up all servers rigorously (Process Tree Destruction)
        print(f"\n[Cleanup] Terminating {len(server_processes)} server process trees...")
        for i, proc in enumerate(server_processes):
            terminate_process_tree(proc)
            print(f"Background server {i+1} cleaned up.")
        print("Lifecycle management finalized successfully. Ready for next run.")


if __name__ == '__main__':
    main()
