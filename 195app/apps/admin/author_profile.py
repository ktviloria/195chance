#for adding author and editing/deleting author profile
#only admin users have access to this page
#if editing a faculty member, profile details of current faculty user being edited is shown

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
                dcc.Store(id='authorprof_toload', storage_type='memory', data=0), 
            ] 
        ), 
        html.H2("Profile Details"), 
        html.H6("* Indicates required field", style={"color": "#d9534f", "font-style": "italic"}),
        html.Hr(), 
        dbc.Alert('Please supply required fields.', color="danger", id='authorprof_inputs_alert', is_open=False),
        dbc.Alert('Author being added is a faculty member. Please modify in the User Management Module.', color="danger", id='authorprof_facadd_alert', is_open=False),
        dbc.Alert('Author being modified is a faculty member. Please modify in the User Management Module.', color="danger", id='authorprof_facmodify_alert', is_open=False),
        html.Br(),
        dbc.Row(
            [
                dbc.Col(
                    [
                        # Last Name Input
                        dbc.Row( 
                            [ 
                                dbc.Col(
                                    [
                                        dbc.Label("Last Name",), 
                                        dbc.Label("*", style={"color": "#d9534f", "font-style": "bold"}),
                                    ],
                                    width=3
                                ),
                                dbc.Col( 
                                    dbc.Input( 
                                        type="text", id="authorprof_ln", placeholder="Enter last name of author" 
                                    ), 
                                ), 
                            ], 
                            className="mb-3", 
                        ), 
                        # First Name Input
                        dbc.Row( 
                            [ 
                                dbc.Col(
                                    [
                                        dbc.Label("First Name",), 
                                        dbc.Label("*", style={"color": "#d9534f", "font-style": "bold"}),
                                    ],
                                    width=3
                                ),
                                dbc.Col( 
                                    dbc.Input( 
                                        type="text", id="authorprof_fn", placeholder="Enter first name of author" 
                                    ), 
                                ), 
                            ], 
                            className="mb-3", 
                        ), 
                        # Email Input
                        dbc.Row( 
                            [ 
                                dbc.Col([
                                    dbc.Label("Email")                                ],
                                width=3), 
                                dbc.Col( 
                                    dbc.Input( 
                                        type="text", id="authorprof_mail", placeholder="Enter email" 
                                    ), 
                                ), 
                            ], 
                            className="mb-3", 
                        ), 
                        # Contact Number Input
                        dbc.Row( 
                            [ 
                                dbc.Label("Contact number", width=3), 
                                dbc.Col( 
                                    dbc.Input( 
                                        type="text", id="authorprof_contact", placeholder="Enter contact number" 
                                    ), 
                                ), 
                            ], 
                            className="mb-3", 
                        ),         
                        # UP Affiliation Dropdown
                        html.Div(
                            [ 
                                dbc.Row( 
                                    [ 
                                        dbc.Col(
                                            [
                                                dbc.Label("UP Affiliation", id = 'authorprof_up_aff_label'), 
                                                dbc.Label("*", style={"color": "#d9534f", "font-style": "bold"}),
                                            ],
                                            width=3
                                        ),  
                                        dbc.Col( 
                                            html.Div( 
                                                dcc.Dropdown( 
                                                    id='authorprof_up_aff_dropdown',clearable=True, searchable=True, placeholder="UP Affiliation"
                                                ),
                                                className="dash-bootstrap" 
                                            ), 
                                        ), 
                                    ], 
                                    className="mb-3", 
                                ),
                                html.Div(
                                    dbc.Row(
                                        [
                                             dbc.Col(
                                                [
                                                    dbc.Label("Specify Other Affiliation", id = 'authorprof_up_aff_others_label'), 
                                                    dbc.Label("*", style={"color": "#d9534f", "font-style": "bold"}),
                                                ],
                                                width=3
                                            ),  
                                            dbc.Col( 
                                                dbc.Input( 
                                                    type="text", id="authorprof_up_aff_others", placeholder="Please specify your affiliation." 
                                                ),
                                                width = 9
                                            ),
                                        ]
                                    ),
                                    id="authorprof_up_aff_others_div"
                                ),
                            ],
                                id = 'authorprof_up_aff_div'
                        ),
                        # UPD Unit Dropdown
                        html.Div(
                            dbc.Row( 
                                [ 
                                    dbc.Col(
                                        [
                                            dbc.Label("UP Diliman Unit", id = 'authorprof_upd_unit_label'), 
                                            # dbc.Label("*", style={"color": "#d9534f", "font-style": "bold"}),
                                        ],
                                        width=3
                                    ),  
                                    dbc.Col( 
                                        html.Div( 
                                            dcc.Dropdown( 
                                                id='authorprof_upd_unit_dropdown', clearable=True, searchable=True, placeholder="UP Affiliation"
                                            ),
                                            className="dash-bootstrap" 
                                        ), 
                                    ), 
                                ], 
                                className="mb-3", 
                            ),
                            id = 'authorprof_upd_unit_div'
                        ),
                        # UPD Engineering Department Dropdown
                        html.Div(
                            dbc.Row( 
                                [ 
                                    dbc.Col(
                                        [
                                            dbc.Label("UPD Engineering Department", id = 'authorprof_engg_dept_label'), 
                                            # dbc.Label("*", style={"color": "#d9534f", "font-style": "bold"}),
                                        ],
                                        width=3
                                    ),  
                                    dbc.Col( 
                                        html.Div( 
                                            dcc.Dropdown( 
                                                id='authorprof_engg_dept_dropdown',clearable=True, searchable=True, placeholder="UP Affiliation"
                                            ),
                                            className="dash-bootstrap" 
                                        ), 
                                    ), 
                                ], 
                                className="mb-3", 
                            ),
                            id = 'authorprof_engg_dept_div'
                        ),
                        # IE Faculty Indication Dropdown
                        html.Div(
                            dbc.Row( 
                                [ 
                                    dbc.Col(
                                        [
                                            dbc.Label("UPD IE Faculty Indication", id = 'authorprof_iefacind_label'), 
                                            # dbc.Label("*", style={"color": "#d9534f", "font-style": "bold"}, id='authorprof_iefacind_star'),
                                        ],
                                        width=3
                                    ),  
                                    dbc.Col( 
                                        [
                                            html.Div( 
                                                dcc.Dropdown( 
                                                    id='authorprof_iefacind_dropdown', 
                                                    options = [
                                                        {'label':'IE Faculty', 'value':'IE Faculty'},
                                                        {'label':'Inactive IE Faculty', 'value':'Inactive IE Faculty'},
                                                        {'label':'Non-IE Faculty', 'value':'Non-IE Faculty'},
                                                    ]
                                                ),
                                                className="dash-bootstrap",
                                            ), 
                                            # html.Div( 
                                            #     dcc.Dropdown( 
                                            #         id='authorprof_noniefacind', 
                                            #         options = [
                                            #             {'label': 'N/A: Non-UP Affiliated', 'value': 'Non-UP'},
                                            #         ]
                                            #     ),
                                            #     className="dash-bootstrap",
                                            # ), 
                                        ]
                                    ), 
                                ], 
                                className="mb-3", 
                            ),
                            id = 'authorprof_iefacind_div'
                        ), 
                        # Delete Indicator
                        html.Div( 
                            dbc.Row( 
                                [ 
                                    dbc.Label("Wish to delete?", width=3), 
                                    dbc.Col( 
                                        dbc.Checklist( 
                                            id='authorprof_removerecord', 
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
                            id = 'authorprof_removerecord_div' 
                        ), 
                    ],
                    width=6
                )
            ]
        ),
        html.Hr(), 
        dbc.Button('Submit', color='danger', id='authorprof_submitbtn'), 
        dbc.Modal( 
            [    
                dbc.ModalHeader(dbc.ModalTitle("Saving Progress"), style=mod_style), 
                dbc.ModalBody("temp message", id = 'authorprof_feedback_message'),  
                dbc.ModalFooter( 
                    dbc.Button("Okay", id="authorprof_closebtn", color='secondary', className="ms-auto", n_clicks=0) 
                ),           
            ], 
            centered=True, 
            id="authorprof_modal", 
            is_open=False, 
        ), 
    ] 
) 

# Delete Record Style
@app.callback ( 
    [
        Output('authorprof_toload', 'data'), 
        Output('authorprof_removerecord_div', 'style')
    ],
    [ 
        Input('url', 'pathname')
    ], 
    [ 
        State('url', 'search')
    ] 
)
def authorprof_load_removerecord(pathname, search): 
    if pathname == '/author_profile': 
        parsed = urlparse(search)
        mode = parse_qs(parsed.query)['mode'][0]

        to_load = 1 if mode == 'edit' else 0 

        removerecord_div = None if to_load else {'display': 'none'}

    else: 
         raise PreventUpdate 
    return [to_load, removerecord_div]

# UP Criteria Style       
@app.callback(
    [
        Output('authorprof_up_aff_others_div', 'style'),
        Output('authorprof_upd_unit_div', 'style'),
        Output('authorprof_engg_dept_div', 'style'),
        Output('authorprof_iefacind_div', 'style'),
    ], 
    [
        Input('url', 'pathname'), 
        Input('authorprof_up_aff_dropdown', 'value'),
        Input('authorprof_upd_unit_dropdown', 'value'),
        Input('authorprof_engg_dept_dropdown', 'value'),
    ]
)
def facinddiv (pathname, up_aff, upd_unit, engg_dept): 
    if pathname == '/author_profile':
        if up_aff == '':
            up_aff = None
        if up_aff == None:
            up_aff_others_div = {'display': 'none'}
            upd_unit_div = {'display': 'none'}
            engg_dept_div = {'display': 'none'}
            ie_fac_ind_div = {'display': 'none'}
        elif up_aff == 'Non-UP':
            up_aff_others_div = {'display': 'contents'}
            upd_unit_div = {'display': 'none'}
            engg_dept_div = {'display': 'none'}
            ie_fac_ind_div = {'display': 'none'}
        elif up_aff == 'UP Diliman':
            up_aff_others_div = {'display': 'none'}
            upd_unit_div = {'display': 'contents'}
            engg_dept_div = {'display': 'none'}
            ie_fac_ind_div = {'display': 'none'}
            if upd_unit == '':
                upd_unit = None
            if upd_unit == None:
                engg_dept_div = {'display': 'none'}
                ie_fac_ind_div = {'display': 'none'}
            elif upd_unit == 'College of Engineering':
                engg_dept_div = {'display': 'contents'}
                ie_fac_ind_div = {'display': 'none'}
                if engg_dept == '':
                    engg_dept = None
                if engg_dept == None:
                    ie_fac_ind_div = {'display': 'none'}
                elif engg_dept == 'Department of Industrial Engineering and Operations Research':
                    ie_fac_ind_div = {'display': 'contents'}
                else:
                    ie_fac_ind_div = {'display': 'none'}
            else:
                engg_dept_div = {'display': 'none'}
                ie_fac_ind_div = {'display': 'none'}
        else:
            up_aff_others_div = {'display': 'none'}
            upd_unit_div = {'display': 'none'}
            engg_dept_div = {'display': 'none'}
            ie_fac_ind_div = {'display': 'none'}
    else:
        raise PreventUpdate
    return(up_aff_others_div, upd_unit_div, engg_dept_div, ie_fac_ind_div)

#UP Constituent filter callback
@app.callback(
    [
        Output('authorprof_up_aff_dropdown', 'options'),
    ],
    [
        Input('url', 'pathname'),
    ]
) 
def loadcons(pathname):
    if pathname == '/author_profile':
        sql_filter1 = """SELECT DISTINCT (cons_name) as label, (cons_name) as value
            FROM up_system
            WHERE cons_delete_ind = FALSE
            ORDER BY value ASC"""
        values_filter1 = []
        cols_filter1 = ['label', 'value']
        fac_filter_included = db.querydatafromdatabase(sql_filter1, values_filter1, cols_filter1)
        fac_filter_options = fac_filter_included.to_dict('records')
    else:
        raise PreventUpdate
    return [fac_filter_options] 

#UPD Units filter callback
@app.callback(
    [
        Output('authorprof_upd_unit_dropdown', 'options'),
    ],
    [
        Input('url', 'pathname'),
    ]
) 
def loadupdunits(pathname):
    if pathname == '/author_profile':
        sql_filter2 = """SELECT DISTINCT (college_name) as label, (college_name) as value
            FROM up_diliman
            WHERE college_delete_ind = FALSE
            ORDER BY value ASC"""
        values_filter2 = []
        cols_filter2 = ['label', 'value']
        fac_filter_included = db.querydatafromdatabase(sql_filter2, values_filter2, cols_filter2)
        fac_filter_options = fac_filter_included.to_dict('records')
    else:
        raise PreventUpdate
    return [fac_filter_options] 

#UPD Engineering Dept filter callback
@app.callback(
    [
        Output('authorprof_engg_dept_dropdown', 'options'),
    ],
    [
        Input('url', 'pathname'),
    ]
) 
def loadenggdept(pathname):
    if pathname == '/author_profile':
        sql_filter3 = """SELECT DISTINCT (dept_name) as label, (dept_name) as value
            FROM upd_engg_depts
            WHERE dept_delete_ind = FALSE
            ORDER BY value ASC"""
        values_filter3 = []
        cols_filter3 = ['label', 'value']
        fac_filter_included = db.querydatafromdatabase(sql_filter3, values_filter3, cols_filter3)
        fac_filter_options = fac_filter_included.to_dict('records')
    else:
        raise PreventUpdate
    return [fac_filter_options] 

# Load Details
@app.callback (
    [
        Output('authorprof_ln', 'value'),
        Output('authorprof_fn', 'value'), 
        Output('authorprof_mail', 'value'), 
        Output('authorprof_contact', 'value'),
        Output('authorprof_up_aff_dropdown', 'value'),
        Output('authorprof_up_aff_others', 'value'),
        Output('authorprof_upd_unit_dropdown', 'value'),
        Output('authorprof_engg_dept_dropdown', 'value'),
        Output('authorprof_iefacind_dropdown', 'value'),    
    ], 
    [
        Input('authorprof_toload', 'modified_timestamp')
    ], 
    [
        State('authorprof_toload','data'), 
        State('url', 'search'), 
    ]
)
def authorprof_load (timestamp, to_load, search):
    if to_load == 1: 
        authorprof_sql = """ SELECT 
                author_id,
                author_user_id,
                author_ln, 
                author_fn,
                author_mail,
                author_contact,
                author_up_constituent,
                author_other_aff,
                author_upd_unit,
                author_engg_dept,
                author_fac_ind
            FROM authors
            WHERE
                author_delete_ind = false
            """
        parsed = urlparse(search)
        authorprofid = parse_qs(parsed.query)['id'][0]
            
        authorprof_val = []
        authorprof_colname = ['authorprof_id','authorprof_user_id', 'authorprof_ln', 'authorprof_fn', 'authorprof_mail', 'authorprof_contact', 'authorprof_up_aff', 'authorprof_other_aff', 'authorprof_upd_unit', 'authorprof_engg_dept', 'authorprof_iefacind']
        authorprof_df = db.querydatafromdatabase(authorprof_sql, authorprof_val, authorprof_colname)
            
        counter = 0 
        for i in range(len(authorprof_df)):
                if authorprof_df['authorprof_id'][i] != int(authorprofid):
                    authorprof_df  = authorprof_df.drop(i)
                else: 
                    counted = counter 
                counter += 1
                    
        authorprof_ln = authorprof_df['authorprof_ln'][counted]
        authorprof_fn = authorprof_df['authorprof_fn'][counted]
        authorprof_mail = authorprof_df['authorprof_mail'][counted]
        authorprof_contact = authorprof_df['authorprof_contact'][counted]
        authorprof_up_aff = authorprof_df['authorprof_up_aff'][counted]
        authorprof_other_aff = authorprof_df['authorprof_other_aff'][counted]
        authorprof_upd_unit = authorprof_df['authorprof_upd_unit'][counted]
        authorprof_engg_dept = authorprof_df['authorprof_engg_dept'][counted]
        authorprof_iefacind = authorprof_df['authorprof_iefacind'][counted]
    else:
        raise PreventUpdate
    return [authorprof_ln, authorprof_fn, authorprof_mail, authorprof_contact, authorprof_up_aff, authorprof_other_aff, authorprof_upd_unit, authorprof_engg_dept, authorprof_iefacind]

# Submit Process 
@app.callback(
    [
        Output('authorprof_modal', 'is_open'), 
        Output('authorprof_feedback_message', 'children'), 
        Output('authorprof_inputs_alert', 'is_open'),
        Output('authorprof_facadd_alert', 'is_open'),
        Output('authorprof_facmodify_alert', 'is_open'), 
        Output('authorprof_closebtn', 'href')
    ], 
    [
        Input('authorprof_submitbtn', 'n_clicks'), 
        Input('authorprof_closebtn', 'n_clicks')
    ],
    [
        State('authorprof_ln', 'value'), 
        State('authorprof_fn', 'value'),
        State('authorprof_mail', 'value'),
        State('authorprof_contact', 'value'),
        State('authorprof_up_aff_dropdown', 'value'),
        State('authorprof_up_aff_others', 'value'),
        State('authorprof_upd_unit_dropdown', 'value'),
        State('authorprof_engg_dept_dropdown', 'value'),
        State('authorprof_iefacind_dropdown', 'value'), 
        State('url', 'search'), 
        State('authorprof_removerecord', 'value'), 
    ]
)

def authorprof_submitprocess (submit_btn, close_btn,
                           lastname, firstname, mail, contact,
                           up_aff, other_aff, upd_unit, engg_dept, iefacind,
                           search, removerecord): 
    ctx = dash.callback_context
    if ctx.triggered: 
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]
        openmodal = False 
        feedbackmessage  = ' '
        inputsopenalert = False
        facaddopenalert = False
        facmodifyopenalert = False
        okay_href = None 
    else: 
        raise PreventUpdate
        
    if eventid == 'authorprof_submitbtn' and  submit_btn:
        required = [lastname, firstname, up_aff]
        if not all (required):
            inputsopenalert = True
        
        else: 
            parsed = urlparse(search)
            mode = parse_qs(parsed.query)['mode'][0]
                
            author_timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            author_timestamp_time = datetime.datetime.strptime(author_timestamp,'%Y-%m-%d %H:%M:%S')

            if up_aff == 'Non-UP':
                if not (other_aff):
                    inputsopenalert = True
            if mode == "add":  
                if iefacind == 'IE Faculty':
                    facaddopenalert = True
                elif iefacind == 'Inactive IE Faculty':
                    facaddopenalert = True
                else:
                        openmodal = True 
                        sql_max = """SELECT MAX(author_id) from authors
                        """
                        sql_max_val = []
                        max_colname = ['max']
                        author_max_value_db =  db.querydatafromdatabase(sql_max, sql_max_val,max_colname )
                        author_max_value = int(author_max_value_db['max'][0]) + 1
                        sql_add = """INSERT INTO authors(
                            author_id,
                            author_ln, 
                            author_fn, 
                            author_mail,
                            author_contact,
                            author_up_constituent,
                            author_other_aff,
                            author_upd_unit,
                            author_engg_dept,
                            author_fac_ind,
                            author_delete_ind, 
                            author_last_upd
                        )
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                        """
                        values_add =[author_max_value, lastname, firstname, mail, contact, up_aff, other_aff, upd_unit, engg_dept, iefacind, False, author_timestamp_time]
                        db.modifydatabase(sql_add,values_add)
                        feedbackmessage = f"Author added to DelPHI."
                        okay_href = '/author_manage'
                    
            elif mode == 'edit': 
                if iefacind == 'IE Faculty':
                    facmodifyopenalert = True
                elif iefacind == 'Inactive IE Faculty':
                    facmodifyopenalert = True
                else:
                        openmodal = True
                        parsed = urlparse(search)
                        authorprof_editmodeid = parse_qs(parsed.query)['id'][0]
                        
                        sql_edit = """UPDATE authors
                        SET 
                            author_ln = %s, 
                            author_fn = %s, 
                            author_mail = %s,
                            author_contact = %s, 
                            author_up_constituent = %s,
                            author_other_aff = %s,
                            author_upd_unit = %s,
                            author_engg_dept = %s,
                            author_fac_ind = %s,
                            author_last_upd = %s,
                            author_delete_ind = %s
                        WHERE 
                            author_id = %s
                        """
                        to_delete = bool(removerecord)
                        values_edit = [lastname, firstname, mail, contact, up_aff, other_aff, upd_unit, engg_dept, iefacind, author_timestamp_time, to_delete, authorprof_editmodeid]
                                
                        db.modifydatabase(sql_edit, values_edit)

                        feedbackmessage = "Author information updated."
                        okay_href = '/author_manage'
            # else: 
            #     raise PreventUpdate
    elif eventid == 'authorprof_closebtn' and close_btn: 
        pass 
    else: 
        raise PreventUpdate
    return [openmodal, feedbackmessage, inputsopenalert, facaddopenalert, facmodifyopenalert, okay_href]
