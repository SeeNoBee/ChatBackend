FROM python:3
EXPOSE 8000

RUN git clone https://github.com/SeeNoBee/ChatBackend
RUN pip install --no-cache-dir -r /NapoleonIT_Backend/requirements.txt