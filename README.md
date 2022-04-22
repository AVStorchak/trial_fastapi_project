# trial_fastapi_project
A FastAPI project created for learning purposes
Required software:

Git, Poetry, RabbitMQ (installation instructions: https://www.rabbitmq.com/install-debian.html)

How to use:

Clone the App repository: git clone https://github.com/AVStorchak/trial_fastapi_project

Enter the created directory:

    - run poetry install

    - run uvicorn app:app --reload

    - run python rabbit_consumer/consumer.py in a separate terminal to launch rabbit consumer