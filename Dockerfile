FROM python:3.10
COPY entrypoint.sh /opt/entrypoint.sh
COPY action /opt/action
COPY requirements.txt /opt/requirements.txt
RUN chmod +x /opt/entrypoint.sh
RUN python -m pip install -r /opt/requirements.txt
ENTRYPOINT ["/opt/entrypoint.sh"]