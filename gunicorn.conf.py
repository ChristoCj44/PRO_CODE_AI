# Gunicorn Configuration

# The address and port to bind to
bind = "0.0.0.0:5000"

# Number of worker processes to handle requests
# For CPU bound tasks, usually (2 * CPUs) + 1. 
# Since we have blocking AI calls, using fewer workers but more threads.
workers = 2

# Number of threads per worker
# Useful for I/O bound tasks (waiting for AI API or Code Execution)
threads = 4

# Timeout in seconds
# Increased to 60s because AI analysis can take time
timeout = 60

# Logging
accesslog = "-"
errorlog = "-"
loglevel = "info"
