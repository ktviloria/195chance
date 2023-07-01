#for editing passwords
#all users have access to this page
#faculty users can only edit their own passwords while admin users can edit passwords of any and all accounts

import hashlib

from dash import dcc
from dash import html
from dash import dash_table
import dash_bootstrap_components as dbc
import dash
from dash.exceptions import PreventUpdate
from dash.dependencies import Input, Output, State
import pandas as pd
import datetime
from datetime import date
 
from app import app
from apps import dbconnect as db
 
from urllib.parse import urlparse, parse_qs

mod_style = { 
 'color': '#fff',
 'background-color': '#b22222',
 'font-size': '25px'
} 

layout= html.Div( 
    [ 
        html.Div( 
            [ 
                dcc.Store(id='editpass_toload', storage_type='memory', data=0)
            ] 
        ), 
        html.H2("Edit Password", id = 'password_header'), 
        html.Hr(),
        dbc.Alert('Please supply required fields.', color="danger", id='editpass_inputs_alert', is_open=False),
        dbc.Alert("Old password is incorrect. Please try again.", color="danger", id='editpass_checkold_alert', is_open=False),
        dbc.Alert("New passwords do not match. Please try again.", color="danger", id='editpass_matchnew_alert', is_open=False), 
        dbc.Row(
            [
                
                html.Div(
                    dbc.Row( 
                        [ 
                            dbc.Label("Old Password", width=2), 
                            dbc.Col( 
                                dbc.Input( 
                                    type="text", id="editpass_old", placeholder="Enter old password" 
                                ), 
                                width= 4,
                                className="mb-3",
                            ), 
                        ],
                    ),
                    id='oldpassdiv'
                ),
                # html.Div(
                #     html.H6("Old password input not needed as admin", style={"color": "#d9534f", "font-style": "italic"}),
                #     id='oldpassdiv'  
                # ),
                html.Div(
                    dbc.Row( 
                        [ 
                            dbc.Label("New Password", width=2), 
                            dbc.Col( 
                                dbc.Input( 
                                    type="text", id="editpass_new1", placeholder="Enter new password" 
                                ),
                                width= 4,
                                className="mb-3", 
                            ), 
                        ],  
                    ),
                    id='newpass1div'
                ),
                html.Div(
                    dbc.Row( 
                        [ 
                            dbc.Label("Confirm Password", width=2), 
                            dbc.Col( 
                                dbc.Input( 
                                    type="text", id="editpass_new2", placeholder="Verify new password" 
                                ), 
                                width= 4,
                                className="mb-3",
                            ), 
                        ],  
                    ),
                    id='newpass2div'
                ),
            ]
        ),
        html.Hr(), 
        dbc.Button('Submit', color='danger', id='editpass_submitbtn'),
        dbc.Modal( 
            [    
                dbc.ModalHeader(dbc.ModalTitle("Saving Progress"), style=mod_style), 
                dbc.ModalBody("tempmessage", id='editpass_feedback_message'), 
                dbc.ModalFooter( 
                    dbc.Button("Okay", color='secondary', id="editpass_closebtn", className="ms-auto", n_clicks=0) 
                ),           
            ], 
        centered=True, 
        id="editpass_modal", 
        is_open=False, 
        ),
    ]
)

@app.callback(
    [
        Output('oldpassdiv', 'style'),
    ], 
    [
        Input('url', 'pathname'), 
    ], 
    [
        State('currentuserid', 'data'), 
        State('url', 'search'), 
    ]
)

def loadoldpassdiv (pathname, currentuserid, search): 
    if pathname == '/edit_password': 
        if currentuserid <= 3: 
            parsed = urlparse(search)
            idparse = parse_qs(parsed.query)['id'][0]
            
            if currentuserid != int(idparse): 
                oldpassdiv =  {'display':'none'}
            else: 
                oldpassdiv = None
            return [oldpassdiv]
        else: 
            raise PreventUpdate
                
        
    else: 
        raise PreventUpdate

#modal callback    
@app.callback(
    [
        Output('editpass_modal', 'is_open'), 
        # Output('oldpassdiv', 'style'),
        # Output('newpass1div', 'style'),
        # Output('newpass2div', 'style'),
        Output('editpass_feedback_message', 'children'),
        Output('editpass_inputs_alert', 'is_open'),
        Output('editpass_checkold_alert', 'is_open'),
        Output('editpass_matchnew_alert', 'is_open'),  
        Output('editpass_closebtn', 'href'),
    ], 
    [
        Input('editpass_submitbtn', 'n_clicks'), 
        Input('editpass_closebtn', 'n_clicks')
    ],
    [
        State('currentuserid', 'data'),
        State('currentrole', 'data'),
        State('editpass_old', 'value'),
        State('editpass_new1', 'value'),
        State('editpass_new2', 'value'),
        State('url', 'search') 
    ]
)
def editpass_submitprocess (submit_btn, close_btn,
                           currentuserid, currentusertype, oldpass, newpass1, newpass2, search): 
    if currentusertype == 'faculty':
        oldpassdiv = {'display':'none'}
    else:
        oldpassdiv = {'display':'contents'}
        
    ctx = dash.callback_context
    if ctx.triggered: 
            eventid = ctx.triggered[0]['prop_id'].split('.')[0]
            inputsopenalert = False
            checkoldopenalert = False
            matchnewopenalert = False
            openmodal = False 
            feedbackmessage  = ' '
            okay_href = None 
    else: 
            raise PreventUpdate

    if eventid == 'editpass_submitbtn' and submit_btn:
        if currentusertype == 'faculty':
            faculty_sql = """ SELECT 
                    faculty.user_id,
                    users.user_pass
                    FROM faculty
                        INNER JOIN users on faculty.user_id = users.user_id
                    WHERE
                        faculty_delete_ind = false AND
                        faculty.user_id = %s
                    ORDER BY
                        faculty.user_id ASC
                """      
            faculty_val = [f"{currentuserid}"]
            faculty_colname = ['faculty_id', 'faculty_oldpass']
            faculty_df = db.querydatafromdatabase(faculty_sql, faculty_val, faculty_colname)
            acc_pass = faculty_df['faculty_oldpass'][0]
    
            encryptedoldpass = hashlib.sha256(oldpass.encode('utf-8')).hexdigest()
            inputs = [oldpass, newpass1, newpass2]

            if not all(inputs): 
                inputsopenalert = True
            elif not encryptedoldpass == acc_pass:
                checkoldopenalert = True
            elif not newpass1 == newpass2:
                matchnewopenalert = True
            else: 
                openmodal=True
                parsed = urlparse(search)
                sql_users = """UPDATE users
                SET 
                    user_pass = %s 
                WHERE 
                    user_id = %s
                """
                encryptednewpass = hashlib.sha256(newpass1.encode('utf-8')).hexdigest()   
                values_users = [encryptednewpass, currentuserid]
                db.modifydatabase(sql_users, values_users)

                fac_timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                fac_timestamp_time = datetime.datetime.strptime(fac_timestamp,'%Y-%m-%d %H:%M:%S')
                
                fp_sqlcode_modifiedby = """SELECT
                user_id,
                user_un
                FROM users
                """
                fp_vals_modifiedby = []
                fp_cols_modifiedby = ['id', 'un']
                username = db.querydatafromdatabase(fp_sqlcode_modifiedby, fp_vals_modifiedby, fp_cols_modifiedby)
                
                username_modifier = ""
                for i in range(len(username['id'])):
                    if int(username['id'][i]) == currentuserid:
                        username_modifier = username['un'][i]

                sql_fac = """UPDATE faculty
                    SET 
                        faculty_last_upd = %s,
                        faculty_modified_by = %s
                    WHERE 
                        user_id = %s
                    """   
                values_fac = [fac_timestamp_time, username_modifier, currentuserid]
                db.modifydatabase(sql_fac, values_fac)

                feedbackmessage = "Faculty information updated."
                okay_href = '/my_profile'
        
        elif currentusertype == 'admin':
            admin_sql = """ SELECT 
                    user_id
                    FROM users
                """      
            admin_val = []
            admin_colname = ['user_id']
            admin_df = db.querydatafromdatabase(admin_sql, admin_val, admin_colname)

            inputs = [newpass1, newpass2]

            if not all(inputs): 
                inputsopenalert = True
            elif not newpass1 == newpass2:
                matchnewopenalert = True
            else: 
                openmodal=True

                fac_timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                fac_timestamp_time = datetime.datetime.strptime(fac_timestamp,'%Y-%m-%d %H:%M:%S')     
                
                fp_sqlcode_modifiedby = """SELECT
                user_id,
                user_un
                FROM users
                """
                fp_vals_modifiedby = []
                fp_cols_modifiedby = ['id', 'un']
                username = db.querydatafromdatabase(fp_sqlcode_modifiedby, fp_vals_modifiedby, fp_cols_modifiedby)
                
                username_modifier = ""
                for i in range(len(username['id'])):
                    if int(username['id'][i]) == currentuserid:
                        username_modifier = username['un'][i]
                
                parsed = urlparse(search)
                editpass_userid = parse_qs(parsed.query)['id'][0]
                    
                sql_fac = """UPDATE users
                        SET 
                            user_pass = %s
                        WHERE 
                            user_id = %s
                        """   
                encryptednewpass = hashlib.sha256(newpass1.encode('utf-8')).hexdigest()
                values_fac = [encryptednewpass, editpass_userid]
                db.modifydatabase(sql_fac, values_fac)

                sql_fac = """UPDATE faculty
                            SET 
                                faculty_last_upd = %s,
                                faculty_modified_by = %s
                            WHERE 
                                user_id = %s
                            """   
                values_fac = [fac_timestamp_time, username_modifier, editpass_userid]
                db.modifydatabase(sql_fac, values_fac)


                feedbackmessage = "User information updated."
                okay_href = '/faculty_manage'
                
    elif eventid == 'editpass_closebtn' and close_btn: 
            pass 
    else: 
            raise PreventUpdate
    return [openmodal, feedbackmessage, inputsopenalert, checkoldopenalert, matchnewopenalert, okay_href]