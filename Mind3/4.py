import numpy as np

# Функция активации (сигмоид)
def sigmoid(x):
    return 1 / (1 + np.exp(-x))

# Производная сигмоидальной функции
def sigmoid_derivative(x):
    return x * (1 - x)

# Входные данные и выходные данные для XOR
X = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
y = np.array([[0], [1], [1], [0]])

# Параметры нейронной сети
input_size = 2
hidden_size = 4
output_size = 1
learning_rate = 0.1

# Инициализация весов случайными значениями
weights_input_hidden = np.random.rand(input_size, hidden_size)
weights_hidden_output = np.random.rand(hidden_size, output_size)

# Обучение нейронной сети
for epoch in range(10000):
    # Прямое распространение (forward propagation)
    hidden_layer_input = np.dot(X, weights_input_hidden)
    hidden_layer_output = sigmoid(hidden_layer_input)

    output_layer_input = np.dot(hidden_layer_output, weights_hidden_output)
    predicted_output = sigmoid(output_layer_input)

    # Вычисление ошибки
    error = y - predicted_output

    # Обратное распространение (backpropagation)
    d_predicted_output = error * sigmoid_derivative(predicted_output)
    d_hidden_layer_output = d_predicted_output.dot(weights_hidden_output.T) * sigmoid_derivative(hidden_layer_output)

    # Обновление весов
    weights_hidden_output += hidden_layer_output.T.dot(d_predicted_output) * learning_rate
    weights_input_hidden += X.T.dot(d_hidden_layer_output) * learning_rate

# Проверка обученной сети
print("Обученная сеть:")
for i in range(len(X)):
    hidden_layer_input = np.dot(X[i:i+1], weights_input_hidden)
    hidden_layer_output = sigmoid(hidden_layer_input)
    output_layer_input = np.dot(hidden_layer_output, weights_hidden_output)
    predicted_output = sigmoid(output_layer_input)
    print(f"Вход: {X[i]}, Выход: {predicted_output[0]:.4f}")
