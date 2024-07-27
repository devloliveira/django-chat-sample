FROM python:3.9

# Set global env vars
ARG install_dev
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Set a working directory
WORKDIR /app

# Install OS libs
RUN apt-get update && apt-get install -y postgresql-client

# Install Python packages
COPY requirements.txt /app
RUN pip install -U pip
RUN pip install "urllib3<2"
RUN pip install -r /app/requirements.txt
RUN pip install -U 'channels[daphne]'

# RUN pip install "setuptools==71.1.0"
# RUN pip install poetry==1.1.13
# RUN poetry config virtualenvs.create false
# COPY pyproject.toml /app
# COPY poetry.lock /app/
# RUN poetry lock --no-update
# RUN poetry install --no-root $([ -z ${install_dev+x} ] && echo --no-dev)



# Install the app
COPY . .

# Run the app
EXPOSE 5000
