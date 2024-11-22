FROM amazon/aws-lambda-python:latest

# Installs python, removes cache file to make things smaller
RUN dnf update -y && \
    dnf install -y gcc gcc-c++ python3-devel

# Copies requirements.txt file into the container
COPY requirements.txt ./
# Installs dependencies found in your requirements.txt file
RUN pip install --upgrade pip
RUN pip install wheel
RUN pip install -r requirements.txt

# Be sure to copy over the function itself!
# Goes last to take advantage of Docker caching.
COPY handler.py ./
COPY app ./app
COPY conversation ./conversation

# Points to the handler function of your lambda function
CMD ["handler.lambda_handler"]