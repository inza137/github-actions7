# .github/actions/my-csv-validator/Dockerfile

# Start from a base image that has Python pre-installed.
# python:3.9-slim is a good lightweight choice.
FROM python:3.9-slim

# Install any dependencies required by your action's script.
# For this example, we need 'pandas' to work with CSV files.
# Using --no-cache-dir reduces image size.
RUN pip install pandas --no-cache-dir

# Copy your action's script (entrypoint.py in this case) from your action's directory
# into the Docker image's filesystem.
COPY entrypoint.py /entrypoint.py

# Make the script executable (good practice, though `python /entrypoint.py` doesn't strictly require it).
RUN chmod +x /entrypoint.py

# Set the entrypoint for the container. This command will be executed when the container starts.
# It tells the container to run our Python script.
ENTRYPOINT ["python", "/entrypoint.py"]