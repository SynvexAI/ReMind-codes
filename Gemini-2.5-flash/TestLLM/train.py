import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, Trainer, TrainingArguments, TextDataset, DataCollatorForLanguageModeling

# 1. Укажите имя модели и путь к вашему файлу данных
MODEL_NAME = "gpt2" # Или "distilgpt2" для еще меньшей модели
DATA_FILE_PATH = "my_data.txt"
OUTPUT_DIR = "./fine_tuned_gpt2" # Папка для сохранения дообученной модели

# Проверяем наличие GPU
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Используется устройство: {device}")
if device == "cpu":
    print("ВНИМАНИЕ: GPU не обнаружен. Обучение будет ОЧЕНЬ медленным.")

# 2. Загрузка токенизатора и модели
print(f"Загрузка токенизатора '{MODEL_NAME}'...")
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
# Добавляем pad_token, так как у GPT-2 его нет по умолчанию, а он нужен для батчей
if tokenizer.pad_token is None:
    tokenizer.add_special_tokens({'pad_token': tokenizer.eos_token}) # Используем EOS как PAD

print(f"Загрузка модели '{MODEL_NAME}'...")
model = AutoModelForCausalLM.from_pretrained(MODEL_NAME).to(device)
model.resize_token_embeddings(len(tokenizer)) # Обновить размер эмбеддингов после добавления pad_token

# 3. Подготовка набора данных
# TextDataset - простой способ загрузить текстовый файл для языкового моделирования
# block_size - максимальная длина последовательности токенов
print(f"Загрузка данных из '{DATA_FILE_PATH}' и токенизация...")
train_dataset = TextDataset(
    tokenizer=tokenizer,
    file_path=DATA_FILE_PATH,
    block_size=128 # Длина текстовых блоков для обучения (макс. 1024 для gpt2)
)

# DataCollatorForLanguageModeling создает батчи данных для обучения
# mlm=False для авторегрессионных моделей (как GPT), т.е. без маскирования токенов
data_collator = DataCollatorForLanguageModeling(
    tokenizer=tokenizer, mlm=False
)

# 4. Настройка параметров обучения
# Эти параметры сильно влияют на результат и время обучения
training_args = TrainingArguments(
    output_dir=OUTPUT_DIR,
    overwrite_output_dir=True,
    num_train_epochs=3,          # Количество эпох обучения (увеличьте для лучшего результата)
    per_device_train_batch_size=4, # Размер батча на GPU (уменьшите, если не хватает памяти)
    save_steps=10_000,           # Сохранять модель каждые N шагов (для небольшого датасета можно убрать)
    save_total_limit=2,          # Оставлять только N последних чекпоинтов
    logging_dir='./logs',        # Папка для логов TensorBoard
    logging_steps=500,           # Логировать каждые N шагов
    do_train=True,               # Флаг для режима обучения
    prediction_loss_only=True,   # Только лосс, без других метрик
    learning_rate=5e-5,          # Скорость обучения
    weight_decay=0.01,           # Регуляризация
    fp16=True if device.type == 'cuda' else False, # Использовать FP16 для экономии памяти GPU и ускорения
)

# 5. Инициализация и запуск Trainer'а
print("Запуск обучения...")
trainer = Trainer(
    model=model,
    args=training_args,
    data_collator=data_collator,
    train_dataset=train_dataset,
)

trainer.train()
print("Обучение завершено!")

# 6. Сохранение дообученной модели
trainer.save_model(OUTPUT_DIR)
print(f"Дообученная модель сохранена в: {OUTPUT_DIR}")

# --- ТЕСТИРОВАНИЕ МОДЕЛИ ---
print("\n--- ТЕСТИРОВАНИЕ ДООБУЧЕННОЙ МОДЕЛИ ---")
# Загружаем сохраненную модель для тестирования
fine_tuned_model = AutoModelForCausalLM.from_pretrained(OUTPUT_DIR).to(device)
fine_tuned_tokenizer = AutoTokenizer.from_pretrained(OUTPUT_DIR)
if fine_tuned_tokenizer.pad_token is None:
    fine_tuned_tokenizer.add_special_tokens({'pad_token': fine_tuned_tokenizer.eos_token})


prompt_text = "Однажды, когда солнце уже клонилось к закату," # Попробуйте продолжить текст из вашего файла

# Кодируем входной текст
input_ids = fine_tuned_tokenizer.encode(prompt_text, return_tensors="pt").to(device)

print(f"\nВаш запрос: {prompt_text}")
print("Генерация текста...")

# Генерация текста
# max_length: максимальная длина генерируемого текста
# num_return_sequences: сколько вариантов сгенерировать
# do_sample=True: использовать семплирование (более креативно)
# top_k, top_p: параметры для семплирования
# temperature: "температура" генерации (выше -> случайнее, ниже -> предсказуемее)
generated_ids = fine_tuned_model.generate(
    input_ids,
    max_length=150, # Увеличьте, если нужен более длинный текст
    num_return_sequences=1,
    pad_token_id=fine_tuned_tokenizer.eos_token_id, # Указываем pad_token_id для генерации
    do_sample=True,
    top_k=50,
    top_p=0.95,
    temperature=0.7
)

# Декодируем сгенерированный текст
generated_text = fine_tuned_tokenizer.decode(generated_ids[0], skip_special_tokens=True)

print("\nСгенерированный текст:")
print(generated_text)
