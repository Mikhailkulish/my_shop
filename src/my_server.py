from http.server import BaseHTTPRequestHandler, HTTPServer
import os
import urllib.parse
import webbrowser
import time
import threading

hostName = "localhost" # Адрес для доступа по сети
serverPort = 8080 # Порт для доступа по сети


class MyServer(BaseHTTPRequestHandler):
    """Класс сервера для обработки входящих запросов от клиента"""

    def do_GET(self):
        """ Метод для обработки входящих GET-запросов """
        self.send_response(200) # Отправка кода ответа
        self.send_header("Content-type", "text/html") # Отправка передаваемого типа данных
        self.end_headers() # Завершение формирования заголовков ответа

        current_dir = os.path.dirname(os.path.abspath(__file__))  # Формирование пути к текущей директории
        project_root = os.path.dirname(current_dir) # Формирование пути к корневому каталогу проекта
        file_path = os.path.join(project_root, "templates", "contacts.html") # Путь к файлу страницы html

        try:
            with open(file_path, 'r', encoding='UTF-8') as file:
                html_contacts = file.read()
            self.wfile.write(bytes(html_contacts, "utf-8")) # Тело ответа
        except FileNotFoundError:
            self.send_response(404)
            self.wfile.write("Файл не найден".encode('utf-8'))

    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length).decode('utf-8')
        data = urllib.parse.parse_qs(post_data)

        name = data.get('name', [''])[0]
        email = data.get('email', [''])[0]
        message = data.get('message', [''])[0]

        print(f"POST: {name}, {email}, {message}")

        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(f"<h2>Спасибо, {name}!</h2><a href='/'>Назад</a>".encode('utf-8'))

if __name__ == "__main__":
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print(f"Старт соединения http://{hostName}:{serverPort}")

    url = f"http://{hostName}:{serverPort}"
    threading.Timer(1, lambda: webbrowser.open(url)).start()

    server_thread = threading.Thread(target=webServer.serve_forever)
    server_thread.start()

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        print("\nПолучен сигнал завершения...")
        webServer.shutdown()

    webServer.server_close()
    print("Завершение соединения.")
