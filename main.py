import streamlit as st
import streamlit_authenticator as stauth
from dependencies import consulta_geral, consulta_nome, add_registro, criar_tabela


COOKIE_EXPIRY_DAYS = 30

def main():

    try:
        consulta_geral()
    except:
        criar_tabela()

    db_query = consulta_geral()

    registros = {'usernames': {}}
    for data in db_query:
        registros['usernames'][data[1]] = {'name' : data[0], 'password': data[2]}


    authenticator = stauth.Authenticate(
        registros,
        'random_cookie_name',
        'random_signature_key',

        COOKIE_EXPIRY_DAYS
    )

    if 'clicou_registrar' not in st.session_state:
        st.session_state['clicou_registrar'] = False
    
    if st.session_state['clicou_registrar'] == False:
        login_form(authenticator=authenticator)
    
    else:
        usuario_form()


def login_form(authenticator):
    name, authentication_status, username = authenticator.login('Login')
    if authentication_status:
        authenticator.logout('Logout', 'main')
               
        st.write('Dashboard')
        
    elif authentication_status == False:
        st.error('Usuário/senha incorretos.')
    
    elif authentication_status == None:
        st.warning('Por favor, informe um usuário e senha.')
        clicou_registrar = st.button('Registrar')
        if clicou_registrar:
            st.session_state['clicou_registrar'] = True
            st.rerun()

def confirm_msg():
    hashed_password = stauth.Hasher([st.session_state.pswrd]).generate()
    if st.session_state.pswrd != st.session_state.confirm_pswrd:
        st.warning('Senha errada.')
        sleep(3)
    
    elif consulta_nome(st.session_state.user):
        st.warning('Nome de usuário já existe.')
        sleep(3)
    
    else:
        add_registro(st.session_state.nome, st.session_state.user, hashed_password[0])
        st.success('Registro Efetuado!')
        sleep(3)


def usuario_form():
    with st.form(key='formulario', clear_on_submit=True):
        nome = st.text_input('Nome', key='nome')
        username = st.text_input('Usuário', key='user')
        password = st.text_input('Senha', key='pswrd', type='password')
        confirm_pass = st.text_input('Confirme a senha', key='confirm_pswrd', type='password')
        submit = st.form_submit_button(
            'Salvar', on_click=confirm_msg 
        )

    ciclou_fazer_login = st.button('Fazer Login')
    if ciclou_fazer_login:
        st.session_state['clicou_registrar'] = False
        st.rerun()





if __name__ == '__main__':
    main()

