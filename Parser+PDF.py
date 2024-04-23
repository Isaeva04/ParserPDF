import os
import requests
from bs4 import BeautifulSoup
from pypdf import PdfWriter

download_folder = input('Куда сохранить скачаные файлы?')
url = input("Введите URL-адрес страницы для скачивания файлов: ")# Получаем URL-адрес страницы от пользователя
def download_files_from_page(download_folder):
    # Отправляем GET-запрос на страницу
    response = requests.get(url)
    # Создаем объект BeautifulSoup для парсинга HTML
    soup = BeautifulSoup(response.content, 'html.parser')

    # Находим все ссылки на файлы на странице
    file_links = soup.find_all('a', href=True)

    # Проходимся по каждой ссылке на файл
    for link in file_links:
        file_url = link['href']
        # Проверяем, что ссылка ведет на файл (можно добавить дополнительные проверки)
        if file_url.endswith('.pdf'):  # Можно изменить расширение файла, если необходимо
            # Определяем имя файла
            filename = os.path.join(download_folder, os.path.basename(file_url))
            if url.endswith('index.htm'):
                url_parts = url.rsplit('/', 1)
                url_parts[-1] = file_url
                full_url = '/'.join(url_parts)
                print('Скачан файл:'+ full_url)
            else:
                full_url = url + file_url
                print('Скачан файл: ' + full_url)

            # Скачиваем файл
            with open(filename, 'wb') as file:
                response = requests.get(full_url)
                file.write(response.content)

download_files_from_page(download_folder)

folder_path = input('Куда сохранить объединенный файл?')
def merge_pdfs_in_folder(download_folder,folder_path):
    merger = PdfWriter()

    pdf_files = [file for file in os.listdir(download_folder) if file.endswith(".pdf")]
    # Проходимся по каждому PDF файлу в папке

    for pdf_file in pdf_files:
        try:
            # Создаем полный путь к файлу
            file_path = os.path.join(download_folder, pdf_file)
            # Добавляем PDF файл к объединителю
            merger.append(file_path)
        except BaseException as e:
            print('Ошибка в файле: '+pdf_file)
            continue
        # Пишем объединенный PDF файл
        output_pdf_path = os.path.join(folder_path, "merged-pdf.pdf")
        merger.write(output_pdf_path)
        merger.close()

        # for pdf_file in pdf_files:
        # file_path = os.path.join(folder_path, pdf_file)
        # os.remove(file_path)

merge_pdfs_in_folder(download_folder,folder_path)
print('Готово!')