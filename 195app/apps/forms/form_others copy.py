#for adding and editing/deleting publications
#only admin users have access to this page
#if editing, profile details of current faculty user being edited is shown

from dash import dcc
from dash import html
from dash import dash_table
import dash_bootstrap_components as dbc
import dash
from dash.exceptions import PreventUpdate
from dash.dependencies import Input, Output, State
import pandas as pd
import datetime as dt
from datetime import date, datetime
 
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
                dcc.Store(id='form_o_toload', storage_type='memory', data=0), 
            ] 
        ), 
        html.H2("Publication Details"), 
        html.H6("* Indicates required field", style={"color": "#d9534f", "font-style": "italic"}),
        html.Hr(), 
        # General pub info needed
        html.Div(
            [
                #Faculty involved
                dbc.Row( 
                    [ 
                        dbc.Col(
                            [
                            dbc.Label("Faculty Involved"),
                            dbc.Label("*", style={"color": "#d9534f", "font-style": "bold"})
                            ], width=2, style={'display': 'flex', 'align-items': 'center'}
                            ),
                        dbc.Col( 
                            html.Div( 
                                dcc.Dropdown( 
                                    id='form_o_fac', 
                                ),
                                className="dash-bootstrap" 
                            ), 
                            width=6,
                        ), 
                    ], 
                    className="mb-3", 
                ), 
                #Publication tag
                dbc.Row( 
                    [ 
                        dbc.Col(
                            [
                            dbc.Label("Publication Criteria"),
                            dbc.Label("*", style={"color": "#d9534f", "font-style": "bold"})
                            ], width=2, style={'display': 'flex', 'align-items': 'center'}
                            ),
                        dbc.Col( 
                            html.Div( 
                                dcc.Dropdown( 
                                    id='form_o_tag', 
                                ),
                                className="dash-bootstrap" 
                            ), 
                            width=6, 
                        ), 
                    ], 
                    className="mb-3", 
                ), 
                #Publication Title
                dbc.Row( 
                    [ 
                        dbc.Col(
                            [
                            dbc.Label("Publication Title"),
                            dbc.Label("*", style={"color": "#d9534f", "font-style": "bold"})
                            ], width=2, style={'display': 'flex', 'align-items': 'center'}
                            ), 
                        dbc.Col( 
                            dbc.Input( 
                                type="text", id="form_o_title", placeholder="Enter publication title" 
                            ), 
                            width=6, 
                        ), 
                    ], 
                    className="mb-3", 
                ), 
            ],
            id='form_o_gen'
        ),
        
        # others
        html.Div(
            [
                #date
                # dbc.Row( 
                #     [ 
                #         dbc.Label("Date", width=2), 
                #         dbc.Col( 
                #             dbc.Input( 
                #                 type="text", id="form_o_date", placeholder="Enter date of publication YYYY or MM/DD/YYYY" 
                #             ), 
                #             width=6,
                #         ), 
                #     ], 
                #     className="mb-3", 
                # ),
                dbc.Row( 
                    [ 
                        dbc.Col(
                            [
                            dbc.Label("Publication Date"),
                            dbc.Label("*", style={"color": "#d9534f", "font-style": "bold"})
                            ], width=2, style={'display': 'flex', 'align-items': 'center'}
                            ), 
                        dbc.Col( 
                            dcc.DatePickerSingle(
                                id='form_o_date',
                                placeholder="MM/DD/YYYY",
                                display_format="MM/DD/YYYY",
                                min_date_allowed=date(2014, 1, 1),
                                max_date_allowed=date.today(),
                                initial_visible_month=date.today(),
                                #note: I couldn't adjust the width of the box to fit the placeholder
                            ), className="DateInput_input_1"
                                #html.Div(id='output-container-date-picker-range')
                                #type="text", id="form_o_presdate", placeholder="Enter date(s) of presentation YYYY or MM/DD/YYYY" 
                        ), 
                    ], 
                    className="mb-3", 
                ),
                #others add info
                dbc.Row( 
                    [ 
                        dbc.Label("Additional Information", width=2, style={'display': 'flex', 'align-items': 'center'}), 
                        dbc.Col( 
                            dbc.Input( 
                                type="text", id="form_o_addinfo", placeholder="Enter any additional information" 
                            ), 
                            width=6,
                        ), 
                    ], 
                    className="mb-3", 
                )
            ],
            id='form_o'
        ),
        html.Div( 
            dbc.Row( 
                [ 
                    dbc.Label("Wish to delete?", width=2), 
                    dbc.Col( 
                        dbc.Checklist( 
                            id='form_o_removerecord', 
                            options=[ 
                                { 
                                    'label': "Mark for Deletion", 'value': 1 
                                } 
                            ], 
                            style={'fontWeight':'bold'}, 
                        ), 
                        width=6, 
                    ), 
                ], 
                className="mb-3", 
            ), 
            id = 'form_o_removerecord_div' 
        ), 
        html.Hr(), 
        dbc.Button('Submit', color='danger', id='form_o_submitbtn'), 
        dbc.Modal( 
            [    
                dbc.ModalHeader("Saving Progress"), 
                dbc.ModalBody("tempmessage", id='form_o_feedback_message'), 
                dbc.ModalFooter( 
                    dbc.Button("Okay", id="form_o_closebtn", className="ms-auto", n_clicks=0) 
                ),           
            ], 
            centered=True, 
            id="form_o_modal", 
            is_open=False, 
        ),  
    ] 
) 

@app.callback (
    [
        Output('form_o_toload', 'data'), 
        Output('form_o_removerecord_div', 'style'),
        Output ('form_o_fac', 'options'), 
        Output ('form_o_tag', 'options')
    ], 
    [
        Input('url', 'pathname'), 
    ], 
    [
        State('url', 'search'),
        State('currentuserid', 'data')
    ]
)

def form_a_load_dropdown(pathname, search, currentuserid): 
    if pathname == '/form_others': 
        sql_faculty_involved = """ SELECT DISTINCT (faculty.faculty_fn ||' '|| faculty.faculty_ln) as label, user_id as value
            from faculty
            ORDER BY value 
        """
        values_faculty = []
        cols_faculty = ['label', 'value']
        faculty_involved = db.querydatafromdatabase(sql_faculty_involved,values_faculty, cols_faculty)
        
        if currentuserid > 3:
            for i in range (len(faculty_involved)): 
                if faculty_involved['value'][i] != int (currentuserid): 
                    faculty_involved = faculty_involved.drop(i)
                else: 
                    pass
        
        faculty_opts = faculty_involved.to_dict('records')
        
        sql_tags = """SELECT DISTINCT (tag_title) AS label, tag_id AS value 
            from tags 
            WHERE tag_sub = 'O' and not tag_delete_ind 
            ORDER BY value
        """
        
        values_tag  = []
        cols_tag = ['label', 'value']
        tag_included = db.querydatafromdatabase(sql_tags, values_tag, cols_tag)
        tag_options = tag_included.to_dict('records')
        
        
        parsed = urlparse(search)
        mode = parse_qs(parsed.query)['mode'][0]
        to_load = 1 if mode == 'edit' else 0 
        removerecord_div = None if to_load else {'display': 'none'}
    else: 
         raise PreventUpdate 
    return(to_load, removerecord_div,faculty_opts,tag_options )


@app.callback(
    [
        Output('form_o_fac', 'value'),
        Output('form_o_tag', 'value'),
        Output('form_o_title', 'value'),
        Output('form_o_date', 'date'),
        Output('form_o_addinfo', 'value')
    
    ],
    [
        Input('form_o_toload', 'modified_timestamp')
    ],
    [
        State('form_o_toload', 'data'),
        State('url', 'search')
    ],
)

def form_o_load(timestamp,to_load, search): 
    if to_load == 1: 
        form_o_sql = """SELECT 
            publications.pub_id,
			publications.user_id,
			publications.tag_id,
            publications.pub_title, 
            others.o_date, 
            others.o_add_info   
        FROM publications 
            INNER JOIN faculty on publications.user_id = faculty.user_id 
            INNER JOIN others on publications.pub_id = others.pub_id 
        WHERE 
            publications.pub_delete_ind = false
		ORDER BY publications.pub_id
        """
        parsed = urlparse(search)
        form_o_id = parse_qs(parsed.query)['id'][0]
        
        form_o_val = []
        form_o_colname  = ['form_o_pub_id', 'form_o_user_id', 'form_o_tag_id', 
                           'form_o_pub_title', 'form_o_date', 'form_o_add_info']
        form_o_df = db.querydatafromdatabase(form_o_sql,form_o_val,form_o_colname)
        
        counter = 0 
        counted = 0
        for i in range(len(form_o_df)): 
            if form_o_df['form_o_pub_id'][i] != int(form_o_id): 
                form_o_df = form_o_df.drop(i)
            else: 
                counted = counter 
            counter += 1
        
        form_o_pub_id = form_o_df['form_o_pub_id'][counted]
        form_o_user_id = form_o_df['form_o_user_id'][counted]
        form_o_tag_id = form_o_df['form_o_tag_id'][counted]
        form_o_pub_title = form_o_df['form_o_pub_title'][counted]
        form_o_date = form_o_df['form_o_date'][counted]
        form_o_add_info = form_o_df['form_o_add_info'][counted]
        
    else: 
        raise PreventUpdate
    return [form_o_user_id, form_o_tag_id, form_o_pub_title, form_o_date, form_o_add_info]

@app.callback(
    [
        Output('form_o_modal', 'is_open'), 
        Output('form_o_feedback_message', 'children'), 
        Output('form_o_closebtn', 'href')
    ], 
    [
        Input('form_o_submitbtn', 'n_clicks'), 
        Input('form_o_closebtn', 'n_clicks')
    ], 
    [
        State('form_o_fac', 'value'),
        State('form_o_tag', 'value'),
        State('form_o_title', 'value'),
        State('form_o_date', 'date'),
        State('form_o_addinfo', 'value'), 
        State('url', 'search'), 
        State('form_o_removerecord', 'value'), 
        State('currentuserid', 'data')
    ]
)  

def form_o_submitprocess (submit_btn, close_btn, o_faculty, o_tag, o_title, o_date, o_addinfo, search, removerecord, cuser_id): 
    
    ctx = dash.callback_context
    if ctx.triggered: 
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]
        openmodal = False 
        feedbackmessage  = ' '
        okay_href = None 
    else: 
        raise PreventUpdate
    
    if eventid == 'form_o_submitbtn' and submit_btn: 
        openmodal = True 
        inputs = [ 
            o_faculty, 
            o_tag, 
            o_title, 
            o_date, 
            # o_addinfo,
        ]
        
        if not all(inputs): 
            feedbackmessage = "Please supply all needed information."
        else: 
            parsed = urlparse(search)
            mode = parse_qs(parsed.query)['mode'][0]
        
            o_sqlcode_modifiedby = """SELECT
            user_id,
            user_un
            FROM users
            """
            o_vals_modifiedby = []
            o_cols_modifiedby = ['id', 'un']
            o_username = db.querydatafromdatabase(o_sqlcode_modifiedby, o_vals_modifiedby, o_cols_modifiedby)
            
            o_username_modifier = ""
            for i in range(len(o_username['id'])):
                if int(o_username['id'][i]) == cuser_id:
                    o_username_modifier = o_username['un'][i]
            
            o_timestamp = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            o_timestamp_time = dt.datetime.strptime(o_timestamp,'%Y-%m-%d %H:%M:%S')

            if mode == "add": 
                sql_max_inquiry  = """SELECT MAX(pub_id) from publications
                """
                sql_max_val = []
                max_colname = ['max']
                pub_max_value_db = db.querydatafromdatabase (sql_max_inquiry, sql_max_val, max_colname)
                sql_pub_max = int(pub_max_value_db['max'][0]) + 1
            
                form_o_sqlcode_add_publications = """INSERT INTO publications(
                    pub_id, 
                    user_id, 
                    tag_id, 
                    pub_title, 
                    pub_delete_ind,
                    pub_last_upd,
                    modified_by
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                """
                
                form_o_values_addpub = [sql_pub_max, o_faculty, o_tag, o_title, False, o_timestamp_time, o_username_modifier]
                db.modifydatabase(form_o_sqlcode_add_publications, form_o_values_addpub)
                
                form_o_sqlcode_add_others = """INSERT INTO others(
                    pub_id, 
                    o_add_info, 
                    o_date, 
                    o_year
                )
                VALUES (%s, %s, %s, %s)
                """
                str_to_date = datetime.strptime(o_date, '%Y-%m-%d').date()
                o_year = str_to_date.year
                
                form_o_values_addothers = [sql_pub_max, o_addinfo, o_date, o_year]
                db.modifydatabase(form_o_sqlcode_add_others,form_o_values_addothers)
                
                feedbackmessage = 'Entry added to database.'
                if cuser_id <= 3: 
                    okay_href = '/publications_manage'
                else: 
                    okay_href = '/my_publications'
            
            elif mode == 'edit': 
                parsed = urlparse(search)
                form_o_editmodeid = parse_qs(parsed.query)['id'][0]
                
                sql_update_publications = """UPDATE publications
                SET 
                    user_id = %s, 
                    tag_id = %s, 
                    pub_title = %s, 
                    pub_delete_ind = %s,
                    pub_last_upd = %s,
                    modified_by = %s
                WHERE 
                    pub_id = %s
                """
                to_delete =  bool(removerecord)
                
                values_update_publications = [o_faculty, o_tag, o_title, to_delete, o_timestamp_time, o_username_modifier, form_o_editmodeid]
                db.modifydatabase(sql_update_publications, values_update_publications)

                sql_update_others = """UPDATE others
                SET
                    o_add_info = %s, 
                    o_date = %s, 
                    o_year = %s
                WHERE
                    pub_id = %s
                """
                
                str_to_date = datetime.strptime(o_date, '%Y-%m-%d').date()
                o_year = str_to_date.year
                
                values_update_others = [o_addinfo, o_date, o_year, form_o_editmodeid]
                db.modifydatabase(sql_update_others,values_update_others )
                feedbackmessage = 'Entry details updated.'
                if cuser_id <= 3: 
                    okay_href = '/publications_manage'
                else: 
                    okay_href = '/my_publications'
            
            else: 
                raise PreventUpdate
    elif eventid == 'form_o_closebtn' and close_btn: 
        pass
    else: 
        raise PreventUpdate
    return [openmodal, feedbackmessage, okay_href]
        
            
        
        