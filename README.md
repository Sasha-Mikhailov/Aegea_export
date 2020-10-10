# Экспорт данных из Эгеи

1. open terminal 

2. clone the repo
    ```
   git clone https://github.com/Sasha-Mikhailov/Aegea_export.git
   cd Aegea_export
    ```
   
3. fill database credentials to the `.env` file:
    ```
    nano .env
    ```
    - DB_USER 
    - DB_PASSWORD
    - DB_HOST
    - DB_NAME
    - BLOG_URL (_not neccessary, just for fine URLs in the result file_)

4. install a `virtualenv`
    ```
    pip3 install virtualenv 
    ```
5. create a new one for the repo:
    ```
    virtualenv -p python3 venv
    ```
6. activate virtual environment
    ```
    source venv/bin/activate
    ```
7. install dependencies according to the requirements.txt
    ```
    pip install -r requirements.txt 
    ```
8. run the script 
    ```
    python3 main.py 
    ```
   _(install Python from [original website](https://www.python.org/downloads/release/python-390/), 
   find your OS in section 'Files')_
## script's logic
1. gets database's credentials from  `.env` file 
2. connects to the database
3. executes SQL query to fetch data
4. writes the result to folder `output`







