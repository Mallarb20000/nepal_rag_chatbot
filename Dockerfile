# Dockerfile

# 1. Start with an official Python base image
FROM python:3.11-slim

# 2. Set the working directory inside the container
WORKDIR /app

# 3. Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# 4. Copy and install dependencies
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy the backend application code
COPY ./backend .

# 6. Expose the port the app will run on
EXPOSE 8000

# 7. The command to run the application
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "core.wsgi"]