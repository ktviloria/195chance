#for editing/deleting own faculty profile
#only faculty users have access to this page

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
                dcc.Store(id='myprof_toload', storage_type='memory', data=0), 
                dcc.Store(id = "oncelang", storage_type='memory', data=1)
            ] 
        ), 
        html.H2("Profile Details"), 
        html.H6("* Indicates required field", style={"color": "#d9534f", "font-style": "italic"}),
        html.Hr(),
        dbc.Alert('Please supply required fields.', color="danger", id='myprof_inputs_alert', is_open=False), 
        dbc.Alert("Old password is incorrect. Please try again.", color="danger", id='myprof_checkold_alert', is_open=False),
        # dbc.Alert('You did not make any changes.', color="danger", id='myprof_currentun_alert', is_open=False),
        # dbc.Alert('Check your changes. Username may already exist!', color="danger", id='myprof_un_alert', is_open=False),
        # dbc.Row(
        #     [
        #         dbc.Col(
        #             dbc.Row( 
        #                 [ 
        #                     dbc.Label("Username", width=2), 
        #                     dbc.Col( 
        #                         dbc.Input( 
        #                             type="text", id="myprof_un", placeholder="Enter new username" 
        #                         ), 
        #                     ), 
        #                 ],  
        #             ),
        #             width=6
        #         ),
        #         dbc.Col( 
        #             dbc.Button('Change Password', color='danger', id='myprof_changepassbtn'),
        #             width=2
        #         ),
        #     ],
        # ),
        html.Br(),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dbc.Row( 
                            [ 
                                dbc.Col(
                                    [
                                        dbc.Label("Last Name",), 
                                        dbc.Label("*", style={"color": "#d9534f", "font-style": "bold"}),
                                    ],
                                    width=2
                                ),
                                dbc.Col( 
                                    dbc.Input( 
                                        type="text", id="myprof_ln", placeholder="Enter last name" 
                                    ), 
                                ), 
                            ], 
                            className="mb-3", 
                        ), 
                        dbc.Row( 
                            [ 
                                dbc.Col(
                                    [
                                        dbc.Label("First Name",), 
                                        dbc.Label("*", style={"color": "#d9534f", "font-style": "bold"}),
                                    ],
                                    width=2
                                ),
                                dbc.Col( 
                                    dbc.Input( 
                                        type="text", id="myprof_fn", placeholder="Enter first name" 
                                    ), 
                                ), 
                            ], 
                            className="mb-3", 
                        ), 
                        dbc.Row( 
                            [ 
                                dbc.Label("Middle Name", width=2), 
                                dbc.Col( 
                                    dbc.Input( 
                                        type="text", id="myprof_mn", placeholder="Enter middle name" 
                                    ), 
                                ), 
                            ], 
                            className="mb-3", 
                        ), 
                        dbc.Row( 
                            [ 
                                dbc.Label("Suffix", width=2), 
                                dbc.Col( 
                                    dbc.Input( 
                                        type="text", id="myprof_suff", placeholder="Enter suffix" 
                                    ), 
                                ), 
                            ], 
                            className="mb-3", 
                        ), 
                        dbc.Row( 
                            [ 
                                dbc.Label("Rank", width=2), 
                                dbc.Col( 
                                    html.Div( 
                                        dbc.Input( 
                                            id='myprof_rank', readonly= 1
                                        ),
                                        className="dash-bootstrap" 
                                    ), 
                                ), 
                            ], 
                            className="mb-3", 
                        ), 
                        dbc.Row( 
                            [ 
                                dbc.Label("Birthdate", width=2), 
                                dbc.Col( 
                                    dbc.Input( 
                                        type="date", id="myprof_bdate", placeholder="Enter birthdate" 
                                    ), 
                                ), 
                            ], 
                            className="mb-3", 
                        ),
                        dbc.Row( 
                            [ 
                                dbc.Label("Email", width=2), 
                                dbc.Col( 
                                    dbc.Input( 
                                        type="text", id="myprof_mail", placeholder="Enter email" 
                                    ), 
                                ), 
                            ], 
                            className="mb-3", 
                        ), 
                    ],
                    width=6
                ), 
                dbc.Col(
                    [
                        dbc.Row( 
                            [ 
                                dbc.Label("Contact number", width=2), 
                                dbc.Col( 
                                    dbc.Input( 
                                        type="number", id="myprof_contact", placeholder="Enter contact number" 
                                    ), 
                                ), 
                            ], 
                            className="mb-3", 
                        ), 
                        html.Div(
                        dbc.Row( 
                            [ 
                                dbc.Label("Expertise 1", width=2), 
                                dbc.Col( 
                                    dbc.Input( 
                                        type="text", id="myprof_expert1", placeholder="Enter area of expertise" 
                                    ), 
                                ), 
                            ], 
                            className="mb-3", 
                            ), id = 'myexpertise1_div'
                        ),
                        html.Div(
                        dbc.Row( 
                            [ 
                                dbc.Label("Expertise 2", width=2), 
                                dbc.Col( 
                                    dbc.Input( 
                                        type="text", id="myprof_expert2", placeholder="Enter area of expertise" 
                                    ), 
                                ), 
                            ], 
                            className="mb-3", 
                        ), id = 'myexpertise2_div' 
                        ),
                        html.Div(
                        dbc.Row( 
                            [ 
                                dbc.Label("Expertise 3", width=2), 
                                dbc.Col( 
                                    dbc.Input( 
                                        type="text", id="myprof_expert3", placeholder="Enter area of expertise" 
                                    ), 
                                ), 
                            ], 
                            className="mb-3", 
                        ), id = 'myexpertise3_div' 
                        ),
                        html.Div(
                        dbc.Row( 
                            [ 
                                dbc.Label("Expertise 4", width=2), 
                                dbc.Col( 
                                    dbc.Input( 
                                        type="text", id="myprof_expert4", placeholder="Enter area of expertise" 
                                    ), 
                                ), 
                            ], 
                            className="mb-3", 
                        ),id = 'myexpertise4_div'
                        ),
                        html.Div(
                        dbc.Row( 
                            [ 
                                dbc.Label("Expertise 5", width=2), 
                                dbc.Col( 
                                    dbc.Input( 
                                        type="text", id="myprof_expert5", placeholder="Enter area of expertise" 
                                    ), 
                                ), 
                            ], 
                            className="mb-3", 
                        ), id = 'myexpertise5_div'
                        ), 
                    ],
                    width=6
                ), 
            ]
        ),
        html.Hr(), 
        dbc.Button('Submit', color='danger', id='myprof_submitbtn'),
        dbc.Modal( 
            [    
                dbc.ModalHeader(dbc.ModalTitle("Saving Progress"), style=mod_style), 
                dbc.ModalBody("tempmessage", id='myprof_feedback_message'), 
                dbc.ModalFooter( 
                    dbc.Button("Okay", color='secondary', id="myprof_closebtn", className="ms-auto", n_clicks=0) 
                ),           
            ], 
        centered=True, 
        id="myprof_modal", 
        is_open=False, 
        ),
        # dbc.Modal( 
        #     [    
        #         dbc.ModalHeader(dbc.ModalTitle("Identity Verification"), style=mod_style), 
        #         dbc.ModalBody(
        #             [
        #                 html.Div(
        #                     dbc.Row( 
        #                         [ 
        #                             dbc.Label("Old Password", width=2), 
        #                             dbc.Col( 
        #                                 dbc.Input( 
        #                                     type="text", id="myprof_oldpass", placeholder="Enter old password" 
        #                                 ), 
        #                                 width= 8,
        #                                 className="mb-3",
        #                             ), 
        #                         ],
        #                     ),
        #                 ),
        #             ]
        #         ), 
        #         dbc.ModalFooter( 
        #             dbc.Button('Submit', color='danger', id='myprof_changepassverbtn')
        #         ),           
        #     ], 
        # centered=True, 
        # id="myprof_modal1", 
        # is_open=False, 
        # ),
    ] 
) 
@app.callback(
    [
        Output('myexpertise2_div', 'style'), 
        Output('myexpertise3_div', 'style'), 
        Output('myexpertise4_div', 'style'), 
        Output('myexpertise5_div', 'style')
    ], 
    [
        Input('url', 'pathname'), 
        Input('myprof_toload', 'modified_timestamp'), 
        Input('myprof_expert1', 'value'),
        Input('myprof_expert2', 'value'), 
        Input('myprof_expert3', 'value'), 
        Input('myprof_expert4', 'value')
        
    ]
)

def expertisedivs (pathname, timestamp, expert1, expert2, expert3, expert4): 
    
    
    if pathname == '/edit_my_profile':
        
        if expert1 == '': 
            expert1 = None
            expert2 = None
            expert3 = None
            expert4 = None
        if expert2 == '':
            expert2 = None
            expert3 = None
            expert4 = None
        if expert3 == '':
            expert3 = None
            expert4 = None
        if expert4 == '':
            expert4 = None
        
        if expert1 == None:  
            div2 = {'display': 'none'}
            div3 = {'display': 'none'}
            div4 = {'display': 'none'}
            div5 = {'display': 'none'}
            
        else: 
            div2 = None
        
        if expert2 == None: 
            div3 = {'display': 'none'}
            div4 = {'display': 'none'}
            div5 = {'display': 'none'}
        else: 
            div3 = None
        
        if expert3 == None:
            div4 = {'display': 'none'}
            div5 = {'display': 'none'}
            
        else: 
            div4 = None
        
        if expert4 == None:
            div5 = {'display': 'none'}
            
        else: 
            div5 = None
        
    else: 
        raise PreventUpdate
    return [div2, div3, div4, div5]






#load data  callback 
@app.callback ( 
    [
        # Output('myprof_un', 'value'),
        Output('myprof_ln', 'value'),
        Output('myprof_fn', 'value'),
        Output('myprof_mn', 'value'), 
        Output('myprof_suff', 'value'),
        Output('myprof_rank', 'value'), 
        Output('myprof_bdate', 'value'), 
        Output('myprof_mail', 'value'), 
        Output('myprof_contact', 'value'), 
        Output('myprof_expert1', 'value'), 
        Output('myprof_expert2', 'value'),
        Output('myprof_expert3', 'value'),
        Output('myprof_expert4', 'value'),
        Output('myprof_expert5', 'value'),
        Output('oncelang', 'data')
    ],
    [ 
        Input('url', 'pathname'),
    ], 
    [ 
        # State('url', 'search'),
        State('currentuserid', 'data'), 
        State('oncelang', 'data')
    ] 
)
def facprof_load(pathname, currentuserid, once): 
    if once ==1: 
        if pathname == '/edit_my_profile': 
            sql_rank = """ SELECT DISTINCT(rank_title) as label, rank_id as value 
                    FROM ranks
                    ORDER BY value ASC
                """ 
            values_rank = [] 
            cols_rank = ['label', 'value'] 
            rank = db.querydatafromdatabase(sql_rank, values_rank, cols_rank) 
            rank_opts = rank.to_dict('records') 
                        
            myprof_sql = """ SELECT 
                faculty.user_id,
                users.user_un,
                faculty_ln, 
                faculty_fn,
                faculty_mn,
                faculty_suff, 
                ranks.rank_title,
                faculty_bdate,
                faculty_mail,
                faculty_contact,
                faculty_expert1,
                faculty_expert2,
                faculty_expert3,
                faculty_expert4,
                faculty_expert5
                
                FROM faculty
                    INNER JOIN ranks ON faculty.rank_id = ranks.rank_id
                    INNER JOIN users on faculty.user_id = users.user_id
                WHERE
                    faculty_delete_ind = false AND
                    faculty.user_id = %s
                ORDER BY
                    faculty.user_id ASC
            """      
            myprof_val = [f"{currentuserid}"]
            myprof_colname = ['myprof_id', 'myprof_un', 'myprof_ln', 'myprof_fn', 'myprof_mn', 'myprof_suff', 
                    'myprof_rank', 'myprof_bday', 'myprof_mail', 'myprof_contact', 
                    'myprof_exp1', 'myprof_exp2', 'myprof_exp3', 'myprof_exp4', 'myprof_exp5']
            myprof_df = db.querydatafromdatabase(myprof_sql, myprof_val, myprof_colname)
            
            myprof_id = myprof_df['myprof_id'][0]
            myprof_un = myprof_df['myprof_un'][0]  
            myprof_ln = myprof_df['myprof_ln'][0]
            myprof_fn = myprof_df['myprof_fn'][0]
            myprof_mn = myprof_df['myprof_mn'][0]
            myprof_suff = myprof_df['myprof_suff'][0]
            myprof_rank = myprof_df['myprof_rank'][0]
            myprof_bday = myprof_df['myprof_bday'][0]
            myprof_mail = myprof_df['myprof_mail'][0]
            myprof_contact = myprof_df['myprof_contact'][0]
            myprof_exp1 = myprof_df['myprof_exp1'][0]
            myprof_exp2 = myprof_df['myprof_exp2'][0]
            myprof_exp3 = myprof_df['myprof_exp3'][0]
            myprof_exp4 = myprof_df['myprof_exp4'][0]
            myprof_exp5 = myprof_df['myprof_exp5'][0]

        else:
            raise PreventUpdate
        once += 1
    else:
        raise PreventUpdate
    return [myprof_ln, myprof_fn, myprof_mn, myprof_suff, myprof_rank, myprof_bday,
            myprof_mail, myprof_contact, myprof_exp1, myprof_exp2, myprof_exp3, myprof_exp4, myprof_exp5, once]

#modal callback    
@app.callback(
    [
        # Output('myprof_modal1', 'is_open'),
        Output('myprof_modal', 'is_open'), 
        Output('myprof_feedback_message', 'children'),
        Output('myprof_inputs_alert', 'is_open'),
        # Output('myprof_checkold_alert', 'is_open'),
        # Output('myprof_currentun_alert', 'is_open'),
        # Output('myprof_un_alert', 'is_open'),  
        # Output('myprof_changepassbtn', 'href'),
        Output('myprof_closebtn', 'href'),
    ], 
    [
        # Input('myprof_changepassbtn', 'n_clicks'),
        # Input('myprof_changepassverbtn', 'n_clicks'),
        Input('myprof_submitbtn', 'n_clicks'), 
        Input('myprof_closebtn', 'n_clicks')
    ],
    [
        State('currentuserid', 'data'),
        # State('myprof_oldpass', 'value'),
        # State('myprof_un', 'value'),
        State('myprof_ln', 'value'), 
        State('myprof_fn', 'value'),
        State('myprof_mn', 'value'),
        State('myprof_suff', 'value'),
        State('myprof_bdate', 'value'),
        State('myprof_mail', 'value'),
        State('myprof_contact', 'value'),
        State('myprof_expert1', 'value'),
        State('myprof_expert2', 'value'),
        State('myprof_expert3', 'value'),
        State('myprof_expert4', 'value'),
        State('myprof_expert5', 'value'), 
        State('url', 'search') 
    ]
)

def facprof_submitprocess ( submit_btn, close_btn,
                           currentuserid, lastname, firstname, middlename, suffix, bdate, mail, contact, 
                           expert1, expert2, expert3, expert4, expert5, search): 
    ctx = dash.callback_context
    if ctx.triggered: 
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]
        inputsopenalert = False
        # checkoldopenalert = False
        # currentunopenalert = False
        unopenalert = False
        # openmodal1 = False
        openmodal = False 
        feedbackmessage  = ' '
        changepass_href = None
        okay_href = None 
    else: 
        raise PreventUpdate
    
    # if eventid == 'myprof_changepassbtn' and changepass_btn:
        # openmodal1=True
        # if eventid == 'myprof_changepassverbtn' and oldpasssubmit_btn:
        #     faculty_sql = """ SELECT 
        #                 faculty.user_id,
        #                 users.user_pass
        #                 FROM faculty
        #                     INNER JOIN users on faculty.user_id = users.user_id
        #                 WHERE
        #                     faculty_delete_ind = false AND
        #                     faculty.user_id = %s
        #                 ORDER BY
        #                     faculty.user_id ASC
        #             """      
        #     faculty_val = [f"{currentuserid}"]
        #     faculty_colname = ['faculty_id', 'faculty_oldpass']
        #     faculty_df = db.querydatafromdatabase(faculty_sql, faculty_val, faculty_colname)
        #     acc_pass = faculty_df['faculty_oldpass'][0]
        
        #     encryptedoldpass = hashlib.sha256(oldpass.encode('utf-8')).hexdigest()
        #     inputs = [oldpass]
            
        #     if not all(inputs): 
        #         inputsopenalert = True
        #     elif not encryptedoldpass == acc_pass:
        #         checkoldopenalert = True
        #     else:
                # changepass_href = '/edit_password'  

    if eventid == 'myprof_submitbtn' and submit_btn:
        inputs = [lastname, firstname]
        
        existingusername_sql = """SELECT 
            users.user_un
        FROM faculty
            INNER JOIN users on faculty.user_id = users.user_id
        WHERE
            faculty_delete_ind = false
        ORDER BY
            faculty.user_id ASC
        """      
        existingusername_val = []
        existingusername_colname = ['existingun1']
        existingusername_df = db.querydatafromdatabase(existingusername_sql, existingusername_val, existingusername_colname)

        # sql = """SELECT
        #     users.user_un
        # FROM faculty
        #     INNER JOIN users on faculty.user_id = users.user_id
        # WHERE
        #     faculty_delete_ind = false AND
        #     users.user_un = %s
        # ORDER BY
        #     faculty.user_id ASC    
        # """
        # val = [f"{currentusername}%"]
        # col = ['existingun2']
        # exstusername = db.querydatafromdatabase(sql, val, col)

        if not all(inputs): 
            inputsopenalert = True
        # elif exstusername.shape[0]:
        #     currentunopenalert = True
        # elif currentusername in existingusername_df['existingun1'].values:
        #     unopenalert = True
        else: 
            openmodal=True
            parsed = urlparse(search)
            # sql_users = """UPDATE users
            # SET 
            #     user_un = %s
            # WHERE 
            #     user_id = %s
            # """   
            # values_users = [currentusername, currentuserid]
            # db.modifydatabase(sql_users, values_users)

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
                faculty_ln = %s, 
                faculty_fn = %s, 
                faculty_mn = %s, 
                faculty_suff = %s, 
                faculty_bdate = %s, 
                faculty_mail = %s, 
                faculty_contact = %s, 
                faculty_expert1 = %s,
                faculty_expert2 = %s,
                faculty_expert3 = %s,
                faculty_expert4 = %s,
                faculty_expert5 = %s,
                faculty_last_upd = %s,
                faculty_modified_by = %s
            WHERE 
                user_id = %s
            """   
            values_fac = [lastname, firstname, middlename, 
                        suffix, bdate, mail, contact, expert1,
                        expert2, expert3, expert4, expert5, fac_timestamp_time, username_modifier, currentuserid]
            db.modifydatabase(sql_fac, values_fac)

            feedbackmessage = "Faculty information updated."
            okay_href = '/my_profile'
            
    elif eventid == 'myprof_closebtn' and close_btn: 
        pass 
    else: 
        raise PreventUpdate
    return [openmodal, feedbackmessage, inputsopenalert, okay_href]