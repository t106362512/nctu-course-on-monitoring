FROM python:3.6.15-slim
RUN pip install prometheus-client
COPY ./my-app.py /app/
CMD ["python", "app/my-app.py"]