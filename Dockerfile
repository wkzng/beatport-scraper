FROM amazon/aws-lambda-python:3.11.2025.05.04.05-x86_64

# Copy requirements.txt
COPY requirements.txt ${LAMBDA_TASK_ROOT}

# upgrade pip version and install requirements
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# install lambda runtime interface client for python
# documentation: https://docs.aws.amazon.com/lambda/latest/dg/python-image.html#python-image-instructions
#RUN pip install awslambdaric
#RUN playwright install --with-deps chromium


# Copy function code
COPY src ./src

# Set runtime interface client as default command for the container runtime
#ENTRYPOINT ["python", "-m", "awslambdaric" ]

# Set the CMD to your handler (could also be done as a parameter override outside of the Dockerfile)
CMD ["src/dummy_handler.main"]

#docker build -t aime .
#docker run -it aime



