import streamlit as st; 
import streamlit as st
from dbconnection import connection;
from streamlit_extras.switch_page_button import switch_page
def Personal():
    st.write(" done with the exceution")
st.header('Login/Signup Page');

import streamlit as st

action = st.radio(
        "",
        ["Login","SignUp"],
        horizontal=True,
    )


# Create an empty container
placeholder = st.empty()


if action == "SignUp":
        with placeholder.form("creata account"):
            st.markdown("#### Create Account")
            #User_ID = st.text_input("UserID");
            Email_id = st.text_input("Email_id");
            Password = st.text_input("Password",type="password");
            cpasword = st.text_input("confirm password",type="password");
            name = st.text_input("Name of the user/Agent");
            Type = st.selectbox('Are u user or Agent?',('User', 'Agent'),index=None);
            #call the function
            submit = st.form_submit_button("Signup");

if action =="Login":
    
    with placeholder.form("login"):
        role = st.radio("",("User","Agent"),horizontal=True);
        st.markdown("#### Enter your credentials")
        email = st.text_input("E-Mail")
        password = st.text_input("Password", type="password")
        submit = st.form_submit_button("Login")
    #st.session_state['username']='';
    
#intializze the connection from the 
#Change username and password as your SQL.
conn,cursor = connection.connect('root','Sharan@0201','softwareticketmanagement');
 #pass the query and retreive the results. 
#store the connection into session varibales. 
st.session_state['conn']=conn;
st.session_state['cursor']=cursor;
print(st.session_state);
if submit:
    if action=="Login":
        if role == 'User':
            results = connection.query_data_select("select * from User where Email = '"+email+"' and Password='"+password+"';",conn,cursor);
        else:
            results = connection.query_data_select("select * from Agent where Email = '"+email+"' and Password='"+password+"';",conn,cursor);
        
        
        print(results);
        if(len(results)>=1):
            for i in results:
                if submit and email == results[0][2] and password == results[0][3]:
                    # If the form is submitted and the email and password are correct,
                    # clear the form/container and display a success message
                    placeholder.empty()
                    st.success("Login successful");
                    #create the session variable with the username logged in . 
                    st.session_state["id"]=results[0][0]
                    st.session_state['Type']= role;
                    #switch page to next page.
                    print("login successfull -----------");
                    if role=="User":
                        switch_page('Task');
                    else:
                        switch_page("Unassignedtickets");
        else:
            st.error("Incorrect username or password !!!");
    else:

        if Password!= cpasword:
            st.error(" Password and confirm password doesnot match");
        elif Email_id=="" or Password=="":
            st.error("username or password cannot be empty ")
       
        else:
            if(Type=="User"):
                stmt = "INSERT INTO User (Name, Email, Password) VALUES"+"('"+name+"','"+Email_id+"','"+Password+"')";
                print(stmt);
                connection.insert_data(stmt,conn,cursor);
                result_id= connection.query_data_select("select * from User where Name ='"+name+"'"+" and Email ='"+Email_id+"'",st.session_state['conn'],st.session_state['cursor'])
                st.session_state["id"]=result_id[0][1]
            else:
                #insert it into the regustration table;
                stmt = "INSERT INTO Agent (Name, Email, Password) VALUES"+"('"+name+"','"+Email_id+"','"+Password+"')";
                print(stmt);
                connection.insert_data(stmt,conn,cursor);
                result_id= connection.query_data_select("select * from Agent where Name ='"+name+"'"+" and Email ='"+Email_id+"'",st.session_state['conn'],st.session_state['cursor']);
                st.session_state["id"]=result_id[0][1]
            st.success("Account Registration done successfully please click on " ); 



