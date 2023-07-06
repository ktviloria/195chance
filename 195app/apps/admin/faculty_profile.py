#for adding faculty and editing/deleting faculty profile
#only admin users have access to this page
#if editing, profile details of current faculty user being edited is shown
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
from dash.dash import no_update
import re

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
                dcc.Store(id='facprof_toload', storage_type='memory', data=0), 
                dcc.Store(id = "onlyonce", storage_type='memory', data=1)
            ] 
        ), 
        html.H2("Profile Details"), 
        html.H6("* Indicates required field", style={"color": "#d9534f", "font-style": "italic"}),
        html.Hr(), 
        dbc.Alert('Please supply required fields.', color="danger", id='facprof_inputs_alert', is_open=False),
        dbc.Alert('Please supply required details.', color="danger", id='facprof_alert', 
                  is_open=False),
        
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
                                        type="text", id="facprof_ln", placeholder="Enter last name of faculty member" 
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
                                        type="text", id="facprof_fn", placeholder="Enter first name of faculty member" 
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
                                        type="text", id="facprof_mn", placeholder="Enter middle name of faculty member" 
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
                                        type="text", id="facprof_suff", placeholder="Enter suffix of faculty member" 
                                    ), 
                                ), 
                            ], 
                            className="mb-3", 
                        ), 
                        dbc.Row( 
                            [ 
                                dbc.Col(
                                    [
                                    dbc.Label("Rank"),
                                    dbc.Label("*", style={"color": "#d9534f", "font-style": "bold"}),
                                    ], 
                                    width=2
                                ), 
                                dbc.Col( 
                                    html.Div( 
                                        dcc.Dropdown( 
                                            id='facprof_rank', 
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
                                        type="date", id="facprof_bdate", placeholder="Enter birthdate" 
                                    ), 
                                ), 
                            ], 
                            className="mb-3", 
                        ), 
                        dbc.Row( 
                            [ 
                                dbc.Col([
                                    dbc.Label("UP Email"), 
                                    dbc.Label("*", style={"color": "#d9534f", "font-style": "bold"}),
                                ],width=2), 
                                dbc.Col( 
                                    dbc.Input( 
                                        type="text", id="facprof_mail", placeholder="Enter email" 
                                    ), 
                                ), 
                            ], 
                            className="mb-3", 
                        ), 
                        dbc.Row( 
                            [ 
                                dbc.Label("Contact number", width=2), 
                                dbc.Col( 
                                    dbc.Input( 
                                        type="text", id="facprof_contact", placeholder="Enter contact number" 
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
                                dbc.Label("Employee Number", width=2), 
                                dbc.Col( 
                                    dbc.Input( 
                                        type="text", id="facprof_emp_num", placeholder="Enter employee number" 
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
                                            type="text", id="facprof_expert1", placeholder="Enter area of expertise" 
                                        ), 
                                    ), 
                                ], 
                                className="mb-3", 
                            ), id = 'expertise1_div'
                        ),
                        html.Div(
                            dbc.Row( 
                            [ 
                                dbc.Label("Expertise 2", width=2), 
                                dbc.Col( 
                                    dbc.Input( 
                                        type="text", id="facprof_expert2", placeholder="Enter area of expertise"
                                    ), 
                                ), 
                            ], 
                            className="mb-3", 
                            ), id = 'expertise2_div'
                        ),
                        html.Div(
                            dbc.Row( 
                                [ 
                                    dbc.Label("Expertise 3", width=2), 
                                    dbc.Col( 
                                        dbc.Input( 
                                            type="text", id="facprof_expert3", placeholder="Enter area of expertise"
                                        ), 
                                    ), 
                                ], 
                                className="mb-3", 
                            ), id = 'expertise3_div'
                        ),
                        html.Div(
                            dbc.Row( 
                                [ 
                                    dbc.Label("Expertise 4", width=2), 
                                    dbc.Col( 
                                        dbc.Input( 
                                            type="text", id="facprof_expert4", placeholder="Enter area of expertise" 
                                        ), 
                                    ), 
                                ], 
                                className="mb-3", 
                            ), id = 'expertise4_div'
                        ), 
                        html.Div(
                            dbc.Row( 
                                [ 
                                    dbc.Label("Expertise 5", width=2), 
                                    dbc.Col( 
                                        dbc.Input( 
                                            type="text", id="facprof_expert5", placeholder="Enter area of expertise" 
                                        ), 
                                    ), 
                                ], 
                                className="mb-3", 
                            ), id = 'expertise5_div'
                        ), 
                        html.Div(
                            dbc.Row( 
                        [ 
                                dbc.Label("Affiliation Status", id = 'facprof_affiliation_label', width=2),  
                                dbc.Col( 
                                    html.Div( 
                                        dcc.Dropdown( 
                                            id='facprof_affiliation', 
                                            options = [{'label':'Active', 'value':True}, {'label':'Inactive', 'value':False} ]
                                        ),
                                        className="dash-bootstrap" 
                                    ), 
                                ), 
                            ], 
                            className="mb-3", 
                        ), id = 'facprof_affiliation'
                        ),
                        html.Div( 
                            dbc.Row( 
                                [ 
                                    dbc.Label("Wish to delete?", width=2), 
                                    dbc.Col( 
                                        dbc.Checklist( 
                                            id='facprof_removerecord', 
                                            options=[ 
                                                { 
                                                    'label': "Mark for Deletion", 'value': 1 
                                                } 
                                            ], 
                                            style={'fontWeight':'bold'}, 
                                        ), 
                                    ), 
                                ], 
                                className="mb-3", 
                            ), 
                            id = 'facprof_removerecord_div' 
                        ), 
                    ],
                    width=6
                )
            ]
        ),
        html.Hr(), 
        dbc.Button('Submit', color='danger', id='facprof_submitbtn'), 
        dbc.Modal( 
            [    
                dbc.ModalHeader(dbc.ModalTitle("Saving Progress"), style=mod_style), 
                dbc.ModalBody([
                    html.Div("upper temp message", id = 'facprof_feedback_message_line1'), 
                    html.Div("middle temp message", id = 'facprof_feedback_message_line2'),
                    html.Div("lowe temp message", id = 'facprof_feedback_message_line3'),  
                    ], id='facprof_feedback_message'), 
                dbc.ModalFooter( 
                    dbc.Button("Okay", id="facprof_closebtn", color='secondary', className="ms-auto", n_clicks=0) 
                ),           
            ], 
            centered=True, 
            id="facprof_modal", 
            is_open=False, 
        ), 
    ] 
) 

@app.callback ( 
    [
        Output('facprof_toload', 'data'), 
        Output('facprof_removerecord_div', 'style'), 
        Output('facprof_rank', 'options'),
        Output('facprof_affiliation', 'style'),
        Output('facprof_affiliation_label', 'style') 
    ],
    [ 
        Input('url', 'pathname'),
    ], 
    [ 
        State('url', 'search')
        
    ] 
)
def facprof_load_dropdown(pathname, search): 
    if pathname == '/faculty_profile': 
        sql_rank = """ SELECT DISTINCT(rank_title) as label, rank_id as value 
            FROM ranks
            WHERE not ranks_delete_ind
            ORDER BY value ASC
            
        """ 
        values_rank = [] 
        cols_rank = ['label','value'] 
        rank = db.querydatafromdatabase(sql_rank, values_rank, cols_rank) 
        rank_opts = rank.to_dict('records') 
        
        parsed = urlparse(search)
        mode = parse_qs(parsed.query)['mode'][0]
        to_load = 1 if mode == 'edit' else 0 
        removerecord_div = None if to_load else {'display': 'none'}
        style_aff = None if to_load else {'display': 'none'} 

    else: 
         raise PreventUpdate 
    return [to_load, removerecord_div, rank_opts, style_aff, style_aff]



@app.callback(
    [
        Output('expertise2_div', 'style'), 
        Output('expertise3_div', 'style'), 
        Output('expertise4_div', 'style'), 
        Output('expertise5_div', 'style')
    ], 
    [
        Input('url', 'pathname'), 
        Input('facprof_toload', 'modified_timestamp'), 
        Input('facprof_expert1', 'value'),
        Input('facprof_expert2', 'value'), 
        Input('facprof_expert3', 'value'), 
        Input('facprof_expert4', 'value')
        
    ]
)

def expertisedivs (pathname, timestamp, expert1, expert2, expert3, expert4): 
    
    
    if pathname == '/faculty_profile':
        
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
            

@app.callback (
    [
        # Output('facprof_id', 'value'),
        # Output('facprof_un', 'value'),
        Output('facprof_ln', 'value'),
        Output('facprof_fn', 'value'),
        Output('facprof_mn', 'value'), 
        Output('facprof_suff', 'value'),
        Output('facprof_rank', 'value'), 
        Output('facprof_bdate', 'date'), 
        Output('facprof_mail', 'value'), 
        Output('facprof_contact', 'value'), 
        Output('facprof_emp_num', 'value'), 
        Output('facprof_expert1', 'value'), 
        Output('facprof_expert2', 'value'),
        Output('facprof_expert3', 'value'),
        Output('facprof_expert4', 'value'),
        Output('facprof_expert5', 'value'),
        Output('facprof_affiliation', 'value'), 
        Output('onlyonce', 'data')      
    ], 
    [
        Input('facprof_toload', 'modified_timestamp')
    ], 
    [
        State('facprof_toload','data' ), 
        State('url', 'search'), 
        State('onlyonce', 'data')
    ]
)

def facprof_load (timestamp, to_load, search, onlyonce):
    if onlyonce == 1:     
        if to_load == 1: 
            facprof_sql = """ SELECT 
                faculty.user_id,
                users.user_un,
                faculty_ln, 
                faculty_fn,
                faculty_mn,
                faculty_suff, 
                ranks.rank_id,
                faculty_bdate,
                faculty_mail,
                faculty_contact,
                faculty_emp_num,
                faculty_expert1,
                faculty_expert2,
                faculty_expert3,
                faculty_expert4,
                faculty_expert5, 
                faculty_active_ind
                
                FROM faculty
                    INNER JOIN ranks ON faculty.rank_id = ranks.rank_id
                    INNER JOIN users on faculty.user_id = users.user_id
                WHERE
                    faculty_delete_ind = false
                ORDER BY
                    faculty.user_id ASC
            """
            
            parsed = urlparse(search)
            facprofid = parse_qs(parsed.query)['id'][0]
            
            facprof_val = []
            facprof_colname = ['facprof_id', 'facprof_un','facprof_ln', 'facprof_fn', 'facprof_mn', 'facprof_suff', 
                    'facprof_rank', 'facprof_bday', 'facprof_mail', 'facprof_contact', 'facprof_emp_num', 
                    'facprof_exp1', 'facprof_exp2', 'facprof_exp3', 'facprof_exp4', 'facprof_exp5', 'status']
            facprof_df = db.querydatafromdatabase(facprof_sql, facprof_val, facprof_colname)
            
            counter = 0 
            for i in range(len(facprof_df)):
                if facprof_df['facprof_id'][i] != int(facprofid):
                    facprof_df  = facprof_df.drop(i)
                else: 
                    counted = counter 
                counter += 1
                    
            # facprof_id = facprof_df['facprof_id'][counted]
            # facprof_un = facprof_df['facprof_un'][counted]
            facprof_ln = facprof_df['facprof_ln'][counted]
            facprof_fn = facprof_df['facprof_fn'][counted]
            facprof_mn = facprof_df['facprof_mn'][counted]
            facprof_suff = facprof_df['facprof_suff'][counted]
            facprof_rank = facprof_df['facprof_rank'][counted]
            facprof_bday = facprof_df['facprof_bday'][counted]
            facprof_mail = facprof_df['facprof_mail'][counted]
            facprof_contact = facprof_df['facprof_contact'][counted]
            facprof_emp_num = facprof_df['facprof_emp_num'][counted]
            facprof_exp1 = facprof_df['facprof_exp1'][counted]
            facprof_exp2 = facprof_df['facprof_exp2'][counted]
            facprof_exp3 = facprof_df['facprof_exp3'][counted]
            facprof_exp4 = facprof_df['facprof_exp4'][counted]
            facprof_exp5 = facprof_df['facprof_exp5'][counted]
            facprof_aff = facprof_df['status'][counted]
        else:
            raise PreventUpdate
        onlyonce += 1
    else:
        raise PreventUpdate
    return [facprof_ln, facprof_fn, facprof_mn, facprof_suff, facprof_rank, facprof_bday, facprof_mail, facprof_contact, facprof_emp_num, facprof_exp1, facprof_exp2, facprof_exp3, facprof_exp4, facprof_exp5, facprof_aff, onlyonce]
        
@app.callback(
    [
        Output('facprof_modal', 'is_open'), 
        Output('facprof_feedback_message_line1', 'children'), 
        Output('facprof_feedback_message_line2', 'children'), 
        Output('facprof_feedback_message_line3', 'children'),
        Output('facprof_inputs_alert', 'is_open'), 
        Output('facprof_closebtn', 'href')
    ], 
    [
        Input('facprof_submitbtn', 'n_clicks'), 
        Input('facprof_closebtn', 'n_clicks')
    ],
    [
        State('facprof_ln', 'value'), 
        State('facprof_fn', 'value'),
        State('facprof_mn', 'value'),
        State('facprof_suff', 'value'),
        State('facprof_rank', 'value'),
        State('facprof_bdate', 'value'),
        State('facprof_mail', 'value'),
        State('facprof_contact', 'value'),
        State('facprof_emp_num', 'value'),
        State('facprof_expert1', 'value'),
        State('facprof_expert2', 'value'),
        State('facprof_expert3', 'value'),
        State('facprof_expert4', 'value'),
        State('facprof_expert5', 'value'),
        State('url', 'search'), 
        State('facprof_removerecord', 'value'), 
        State('expertise2_div', 'style'),
        State('expertise3_div', 'style'),
        State('expertise4_div', 'style'), 
        State('expertise5_div', 'style'), 
        State('facprof_affiliation', 'value'),
        State('currentuserid', 'data'),
    ]
)

def facprof_submitprocess (submit_btn, close_btn, lastname, firstname, middlename, 
                           suffix, rank, bdate, mail, contact, emp_num, expert1,
                           expert2, expert3, expert4, expert5, search, facremoverecord, 
                           expertdiv_2, expertdiv_3, expertdiv_4, expertdiv_5, status, cuser_id): 
    ctx = dash.callback_context
    if ctx.triggered: 
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]
        openmodal = False 
        feedbackmessage1  = ' '
        feedbackmessage2 = ' '
        feedbackmessage3 = ' '
        inputsopenalert = False
        okay_href = None 
    else: 
        raise PreventUpdate
    
    # if eventid == 'facprof_changepassbtn' and changepass_btn:
    #     sql = """SELECT
    #             user_id
    #         FROM users
    #         WHERE
    #             user_id=%s
    #         """
    #     values = [f"{editid}"]
    #     cols = ['userID']
    #     faculty = db.querydatafromdatabase(sql, values, cols)

    #     if faculty.shape[0]: 
    #         changepass_href=f"/edit_password?mode=edit&id={editid}"
        
    if eventid == 'facprof_submitbtn' and  submit_btn: 
        inputs = [
            lastname, 
            firstname, 
            # middlename, 
            # suffix, 
            rank, 
            # bdate, 
            mail, 
            # contact, 
            # emp_num, 
            # expert1,
            # expert2, 
            # expert3, 
            # expert4, 
            # expert5
        ]
    
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

        if not all(inputs): 
            inputsopenalert = True
            # feedbackmessage1 = "Please supply all information needed"
            # feedbackmessage2 = " "
            # feedbackmessage3 = " "
        else: 
            openmodal = True 
            parsed = urlparse(search)
            mode = parse_qs(parsed.query)['mode'][0]
            
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
                if int(username['id'][i]) == cuser_id:
                    username_modifier = username['un'][i]

            if mode == "add": 
                users_sqlcode_add = """INSERT INTO users(
                    user_id, 
                    user_un,
                    user_pass,
                    user_type
                )
                VALUES (%s, %s, %s, %s)            
                """
                
                sql_max = """SELECT MAX(user_id) from users
                """
                sql_max_val = []
                max_colname = ['max']
                user_max_value_db =  db.querydatafromdatabase(sql_max, sql_max_val,max_colname )
                user_max_value = int(user_max_value_db['max'][0]) + 1 

                usernamee = mail.partition('@')[0]

                encrypt_string = lambda string: hashlib.sha256(string.encode('utf-8')).hexdigest()
                encrypted_pass = encrypt_string('pass')
                
                user_values = [user_max_value,usernamee, encrypted_pass, 'faculty']
                db.modifydatabase(users_sqlcode_add,user_values)

                author_sqlcode_add = """INSERT INTO authors(
                    author_user_id,
                    author_ln,
                    author_fn,
                    author_mail,
                    author_contact,
                    author_up_constituent,
                    author_upd_unit,
                    author_engg_dept,
                    author_fac_ind,
                    author_last_upd
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)            
                """
                
                # author_sql_max = """SELECT MAX(author_id) from authors
                # """
                # author_sql_max_val = []
                # author_max_colname = ['max']
                # author_max_value_db =  db.querydatafromdatabase(author_sql_max, author_sql_max_val, author_max_colname )
                # author_max_value = int(author_max_value_db['max'][0]) + 1 

                author_values = [user_max_value, lastname, firstname, mail, contact, 'UP Diliman', 'College of Engineering' , 'Departmeng of Industrial Engineering and Operations Research', 'IE Faculty', fac_timestamp_time]
                db.modifydatabase(author_sqlcode_add, author_values)
            
                sql = """INSERT INTO faculty(
                    user_id,
                    faculty_ln, 
                    faculty_fn, 
                    faculty_mn, 
                    faculty_suff, 
                    rank_id, 
                    faculty_bdate, 
                    faculty_mail, 
                    faculty_contact, 
                    faculty_emp_num, 
                    faculty_expert1,
                    faculty_expert2,
                    faculty_expert3,
                    faculty_expert4,
                    faculty_expert5, 
                    faculty_active_ind, 
                    faculty_delete_ind, 
                    faculty_last_upd,
                    faculty_modified_by
                )
                VALUES (%s, %s, %s, %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s, %s, %s)
                """
                if expertdiv_2 == {'display':'none'}: 
                    expert2 = None
                if expertdiv_3 == {'display':'none'}: 
                    expert3 = None
                if expertdiv_4 == {'display':'none'}: 
                    expert4 = None
                if expertdiv_5 == {'display':'none'}: 
                    expert5 = None

                values =[user_max_value, lastname, firstname, middlename, 
                            suffix, rank, bdate, mail, contact, emp_num, expert1,
                            expert2, expert3, expert4, expert5, True, False, fac_timestamp_time, username_modifier]
                db.modifydatabase(sql,values)
                feedbackmessage1 = f"Faculty added to DelPHI."
                feedbackmessage2 = f"Username: %s" %usernamee
                feedbackmessage3 = f"Password: pass" 
                okay_href = '/faculty_manage'
            
            elif mode == 'edit': 
                parsed = urlparse(search)
                facprof_editmodeid = parse_qs(parsed.query)['id'][0]
                sql = """UPDATE faculty
                SET 
                    faculty_ln = %s, 
                    faculty_fn = %s, 
                    faculty_mn = %s, 
                    faculty_suff = %s, 
                    rank_id = %s, 
                    faculty_bdate = %s, 
                    faculty_mail = %s, 
                    faculty_contact = %s, 
                    faculty_emp_num = %s, 
                    faculty_expert1 = %s,
                    faculty_expert2 = %s,
                    faculty_expert3 = %s,
                    faculty_expert4 = %s,
                    faculty_expert5 = %s, 
                    faculty_delete_ind =%s, 
                    faculty_active_ind = %s,
                    faculty_last_upd = %s,
                    faculty_modified_by = %s
                WHERE 
                    user_id = %s
                """
                to_delete = bool(facremoverecord)
                if to_delete == True: 
                    status = False
                    iefac_to_delete = True
                    iefacind = ''
                if to_delete == False:
                    if status == False:
                        iefacind = 'Inactive IE Faculty'
                    if status == True:
                        iefacind = 'IE Faculty'
                values = [lastname, firstname, middlename, 
                            suffix, rank, bdate, mail, contact, emp_num, expert1,
                            expert2, expert3, expert4, expert5, to_delete, status, fac_timestamp_time, username_modifier, facprof_editmodeid]
                db.modifydatabase(sql, values)

                sql = """UPDATE authors
                SET 
                    author_ln = %s, 
                    author_fn = %s, 
                    author_mail = %s, 
                    author_contact = %s, 
                    author_fac_ind = %s,
                    author_last_upd = %s,
                    author_delete_ind = %s
                WHERE 
                    author_user_id = %s
                """
                iefac_to_delete = bool(facremoverecord)
                values = [lastname, firstname, mail, contact, iefacind, fac_timestamp_time, iefac_to_delete, facprof_editmodeid]
                db.modifydatabase(sql, values)

                feedbackmessage1 = "Faculty information updated."
                feedbackmessage2 = " "
                feedbackmessage3 = " "
                okay_href = '/faculty_manage'
            else: 
                raise PreventUpdate
    elif eventid == 'facprof_closebtn' and close_btn: 
        pass 
    else: 
        raise PreventUpdate
    return [openmodal, feedbackmessage1, feedbackmessage2, feedbackmessage3, inputsopenalert, okay_href]
