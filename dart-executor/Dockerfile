FROM alpine:3.18

RUN apk add --no-cache python3 py3-pip curl unzip bash gcompat

RUN curl -fsSL https://storage.googleapis.com/dart-archive/channels/stable/release/latest/sdk/dartsdk-linux-x64-release.zip -o dart-sdk.zip && \
    unzip dart-sdk.zip && \
    mv dart-sdk /usr/lib/dart && \
    rm dart-sdk.zip

ENV PATH="/usr/lib/dart/bin:${PATH}"

WORKDIR /app
COPY requirements.txt .
RUN pip3 install -r requirements.txt
COPY app.py .
EXPOSE 5003
CMD ["python3", "app.py"]