import streamlit as st
import auth_functions

# Delete Account
#st.header('Delete account:')
#password = st.text_input(label='Confirm your password', type='password')
#if st.button(label='Delete Account'):
 #   auth_functions.delete_account(password)

# Change Password
st.header('Change Password:')
email = st.text_input(label='Email')
old_password = st.text_input(label='Old Password', type='password')
new_password = st.text_input(label='New Password', type='password')
confirm_new_password = st.text_input(label='Confirm New Password', type='password')

if st.button('Change Password'):
    if new_password == confirm_new_password:
        auth_functions.change_password(email, old_password, new_password)
        st.success('Password changed successfully.')
    else:
        st.error("New password and confirm new password must match.")
