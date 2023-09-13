import streamlit as st


st.title("Contacto")

#----CONTACT----

with st.container():
    st.write("---")
    st.header("Contactate con nosotros")
    st.write("##")

    contact_form= """
    <form action="https://formsubmit.co/david.jung@fraunhofer.cl" method="POST">
        <input type="hidden" name="_captcha" value = "false">
        <input type="text" name="name" placeholder ="Tu nombre" required>
        <input type="email" name="email" placeholder = "Tu email" required>
        <textarea name= "message" placeholder = "Tu mensaje aqui" required></textarea>
        <button type="submit">Send</button>
    </form>
    """
left_column, right_column = st.columns(2)
with left_column:
    st.markdown(contact_form, unsafe_allow_html=True)
with right_column:
    st.empty()

#Use local css
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}<style>",unsafe_allow_html=True)

local_css("style.css")