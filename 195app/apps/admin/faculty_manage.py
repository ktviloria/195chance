#for viewing all faculty members wiht buttons leading to editing and adding
#only admin users have access to this page
#profile details of all faculty members are shown

from dash import dcc
from dash import html
from dash import dash_table
import dash_bootstrap_components as dbc
import dash
from dash.exceptions import PreventUpdate
from dash.dependencies import Input, Output, State
import pandas as pd
from datetime import date
 
from app import app
from apps import dbconnect as db
 
from urllib.parse import urlparse, parse_qs

layout= html.Div( 
    [ 
        dbc.Card(
            [
                dbc.CardHeader(html.H2("Admin Management")),
                dbc.CardBody(
                    [
                        # dbc.Button('Add Faculty', color='danger', href='/faculty_profile?mode=add'),
                        # html.Hr(),
                        html.Div(id='adminlist')
                    ]
                ),
            ]
        ),
        html.Br(),
        dbc.Card(
            [
                dbc.CardHeader(html.H2("Faculty Member Management")),
                dbc.CardBody(
                    [
                        dbc.Button('Add Faculty', color='danger', href='/faculty_profile?mode=add'),
                        html.Hr(),
                        html.Div(
                            [
                                html.H4("Find Faculty Member", style={'fontWeight': 'bold'}),
                                dbc.Row(
                                    [
                                        dbc.Label(
                                            html.Div([
                                                html.Img(src=app.get_asset_url('search.png'), height="20px", width="18px", style={'position':'left','vertical-align':'middle'}),
                                                html.Span("Search", style={'vertical-align': 'right', 'padding-left':'5px', 'font-size':'20px'}),
                                            ]),
                                            width=1),
                                        dbc.Col(
                                            dbc.Input(
                                                type="text", id="faculty_filter", placeholder="Enter faculty name, rank, email, or employee number"
                                            ),
                                            width=6),
                                        #active inactive dropdown
                                        dbc.Col(
                                            dcc.Dropdown(
                                                options=[
                                                {'label': 'Active', 'value': True},
                                                {'label': 'Inactive', 'value': False},
                                                ],
                                                id='status_dropdown', clearable=True, placeholder="Status"), width = 2,
                                        ),
                                    ],
                                    className="mb-3",
                                ),
                                html.Div(
                                    id='facultylist'
                                )
                            ]
                        )
                    ]
                ),
            ]
        )
    ]
)

@app.callback(
    [
        Output('adminlist', 'children')
    ],
    [
        Input('url', 'pathname'),
    ]
)
def facultymanage_loadadminlist(pathname):
    if pathname == '/faculty_manage':
        sql = """SELECT
                user_id,
                user_un
            FROM users
            WHERE
                user_id<4
            ORDER BY 
                user_id 
            """
        values = []
        cols = ['userID', 'Admin Username'] 
        admin = db.querydatafromdatabase(sql, values, cols)

        if admin.shape[0]: 
            password_buttons = [] 
            username_buttons = []
            modify_buttons = []
            
            for idnumber in admin['userID']: 
                # username_buttons += [ 
                #     html.Div( 
                #         dbc.Button('Change Username', href=f"/edit_username?mode=edit&id={idnumber}", size='sm', color='secondary', ), 
                #         style={'text-align': 'left'} 
                #     ) 
                # ] 
                # password_buttons += [ 
                #     html.Div( 
                #         dbc.Button('Change Password', href=f"/edit_password?mode=edit&id={idnumber}", size='sm', color='secondary', ), 
                #         style={'text-align': 'left'} 
                #     ) 
                # ] 
                
                modify_buttons += [ 
                    dbc.DropdownMenu(
                        children=[
                            dbc.DropdownMenuItem("Edit Username", href=f"/edit_username?mode=edit&id={idnumber}"),
                            dbc.DropdownMenuItem("Edit Password", href=f"/edit_password?mode=edit&id={idnumber}")
                        ],
                        label='Modify Credentials', color='secondary'),
                ]
                
                
            # admin['Change Username'] = username_buttons 
            
            # admin['Change Password'] = password_buttons 
            admin['Modify Credentials'] = modify_buttons 
                
        admin.drop(['userID'],axis=1,inplace=True) 
        table = dbc.Table.from_dataframe(admin, striped=True, bordered=True, hover=True, size='sm') 
        return [table] 
    else: 
        return ["No records to display."]     


@app.callback(
    [
        Output('facultylist', 'children')
    ],
    [
        Input('url', 'pathname'),
        Input('faculty_filter', 'value'),
        Input('status_dropdown', 'value')
    ]
)
def facultymanage_loadfacultylist(pathname, searchterm, statusfilter):
    if pathname == '/faculty_manage':
        sql = """SELECT
                faculty.user_id,
                faculty_ln || ', ' || faculty_fn AS faculty_full_name,
                rank_title,
                faculty_mail,
                faculty_emp_num, 
                faculty_active_ind, 
                to_char(faculty_last_upd::timestamp, 'Month DD YYYY HH24:MI:SS'),
                faculty_modified_by
            FROM faculty
                INNER JOIN ranks ON faculty.rank_id = ranks.rank_id
                FULL OUTER JOIN users on faculty.user_id = users.user_id
            WHERE
                faculty_delete_ind = false
            """
        values = []
        cols = ['userID', 'Full Name', 'Rank','Email', 'Employee Number', 'Affiliation Status', 'Last Updated', 'Last Modified By' ] 


        if statusfilter == True:
            sql += """ AND faculty_active_ind = true """ 
            if searchterm:
                sql += """ AND (((faculty_fn || ' ' || faculty_ln) ILIKE %s) OR (rank_title ILIKE %s) OR (faculty_mail ILIKE %s) OR (faculty_emp_num ILIKE %s)
                    OR (faculty_expert1 ILIKE %s) OR (faculty_expert2 ILIKE %s) OR (faculty_expert3 ILIKE %s) OR (faculty_expert4 ILIKE %s) OR (faculty_expert5 ILIKE %s))"""
                values += [f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", 
                        f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%"]

        elif statusfilter == False: 
            sql += """ AND faculty_active_ind = false """ 
            if searchterm:
                sql += """ AND (((faculty_fn || ' ' || faculty_ln) ILIKE %s) OR (rank_title ILIKE %s) OR (faculty_mail ILIKE %s) OR (faculty_emp_num ILIKE %s)
                    OR (faculty_expert1 ILIKE %s) OR (faculty_expert2 ILIKE %s) OR (faculty_expert3 ILIKE %s) OR (faculty_expert4 ILIKE %s) OR (faculty_expert5 ILIKE %s))"""
                values += [f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", 
                        f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%"]
        elif searchterm:
            sql += """ AND (((faculty_fn || ' ' || faculty_ln) ILIKE %s) OR (rank_title ILIKE %s) OR (faculty_mail ILIKE %s) OR (faculty_emp_num ILIKE %s)
                OR (faculty_expert1 ILIKE %s) OR (faculty_expert2 ILIKE %s) OR (faculty_expert3 ILIKE %s) OR (faculty_expert4 ILIKE %s) OR (faculty_expert5 ILIKE %s))"""
            values += [f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", 
                    f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%"]
            if statusfilter == True:
                sql += """ AND faculty_active_ind = true """   
            elif statusfilter == False: 
                sql += """ AND faculty_active_ind = false """ 
             


        # if searchterm:
        #     sql += """ AND ((faculty_fn || ' ' || faculty_ln) ILIKE %s) OR (rank_title ILIKE %s) OR (faculty_mail ILIKE %s) OR (faculty_emp_num ILIKE %s)
        #         OR (faculty_expert1 ILIKE %s) OR (faculty_expert2 ILIKE %s) OR (faculty_expert3 ILIKE %s) OR (faculty_expert4 ILIKE %s) OR (faculty_expert5 ILIKE %s)"""
        #     values += [f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", 
        #             f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%"]

        # elif searchterm:
        #     sql += """ AND (((faculty_fn || ' ' || faculty_ln) ILIKE %s) OR (rank_title ILIKE %s) OR (faculty_mail ILIKE %s) OR (faculty_emp_num ILIKE %s)
        #         OR (faculty_expert1 ILIKE %s) OR (faculty_expert2 ILIKE %s) OR (faculty_expert3 ILIKE %s) OR (faculty_expert4 ILIKE %s) OR (faculty_expert5 ILIKE %s))"""
        #     values += [f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", 
        #             f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%"]
        #     if statusfilter == True:
        #         sql += """ AND faculty_active_ind = true """ 
        #     if statusfilter == False:
        #         sql += """ AND faculty_active_ind = false """ 

        # elif statusfilter == True:
        #     if searchterm:
        #         sql += """ AND (((faculty_fn || ' ' || faculty_ln) ILIKE %s) OR (rank_title ILIKE %s) OR (faculty_mail ILIKE %s) OR (faculty_emp_num ILIKE %s)
        #             OR (faculty_expert1 ILIKE %s) OR (faculty_expert2 ILIKE %s) OR (faculty_expert3 ILIKE %s) OR (faculty_expert4 ILIKE %s) OR (faculty_expert5 ILIKE %s))"""
        #         values += [f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", 
        #                 f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%"]
        #         sql += """ AND faculty_active_ind = true """ 
        #     else:
        #         sql += """"""
        #         values += []

        # elif statusfilter == False:
             
        #     if searchterm:
        #         sql += """ AND (((faculty_fn || ' ' || faculty_ln) ILIKE %s) OR (rank_title ILIKE %s) OR (faculty_mail ILIKE %s) OR (faculty_emp_num ILIKE %s)
        #             OR (faculty_expert1 ILIKE %s) OR (faculty_expert2 ILIKE %s) OR (faculty_expert3 ILIKE %s) OR (faculty_expert4 ILIKE %s) OR (faculty_expert5 ILIKE %s))"""
        #         values += [f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", 
        #                 f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%"]
        #         sql += """ AND faculty_active_ind = false """
            
        #     else:
        #         sql += """"""
        #         values += []               


        sql += """ORDER BY faculty.faculty_ln ASC"""
        faculty = db.querydatafromdatabase(sql, values, cols)

        if faculty.shape[0]: 
            # buttons = [] 
            modify_buttons = []
            for idnumber in faculty['userID']: 
                # buttons += [ 
                #     html.Div( 
                #         dbc.Button('Edit/Delete', href=f"/faculty_profile?mode=edit&id={idnumber}", size='sm', color='secondary', ), 
                #         style={'text-align': 'center'} 
                #     ) 
                # ] 
                
                modify_buttons += [ 
                    dbc.DropdownMenu(
                        children=[
                            dbc.DropdownMenuItem("Edit Profile", href=f"/faculty_profile?mode=edit&id={idnumber}"), 
                            dbc.DropdownMenuItem("Edit Username", href=f"/edit_username?mode=edit&id={idnumber}"),
                            dbc.DropdownMenuItem("Edit Password", href=f"/edit_password?mode=edit&id={idnumber}")
                        ],
                        label='Modify', color='secondary', style={'text-align': 'center'}),
                ]
                
                
            faculty['Modify'] = modify_buttons
            # faculty['Action'] = buttons 
            
            for i in range(len(faculty['Affiliation Status'])): 
                if faculty['Affiliation Status'][i] == True: 
                    faculty['Affiliation Status'][i] = 'Active'
                else: 
                    faculty['Affiliation Status'][i] = 'Inactive'
                
        faculty.drop(['userID'],axis=1,inplace=True) 
        table = dbc.Table.from_dataframe(faculty, striped=True, bordered=True, hover=True, size='sm') 
        return [table] 

    else: 
        return ["No records to display."]        

