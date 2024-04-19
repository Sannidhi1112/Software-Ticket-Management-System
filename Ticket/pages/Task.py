#create the tasks as per the user request; 

import streamlit as st; 
import pandas as pd;
from streamlit_extras.switch_page_button import switch_page
from datetime import datetime
from dbconnection import connection;
import time;


def task_processing():
    msg = st.toast('Comment added successfully...')
    time.sleep(1)
    msg.toast('Status of the task changed ')
    time.sleep(1)
    msg.toast('Successfull')


def comment(ticketID,i):
    
    results = connection.query_data_select("select * from commentticket where TicketID ="+str(ticketID)+";",st.session_state["conn"],st.session_state["cursor"]);
    
    print(results);
    if len(results)>0 : 
        #print the announcements on to the screen; 
        #using the elements
        for a in results:
            
            #ST.CHAT_ELEMENTS TO BE USED TO PRINT ON TO THE SCREEN
            if (a[3] and a[3]!=''):
                user_stmt = "select Name from User where UserID="+str(a[3])+";"
                username= connection.query_data_select(user_stmt,st.session_state['conn'],st.session_state['cursor']);
                with st.chat_message(name = 'user'):
                    msg = """<h5>Posted By """+str(username[0][0])+"""</a></h5> <p>"""+str(a[1])+"""</p>""";
                    st.markdown(msg,unsafe_allow_html=True);
                    #print(a[1]);   
            elif (a[4]!=''):
                agent_stmt = "select Name from Agent where AgentID="+str(a[4])+";"
                agentname= connection.query_data_select(agent_stmt,st.session_state['conn'],st.session_state['cursor']);
                with st.chat_message(name = 'user',avatar='🧑'):
                    msg = """<h5>Posted By Agent: """+str(agentname[0][0])+"""</a></h5> <p>"""+str(a[1])+"""</p>""";
                    st.markdown(msg,unsafe_allow_html=True);
                #st.chat_message(name = 'user',avatar='🧑').write(a[4]);
    
    prompt = st.chat_input("Comment",key=i,disabled=st.session_state['disabled']);
    #post on to the ui ; 
    if prompt and len(prompt.strip())>0:
        if st.session_state['Type'] == 'User':
            print("inside the prmopt")
              
            
            stmt = "INSERT INTO commentticket (Description, TicketID, UserID) VALUES ('"+prompt+"',"+str(ticketID)+","+str(st.session_state["id"])+");"
            ticketstmt = "select Status from Ticket where TicketID="+str(ticketID)+";"
            ticketresult= connection.query_data_select(ticketstmt,st.session_state['conn'],st.session_state['cursor']);
            connection.insert_data(stmt,st.session_state["conn"],st.session_state["cursor"]);
            if ticketresult[0][0]=="Pending":
                #update the statement to in progress;
                updt_stmt = "Update Ticket SET Status='InProgress' where TicketID ="+str(ticketID)+";"
                if(connection.query_data_select(updt_stmt,st.session_state['conn'],st.session_state['cursor'])):
                    
                    task_processing();

                    st.success('Comment added')

          
            
        else:
            aid = 'A'+str(len(results));
            stmt = "INSERT INTO commentticket (Description, TicketID, AgentID) VALUES ('"+prompt+"',"+str(ticketID)+","+str(st.session_state["id"])+");"
            connection.insert_data(stmt,st.session_state["conn"],st.session_state["cursor"]);
        with st.chat_message(name = 'user'):
                msg = """<h5>Posted By : """+str(st.session_state['id'])+"""</a></h5> <p>"""+prompt+"""</p>""";
                st.markdown(msg,unsafe_allow_html=True);
                #print(a[1]);   
    #send it to the db;
    
#now first thing is to establish the connection ; get all the information related to anouncements. 
#and then display it on to the screen 

def logout():
    st.session_state.clear()
    st.experimental_rerun()

def start():
    if 'id' not in st.session_state or st.session_state['id']=='':
        #redirected to teh login page. 
        switch_page('login');
    else:
        st.header("My Tickets");
        st.sidebar.button("Logout",on_click=logout)

        #to get the my task list , get the user_id of the one associated with it and then 
        #apply the where condition to the where list present in this. 
        #Now all the tickets related to user has to be shown and then button to create a new ticket. 
        #get the userid from the usertable based on the username from session state variable.
        if st.session_state['Type']=="User":
            stmt = "select TicketID,Title,OpenDate,Priority,Status from Ticket where UserID = "+str(st.session_state['id'])+";"
            result = connection.query_data_select(stmt,st.session_state["conn"],st.session_state["cursor"]);
            #now pouplate into the table in the dataframe; 
            dataframe = pd.DataFrame(result,columns=("TicketID","Title","OpenDate","Priority","Status"))
            #print(list(result[0]))
            for i in range(0,len(result)):
                with st.expander(str(dataframe.iloc[i,0])):
                    print("----------row data -------");
                    escalation_stmt = "select * from Escalate where TicketID="+str(result[i][0])+";"
                    if result[i][4]=='Closed':
                        st.session_state['disabled']=True;  
                    else:
                        st.session_state['disabled']=False;
                    escalation_result= connection.query_data_select(escalation_stmt,st.session_state['conn'],st.session_state['cursor']);
                    if len(escalation_result)>=1:
                        estatus = "Escaleted"
                    else:
                        estatus= "Not escalated"
                    df = {"TicketID":[result[i][0]],"Title":[result[i][1]],"OpenDate":[result[i][2]],"Priority":[result[i][3]],"Status":[result[i][4]],"EscalationStatus":estatus}
                    
                    st.table(pd.DataFrame(df));
                    #add the comment for each task and then able to find all the details of the task 
                    print(result[0][0]);
                    comment(result[i][0],i);
                
                    #comment1 = st.text_input("",placeholder="Add comment ....",key=i)
                    
            #st.table(dataframe);
                    if (st.button('Escalate',key = "button_"+str(i),disabled=st.session_state['disabled'])):
                        switch_page('escalate');
                    
        else:
            stmt = "select TicketID,Title,OpenDate,Priority,Status from Ticket where AgentID = "+str(st.session_state['id'])+";"
            result = connection.query_data_select(stmt,st.session_state["conn"],st.session_state["cursor"]);
            #now pouplate into the table in the dataframe; 
            dataframe = pd.DataFrame(result,columns=("TicketID","Title","OpenDate","Priority","Status"))
            
            for i in range(0,len(result)):
                with st.expander("Ticket : "+str(dataframe.iloc[i,0])):
                    print("----------row data -------");
                    escalation_stmt = "select * from Escalate where TicketID="+str(result[i][0])+";"
                    escalation_result= connection.query_data_select(escalation_stmt,st.session_state['conn'],st.session_state['cursor']);
                    if len(escalation_result)>=1:
                        estatus = "Escaleted"
                    else:
                        estatus= "Not escalated"
                    df = {"TicketID":[result[i][0]],"Title":[result[i][1]],"OpenDate":[result[i][2]],"Priority":[result[i][3]],"Status":[result[i][4]],"EscalationStatus":estatus}
                    if result[i][4]=='Closed':
                        st.session_state['disabled']=True;  
                    else:
                        st.session_state['disabled']=False;
                    st.table(pd.DataFrame(df));
                    
                    taskstatus = st.selectbox('Ticket Status',['Inprogress','Pending','Closed'],key="status_"+str(i),disabled=st.session_state['disabled']);
                    comment(result[i][0],i);
                    #comment1 = st.text_input("",placeholder="Add comment ....",key=i)
                    #change the status of the ticket to the pending or closed.
                    save = st.button('Save',key='button_'+str(i),disabled=st.session_state['disabled']);
                    if save:
                        #update command to change the status of the task and then add the comments into the table comment.
                        stmt = "UPDATE Ticket SET Status ='"+str(taskstatus)+"' Where TicketID = "+str(result[i][0])+";"
                        if(connection.insert_data(stmt,st.session_state["conn"],st.session_state["cursor"])):
                            task_processing();
                            st.success("Task is "+str(taskstatus));
        if(st.session_state['Type']=='User'):
            with st.popover("Create Ticket"):
                #create all the required fields for the task ;
                with st.form("Ticket",clear_on_submit=True):
                    title = st.text_input("Title ");
                    description = st.text_input("Description of the ticket");
                    openDate = datetime.now().date().strftime("%Y-%m-%D")
                    priority = st.radio("Priority of the Task",["Low","Medium","High"],horizontal=True);
                    user_id= st.session_state['id'];
                    submit = st.form_submit_button("Submit")
                if submit:
                    #creata an insert statement for the task to enter into the ticket table;
                    print("inside the sub,it button")
                    stmt = "INSERT INTO Ticket (Title, Description, OpenDate, Priority, UserID) VALUES"+"('"+title+"','"+description+"','"+openDate+"','"+priority+"',"+str(user_id)+")";
                    print(stmt);
                    connection.insert_data(stmt,st.session_state["conn"],st.session_state["cursor"]);
                    st.success("Ticket created successfully")

start()
