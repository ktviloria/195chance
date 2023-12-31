#for adding and editing/deleting publications
#only admin users have access to this page

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

# from selenium import webdriver 
# import urllib
# import urllib2

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
                dcc.Store(id='form_a_toload', storage_type='memory', data=0), 
                dcc.Store(id ='onlyloadonce', storage_type='memory', data=1), 
                dcc.Store(id = 'dummy', storage_type='memory', data='')
            ] 
        ), 
        html.H2("Publication Details"), 
        html.H6("* Indicates required field", style={"color": "#d9534f", "font-style": "italic"}),
        html.Hr(), 
        # Add publication form and add author button
        dbc.Row(
            [
                #Add/Modify publication form
                dbc.Col(
                    [
                        html.Div(
                            [
                                #alerts
                                dbc.Alert('Please supply required fields.', color="danger", id='a_inputs_alert', is_open=False),
                                dbc.Alert('Please supply required fields.', color="danger", id='a_lead_alert', is_open=False),
                                dbc.Alert('Please supply either a DOI or ISXN', color="danger", id='a_inputs_alert2', is_open=False),
                                dbc.Alert('Lead authors cannot be other contributing authors. Please check your selection.', color="danger", id='a_authors_alert', is_open=False),
                                #Authors involved
                                dbc.Row( 
                                    [ 
                                        dbc.Col(
                                            [
                                            dbc.Label("Lead Author(s)"),
                                            dbc.Label("*", style={"color": "#d9534f", "font-style": "bold"})
                                            ], width=2, style={'display': 'flex', 'align-items': 'center'}
                                            ), 
                                        dbc.Col( 
                                            dcc.Dropdown( 
                                                    id='form_a_lead', multi = True, searchable = True
                                                ),
                                            width=8
                                        ), 
                                    ], 
                                    className="mb-3", 
                                ), 
                                dbc.Row(
                                    [ 
                                        dbc.Col(
                                            [
                                            dbc.Label("Contributing Author(s)"),
                                            #dbc.Label("*", style={"color": "#d9534f", "font-style": "bold"})
                                            ], width=2, style={'display': 'flex', 'align-items': 'center'}
                                            ), 
                                        dbc.Col( 
                                                dcc.Dropdown( 
                                                    id='form_a_contributing', multi = True, searchable = True
                                                ),
                                            width=8
                                        ), 
                                    ], 
                                    className="mb-3",  
                                ), 
                                #Publication tag
                                dbc.Row( 
                                    [ 
                                        dbc.Col(
                                            [
                                            dbc.Label("Criteria"),
                                            dbc.Label("*", style={"color": "#d9534f", "font-style": "bold"})
                                            ], width=2, style={'display': 'flex', 'align-items': 'center'}
                                            ), 
                                        dbc.Col( 
                                            html.Div( 
                                                dcc.Dropdown( 
                                                    id='form_a_tag', optionHeight=60
                                                ),
                                                className="dash-bootstrap" 
                                            ), 
                                            width=8,
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
                                            dbc.Textarea( 
                                                #type="text", 
                                                id="form_a_title", placeholder="Enter title",
                                            ), 
                                            width=8,
                                        ), 
                                    ], 
                                    className="mb-3", 
                                ), 
                                #Publication Date
                                dbc.Row( 
                                    [ 
                                        dbc.Col(
                                            [
                                            dbc.Label("Publication Date"),
                                            dbc.Label("*", style={"color": "#d9534f", "font-style": "bold"})
                                            ], width=2, style={'display': 'flex', 'align-items': 'center'}
                                            ), 
                                        dbc.Col( 
                                            html.Div(
                                                dcc.DatePickerSingle(
                                                    id='form_a_date',
                                                    placeholder="MM/DD/YYYY",
                                                    display_format="MM/DD/YYYY",
                                                    min_date_allowed=date(2014, 1, 1),
                                                    max_date_allowed=date.today(),
                                                    initial_visible_month=date.today(),                                    
                                                ), className="DateInput_input_1"
                
                                            ), 
                                        ), 
                                    ], 
                                    className="mb-3", 
                                ),
                                #Publisher
                                dbc.Row( 
                                    [ 
                                        dbc.Col(
                                            [
                                            dbc.Label("Publisher"),
                                            dbc.Label("*", style={"color": "#d9534f", "font-style": "bold"})
                                            ], width=2, style={'display': 'flex', 'align-items': 'center'}
                                            ), 
                                        dbc.Col( 
                                            dbc.Textarea( 
                                                #type="text", 
                                                id="form_a_publisher", placeholder="Enter publishing house or publishing company", style={"height":"15px"}  
                                            ), 
                                            width=8, 
                                        ), 
                                    ], 
                                    className="mb-3", 
                                ),
                                #Name of Publication
                                dbc.Row( 
                                    [ 
                                        dbc.Col(
                                            [
                                            dbc.Label("Name of Journal"),
                                            dbc.Label("*", style={"color": "#d9534f", "font-style": "bold"})
                                            ], width=2, style={'display': 'flex', 'align-items': 'center'}
                                            ), 
                                        dbc.Col( 
                                            dbc.Textarea( 
                                                #type="text", 
                                                id="form_a_pubname", placeholder="Enter name of publication or journal",
                                                style={"height":"15px"}
                                            ), 
                                            width=8,
                                        ), 
                                    ], 
                                    className="mb-3", 
                                ),
                                #Scopus
                                dbc.Row( 
                                    [ 
                                        dbc.Label("Scopus (Optional)",
                                            width=2, style={'display': 'flex', 'align-items': 'center'}), 
                                        dbc.Col( 
                                            dbc.Input( 
                                                type="text", id="form_a_scopus", placeholder="Enter scopus" 
                                            ), 
                                            width=8,
                                        ), 
                                    ], 
                                    className="mb-3", 
                                ),
                                #Text prompt for requiring DOI/ISXN
                                dbc.Row(
                                    [
                                    dbc.Col(
                                        html.H6("Please provide at least one of the following:", style={"margin-bottom": "15px", "color": "#d9534f", "font-style": "italic"})
                                        )
                                    ]
                                ),
                                #DOI
                                dbc.Row( 
                                    [ 
                                        dbc.Col(
                                            [
                                            dbc.Label("DOI"),
                                            ], width=2, style={'display': 'flex', 'align-items': 'center'}
                                            ),  
                                        dbc.Col( 
                                            dbc.Input( 
                                                type="text", 
                                                id="form_a_doi", placeholder="Enter DOI"
                                            ), 
                                            width=8,
                                        ), 
                                    ], 
                                    className="mb-3", 
                                ),
                                #isxn
                                dbc.Row( 
                                    [ 
                                        dbc.Col(
                                            [
                                            dbc.Label("ISBN/ISSN"),
                                            ], width=2, style={'display': 'flex', 'align-items': 'center'}
                                            ),  
                                        dbc.Col( 
                                            dbc.Input( 
                                                type="text", 
                                                id="form_a_isxn", placeholder="Enter ISBN/ISSN"
                                            ), 
                                            width=8,
                                        ), 
                                    ], 
                                    className="mb-3", 
                                ),
                                #delete div
                                html.Div( 
                                    dbc.Row( 
                                        [ 
                                            dbc.Label("Wish to delete?", width=2), 
                                            dbc.Col( 
                                                dbc.Checklist( 
                                                    id='form_a_removerecord', 
                                                    options=[ 
                                                        { 
                                                            'label': "Mark for Deletion", 'value': 1 
                                                        } 
                                                    ], 
                                                    style={'fontWeight':'bold'}, 
                                                ), 
                                                width=8, 
                                            ), 
                                        ], 
                                        className="mb-3", 
                                    ), 
                                    id = 'form_a_removerecord_div' 
                                ), 
                                html.Hr(), 
                                dbc.Button('Submit', color='danger', id='form_a_submitbtn')
                            ],
                            style={'width': '100%'}
                        )
                    ],
                    width=9, style={'display': 'flex', 'align-items': 'center'}
                ),
                #Add author button
                dbc.Col(
                    dbc.Row([
                        dbc.Col(html.H6('Author not in options?', style={'text-align': 'right', "font-style": "italic"}), width = 6),
                        dbc.Col(dbc.Button('Add Author', color='danger', id='form_a_add_author_btn'), width=6),
                    ]),
                    width=3, style={'align-items': 'baseline'}
                ),
            ]
        ),
        #Submit publication modal
        dbc.Modal( 
            [    
                dbc.ModalHeader(dbc.ModalTitle("Saving Progress"), style=mod_style), 
                dbc.ModalBody("tempmessage", id='form_a_feedback_message'), 
                dbc.ModalFooter( 
                    dbc.Button("Okay", color='secondary', id="form_a_closebtn", className="ms-auto", n_clicks=0) 
                ),           
            ], 
            centered=True, 
            id="form_a_modal", 
            is_open=False, 
        ),
        #Add author modal
        dbc.Modal(   
            [
                dbc.ModalHeader(
                    dbc.Row(dbc.ModalTitle("Add Author Into Dropdown Options")),
                style=mod_style), 
                dbc.ModalBody(
                    [
                    html.H6("* Indicates required field", style={"color": "#d9534f", "font-style": "italic"}),
                    dbc.Alert('Please supply required fields.', color="danger", id='a_add_inputs_alert', is_open=False),
                    dbc.Alert('Author successfully added to database. Please reload page to reflect added author in options.', color="success", id='a_add_success_alert', is_open=False),
                    dbc.Row( 
                        [ 
                            dbc.Col(
                                [
                                    dbc.Label("First Name/Initials"),
                                    dbc.Label("*", style={"color": "#d9534f", "font-style": "bold"})
                                ],
                                width=5, style={'display': 'flex', 'align-items': 'center'}
                            ),  
                            dbc.Col( 
                                dbc.Textarea(id="form_a_add_author_fn", placeholder="Enter author's first name/initials"), 
                                width=7,
                            ), 
                        ], 
                        className="mb-3", 
                    ),
                    dbc.Row( 
                        [ 
                            dbc.Col(
                                [
                                    dbc.Label("Last Name"),
                                    dbc.Label("*", style={"color": "#d9534f", "font-style": "bold"})
                                ],
                                width=5, style={'display': 'flex', 'align-items': 'center'}
                            ),  
                            dbc.Col( 
                                dbc.Textarea(id="form_a_add_author_ln", placeholder="Enter author's last name"), 
                                width=7,
                            ), 
                        ], 
                        className="mb-3", 
                    ),
                    dbc.Row( 
                        [ 
                            dbc.Col(
                                dbc.Label("Email"),
                                width=5, style={'display': 'flex', 'align-items': 'center'}
                            ),  
                            dbc.Col( 
                                dbc.Textarea(id="form_a_add_author_mail", placeholder="Enter author's email"), 
                                width=7,
                            ), 
                        ], 
                        className="mb-3", 
                    ),
                    dbc.Row( 
                        [ 
                            dbc.Col(
                                dbc.Label("Contact Number"),
                                width=5, style={'display': 'flex', 'align-items': 'center'}
                            ),  
                            dbc.Col( 
                                dbc.Textarea(id="form_a_add_author_contact", placeholder="Enter author's contact number"), 
                                width=7,
                            ), 
                        ], 
                        className="mb-3", 
                    ),
                    #UP Affiliation Dropdown
                    dbc.Row( 
                        [ 
                            dbc.Col(
                                [
                                    dbc.Label("UP Affiliation"),
                                    dbc.Label("*", style={"color": "#d9534f", "font-style": "bold"})
                                ],
                                width=5, style={'display': 'flex', 'align-items': 'center'}
                            ), 
                            dbc.Col( 
                                html.Div( 
                                    dcc.Dropdown(id='form_a_add_author_up_aff_dropdown', optionHeight=60, placeholder="UP Affiliation"),
                                    className="dash-bootstrap" 
                                ), 
                                width=7,
                            ), 
                        ], 
                        className="mb-3", 
                    ), 
                    html.Div(
                                    dbc.Row(
                                        [
                                             dbc.Col(
                                                [
                                                    dbc.Label("Specify Other Affiliation", id = 'form_a_up_aff_others_label'), 
                                                    dbc.Label("*", style={"color": "#d9534f", "font-style": "bold"}),
                                                ],
                                                width=5
                                            ),  
                                            dbc.Col( 
                                                dbc.Input( 
                                                    type="text", id="form_a_up_aff_others", placeholder="Please specify affiliation." 
                                                ),
                                                width = 7
                                            ),
                                        ]
                                    ),
                                    id="form_a_up_aff_others_div"
                                ),
                    # UPD Unit Dropdown
                    html.Div(
                            dbc.Row( 
                                [ 
                                    dbc.Col(
                                        [
                                            dbc.Label("UP Diliman Unit", id = 'form_a_upd_unit_label'), 
                                            # dbc.Label("*", style={"color": "#d9534f", "font-style": "bold"}),
                                        ],
                                        width=5
                                    ),  
                                    dbc.Col( 
                                        html.Div( 
                                            dcc.Dropdown( 
                                                id='form_a_upd_unit_dropdown', clearable=True, searchable=True, placeholder="UP Diliman Unit"
                                            ),
                                            className="dash-bootstrap" 
                                        ), 
                                    ), 
                                ], 
                                className="mb-3", 
                            ),
                            id = 'form_a_upd_unit_div'
                        ),
                    # UPD Engineering Department Dropdown
                    html.Div(
                            dbc.Row( 
                                [ 
                                    dbc.Col(
                                        [
                                            dbc.Label("UPD Engineering Department", id = 'form_a_engg_dept_label'), 
                                            # dbc.Label("*", style={"color": "#d9534f", "font-style": "bold"}),
                                        ],
                                        width=5
                                    ),  
                                    dbc.Col( 
                                        html.Div( 
                                            dcc.Dropdown( 
                                                id='form_a_engg_dept_dropdown',clearable=True, searchable=True, placeholder="UPD Engineering Department"
                                            ),
                                            className="dash-bootstrap" 
                                        ), 
                                    ), 
                                ], 
                                className="mb-3", 
                            ),
                            id = 'form_a_engg_dept_div'
                        ),
                    # UPD IE Faculty Indication Dropdown
                    html.Div(
                            dbc.Row( 
                                [ 
                                    dbc.Col(
                                        [
                                            dbc.Label("UPD IE Faculty Indication", id = 'form_a_iefacind_label'), 
                                            # dbc.Label("*", style={"color": "#d9534f", "font-style": "bold"}, id='authorprof_iefacind_star'),
                                        ],
                                        width=5
                                    ),  
                                    dbc.Col( 
                                        [
                                            html.Div( 
                                                dcc.Dropdown( 
                                                    id='form_a_iefacind_dropdown', 
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
                            id = 'form_a_iefacind_div'
                        ), 
                    ]
                ),
                dbc.ModalFooter( 
                    dbc.Button('Submit', color='danger', id='form_a_submit_author_submitbtn') 
                ),           
            ], 
            centered=True, 
            id="form_a_add_author_modal", 
            is_open=False, 
            size = "lg"
        ),  
    ] 
)

# Delete Record Style
@app.callback ( 
    [
        Output('form_a_toload', 'data'),
        Output('form_a_removerecord_div', 'style'),
    ],
    [ 
        Input('url', 'pathname')
    ], 
    [ 
        State('url', 'search')
    ] 
)
def form_a_load_removerecord(pathname, search): 
    if pathname == '/form_authorships': 
        parsed = urlparse(search)
        mode = parse_qs(parsed.query)['mode'][0]
        to_load = 1 if mode == 'edit' else 0 
        removerecord_div = None if to_load else {'display': 'none'}
    else: 
         raise PreventUpdate 
    return [to_load, removerecord_div]

# Load Dropdown Options
@app.callback (
    [
        # Output('form_a_toload', 'data'), 
        Output ('form_a_lead', 'options'),
        Output ('form_a_contributing', 'options'), 
        Output ('form_a_tag', 'options'),
        Output('form_a_add_author_up_aff_dropdown', 'options')
    ], 
    [
        Input('url', 'pathname'), 
        Input('form_a_lead', 'value'),
        Input('form_a_contributing', 'value')
    ], 
    [
        State('currentuserid', 'data'),  
    ]
)
def form_a_load_dropdown(pathname, lead, contributing, currentuserid): 
    if pathname == '/form_authorships': 
        #lead author options
        sql_lead_author = """ SELECT
            DISTINCT (author_fn ||' '|| author_ln) as label, author_id as value,
			author_user_id
            from authors
            WHERE not author_delete_ind
			ORDER BY authors.author_user_id 
        """
        values_lead_author = []
        
        cols_lead_author = ['label', 'value', 'faculty_ind']
        lead_author_involved = db.querydatafromdatabase(sql_lead_author, values_lead_author, cols_lead_author)

        lead_author_opts = lead_author_involved.to_dict('records')

        #contributing author options
        sql_contributing_author = """ SELECT
            DISTINCT (author_fn ||' '|| author_ln) as label, author_id as value,
            author_user_id
            from authors
            WHERE not author_delete_ind
            ORDER BY authors.author_user_id 
        """
        values_contributing_author = []
        
        cols_contributing_author = ['label', 'value', 'faculty_ind']
        contributing_author_involved = db.querydatafromdatabase(sql_contributing_author, values_contributing_author, cols_contributing_author)

        contributing_author_opts = contributing_author_involved.to_dict('records')

        # for x in x in
        #     sql_contributing_author = """ SELECT DISTINCT (authors.author_fn ||' '|| authors.author_ln) as label, author_id as value
        #         from authors
        #         WHERE not author_delete_ind and not author_id = %s
        #         ORDER BY value 
        #     """
        #     values_contributing_author = [lead]
        #     contributing_author_involved = db.querydatafromdatabase(sql_contributing_author, values_contributing_author, cols_lead_author)
        
        # contributing_author_involved = [x for x in lead_author_involved
        #                                 if x[id] != lead
        #                                 and x[id] != contributing]
        
        #criteria options
        sql_tags = """SELECT DISTINCT (tag_title) AS label, tag_id AS value 
            from tags 
            WHERE tag_sub = 'A' and not tag_delete_ind 
                
            ORDER BY value
        """
        values_tag  = []
        cols_tag = ['label', 'value']
        tag_included = db.querydatafromdatabase(sql_tags, values_tag, cols_tag)
        tag_options = tag_included.to_dict('records')

        #up_aff options
        sql_up_aff = """SELECT DISTINCT (cons_name) AS label, cons_name AS value 
            from up_system 
            WHERE cons_delete_ind = false
                
            ORDER BY value
        """
        values_up_aff  = []
        cols_up_aff = ['label', 'value']
        up_aff_included = db.querydatafromdatabase(sql_up_aff, values_up_aff, cols_up_aff)
        up_aff_options = up_aff_included.to_dict('records')
        
    else: 
         raise PreventUpdate 
    return(lead_author_opts, contributing_author_opts, tag_options, up_aff_options)

# UP Criteria Style       
@app.callback(
    [
        Output('form_a_up_aff_others_div', 'style'),
        Output('form_a_upd_unit_div', 'style'),
        Output('form_a_engg_dept_div', 'style'),
        Output('form_a_iefacind_div', 'style'),
    ], 
    [
        Input('url', 'pathname'), 
        Input('form_a_add_author_up_aff_dropdown', 'value'),
        Input('form_a_upd_unit_dropdown', 'value'),
        Input('form_a_engg_dept_dropdown', 'value'),
    ]
)
def facinddiv (pathname, up_aff, upd_unit, engg_dept): 
    if pathname == '/form_authorships':
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
        Output('form_a_up_aff_dropdown', 'options'),
    ],
    [
        Input('url', 'pathname'),
    ]
) 
def loadcons(pathname):
    if pathname == '/form_authorships':
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
        Output('form_a_upd_unit_dropdown', 'options'),
    ],
    [
        Input('url', 'pathname'),
    ]
) 
def loadupdunits(pathname):
    if pathname == '/form_authorships':
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
        Output('form_a_engg_dept_dropdown', 'options'),
    ],
    [
        Input('url', 'pathname'),
    ]
) 
def loadenggdept(pathname):
    if pathname == '/form_authorships':
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

#Load Data    
@app.callback(
    [
        Output('form_a_lead', 'value'),
        Output('form_a_contributing', 'value'),
        Output('form_a_title', 'value'),
        Output('form_a_tag', 'value'),
        Output('form_a_date', 'date'),
        Output('form_a_publisher', 'value'),
        Output('form_a_pubname', 'value'),
        Output('form_a_doi', 'value'),
        Output('form_a_isxn', 'value'),
        Output('form_a_scopus', 'value'), 
        Output('onlyloadonce','data' )
    ],
    [
        Input('form_a_toload', 'modified_timestamp'), 
    ],
    [
        State('form_a_toload', 'data'),
        State('url', 'search'), 
        State('onlyloadonce', 'data')
    ],
)
def form_a_load(timestamp, to_load, search, onlyloadonce): 
    parsed = urlparse(search)
    mode = parse_qs(parsed.query)['mode'][0]
    to_load = 1 if mode == 'edit' else 0 
    
    if onlyloadonce == 1: 
        if to_load == 1: 
            form_a_sql = """ SELECT distinct authorships.pub_id,
				(select string_agg(lead_author_name, ', ')
				 from pub_lead_authors
				 where pub_lead_authors.pub_id = authorships.pub_id
				) as lead_authors, 
                (select string_agg(contributing_author_name, ', ')
				 from pub_contributing_authors
				 where pub_contributing_authors.pub_id = authorships.pub_id
				) as contributing_authors, 
                publications.pub_title, 
                publications.tag_id,
                authorships.a_date,
                authorships.a_publisher,
                authorships.a_pub_name, 
                authorships.a_doi, 
                authorships.a_isxn, 
                authorships.a_scopus

                FROM authorships 
                    INNER JOIN publications on authorships.pub_id = publications.pub_id 
					LEFT OUTER JOIN pub_lead_authors on publications.pub_id = pub_lead_authors.pub_id
					LEFT OUTER JOIN pub_contributing_authors on publications.pub_id = pub_contributing_authors.pub_id
                WHERE
                    publications.pub_delete_ind = false and authorships.pub_id = %s
                ORDER BY authorships.pub_id
            """
        
            parsed = urlparse(search)
            form_a_id = parse_qs(parsed.query)['id'][0]
            form_a_val = [int(form_a_id)]
            form_a_colname = ['form_a_pub_id',
                              'form_a_lead', 'form_a_contributing',
                              'form_a_pub_title', 'form_a_tag_id',
                              'form_a_date', 'form_a_publisher', 'form_a_pub_name', 'form_a_doi', 'form_a_isxn', 'form_a_scopus']
            form_a_df = db.querydatafromdatabase(form_a_sql,  form_a_val, form_a_colname )
            
            form_a_lead_sql = """SELECT distinct a_lead_id
                from
                    authorships
                where
                    a_lead_id in (SELECT distinct a_lead_id
                                from pub_lead_authors
                                where pub_lead_authors.pub_id = authorships.pub_id)
                    and authorships.pub_id = %s"""
            form_a_lead_val = [int(form_a_id)]
            form_a_lead_cols = ['a_lead_ids']
            form_a_lead_df = db.querydatafromdatabase(form_a_lead_sql, form_a_lead_val, form_a_lead_cols)
            form_a_lead= form_a_lead_df['a_lead_ids'][0]
            form_a_lead=[]
            for i in range(len(form_a_lead_df['a_lead_ids'])): 
                form_a_lead.append(form_a_lead_df['a_lead_ids'][i])
            
            form_a_contributing_sql = """SELECT distinct a_contributing_id
                from
                    authorships
                where
                    a_contributing_id in (SELECT distinct a_contributing_id
                                from pub_contributing_authors
                                where pub_contributing_authors.pub_id = authorships.pub_id)
                    and authorships.pub_id = %s"""
            form_a_contributing_val = [int(form_a_id)]
            form_a_contributing_cols = ['a_contributing_ids']
            form_a_contributing_df = db.querydatafromdatabase(form_a_contributing_sql, form_a_contributing_val, form_a_contributing_cols)
            
            if len(form_a_contributing_df) == 0:
                form_a_contributing = []
            else:
                form_a_contributing= form_a_contributing_df['a_contributing_ids'][0]
                form_a_contributing = []
                for i in range(len(form_a_contributing_df['a_contributing_ids'])): 
                    form_a_contributing.append(form_a_contributing_df['a_contributing_ids'][i])

            form_a_pub_id = form_a_df['form_a_pub_id'][0]
            form_a_pub_title = form_a_df['form_a_pub_title'][0]
            form_a_tag_id = form_a_df['form_a_tag_id'][0]
            form_a_date = form_a_df['form_a_date'][0]
            form_a_publisher = form_a_df['form_a_publisher'][0]
            form_a_pub_name = form_a_df['form_a_pub_name'][0]
            form_a_doi = form_a_df['form_a_doi'][0]
            form_a_isxn = form_a_df['form_a_isxn'][0]
            form_a_scopus = form_a_df['form_a_scopus'][0] 

        else: 
            raise PreventUpdate 
        onlyloadonce += 1       
        
    else: 
        raise PreventUpdate
    return [form_a_lead, form_a_contributing,
            form_a_pub_title, form_a_tag_id, form_a_date, form_a_publisher, form_a_pub_name, 
            form_a_doi, form_a_isxn, form_a_scopus, onlyloadonce ]

#Add Publication Submit process
@app.callback(
    [
        Output('form_a_add_author_modal', 'is_open'),
        Output('form_a_modal', 'is_open'), 
        Output('form_a_feedback_message', 'children'), 
        Output('form_a_closebtn', 'href'), 
        Output('a_inputs_alert', 'is_open'),
        Output('a_lead_alert', 'is_open'),
        Output('a_inputs_alert2', 'is_open'),
        Output('a_authors_alert', 'is_open'),
    ], 
    [
        Input('form_a_add_author_btn', 'n_clicks'),
        Input('form_a_submitbtn', 'n_clicks'), 
        Input('form_a_closebtn', 'n_clicks') 
    ], 
    [
        State('form_a_lead', 'value'),
        State('form_a_contributing', 'value'),
        State('form_a_title', 'value'),
        State('form_a_tag', 'value'),
        State('form_a_date', 'date'),
        State('form_a_publisher', 'value'),
        State('form_a_pubname', 'value'),
        State('form_a_doi', 'value'),
        State('form_a_isxn', 'value'),
        State('form_a_scopus', 'value'), 
        State('url', 'search' ),
        State('form_a_removerecord', 'value'),  
        State('currentuserid', 'data')
    ]
)
def form_a_submitprocess (addauthor_btn, submit_btn, close_btn, a_lead, a_contributing, 
                          a_title, a_tag, a_date, a_publisher, a_pubname,
                          a_doi, a_isxn, a_scopus, search, removerecord, cuser_id):
    ctx = dash.callback_context
    if ctx.triggered: 
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]
        addauthoropenmodal = False
        openmodal = False 
        feedbackmessage  = ' '
        inputsalert = False
        leadalert= False
        DOI_alert = False
        authoralert = False
        okay_href = None 
    else: 
        raise PreventUpdate
    
    if eventid == 'form_a_add_author_btn' and addauthor_btn: 
        addauthoropenmodal = True
    elif eventid == 'form_a_submitbtn' and submit_btn:     
        inputs = [
            a_lead,
            a_tag, 
            a_title, 
            a_date, 
            a_publisher, 
            a_pubname
        ]
        
        # inputs2 = [
        #     a_lead, 
        #     a_tag, 
        #     a_title, 
        #     a_date, 
        #     a_publisher, 
        #     a_pubname
        # ]
        a_contributing_list = a_contributing
        if a_contributing is not None:
            for a_contributing in a_contributing:
                if a_contributing in a_lead:
                    authoralert = True
        if not all(inputs): 
            inputsalert = True
        elif (not(a_doi) and not(a_isxn)): 
            DOI_alert = True 
        elif authoralert == True:
            pass
        else:
            openmodal = True  
            parsed = urlparse(search)
            mode = parse_qs(parsed.query)['mode'][0]
            
            a_sqlcode_modifiedby = """SELECT
            user_id,
            user_un
            FROM users
            """
            a_vals_modifiedby = []
            a_cols_modifiedby = ['id', 'un']
            a_username = db.querydatafromdatabase(a_sqlcode_modifiedby, a_vals_modifiedby, a_cols_modifiedby)
            
            a_username_modifier = ""
            for i in range(len(a_username['id'])):
                if int(a_username['id'][i]) == cuser_id:
                    a_username_modifier = a_username['un'][i]

            a_timestamp = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            a_timestamp_time = dt.datetime.strptime(a_timestamp,'%Y-%m-%d %H:%M:%S')
                
            if mode == "add": 
                sql_max_inquiry = """SELECT MAX(pub_id) from publications
                """
                sql_max_val = []
                max_colname = ['max']
                pub_max_value_db = db.querydatafromdatabase (sql_max_inquiry, sql_max_val, max_colname)
                sql_pub_max = int(pub_max_value_db['max'][0]) + 1

                # sql_author_user_id = """select distinct publications.pub_id, user_id
                # from publications
                # inner join authors on publications.user_id = authors.author_user_id
                # left outer join authorships on authors.author_user_id = authorships.a_lead_id or authors.author_user_id = authorships.a_contributing_id
                # where author_user_id >0
                # """
                # val_author_user_id = []
                # cols_author_user_id = ['id', 'user_id']
                # author_user_id = db.querydatafromdatabase (sql_author_user_id, val_author_user_id , cols_author_user_id)
                # print(author_user_id)

                form_a_sqlcode_add_publications = """INSERT INTO publications(
                    pub_id,  
                    tag_id, 
                    pub_title, 
                    pub_delete_ind, 
                    pub_last_upd,
                    modified_by
                )
                VALUES (%s, %s, %s, %s, %s, %s)
                """ 
                
                form_a_values_addpub = [sql_pub_max, a_tag, a_title, False, a_timestamp_time, a_username_modifier]
                db.modifydatabase(form_a_sqlcode_add_publications, form_a_values_addpub)
                
                if a_lead == None:
                    a_lead = []
                if type(a_lead) == int: 
                    a_lead = [a_lead]
                    
                if a_contributing_list == None: 
                    a_contributing_list = []
                if type(a_contributing_list) == int: 
                    a_contributing_list = [a_contributing_list]

                #LEAD AUTHOR ADD
                for i in range(len(a_lead)): 
                    sql_pub_lead = """INSERT INTO pub_lead_authors(
                        pub_id, 
                        a_lead_id
                    )
                    VALUES (%s, %s)
                    """
                    val_pub_lead = [sql_pub_max, a_lead[i]]
                    db.modifydatabase(sql_pub_lead, val_pub_lead)

                    sql_pub_lead_upd = """UPDATE pub_lead_authors
                        SET
                        lead_author_name = (SELECT author_fn || ' ' || author_ln FROM authors WHERE a_lead_id=author_id)
                        WHERE a_lead_id > 0;
                    """
                    val_pub_lead_upd = []
                    db.modifydatabase(sql_pub_lead_upd, val_pub_lead_upd)

                #     form_a_sqlcode_upd_publications = """UPDATE publications
                #         SET
                #         user_id = (SELECT author_user_id FROM authors WHERE author_user_id=user_id)
                #         WHERE pub_id > 0;
                # """ 
                #     form_a_values_updpub = []
                #     db.modifydatabase(form_a_sqlcode_upd_publications, form_a_values_updpub)

                    form_a_sqlcode_add_authorships_l = """INSERT INTO authorships(
                        pub_id, 
                        a_lead_id,
                        a_date, 
                        a_year, 
                        a_publisher, 
                        a_pub_name, 
                        a_doi, 
                        a_isxn, 
                        a_scopus 
                    )
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """
                    str_to_date = datetime.strptime(a_date, '%Y-%m-%d').date()
                    a_year = str_to_date.year

                    form_a_values_addauthorship_l = [sql_pub_max, a_lead[i], a_date, a_year, a_publisher, a_pubname, a_doi, a_isxn, a_scopus]
                    db.modifydatabase(form_a_sqlcode_add_authorships_l, form_a_values_addauthorship_l)
                
                # CONTRIBUTING AUTHOR ADD
                for i in range(len(a_contributing_list)):
                    sql_pub_contributing = """INSERT INTO pub_contributing_authors(
                            pub_id, 
                            a_contributing_id
                        )
                        VALUES (%s, %s)
                        """
                    val_pub_contributing = [sql_pub_max, a_contributing_list[i]]
                    db.modifydatabase(sql_pub_contributing, val_pub_contributing)

                    sql_pub_contributing_upd = """UPDATE pub_contributing_authors
                            SET
                            contributing_author_name = (SELECT author_fn || ' ' || author_ln FROM authors WHERE a_contributing_id=author_id)
                            WHERE a_contributing_id > 0;
                        """
                    val_pub_contributing_upd = []
                    db.modifydatabase(sql_pub_contributing_upd, val_pub_contributing_upd)

                    form_a_sqlcode_add_authorships_c = """INSERT INTO authorships(
                            pub_id, 
                            a_contributing_id,
                            a_date, 
                            a_year, 
                            a_publisher, 
                            a_pub_name, 
                            a_doi, 
                            a_isxn, 
                            a_scopus 
                        )
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                        """
                    str_to_date = datetime.strptime(a_date, '%Y-%m-%d').date()
                    a_year = str_to_date.year

                    form_a_values_addauthorship_c = [sql_pub_max, a_contributing_list[i], a_date, a_year, a_publisher, a_pubname, a_doi, a_isxn, a_scopus]
                    db.modifydatabase(form_a_sqlcode_add_authorships_c, form_a_values_addauthorship_c)

                feedbackmessage = 'Authorship entry added to database.'
                if cuser_id <= 3: 
                    okay_href = '/publications_manage'
                else: 
                    okay_href = '/my_publications'
            
            elif mode == 'edit': 
                parsed = urlparse(search)
                form_a_editmodeid = parse_qs(parsed.query)['id'][0]
                
                sql_update_publications = """UPDATE publications
                SET 
                    tag_id = %s, 
                    pub_title = %s, 
                    pub_delete_ind = %s, 
                    pub_last_upd = %s,
                    modified_by = %s
                WHERE 
                    pub_id = %s
                """
                to_delete = bool(removerecord)
                
                values_update_publications = [a_tag, a_title, to_delete, a_timestamp_time, a_username_modifier, form_a_editmodeid]
                db.modifydatabase(sql_update_publications,values_update_publications )
                
                sql_delete_lead_a = """DELETE FROM authorships
                        WHERE pub_id = %s"""
                val_delete_lead_a =[int(form_a_editmodeid)]
                db.modifydatabase(sql_delete_lead_a, val_delete_lead_a)  

                if a_lead == None: 
                    a_lead = []
                if type(a_lead) == int: 
                        a_lead = [a_lead]

                if a_contributing_list == None: 
                    a_contributing_list = []
                if type(a_contributing_list) == int: 
                    a_contributing_list = [a_contributing_list]
                
                #LEAD AUTHOR EDIT

                #delete all lead
                sql_delete_lead_a = """DELETE FROM pub_lead_authors
                        WHERE pub_id = %s"""
                val_delete_lead_a =[int(form_a_editmodeid)]
                db.modifydatabase(sql_delete_lead_a, val_delete_lead_a)
                             
                #re-add pub w updated lead
                for i in range(len(a_lead)):
                    sql_pub_lead = """INSERT INTO pub_lead_authors(pub_id, a_lead_id)
                        VALUES (%s, %s)
                        """
                    pub_lead_values = [int(form_a_editmodeid), a_lead[i]]
                    db.modifydatabase(sql_pub_lead, pub_lead_values) 

                    sql_pub_lead_upd ="""update pub_lead_authors
                        set
                        lead_author_name = (select author_fn || ' ' || author_ln from authors where a_lead_id=author_id)
                        where a_lead_id>0;
                        """
                    val_pub_lead_upd =[]
                    db.modifydatabase(sql_pub_lead_upd, val_pub_lead_upd)

                    sql_update_authorships_l = """ INSERT INTO authorships ( 
                        pub_id,
                        a_lead_id,
                        a_date, 
                        a_year, 
                        a_publisher, 
                        a_pub_name, 
                        a_doi, 
                        a_isxn, 
                        a_scopus
                        )
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s) 
                        """
                    str_to_date = datetime.strptime(a_date, '%Y-%m-%d').date()
                    a_year = str_to_date.year
                    values_update_authorships_l = [int(form_a_editmodeid), a_lead[i], a_date, a_year, a_publisher, a_pubname, a_doi, a_isxn, a_scopus]
                    db.modifydatabase(sql_update_authorships_l, values_update_authorships_l)
                
                #CONTRIBUTING AUTHOR EDIT

                #delete all contributing
                sql_delete_contributing_a = """DELETE FROM pub_contributing_authors
                        WHERE pub_id = %s"""
                val_delete_contributing_a =[int(form_a_editmodeid)]
                db.modifydatabase(sql_delete_contributing_a, val_delete_contributing_a)               
                #add all new contributing
                for i in range(len(a_contributing_list)):
                    sql_pub_contributing = """INSERT INTO pub_contributing_authors(pub_id, a_contributing_id)
                        VALUES (%s, %s)
                        """
                    pub_contributing_values = [int(form_a_editmodeid), a_contributing_list[i]]
                    db.modifydatabase(sql_pub_contributing, pub_contributing_values) 

                    sql_pub_contributing_upd ="""update pub_contributing_authors
                        set
                        contributing_author_name = (select author_fn || ' ' || author_ln from authors where a_contributing_id=author_id)
                        where a_contributing_id>0;
                        """
                    val_pub_contributing_upd =[]
                    db.modifydatabase(sql_pub_contributing_upd, val_pub_contributing_upd)

                    sql_update_authorships_c = """ INSERT INTO authorships ( 
                        pub_id,
                        a_contributing_id,
                        a_date, 
                        a_year, 
                        a_publisher, 
                        a_pub_name, 
                        a_doi, 
                        a_isxn, 
                        a_scopus
                        )
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s) 
                        """
                    str_to_date = datetime.strptime(a_date, '%Y-%m-%d').date()
                    a_year = str_to_date.year
                    values_update_authorships_c = [int(form_a_editmodeid), a_contributing_list[i], a_date, a_year, a_publisher, a_pubname, a_doi, a_isxn, a_scopus]
                    db.modifydatabase(sql_update_authorships_c, values_update_authorships_c)
                feedbackmessage = 'Authorship details updated.'
                if cuser_id <= 3: 
                    okay_href = '/publications_manage'
                else: 
                    okay_href = '/my_publications'
            else: 
                raise PreventUpdate
    elif eventid == 'form_a_closebtn' and close_btn: 
        pass
    else: 
        raise PreventUpdate
    return [addauthoropenmodal, openmodal, feedbackmessage, okay_href, inputsalert, leadalert, DOI_alert, authoralert]

#Add Author Submit process
@app.callback(
    [
        Output('a_add_inputs_alert', 'is_open'),
        Output('a_add_success_alert', 'is_open')
    ], 
    [
        Input('form_a_submit_author_submitbtn', 'n_clicks'), 
    ], 
    [
        State('form_a_add_author_fn', 'value'),
        State('form_a_add_author_ln', 'value'),
        State('form_a_add_author_up_aff_dropdown', 'value'),
        State('form_a_up_aff_others', 'value'),
        State('form_a_upd_unit_dropdown', 'value'),
        State('form_a_engg_dept_dropdown', 'value'),
        State('form_a_iefacind_dropdown', 'value'),
        State('form_a_add_author_mail', 'value'),
        State('form_a_add_author_contact', 'value'),
        State('url', 'search' ),
    ]
)
def form_a_submitauthorprocess (add_submit_btn,
                            firstname, lastname,
                            affiliation, other_aff, upd_unit, engg_dept, iefacind,
                            mail, contact,
                            add_search):
    ctx = dash.callback_context
    if ctx.triggered: 
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]
        add_inputsalert = False
        add_successalert = False
    else: 
        raise PreventUpdate
    
    if eventid == 'form_a_submit_author_submitbtn' and add_submit_btn:     
        add_inputs = [firstname, lastname, affiliation]
        if not all(add_inputs): 
            add_inputsalert = True
        else: 
            if affiliation == 'Non-UP':
                if not (other_aff):
                    add_inputsalert = True
                else:
                    add_successalert = True
                    parsed = urlparse(add_search)
                    mode = parse_qs(parsed.query)['mode'][0]

                    a_add_timestamp = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    a_add_timestamp_time = dt.datetime.strptime(a_add_timestamp,'%Y-%m-%d %H:%M:%S')

                    sql_max_author_inquiry = """SELECT MAX(author_id) from authors"""
                    max_author_val = []
                    max_author_colname = ['max']
                    max_author_value_db = db.querydatafromdatabase (sql_max_author_inquiry, max_author_val, max_author_colname)
                    max_author_id = int(max_author_value_db['max'][0]) + 1

                    form_a_sqlcode_add_author = """INSERT INTO authors(
                                author_id,  
                                author_fn,
                                author_ln,
                                author_mail,
                                author_contact,
                                author_up_constituent,
                                author_other_aff,
                                author_upd_unit,
                                author_engg_dept,
                                author_fac_ind,
                                author_last_upd
                            )
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                            """                 
                    form_a_values_add_author = [max_author_id, firstname, lastname, mail, contact, affiliation, other_aff, upd_unit, engg_dept, iefacind, a_add_timestamp_time]
                    db.modifydatabase(form_a_sqlcode_add_author, form_a_values_add_author)
            else:
                add_successalert = True
                parsed = urlparse(add_search)
                mode = parse_qs(parsed.query)['mode'][0]

                a_add_timestamp = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                a_add_timestamp_time = dt.datetime.strptime(a_add_timestamp,'%Y-%m-%d %H:%M:%S')

                sql_max_author_inquiry = """SELECT MAX(author_id) from authors"""
                max_author_val = []
                max_author_colname = ['max']
                max_author_value_db = db.querydatafromdatabase (sql_max_author_inquiry, max_author_val, max_author_colname)
                max_author_id = int(max_author_value_db['max'][0]) + 1

                form_a_sqlcode_add_author = """INSERT INTO authors(
                            author_id,  
                            author_fn,
                            author_ln,
                            author_mail,
                            author_contact,
                            author_up_constituent,
                            author_other_aff,
                            author_upd_unit,
                            author_engg_dept,
                            author_fac_ind,
                            author_last_upd
                        )
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                        """                 
                form_a_values_add_author = [max_author_id, firstname, lastname, mail, contact, affiliation, other_aff, upd_unit, engg_dept, iefacind, a_add_timestamp_time]
                db.modifydatabase(form_a_sqlcode_add_author, form_a_values_add_author)
                    
    else: 
        raise PreventUpdate
    return [add_inputsalert, add_successalert]

