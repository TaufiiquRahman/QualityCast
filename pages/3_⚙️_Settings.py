import streamlit as st
import auth_functions



# Delete Account
st.header('Delete account:')
password = st.text_input(label='Confirm your password',type='password')
st.button(label='Delete Account',on_click=auth_functions.delete_account,args=[password],type='primary') 
