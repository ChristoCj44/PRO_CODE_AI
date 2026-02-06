import subprocess
import sys
import time

class PythonHandler:
    def execute(self, code):
        start_time = time.time()
        try:
            # -u for unbuffered output
            result = subprocess.run(
                [sys.executable, "-u", "-c", code],
                capture_output=True,
                text=True,
                timeout=2 # 2 second execution timeout
            )
            execution_time = (time.time() - start_time) * 1000 # ms
            return {
                'output': result.stdout,
                'error': result.stderr,
                'execution_time': f"{execution_time:.2f}ms"
            }
        except subprocess.TimeoutExpired:
            return {
                'output': '',
                'error': 'Error: Execution Timed Out (Possible Infinite Loop)',
                'execution_time': '> 2000ms'
            }
        except Exception as e:
            return {
                'output': '',
                'error': str(e),
                'execution_time': '0ms'
            }
