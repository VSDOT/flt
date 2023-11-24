FROM python:3.8-slim-buster

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

ENV DB_URL="mysql+pymysql://root:password@172.17.0.2:3306/dashboard"

ENV GIT_TOKEN="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"

ENV GIT_USERNAME="VSMANI"

ENV REPO_CLONE_PATH="/app/output/"

ENV GIT_PYTHON_REFRESH=quiet

EXPOSE 5000

CMD ["python3", "-m", "flask", "run", "--host=0.0.0.0"]
