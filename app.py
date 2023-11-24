# Carregar o modelo treinado
model = joblib.load('modelo.pkl') 

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
