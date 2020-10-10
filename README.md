# Экспорт данных из Эгеи

1. download repo

2. open terminal

3. activate virtual environment
    ```
    source venv/bin/activate
    ```
4. install dependencies according to the requirements.txt
    ```
    pip install -r requirements.txt 
    ```
5. script's logic:
    1. gets database's credentials from  `.env` file 
    2. connects to the database
    3. executes SQL query to fetch data
    4. writes the result to folder `output`







