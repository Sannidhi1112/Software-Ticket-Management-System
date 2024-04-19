import streamlit as st;
from streamlit_extras.switch_page_button import switch_page
from streamlit_star_rating import st_star_rating

from dbconnection import connection;


if 'id' not in st.session_state or st.session_state['id']=='':
    #redirected to teh login page. 

    switch_page('login');
else:
    if st.session_state['Type']=="User":
        placeholder = st.empty()
        with placeholder.form("Feedback"):
            #POST THE FEEDBACK

            st.header("Feedback form");
            #data needs the list of student or proffessor ids.
        
            stmt = "select TicketID,Title,OpenDate,Priority,Status,AgentID from Ticket where UserID = "+str(st.session_state['id'])+" and Status='Closed';"
            results = connection.query_data_select(stmt,st.session_state["conn"],st.session_state["cursor"]);
            closed_tickets_description = [];
            
            for i in results:
                closed_tickets_description.append(i[1]);
            
            fbticketid = st.selectbox('Ticket Description',closed_tickets_description);
            #name of the agent to be displayed. 
            
            desc = st.text_area("Feedback description",placeholder="Write Something... ");
            agentID = "";
            for i in results: 
                if i[1]==fbticketid:
                    agentID= i[5];
            if(agentID != ""):
                stmt = "select Name from Agent where AgentID="+str(agentID)+";"
                agentname= connection.query_data_select(stmt,st.session_state['conn'],st.session_state['cursor']);
                st.selectbox("Agent Name " , agentname[0]);
            else:
                st.session_state['disabled'] = True
            
           
            sl = st_star_rating(label = "Please rate you experience", maxValue = 5, defaultValue = 1, key = "rating", emoticons = True );

            print(sl);
            submit = st.form_submit_button("Submit",disabled= st.session_state['disabled'])
            if submit:  
                #post it into the datbase;
                
                stmt = "INSERT INTO Feedback (Description, Rating, AgentID, UserID) VALUES ('"+desc+"','"+str(int(sl)-1)+"',"+str(agentID)+","+str(st.session_state['id'])+")";
                print(stmt);
                if connection.insert_data(stmt,st.session_state['conn'],st.session_state['cursor']):
                    st.success('FeedBackSubmitted !!!!')
                else:
                    st.warning('No Tickets closed to submit Feedback!!!')
    else:
        st.error("Feedback can be given only by the User")
                
        
        