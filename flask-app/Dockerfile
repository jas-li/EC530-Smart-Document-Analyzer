# Use an official Python runtime as a parent image, matching a version used in your CI
FROM python:3.11

# Set the working directory in the container
WORKDIR /app

# Copy the local directory contents into the container
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Download NLTK data
RUN python -c "import nltk; nltk.download(['punkt', 'stopwords', 'vader_lexicon'])"

# Optionally, run linter and tests
# RUN flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
# RUN pytest

# Make port 80 available to the world outside this container
EXPOSE 80

# # Define environment variable
# ENV FLASK_ENV production

# Run the application
CMD ["python", "app.py"]
