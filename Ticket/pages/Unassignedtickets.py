import streamlit as st; 
import pandas as pd; 
from streamlit_extras.switch_page_button import switch_page
from datetime import datetime
from dbconnection import connection;

def logout():
    st.session_state.clear()
    st.experimental_rerun()

if "Type" in st.session_state and st.session_state["Type"]=="Agent":
    st.header(" Unassigned Tickets");
    stmt = "select TicketID,Title,OpenDate,Priority,Status from Ticket where AgentID IS NULL;"
    result = connection.query_data_select(stmt,st.session_state["conn"],st.session_state["cursor"]);
    #now pouplate into the table in the dataframe; 
    print(result);  
    dataframe = pd.DataFrame(result,columns=("TicketID","Title","OpenDate","Priority","Status"))
    #print(list(result[0]))
    for i in range(0,len(result)):
        with st.expander("Ticket : "+str(dataframe.iloc[i,0])):
            print("----------row data -------");
            
            df = {"TicketID":[result[i][0]],"Title":[result[i][1]],"OpenDate":[result[i][2]],"Priority":[result[i][3]],"Status":[result[i][4]]}
            
            st.table(pd.DataFrame(df));
            #add the comment for each task and then able to find all the details of the task 
            print(result[0][0]);
            Assign = st.button('Assign',key="button"+str(i));
            if Assign:
                #update query to update the ticket id and also update the ticket table status to In progress; 
                stmt = "UPDATE Ticket SET AgentID = "+str(st.session_state['id'])+", Status ='InProgress'"+"Where TicketID = "+str(result[i][0])+";"
                if(connection.insert_data(stmt,st.session_state["conn"],st.session_state["cursor"])):
                    st.success('Assignned Successfully');  
                else:
                    st.error("Ticket cannot be assigned ;")     
else:
    switch_page('Task');

st.sidebar.button("Logout",on_click=logout)