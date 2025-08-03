# OmskDigital
**Сайт для поомщи абитуриентам построить карьерный путь в IT-сфере**

## Технологии
- FastaAPI
- Pydantic
- SQLalchemy

## Инструкция по запуску
1.Сначала устанавливаем све зависимости:
```bash
pip3 install requirements.txt
```

2.Включить виртуальное окруженик:
```bash
source .venv/bin/activate
```

3.Запустить главные файл `main.py`:
```bash
python3 main.py 
```

3.Перейти по ссылке на Swager UI:
```bash
http://127.0.0.1:8000/docs
```

## API Методы

### База данных
- **POST** `/method/api/admin/create_table` - Создание таблиц в базе данных

### Компании

#### Получение данных
- **GET** `/method/api/admin/get_company` - Получить список всех компаний
  - Возвращает: список компаний с основной информацией (id, название, иконка, ключевые слова, краткое описание)

- **GET** `/method/api/admin/get_company/{company_id}` - Получить детальную информацию о компании по ID
  - Параметры: `company_id` (int) - ID компании
  - Возвращает: полную информацию о компании включая проекты

#### Управление компаниями
- **POST** `/method/api/admin/company/` - Добавить новую компанию
  - Параметры: 
    - `company` (CompanySchema) - данные компании
    - `icon` (UploadFile) - иконка компании
    - `photo_company` (List[UploadFile]) - фотографии компании
  - Возвращает: подтверждение создания

- **PUT** `/method/api/admin/update_company/{id_company}` - Обновить информацию о компании
  - Параметры:
    - `id_company` (int) - ID компании
    - `company` (CompanySchema) - обновленные данные
    - `icon` (UploadFile) - новая иконка
    - `photo_company` (List[UploadFile]) - новые фотографии
  - Возвращает: подтверждение обновления

- **DELETE** `/method/api/admin/delete_company/{id_company}` - Удалить компанию
  - Параметры: `id_company` (int) - ID компании
  - Возвращает: подтверждение удаления

### Проекты компаний

- **POST** `/method/api/admin/company/project/` - Добавить проект к компании
  - Параметры:
    - `project` (ProjectCompanySchema) - данные проекта
    - `project_photo` (UploadFile) - фотография проекта
  - Возвращает: подтверждение создания

- **PUT** `/method/api/admin/update_company/project/{id_project}` - Обновить проект компании
  - Параметры:
    - `id_project` (int) - ID проекта
    - `project` (ProjectCompanySchema) - обновленные данные проекта
    - `project_photo` (UploadFile) - новая фотография проекта
  - Возвращает: подтверждение обновления

## Особенности
- Все изображения автоматически сохраняются в папку `app/Img Company/`
- Поддерживается загрузка множественных изображений для компаний
- API использует асинхронные операции для работы с базой данных
- Автоматическая валидация данных через Pydantic
