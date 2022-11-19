FROM python:3.10 as compiler
ENV PYTHONUNBUFFERED 1

WORKDIR /personal_expense_tracker-project/

RUN python -m venv /opt/venv
# Enable venv
ENV PATH="/opt/venv/bin:$PATH"

COPY ./requirements.txt /personal_expense_tracker-project/requirements.txt
RUN pip install -r requirements.txt --no-cache-dir

FROM python:3.10-slim as runner
WORKDIR /personal_expense_tracker-project/
COPY --from=compiler /opt/venv /opt/venv

# Enable venv
ENV PATH="/opt/venv/bin:$PATH"
RUN apt-get update && apt-get install -y libxml2
COPY . /personal_expense_tracker-project/
EXPOSE 8080
CMD python app.py