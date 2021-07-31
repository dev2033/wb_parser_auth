# Парсер для Wildberries


### Установка и запуск проекта (если файл с куками уже есть)

1. Клонировать репозиторий:

    ```bash
    git clone https://github.com/dev2033/wb_parser.git
    ```
   
2. Перейти в директорию с проектом:

    ```bash
    cd wb_parser/
    ```
   
3. В файле конфигурации `srs/config.py` 
   изменить токен для телеграм бота, логин для авторизации на wildberries и путь
   до chromedriver'а (путь нужен абсолютный)
   

4. В файле `systemd_config/parser.service` изменить пути до 
   рабочей директории(`WorkingDirectory=`) 
   и до файла `run.sh` (`ExecStart=`)
   

5. После этого нужно скопировать файл Unit'а (`systemd_config/parser.service`) в 
   `/etc/systemd/system/`:
   
   ```bash
   sudo cp parser.service /etc/systemd/system/
   ```


6. Запускаем демон:

   ```bash
   sudo service parser start
   ```

7. Для проверки работы демона, выполнить команду:

   ```bash
   sudo service parser status
   ```

8. Чтобы остановить демон:

   ```bash
   sudo service parser stop
   ```

9. Чтобы запустить службу при загрузке системы, 
    используйте команду - `sudo systemctl enable parser.service`
   
<hr>

**Настройки nginx, если нужно слушать 80 порт**

<hr>

11. Настройка nginx (`/etc/nginx/site-available/default`): 

    ```bash
        server {
        listen 80;
        server_name localhost;
        access_log  /var/log/nginx/example.log;
     
        location / {
            proxy_pass http://127.0.0.1:8000; 
            proxy_set_header Host $server_name;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        }
    }
    ```

12. Перезапустить nginx командой - `sudo service nginx restart`
    

13. Проверить работоспособность nginx - `sudo service nginx status`


14. Чтобы отправить новый csv файл и начать парсинг, нужно выполнить команду 
    (для `80 порта`):

    ```bash
        curl -X 'POST' \
          'http://localhost:80/' \
          -H 'accept: application/json' \
          -H 'Content-Type: multipart/form-data' \
          -F 'file=@полный_путь_до_файла_csv;type=text/csv'
    ```
    
    Чтобы отправить новый csv файл и начать парсинг, нужно выполнить команду 
        (для `8000 порта`):

    ```bash
        curl -X 'POST' \
          'http://127.0.0.1:8000/' \
          -H 'accept: application/json' \
          -H 'Content-Type: multipart/form-data' \
          -F 'file=@полный_путь_до_файла_csv;type=text/csv'
    ```
    
    ***Пример команды:***
        
    ```bash
        curl -X 'POST' \
          'http://127.0.0.1:8000/' \
          -H 'accept: application/json' \
          -H 'Content-Type: multipart/form-data' \
          -F 'file=@/home/user/id.csv;type=text/csv'    
    ```

    
<hr>
<hr>

### Установка и запуск проекта (если нужно получить куки)

Запуск проекта для получения новых куков

1. Клонировать репозиторий:

    ```bash
    git clone https://github.com/dev2033/wb_parser.git
    ```
   
2. Перейти в директорию с проектом:

    ```bash
    cd wb_parser/
    ```
   
3. В файле конфигурации `srs/config.py` 
   изменить токен для телеграм бота, логин для авторизации на wildberries и путь
   до chromedriver'а (путь нужен абсолютный)
   

4. В файле `systemd_config/parser_new_cookies.service` изменить пути до 
   рабочей директории(`WorkingDirectory=`) 
   и до файла `run.sh` (`ExecStart=`)
   

5. После этого нужно скопировать файл Unit'а (`systemd_config/parser_new_cookies.service`) в 
   `/etc/systemd/system/`:
   
   ```bash
   sudo cp parser_new_cookies.service /etc/systemd/system/
   ```

6. Далее нужно установить дополнительные google-chrome пакеты для
   корректной работы:
   
   ```bash
   sudo apt install -y libxss1 libappindicator1 libindicator7
   ```

7. Установка Chrome:

   ```bash
   wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
   ```
   ```bash
   sudo dpkg -i google-chrome-stable_current_amd64.deb
   ```


8. Фиксим/подтягиваем зависимости:

   ```bash
   sudo apt install -y -f
   ```
   
9. Проверка версии Chrome - `google-chrome --version`


10. В корневой директории проекта(`wb_parser`) устанавливаем 
    виртуальное окружение и устанавливаем зависимости:
    
   ```bash
   python3 -m venv env && source env/bin/activate
   ```
   ```bash
    pip install -U pip && pip install -r requirements.txt
   ```
   ```bash
   deactivate
   ```

11. Запускаем демон:

   ```bash
   sudo service parser_new_cookies start
   ```

12. Для проверки работы демона, выполнить команду:

   ```bash
   sudo service parser_new_cookies status
   ```

13. Чтобы остановить демон:

   ```bash
   sudo service parser_new_cookies stop
   ```

14. Чтобы запустить службу при загрузке системы, 
    используйте команду - `sudo systemctl enable parser_new_cookies.service`
    
<hr>

### Дополнительная информация о проекте
- Файл с id товаров (`id.csv`) храниться в директории `src/data_csv/id.csv` ;


- Выходной файл `.json` храниться в директории `src/results/data_out.json` ;


