import os
import shutil
import json
import logging
import datetime
import time

# --- Константы и конфигурация ---
TEST_ROOT_DIR = "temp_test_data"
LOG_FILE_NAME = "test_script_log.txt"
TEST_TEXT_FILE = os.path.join(TEST_ROOT_DIR, "sample_text.txt")
TEST_JSON_FILE = os.path.join(TEST_ROOT_DIR, "sample_data.json")

# --- Настройка логирования ---
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE_NAME, encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger()

# --- Вспомогательные функции для тестов ---
def log_test_result(test_name: str, passed: bool, message: str = ""):
    """Логирует результат выполнения теста."""
    status = "УСПЕШНО" if passed else "ПРОВАЛ"
    log_func = logger.info if passed else logger.error
    log_func(f"[{test_name}] - {status}: {message}")
    return passed

def setup_test_environment():
    """Создает чистую тестовую директорию."""
    logger.info(f"--- НАЧАЛО ТЕСТОВ ---")
    logger.info(f"Подготовка тестовой среды: {TEST_ROOT_DIR}")
    if os.path.exists(TEST_ROOT_DIR):
        try:
            shutil.rmtree(TEST_ROOT_DIR)
            logger.info(f"Удалена существующая директория: {TEST_ROOT_DIR}")
        except OSError as e:
            logger.error(f"Ошибка при удалении {TEST_ROOT_DIR}: {e}")
            return False
    
    try:
        os.makedirs(TEST_ROOT_DIR)
        logger.info(f"Создана новая тестовая директория: {TEST_ROOT_DIR}")
        return True
    except OSError as e:
        logger.error(f"Ошибка при создании {TEST_ROOT_DIR}: {e}")
        return False

def cleanup_test_environment():
    """Удаляет тестовую директорию."""
    logger.info(f"Завершение тестов. Очистка тестовой среды: {TEST_ROOT_DIR}")
    if os.path.exists(TEST_ROOT_DIR):
        try:
            shutil.rmtree(TEST_ROOT_DIR)
            logger.info(f"Тестовая директория {TEST_ROOT_DIR} успешно удалена.")
        except OSError as e:
            logger.error(f"Ошибка при удалении {TEST_ROOT_DIR} во время очистки: {e}")
    logger.info(f"--- КОНЕЦ ТЕСТОВ ---")

# --- Тестовые сценарии ---
def test_1_directory_creation():
    """Тест: Создание директории и проверка ее существования."""
    test_name = "test_1_directory_creation"
    logger.info(f"\nЗапуск {test_name}...")
    
    dir_path = os.path.join(TEST_ROOT_DIR, "subdir_test")
    try:
        os.makedirs(dir_path)
        result = os.path.isdir(dir_path)
        return log_test_result(test_name, result, "Директория создана и существует." if result else "Директория не найдена.")
    except Exception as e:
        return log_test_result(test_name, False, f"Ошибка при создании директории: {e}")

def test_2_file_creation_and_content():
    """Тест: Создание текстового файла, запись и чтение содержимого."""
    test_name = "test_2_file_creation_and_content"
    logger.info(f"\nЗапуск {test_name}...")
    
    expected_content = "Это тестовая строка для файла.\nВторая строка."
    
    try:
        with open(TEST_TEXT_FILE, "w", encoding="utf-8") as f:
            f.write(expected_content)
        
        if not os.path.exists(TEST_TEXT_FILE):
            return log_test_result(test_name, False, "Файл не был создан.")
            
        with open(TEST_TEXT_FILE, "r", encoding="utf-8") as f:
            read_content = f.read()
            
        result = (read_content == expected_content)
        return log_test_result(test_name, result, 
                               "Содержимое файла совпадает." if result else 
                               f"Содержимое не совпадает. Ожидалось: '{expected_content}', Получено: '{read_content}'")
    except Exception as e:
        return log_test_result(test_name, False, f"Ошибка при работе с текстовым файлом: {e}")

def test_3_json_read_write():
    """Тест: Запись и чтение JSON-данных."""
    test_name = "test_3_json_read_write"
    logger.info(f"\nЗапуск {test_name}...")
    
    test_data = {
        "name": "Тестовый Объект",
        "id": 123,
        "is_active": True,
        "timestamp": datetime.datetime.now().isoformat()
    }
    
    try:
        with open(TEST_JSON_FILE, "w", encoding="utf-8") as f:
            json.dump(test_data, f, indent=4, ensure_ascii=False)
        
        if not os.path.exists(TEST_JSON_FILE):
            return log_test_result(test_name, False, "JSON файл не был создан.")
            
        with open(TEST_JSON_FILE, "r", encoding="utf-8") as f:
            read_data = json.load(f)
            
        result = (read_data == test_data)
        return log_test_result(test_name, result, 
                               "JSON данные совпадают." if result else 
                               f"JSON данные не совпадают. Ожидалось: {test_data}, Получено: {read_data}")
    except Exception as e:
        return log_test_result(test_name, False, f"Ошибка при работе с JSON файлом: {e}")

def test_4_file_deletion():
    """Тест: Удаление файла и проверка его отсутствия."""
    test_name = "test_4_file_deletion"
    logger.info(f"\nЗапуск {test_name}...")
    
    # Убедимся, что файл существует перед удалением
    if not os.path.exists(TEST_TEXT_FILE):
        with open(TEST_TEXT_FILE, "w", encoding="utf-8") as f:
            f.write("временный контент")
        logger.info(f"Создан временный файл {TEST_TEXT_FILE} для удаления.")

    try:
        os.remove(TEST_TEXT_FILE)
        result = not os.path.exists(TEST_TEXT_FILE)
        return log_test_result(test_name, result, 
                               "Файл успешно удален и не существует." if result else 
                               "Файл не был удален.")
    except Exception as e:
        return log_test_result(test_name, False, f"Ошибка при удалении файла: {e}")

def test_5_error_handling_non_existent_file():
    """Тест: Попытка чтения несуществующего файла (ожидаем ошибку)."""
    test_name = "test_5_error_handling_non_existent_file"
    logger.info(f"\nЗапуск {test_name}...")
    
    non_existent_file = os.path.join(TEST_ROOT_DIR, "non_existent.txt")
    
    try:
        with open(non_existent_file, "r", encoding="utf-8") as f:
            _ = f.read()
        return log_test_result(test_name, False, "Неожиданно прочитан несуществующий файл.")
    except FileNotFoundError:
        return log_test_result(test_name, True, "Ожидаемая ошибка FileNotFoundError получена.")
    except Exception as e:
        return log_test_result(test_name, False, f"Получена неожиданная ошибка: {type(e).__name__} вместо FileNotFoundError.")

# --- Главная функция для запуска тестов ---
def run_all_tests():
    """Запускает все определенные тестовые сценарии."""
    overall_start_time = time.perf_counter()
    test_results = []

    if not setup_test_environment():
        logger.critical("Не удалось подготовить тестовую среду. Тесты не будут запущены.")
        return 1 # Код ошибки

    # Список тестов для выполнения
    tests_to_run = [
        test_1_directory_creation,
        test_2_file_creation_and_content,
        test_3_json_read_write,
        test_4_file_deletion,
        test_5_error_handling_non_existent_file,
    ]

    for test_func in tests_to_run:
        test_results.append(test_func())
        time.sleep(0.1) # Небольшая пауза между тестами для лучшей читаемости логов

    passed_count = test_results.count(True)
    failed_count = test_results.count(False)
    total_count = len(test_results)
    
    overall_end_time = time.perf_counter()
    duration = overall_end_time - overall_start_time

    logger.info(f"\n--- СВОДКА ПО РЕЗУЛЬТАТАМ ТЕСТОВ ---")
    logger.info(f"Всего тестов: {total_count}")
    logger.info(f"Успешно: {passed_count}")
    logger.info(f"Провалено: {failed_count}")
    logger.info(f"Общее время выполнения: {duration:.2f} секунд")

    cleanup_test_environment()
    
    return 0 if failed_count == 0 else 1

if __name__ == "__main__":
    exit_code = run_all_tests()
    # sys.exit(exit_code) # Можно использовать sys.exit, чтобы вернуть код завершения ОС
