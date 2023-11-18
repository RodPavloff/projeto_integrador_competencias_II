# from flask import Flask, render_template
import streamlit as st
import mysql.connector
import pymysql
import hashlib as hl

def initialize_session():
    """
    Função para inicializar a sessão se não existir.
    """
    if 'carrinho' not in st.session_state:
        st.session_state.carrinho = []

def calcular_total(carrinho):
    """
    Função para calcular o total do carrinho.
    """
    return sum(item['price'] for item in carrinho)

def create_user(username, email, password):
    # Conectar ao banco de dados MySQL
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='root',
        database='PIT_II'
    )

    try:
        with conn.cursor() as cursor:
            # Verificar se o usuário já existe
            cursor.execute('SELECT id_cliente FROM cliente WHERE nome=%s', (username,))
            existing_user = cursor.fetchone()

            if existing_user:
                st.error("Usuário já existe. Por favor, escolha outro nome.")
                return False

            # Criar um novo usuário
            hashed_password = hl.sha256(password.encode()).hexdigest()
            cursor.execute('INSERT INTO cliente (nome, email, senha) VALUES (%s, %s, %s)', (username, email, hashed_password))
            st.success(f"Usuário '{username}' criado com sucesso!")

    except mysql.connector.Error as err:
        st.error(f"Erro MySQL: {err}")
        return False

    finally:
        # Commit e fechar a conexão
        conn.commit()
        conn.close()

    return True

def authenticate_user(username, password):
    # Conectar ao banco de dados MySQL
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='root',
        database='PIT_II'
    )

    try:
        with conn.cursor() as cursor:
            # Buscar usuário por nome
            cursor.execute('SELECT id_cliente, senha FROM cliente WHERE nome=%s', (username,))
            user_data = cursor.fetchone()

            if not user_data:
                # Remova esta linha para permitir login para usuários não cadastrados
                # st.error("Usuário não encontrado. Por favor, verifique o nome.")
                pass

            # Verificar senha
            hashed_password = hl.sha256(password.encode()).hexdigest()
            if hashed_password != user_data[1]:
                st.error("Senha incorreta. Por favor, tente novamente.")
                return False

            st.success(f"Login bem-sucedido! Bem-vindo, {username}!")

    except mysql.connector.Error as err:
        st.error(f"Erro MySQL: {err}")
        return False

    finally:
        # Fechar a conexão
        conn.close()

    return True

def connect_to_database():
    """ abre conexao com database no mysql"""
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='root',
        database='PIT_II'
    )

# Configuração da barra superior
st.set_page_config(
    page_title="Duck'n Coffee",
    page_icon="../img/icone.jpeg"
)

# Inicializar a sessão
initialize_session()

# Variável para armazenar o nome do usuário logado
logged_in_username = None

st.sidebar.title("Menu")

# Se já houver um usuário logado, exiba a mensagem de boas-vindas
if 'logged_in_username' not in st.session_state:
    st.session_state.logged_in_username = None

if st.session_state.logged_in_username:
    st.sidebar.write(f"Bem-vindo, {st.session_state.logged_in_username}!")

selected_page = st.sidebar.radio("Selecione uma página", ["Início", "Bebidas", "Salgados", "Doces", "Conheça mais", "Carrinho", "Sobre nós", "Login / Cadastro"])

# Seção do corpo principal
if selected_page == "Início":
    st.markdown(
    """
    <div style="text-align: center;">
        <h1>Bem-vindo à Dunk'n Coffee</h1>
    </div>
    """, unsafe_allow_html=True,
    )
    col1, col2, col3 = st.columns([1,3,1])
    with col2:
        st.image('../img/Dunkn_Coffee.jpg', width=1 ,caption='Delightfully Awake Cafe', use_column_width=True)

elif selected_page == "Bebidas":
    st.header("Nossos Produtos")

    # Lista de Produtos
    products = [
        {"name": "Café Longo", "descricao": "Café 100% Grão Arábica - Irresistível", "image": "../img/Cafe-xicara.jpg", "price": 10.99},
        {"name": "Café Curto", "descricao": "Intenso, breve, sabor inesquecível", "image": "../img/cafe_curto.jpg", "price": 7.99},
        {"name": "Café/Leite", "descricao": "Aroma profundo, desperte seus sentidos", "image": "../img/cafe_leite.jpeg", "price": 13.99},
        {"name": "Café Coado", "descricao": "Artesanal, coado na hora", "image": "../img/coado.jpg", "price": 12.99},
        {"name": "Frappuccino Mocha", "descricao": "Café 100% Grão Arábica Gelado e leite vaporizado" , "image": "../img/frappuccino.jpeg", "price": 19.99},
        {"name": "Iced Coffee", "descricao": "Café Kpop" , "image": "../img/iced.png", "price": 19.99},
    ]

    # Exibir os produtos em colunas
    # col1, col2, col3 = st.columns(3)
    # for i, product in enumerate(products):
    #     with col1 if i % 3 == 0 else col2 if i % 3 == 1 else col3:
    #         st.image(product["image"], use_column_width=True)
    #         st.write(f"**{product['name']}**")
    #         st.write(f"**{product['descricao']}**")
    #         st.write(f"Preço: R${product['price']:.2f}")

    #         quantidade = st.number_input(f"Quantidade de {product['name']}", min_value=1, max_value=10, value=1, step=1)
    #         if st.button(f"Adicionar ao Carrinho - {product['name']}"):
    #             # Adiciona item ao carrinho com a quantidade
    #             product_copy = product.copy()
    #             product_copy['quantidade'] = quantidade
    #             st.session_state.carrinho.append(product_copy)
    #             st.success(f"{product['name']} adicionado ao carrinho!")

    col1, col2, col3 = st.columns(3)

    for i, product in enumerate(products):
        with col1 if i % 3 == 0 else col2 if i % 3 == 1 else col3:
            st.image(product["image"], use_column_width=True)
            st.write(f"**{product['name']}**")
            st.write(f"**{product['descricao']}**")
            st.write(f"Preço: R${product['price']:.2f}")

            quantidade = st.number_input(f"Quantidade de {product['name']}", min_value=1, max_value=10, value=1, step=1)

            if st.button(f"Adicionar ao Carrinho - {product['name']}"):
                # Conectar ao banco de dados
                conn = connect_to_database()

                try:
                    # Adiciona item ao carrinho com a quantidade
                    product_copy = product.copy()

                    # Busca o id_produto do produto no banco de dados
                    with conn.cursor() as cursor:
                        cursor.execute('SELECT id_produto FROM Produto WHERE nome=%s', (product['name'],))
                        id_produto = cursor.fetchone()

                    product_copy['quantidade'] = quantidade
                    product_copy['id_produto'] = id_produto[0] if id_produto else None  # Se não encontrar, pode ser None
                    st.session_state.carrinho.append(product_copy)
                    st.success(f"{product['name']} adicionado ao carrinho!")

                except mysql.connector.Error as err:
                    print(f"Erro MySQL: {err}")

                finally:
                    # Fechar a conexão
                    if conn:
                        conn.close()


elif selected_page == "Salgados":
    st.title("Todos os produtos são de Fabricação Própria.")

    # Lista de Produtos
    products = [
        {"name": "Esfirra", "descricao": "Irresistível - Carne / Queijo / Palmito / Escarola e Bacon"   , "image": "../img/esfirra.jpg", "price": 8.99},
        {"name": "Empada" , "descricao": "Carne / Palmito", "image": "../img/empada.jpg", "price": 11.99},
        {"name": "Coxinha Porção", "descricao": "Porção com 12 mini coxinhas e molho Barbecue da casa", "image": "../img/coxinha_porcao.jpg", "price": 24.99},
        {"name": "Coxinha", "descricao": "Frango receita caseira com catupiry Original", "image": "../img/coxinha.jpg", "price": 9.99},
    ]

    # Exibir os produtos em colunas
    col1, col2, col3 = st.columns(3)
    for i, product in enumerate(products):
        with col1 if i % 3 == 0 else col2 if i % 3 == 1 else col3:
            st.image(product["image"], use_column_width=True)
            st.write(f"**{product['name']}**")
            st.write(f"**{product['descricao']}**")
            st.write(f"Preço: R${product['price']:.2f}")

            quantidade = st.number_input(f"Quantidade de {product['name']}", min_value=1, max_value=10, value=1, step=1)
            if st.button(f"Adicionar ao Carrinho - {product['name']}"):
                # Adiciona item ao carrinho com a quantidade
                product_copy = product.copy()
                product_copy['quantidade'] = quantidade
                st.session_state.carrinho.append(product_copy)
                st.success(f"{product['name']} adicionado ao carrinho!")

elif selected_page == "Doces":
    st.title("Todos os produtos são de Fabricação Própria.")

    # Lista de Produtos
    products = [
        {"name": "Pedaço de Bolo", "descricao": "Chocolate Belga", "image": "../img/bolo_chocolate.jpg", "price": 16.99},
        {"name": "Manjar" , "descricao": "Ameixa e Côco", "image": "../img/manjar.jpg", "price": 13.99},
        {"name": "Pavlova", "descricao": "Receita Russa, uma delícia", "image": "../img/pavlova.jpeg", "price": 24.99},
        {"name": "Frappuccino Mocha", "descricao": "Café 100% Grão Arábica Gelado" , "image": "../img/frappuccino.jpeg", "price": 17.99},
    ]

    # Exibir os produtos em colunas
    col1, col2, col3 = st.columns(3)
    for i, product in enumerate(products):
        with col1 if i % 3 == 0 else col2 if i % 3 == 1 else col3:
            st.image(product["image"], use_column_width=True)
            st.write(f"**{product['name']}**")
            st.write(f"**{product['descricao']}**")
            st.write(f"Preço: R${product['price']:.2f}")
            quantidade = st.number_input(f"Quantidade de {product['name']}", min_value=1, max_value=10, value=1, step=1)
            if st.button(f"Adicionar ao Carrinho - {product['name']}"):
                # Adiciona item ao carrinho com a quantidade
                product_copy = product.copy()
                product_copy['quantidade'] = quantidade
                st.session_state.carrinho.append(product_copy)
                st.success(f"{product['name']} adicionado ao carrinho!")

elif selected_page == "Conheça mais":
    st.markdown(
    """
    <div style="text-align: center;">
        <h1>Conheça mais sobre os tipos de café</h1><p> <h1> </h1></p>
    </div>
    """, unsafe_allow_html=True,
    )

    st.image('../img/tipos_café.jpg', width=1 ,caption='Delightfully Awake Cafe', use_column_width=True)

elif selected_page == "Carrinho":
    st.title("Seu Carrinho de Compras")

    # Exibir produtos
    produtos_tabela = [{"Produto": item['name'], "Valor": f"R${item['price']:.2f}", "Quantidade": item.get('quantidade', 1)} for item in st.session_state.carrinho]
    st.table(data=produtos_tabela)

    # Total
    total = calcular_total(st.session_state.carrinho)
    st.write("---")
    st.write(f"**Total: R${total:.2f}**")

    if st.button("Finalizar Compra"):
        try:
            # Conectar ao banco de dados MySQL
            conn = mysql.connector.connect(
                host='localhost',
                user='root',
                password='root',
                database='PIT_II'
            )

            with conn.cursor() as cursor:
                # Inserir um novo pedido
                cursor.execute('INSERT INTO Pedido (data) VALUES (NOW())')
                id_pedido = cursor.lastrowid

                # Inserir itens do carrinho na tabela de ItemPedido
                for item in st.session_state.carrinho:
                    cursor.execute('INSERT INTO ItemPedido (quantidade, id_pedido, id_produto) VALUES (%s, %s, %s)',
                                (item.get('quantidade', 1), id_pedido, item.get('id_produto')))
            
            # Commit (salvar) as alterações no banco de dados
            conn.commit()

            # Limpar o carrinho depois da compra
            st.session_state.carrinho = []
            st.success("Compra finalizada com sucesso! Um recibo será enviado para o seu e-mail.")

        except mysql.connector.Error as err:
            print(f"Erro MySQL: {err}")

        finally:
            # Fechar a conexão
            if conn:
                conn.close()

elif selected_page == "Login / Cadastro":
    st.title("Login / Cadastro")

    # Formulário de login
    login_username = st.text_input("Nome de Usuário (Login):")
    login_password = st.text_input("Senha (Login):", type="password")

    if st.button("Login"):
        if authenticate_user(login_username, login_password):
            # Atribui o nome do usuário logado à variável de estado
            st.session_state.logged_in_username = login_username
            st.success(f"Login bem-sucedido! Bem-vindo, {st.session_state.logged_in_username}!")

            # Força a reinicialização da página após o login
            st.rerun()

        else:
            st.warning("Falha no login. Verifique seu nome de usuário e senha.")

    st.write("\n\n---\n\n")
    st.write("\n\n---\n\n")
    # Formulário de cadastro
    register_username = st.text_input("Nome de Usuário (Cadastro):", key="register_username")
    register_email = st.text_input("Email (Cadastro):", key="register_email")
    register_password = st.text_input("Senha (Cadastro):", type="password", key="register_password")

    if st.button("Registrar"):
        # Chama a função para criar um novo usuário
        if create_user(register_username, register_email, register_password):
            st.success(f"Usuário '{register_username}' registrado com sucesso! Faça login agora.")
        else:
            st.warning("Falha ao registrar o usuário. Por favor, escolha outro nome de usuário e verifique os detalhes.")


else:
    st.title("Sobre Nós")

    st.write(" ")

    # Informações sobre a empresa
    st.subheader("Somos uma empresa fictícia que vende produtos incríveis online.")
    st.subheader("Entregamos os melhores produtos, fabricação própia especialmente para você!")
    st.write("---")
    st.write("Endereço.:")
    st.write("Rua Lorem Ipsum, 1469, Massachusetts")
    st.write("Excepteur - SP")
    st.write("Entre em contato conosco em contato@minhaloja.com")

# Rodapé
st.write("---")
st.write("© 2023 Minha Loja Online")