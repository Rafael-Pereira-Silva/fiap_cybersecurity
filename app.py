import streamlit as st
import pandas as pd
import joblib
from sklearn.linear_model import LinearRegression
from sklearn.datasets import make_regression
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import mean_squared_error


# Caminho para o arquivo CSV
file_path = '/content/dataset.csv'

# Carregar o conjunto de dados com o separador correto
data = pd.read_csv(file_path, sep=';')

# Visualizar as primeiras linhas do conjunto de dados para verificar se foi carregado corretamente
data.head(5)

print(data.columns)

# Remoção de valores duplicados
data.drop_duplicates(inplace=True)

# Tratamento de valores ausentes
data.dropna(subset=['Organização', 'Nome'], inplace=True)  # Remove linhas onde 'Organização' ou 'Nome' estão ausentes

# Se necessário, ajuste dos tipos de dados
# data['Quantidade Recursos'] = pd.to_numeric(data['Quantidade Recursos'], errors='coerce')  # Converter para tipo numérico, caso aplicável

# Visualizar as primeiras linhas após a limpeza
print(data.head())

# Salvar os dados limpos em um novo arquivo CSV
data.to_csv('dados_limpos.csv', index=False)

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Carregamento do conjunto de dados limpo
file_path_limpo = '/content/dados_limpos.csv'  # Atualize com o caminho do arquivo de dados limpos
data_limpo = pd.read_csv(file_path_limpo)

# Resumo estatístico
print(data_limpo.describe())

# Histogramas para variáveis numéricas
data_limpo.hist(figsize=(10, 8))
plt.tight_layout()
plt.show()

# Gráfico de contagem para variáveis categóricas ('Organização' e 'Tags')
plt.figure(figsize=(5, 3))
sns.countplot(data=data_limpo, x='Organização')
plt.xticks(rotation=90)
plt.show()

plt.figure(figsize=(10, 6))
sns.countplot(data=data_limpo, x='Tags')
plt.xticks(rotation=90)
plt.show()

# Matriz de correlação (se houver variáveis numéricas)
numeric_data = data_limpo.select_dtypes(include='number')
correlation_matrix = numeric_data.corr()

plt.figure(figsize=(10, 8))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f")
plt.title('Matriz de Correlação')
plt.show()

# Divisão dos dados em features (X) e target (y)
X = data_limpo.drop(columns=['Quantidade Seguidores'])  # Substitua 'Seu_Target_Aqui' pelo nome da coluna alvo
y = data_limpo['Quantidade Recursos']


# Tratamento das variáveis categóricas usando get_dummies
X = pd.get_dummies(X)

# Divisão em conjunto de treino e teste
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Definição do modelo (exemplo: regressão linear)
model = LinearRegression()

# Definição dos hiperparâmetros para tuning
parameters = {'fit_intercept': [True, False]}

# Aplicação do GridSearchCV para tuning de hiperparâmetros
grid_search = GridSearchCV(model, parameters, scoring='neg_mean_squared_error', cv=5)
grid_search.fit(X_train, y_train)

# Melhores hiperparâmetros encontrados
best_params = grid_search.best_params_
print("Melhores Hiperparâmetros Encontrados:", best_params)

# Treinamento do modelo com os melhores hiperparâmetros
best_model = LinearRegression(**best_params)
best_model.fit(X_train, y_train)

# Predição no conjunto de teste
predictions = best_model.predict(X_test)

# Avaliação do modelo usando métricas (exemplo: MSE)
mse = mean_squared_error(y_test, predictions)
print("Mean Squared Error (MSE):", mse)

# Gerar dados sintéticos para treinar um modelo (substitua com seus próprios dados)
X, y = make_regression(n_samples=100, n_features=2, noise=0.1, random_state=42)

# Treinar um modelo (usando regressão linear como exemplo)
model = LinearRegression()
model.fit(X, y)

# Salvar o modelo treinado em um arquivo
joblib.dump(model, 'modelo.pkl')

# Carregar o modelo treinado
model = joblib.load('modelo.pkl')  # Substitua com o caminho para o seu modelo treinado

# Cabeçalho do aplicativo
st.title('Aplicativo de Predição')

# Sidebar para entrada de dados
st.sidebar.header('Insira os Dados')

# Exemplo de entrada para cada variável do modelo
feature1 = st.sidebar.number_input('Feature 1')
feature2 = st.sidebar.number_input('Feature 2')

# Previsão com base nos dados inseridos
if st.sidebar.button('Prever'):
    # Criando um DataFrame com os dados inseridos
    user_data = pd.DataFrame({'Feature 1': [feature1], 'Feature 2': [feature2]})

    # Fazendo a previsão usando o modelo
    prediction = model.predict(user_data)

    # Mostrando a previsão ao usuário
    st.sidebar.subheader('Resultado da Previsão')
    st.sidebar.write(prediction)
