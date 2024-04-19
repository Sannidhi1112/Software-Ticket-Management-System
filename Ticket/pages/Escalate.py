import streamlit as st; 
import pandas as pd; 

from streamlit_extras.switch_page_button import switch_page

from dbconnection import connection;


if "Type" in st.session_state and st.session_state['Type']=="User": 
    st.header("Escalate a ticket");
    #Now we select the onl;y the open tickets , to escalate the ticket. 
    #select from the drop dwon to escalte the ticket 
    #get the tickets which are open in the user profile 
    with st.form("escalate",clear_on_submit=True):
        stmt = "select TicketID,Title,OpenDate,Priority,Status from Ticket where UserID = "+str(st.session_state['id'])+" and Status != 'Closed';"
        result = connection.query_data_select(stmt,st.session_state["conn"],st.session_state["cursor"]);
        #now pouplate into the table in the dataframe; 
        print(result);  
        ticketid_list =[];
        for i in result:
            if i[4]!='Open':
                ticketid_list.append(i[0]);
        selected_ticket_id = st.selectbox('Select the ticketid to be escalted ?',ticketid_list);
        details = st.text_area('Description',placeholder='Reason for escaltion of ticket',max_chars=300);
        escalte_button= st.form_submit_button("Escalate")
        #insert data into the table escalate. 
        if escalte_button:
            if details and len(details)>0:
                stmt = "INSERT INTO Escalate (Details, TicketID, UserID) VALUES ('"+details+"',"+str(selected_ticket_id)+","+str(st.session_state['id'])+")";
                print(stmt);
                if connection.insert_data(stmt,st.session_state["conn"],st.session_state["cursor"]):
                    st.success("Ticket Escalated successfully");
                
            else:
                st.error('Description should not be empty !!!');
elif "Type" in st.session_state and st.session_state['Type']=="Agent":
    st.write("agent cannot escalate the ticket only users can do it.");
else:
    switch_page('login')