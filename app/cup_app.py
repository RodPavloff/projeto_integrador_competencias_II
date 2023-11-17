from flask import Flask, render_template
import streamlit as st
import mysql.connector
import pymysql


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

# Configuração da barra superior
st.set_page_config(
    page_title="Duck'n Coffee",
    page_icon="../img/icone.jpeg"
)

# Barra de navegação - Imagem do café
# user_image = st.sidebar.image("../img/dunkn_Coffee_0.jpg", width=250) # TIRAR

st.sidebar.title("Menu")
selected_page = st.sidebar.radio("Selecione uma página", ["Início", "Bebidas", "Salgados", "Doces", "Conheça mais", "Carrinho", "Sobre nós"])

# Inicializar a sessão
initialize_session()

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

            # if st.button(f"Adicionar ao Carrinho - {product['name']}"):
            #     # Adiciona item ao carrinho
            #     st.session_state.carrinho.append(product)
            #     st.success(f"{product['name']} adicionado ao carrinho!")

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
            if st.button(f"Adicionar ao Carrinho - {product['name']}"):
                # Adiciona item ao carrinho
                st.session_state.carrinho.append(product)
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
            if st.button(f"Adicionar ao Carrinho - {product['name']}"):
                # Adiciona item ao carrinho
                st.session_state.carrinho.append(product)
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

    # Botões
    if st.button("Esvaziar Carrinho"):
        # Esvazia o carrinho diretamente no estado
        st.session_state.carrinho = []

    if not st.session_state.carrinho:
        st.warning("Carrinho vazio. Adicione itens antes de finalizar a compra.")

    # Botão Finalizar Compra sempre disponível
    if st.button("Finalizar Compra"):
        # Conectar ao banco de dados MySQL
        conn = mysql.connector.connect(
            host='127.0.0.1',
            user='root',
            password='root',
            database='PIT_II'
        )

        try:
            with conn.cursor() as cursor:
                # Inserir itens do carrinho na tabela de pedidos
                cursor.execute('INSERT INTO Pedido (data) VALUES (NOW())')
                id_pedido = cursor.lastrowid

                for item in st.session_state.carrinho:
                    cursor.execute('INSERT INTO ItemPedido (quantidade, id_pedido, id_produto) VALUES (%s, %s, %s)', (item.get('quantidade', 1), id_pedido, item.get('id_produto')))
        except mysql.connector.Error as err:
            print(f"Erro MySQL: {err}")
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
            # Limpar o carrinho depois da compra
                st.session_state.carrinho = []
                st.success("Compra finalizada com sucesso! Um recibo será enviado para o seu e-mail.")

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