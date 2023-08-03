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

from datetime import date
from dash import Dash, dcc, html
from dash.dependencies import Input, Output

mod_style = { 
 'color': '#fff',
 'background-color': '#b22222',
 'font-size': '25px'
} 

layout= html.Div( 
    [ 
        html.Div( 
            [ 
                dcc.Store(id='form_p_toload2', storage_type='memory', data=0),
                dcc.Store(id='form_p_loadonce', storage_type='memory', data=1), 
            ] 
        ), 
        html.H2("Presentation Details"), 
        html.H6("* Indicates required field", style={"color": "#d9534f", "font-style": "italic"}),
        html.Hr(), 
        # Add presentation form and add presenter button
        dbc.Row(
            [
                #Add/Modify publication form
                dbc.Col(
                    [
                        html.Div(
                            [
                                #alerts
                                dbc.Alert('Please supply required fields.', color="danger", id='p_inputs_alert2', is_open=False),
                                #Authors involved
                                dbc.Row( 
                                    [   
                                        dbc.Col(
                                            [
                                            dbc.Label("Presenter(s)"),
                                            dbc.Label("*", style={"color": "#d9534f", "font-style": "bold"})
                                            ], width=2, style={'display': 'flex', 'align-items': 'center'}
                                            ), 
                                        dbc.Col( 
                                                dcc.Dropdown( 
                                                    id= 'form_p_pres', multi= True, searchable = True
                                                ),
                                            width=8,
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
                                                    id='form_p_tag2', 
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
                                                id="form_p_title2", placeholder="Enter publication title" 
                                            ), 
                                            width=8, 
                                        ), 
                                    ], 
                                    className="mb-3", 
                                ), 
                                #conference
                                dbc.Row( 
                                    [ 
                                        dbc.Col(
                                            [
                                            dbc.Label("Conference"),
                                            dbc.Label("*", style={"color": "#d9534f", "font-style": "bold"})
                                            ], width=2, style={'display': 'flex', 'align-items': 'center'}
                                            ), 
                                        dbc.Col( 
                                            dbc.Textarea( 
                                                #type="text", 
                                                id="form_p_conf2", placeholder="Enter conference", style={"height":"15px"} 
                                            ), 
                                            width=8,
                                        ), 
                                    ], 
                                    className="mb-3", 
                                ),
                                #location
                                dbc.Row( 
                                    [ 
                                        dbc.Label("Location", width=2, style={'display': 'flex', 'align-items': 'center'}), 
                                        dbc.Col( 
                                            dbc.Textarea( 
                                                #type="text", 
                                                id="form_p_loc2", placeholder="Enter location of conference", style={"height":"15px"}  
                                            ), 
                                            width=8,
                                        ), 
                                    ], 
                                    className="mb-3", 
                                ),
                                #pres date - start
                                dbc.Row( 
                                    [ 
                                        dbc.Col(
                                            [
                                            dbc.Label("Start Date"),
                                            dbc.Label("*", style={"color": "#d9534f", "font-style": "bold"})
                                            ], width=2, style={'display': 'flex', 'align-items': 'center'}
                                            ), 
                                        dbc.Col( 
                                            dcc.DatePickerSingle(
                                                id='form_p_start_date2',
                                                placeholder="MM/DD/YYYY",
                                                display_format="MM/DD/YYYY",
                                                min_date_allowed=date(2014, 1, 1),
                                                max_date_allowed=date.today(),
                                                initial_visible_month=date.today(),
                                                #note: I couldn't adjust the width of the box to fit the placeholder
                                            ), className="DateInput_input_1"
                                                    #html.Div(id='output-container-date-picker-range')
                                                #type="text", id="form_p_presdate", placeholder="Enter date(s) of presentation YYYY or MM/DD/YYYY" 
                                        ), 
                                    ], 
                                    className="mb-3", 
                                ),
                                #pres date - end
                                dbc.Row( 
                                    [ 
                                        dbc.Col(
                                            [
                                            dbc.Label("End Date"),
                                            dbc.Label("*", style={"color": "#d9534f", "font-style": "bold"})
                                            ], width=2, style={'display': 'flex', 'align-items': 'center'}
                                            ), 
                                        dbc.Col( 
                                            dcc.DatePickerSingle(
                                                id='form_p_end_date2',
                                                placeholder="MM/DD/YYYY",
                                                display_format="MM/DD/YYYY",
                                                min_date_allowed=date(2014, 1, 1),
                                                max_date_allowed=date.today(),
                                                initial_visible_month=date.today(),
                                                #note: I couldn't adjust the width of the box to fit the placeholder
                                            ), className="DateInput_input_1"
                                                    #html.Div(id='output-container-date-picker-range')
                                                #type="text", id="form_p_presdate", placeholder="Enter date(s) of presentation YYYY or MM/DD/YYYY" 
                                        ), 
                                    ], 
                                    className="mb-3", 
                                ),

                                #if you want to use date range picker, just separated start and end date above in case these need to be shown separately in the database
                                # dbc.Row( 
                                #     [ 
                                #         dbc.Label("Date Range", width=2), 
                                #         dbc.Col( 
                                #             dcc.DatePickerRange(
                                #             id='p_date_range',
                                #             min_date_allowed=date(2014, 1, 1),
                                #             max_date_allowed=date.today(),
                                #             initial_visible_month=date.today(),
                                #             start_date_placeholder_text="MM/DD/YYYY",
                                #             end_date_placeholder_text="MM/DD/YYYY",
                                #                 #note: I couldn't adjust the width of the box to fit the placeholder
                                #             ),
                                #                     #html.Div(id='output-container-date-picker-range')
                                #                 #type="text", id="form_p_presdate", placeholder="Enter date(s) of presentation YYYY or MM/DD/YYYY" 
                                #         ), 
                                #     ], 
                                #     className="mb-3", 
                                # ),

                                #pres add info
                                dbc.Row( 
                                    [ 
                                        dbc.Label("Additional Information", width=2, style={'display': 'flex', 'align-items': 'center'}), 
                                        dbc.Col( 
                                            dbc.Textarea( 
                                                #type="text", 
                                                id="form_p_addinfo2", placeholder="Enter any additional information", style={"min-height":"80px"} 
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
                                                    id='form_p_removerecord2', 
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
                                    id = 'form_p_removerecord_div2' 
                                ), 
                                html.Hr(), 
                                dbc.Button('Submit', color='danger', id='form_p_submitbtn2'),
                            ],
                            style={'width': '100%'}
                        )
                    ],
                    width=9, style={'display': 'flex', 'align-items': 'center'}
                ),
                #Add author button
                dbc.Col(
                    dbc.Row([
                        dbc.Col(html.H6('Presenter not in options?', style={'text-align': 'right', "font-style": "italic"}), width = 6),
                        dbc.Col(dbc.Button('Add Presenter', color='danger', id='form_p_add_author_btn'), width=6),
                    ]),
                    width=3, style={'align-items': 'baseline'}
                ),
            ]
        ),
        #Submit presentation modal
        dbc.Modal( 
            [    
                dbc.ModalHeader(dbc.ModalTitle("Saving Progress"), style=mod_style), 
                dbc.ModalBody("tempmessage", id='form_p_feedback_message2'), 
                dbc.ModalFooter( 
                    dbc.Button("Okay", color='secondary', id="form_p_closebtn2", className="ms-auto", n_clicks=0) 
                ),           
            ], 
            centered=True, 
            id="form_p_modal2", 
            is_open=False, 
        ),  
        #Add presenter modal
        dbc.Modal(   
            [
                dbc.ModalHeader(
                    dbc.Row(dbc.ModalTitle("Add Presenter Into Dropdown Options")),
                style=mod_style), 
                dbc.ModalBody(
                    [
                    html.H6("* Indicates required field", style={"color": "#d9534f", "font-style": "italic"}),
                    dbc.Alert('Please supply required fields.', color="danger", id='p_add_inputs_alert', is_open=False),
                    dbc.Alert('Presenter successfully added to database. Please reload page to reflect added presenter in options.', color="success", id='p_add_success_alert', is_open=False),
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
                                dbc.Textarea(id="form_p_add_author_fn", placeholder="Enter presenter's first name/initials"), 
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
                                dbc.Textarea(id="form_p_add_author_ln", placeholder="Enter presenter's last name"), 
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
                                dbc.Textarea(id="form_p_add_author_mail", placeholder="Enter presenter's email"), 
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
                                dbc.Textarea(id="form_p_add_author_contact", placeholder="Enter presenter's contact number"), 
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
                                    dcc.Dropdown(id='form_p_add_author_up_aff_dropdown', optionHeight=60, placeholder="UP Affiliation"),
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
                                                    dbc.Label("Specify Other Affiliation", id = 'form_p_up_aff_others_label'), 
                                                    dbc.Label("*", style={"color": "#d9534f", "font-style": "bold"}),
                                                ],
                                                width=5
                                            ),  
                                            dbc.Col( 
                                                dbc.Input( 
                                                    type="text", id="form_p_up_aff_others", placeholder="Please specify affiliation." 
                                                ),
                                                width = 7
                                            ),
                                        ]
                                    ),
                                    id="form_p_up_aff_others_div"
                                ),
                    # UPD Unit Dropdown
                    html.Div(
                            dbc.Row( 
                                [ 
                                    dbc.Col(
                                        [
                                            dbc.Label("UP Diliman Unit", id = 'form_p_upd_unit_label'), 
                                            # dbc.Label("*", style={"color": "#d9534f", "font-style": "bold"}),
                                        ],
                                        width=5
                                    ),  
                                    dbc.Col( 
                                        html.Div( 
                                            dcc.Dropdown( 
                                                id='form_p_upd_unit_dropdown', clearable=True, searchable=True, placeholder="UP Diliman Unit"
                                            ),
                                            className="dash-bootstrap" 
                                        ), 
                                    ), 
                                ], 
                                className="mb-3", 
                            ),
                            id = 'form_p_upd_unit_div'
                        ),
                    # UPD Engineering Department Dropdown
                    html.Div(
                            dbc.Row( 
                                [ 
                                    dbc.Col(
                                        [
                                            dbc.Label("UPD Engineering Department", id = 'form_p_engg_dept_label'), 
                                            # dbc.Label("*", style={"color": "#d9534f", "font-style": "bold"}),
                                        ],
                                        width=5
                                    ),  
                                    dbc.Col( 
                                        html.Div( 
                                            dcc.Dropdown( 
                                                id='form_p_engg_dept_dropdown',clearable=True, searchable=True, placeholder="UPD Engineering Department"
                                            ),
                                            className="dash-bootstrap" 
                                        ), 
                                    ), 
                                ], 
                                className="mb-3", 
                            ),
                            id = 'form_p_engg_dept_div'
                        ),
                    # UPD IE Faculty Indication Dropdown
                    html.Div(
                            dbc.Row( 
                                [ 
                                    dbc.Col(
                                        [
                                            dbc.Label("UPD IE Faculty Indication", id = 'form_p_iefacind_label'), 
                                            # dbc.Label("*", style={"color": "#d9534f", "font-style": "bold"}, id='authorprof_iefacind_star'),
                                        ],
                                        width=5
                                    ),  
                                    dbc.Col( 
                                        [
                                            html.Div( 
                                                dcc.Dropdown( 
                                                    id='form_p_iefacind_dropdown', 
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
                            id = 'form_p_iefacind_div'
                        ), 
                    ]
                ),
                dbc.ModalFooter( 
                    dbc.Button('Submit', color='danger', id='form_p_submit_author_submitbtn') 
                ),           
            ], 
            centered=True, 
            id="form_p_add_author_modal", 
            is_open=False, 
            size = "lg"
        ), 
    ] 
) 

#Load Dropwdown Options and delete record style
@app.callback(
     [
        Output('form_p_toload2', 'data'), 
        Output('form_p_removerecord_div2', 'style'),
        Output ('form_p_pres', 'options'), 
        Output ('form_p_tag2', 'options') ,
        Output('form_p_add_author_up_aff_dropdown', 'options')
    ], 
    [
        Input('url', 'pathname'),
        Input ('form_p_pres', 'value'),
    ], 
    [
        State('url', 'search'),
        State('currentuserid', 'data'), 
        
    ] 
)
def form_a_load_dropdown(pathname, pres, search, currentuserid): 
    if pathname == '/form_presentations': 
        sql_presenter = """ SELECT
            DISTINCT (author_fn ||' '|| author_ln) as label, author_id as value,
			author_user_id
            from authors
            WHERE not author_delete_ind
				ORDER BY authors.author_user_id 
        """
        values_presenter = []
        
        cols_presenter = ['label', 'value', 'faculty_ind']
        presenter_involved = db.querydatafromdatabase(sql_presenter, values_presenter, cols_presenter)

        presenter_opts = presenter_involved.to_dict('records')

        sql_tags = """SELECT DISTINCT (tag_title) AS label, tag_id AS value 
            from tags 
            WHERE tag_sub = 'P' and not tag_delete_ind 
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
    return(to_load, removerecord_div, presenter_opts, tag_options, up_aff_options)  

# UP Criteria Style       
@app.callback(
    [
        Output('form_p_up_aff_others_div', 'style'),
        Output('form_p_upd_unit_div', 'style'),
        Output('form_p_engg_dept_div', 'style'),
        Output('form_p_iefacind_div', 'style'),
    ], 
    [
        Input('url', 'pathname'), 
        Input('form_p_add_author_up_aff_dropdown', 'value'),
        Input('form_p_upd_unit_dropdown', 'value'),
        Input('form_p_engg_dept_dropdown', 'value'),
    ]
)
def facinddiv (pathname, up_aff, upd_unit, engg_dept): 
    if pathname == '/form_presentations':
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
        Output('form_p_up_aff_dropdown', 'options'),
    ],
    [
        Input('url', 'pathname'),
    ]
) 
def loadcons(pathname):
    if pathname == '/form_presentations':
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
        Output('form_p_upd_unit_dropdown', 'options'),
    ],
    [
        Input('url', 'pathname'),
    ]
) 
def loadupdunits(pathname):
    if pathname == '/form_presentations':
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
        Output('form_p_engg_dept_dropdown', 'options'),
    ],
    [
        Input('url', 'pathname'),
    ]
) 
def loadenggdept(pathname):
    if pathname == '/form_presentations':
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
@app.callback (
    [
        Output('form_p_pres', 'value'),
        Output('form_p_tag2', 'value'),
        Output('form_p_title2', 'value'),
        Output('form_p_conf2', 'value'),
        Output('form_p_loc2', 'value'),
        Output('form_p_start_date2', 'date'),
        Output('form_p_end_date2', 'date'),
        Output('form_p_addinfo2', 'value'), 
        Output('form_p_loadonce', 'data')
    ], 
    [
        Input('form_p_toload2' , 'modified_timestamp')
    ], 
    [
        State('form_p_toload2', 'data'),
        State('url', 'search'), 
        State('form_p_loadonce', 'data')
    ]
)
def form_p_load (timestamp, to_load, search, loadonce): 
    parsed = urlparse(search)
    mode = parse_qs(parsed.query)['mode'][0]
    to_load = 1 if mode == 'edit' else 0
    
    if loadonce == 1: 
        if to_load == 1: 
            form_p_sql = """SELECT distinct presentations.pub_id,
                (select string_agg(author_name, ', ')
                from pres_authors
                where pres_authors.pub_id = presentations.pub_id
                ) as p_authors, 
                publications.tag_id,
                publications.pub_title, 
                presentations.p_conf, 
                presentations.p_loc, 
                presentations.p_start_date, 
                presentations.p_end_date,
                presentations.p_add_info 
            FROM presentations 
                INNER JOIN publications on presentations.pub_id = publications.pub_id
                LEFT OUTER JOIN pres_authors on publications.pub_id = pres_authors.pub_id
            WHERE
                publications.pub_delete_ind = false
                and presentations.pub_id = %s
            ORDER BY presentations.pub_id
            """
            
            parsed = urlparse(search)
            form_p_id = parse_qs(parsed.query)['id'][0]
            form_p_val = [int(form_p_id)]
            form_p_colname = ['form_p_pub_id',
                            'form_p_pres',
                            'form_p_tag_id', 'form_p_pub_title',
                            'form_p_conf', 'form_p_loc', 'form_p_start_date', 'form_p_end_date', 'form_p_add_info']
            form_p_df = db.querydatafromdatabase(form_p_sql, form_p_val, form_p_colname)

            form_p_pres_sql = """SELECT distinct p_author_id
                from
                    presentations
                where
                    p_author_id in (SELECT distinct p_author_id
                                    from pres_authors
                                    where pres_authors.pub_id = presentations.pub_id)
                    and presentations.pub_id = %s"""
            form_p_pres_val = [int(form_p_id)]
            form_p_pres_cols = ['p_pres_ids']
            form_p_pres_df = db.querydatafromdatabase(form_p_pres_sql, form_p_pres_val, form_p_pres_cols)

            form_p_pres = []
            for i in range(len(form_p_pres_df['p_pres_ids'])): 
                form_p_pres.append(form_p_pres_df['p_pres_ids'][i])

            form_p_pub_id = form_p_df['form_p_pub_id'][0]
            form_p_tag_id = form_p_df['form_p_tag_id'][0]
            form_p_pub_title = form_p_df['form_p_pub_title'][0]
            form_p_conf = form_p_df['form_p_conf'][0]
            form_p_loc = form_p_df['form_p_loc'][0]
            form_p_start_date = form_p_df['form_p_start_date'][0]
            form_p_end_date = form_p_df['form_p_end_date'][0]
            form_p_add_info = form_p_df['form_p_add_info'][0]
        else: 
            raise PreventUpdate
        loadonce += 1
        print("loadonce:", loadonce)  # Check the updated value of loadonce
    else: 
        raise PreventUpdate
    return [form_p_pres, form_p_tag_id, form_p_pub_title, 
            form_p_conf, form_p_loc, form_p_start_date, form_p_end_date, 
            form_p_add_info, loadonce]

#Add Presentation Submit Process   
@app.callback(
    [
        Output('form_p_add_author_modal', 'is_open'),
        Output('form_p_modal2', 'is_open'), 
        Output('form_p_feedback_message2', 'children'), 
        Output('form_p_closebtn2', 'href'), 
        Output('p_inputs_alert2', 'is_open')
    ], 
    [
        Input('form_p_add_author_btn', 'n_clicks'),
        Input('form_p_submitbtn2', 'n_clicks'), 
        Input('form_p_closebtn2', 'n_clicks')
    ], 
    [
        State('form_p_pres', 'value'),
        State('form_p_tag2', 'value'),
        State('form_p_title2', 'value'),
        State('form_p_conf2', 'value'),
        State('form_p_loc2', 'value'),
        State('form_p_start_date2', 'date'),
        State('form_p_end_date2', 'date'),
        State('form_p_addinfo2', 'value'), 
        State('url', 'search' ),
        State('form_p_removerecord2', 'value'), 
        State('currentuserid', 'data')
    ]
)
def form_p_submitprocess (addauthor_btn, submit_btn, close_btn, p_pres,
                          p_tag, p_title, p_conf, 
                          p_loc, p_start_date, p_end_date, p_addinfo, search, removerecord, cuser_id):
    
    ctx = dash.callback_context
    if ctx.triggered: 
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]
        addauthoropenmodal = False
        openmodal = False 
        feedbackmessage  = ' '
        all_inputsalert = False
        okay_href = None 
    else: 
        raise PreventUpdate
    
    if eventid == 'form_p_add_author_btn' and addauthor_btn: 
        addauthoropenmodal = True
    elif eventid == 'form_p_submitbtn2' and submit_btn: 
        inputs = [
            p_pres, 
            p_tag,
            p_title, 
            p_conf, 
            # p_loc, 
            p_start_date, 
            p_end_date, 
            # p_addinfo
        ]
        
        if not all(inputs): 
            all_inputsalert = True
        else: 
            openmodal = True 
            parsed = urlparse(search)
            mode = parse_qs(parsed.query)['mode'][0]

            p_sqlcode_modifiedby = """SELECT
            user_id,
            user_un
            FROM users
            """
            p_vals_modifiedby = []
            p_cols_modifiedby = ['id', 'un']
            p_username = db.querydatafromdatabase(p_sqlcode_modifiedby, p_vals_modifiedby, p_cols_modifiedby)

            p_username_modifier = ""
            for i in range(len(p_username['id'])):
                if int(p_username['id'][i]) == cuser_id:
                    p_username_modifier = p_username['un'][i]

            p_timestamp = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            p_timestamp_time = dt.datetime.strptime(p_timestamp,'%Y-%m-%d %H:%M:%S')

            if mode == "add":   
                sql_max_inquiry  = """SELECT MAX(pub_id) from publications
                """
                sql_max_val = []
                max_colname = ['max']
                pub_max_value_db = db.querydatafromdatabase (sql_max_inquiry, sql_max_val, max_colname)
                sql_pub_max = int(pub_max_value_db['max'][0]) + 1
                
                form_p_sqlcode_add_publications = """INSERT INTO publications(
                    pub_id, 
                    tag_id, 
                    pub_title, 
                    pub_delete_ind, 
                    pub_last_upd,
                    modified_by
                )
                VALUES (%s, %s, %s, %s, %s, %s)
                """
                form_p_values_addpub = [sql_pub_max, p_tag, p_title, False, p_timestamp_time, p_username_modifier]
                db.modifydatabase(form_p_sqlcode_add_publications, form_p_values_addpub)
                
                if p_pres == None:
                    p_pres = []
                if type(p_pres) == int: 
                    p_pres = [p_pres]
                
                # PRESENTER ADD
                for i in range(len(p_pres)): 
                    sql_pres = """INSERT INTO pres_authors(
                        pub_id, 
                        p_author_id 
                    )
                    VALUES (%s, %s)
                    """
                    pres_values = [sql_pub_max, p_pres[i]]
                    db.modifydatabase(sql_pres, pres_values)

                    sql_pres_upd = """UPDATE pres_authors
                        SET
                        author_name = (SELECT author_fn || ' ' || author_ln FROM authors WHERE p_author_id=author_id)
                        WHERE p_author_id > 0;
                    """
                    val_pres_upd = []
                    db.modifydatabase(sql_pres_upd, val_pres_upd)
                
                    form_p_sqlcode_add_presentations = """INSERT INTO presentations(
                        pub_id, 
                        p_author_id, 
                        p_conf, 
                        p_loc, 
                        p_start_date,
                        p_end_date, 
                        p_add_info, 
                        p_year, 
                        p_date_range
                    )
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s )
                    """
                    
                    str_to_date = datetime.strptime(p_end_date, '%Y-%m-%d').date()
                    p_year = str_to_date.year
                    p_date_range = str(p_start_date + ' ' + p_end_date )

                    form_p_values_addpresentations = [sql_pub_max, p_pres[i], p_conf, p_loc, p_start_date, p_end_date, p_addinfo, p_year, p_date_range]
                    db.modifydatabase(form_p_sqlcode_add_presentations, form_p_values_addpresentations)
                    
                feedbackmessage = 'Presentation entry added to database.'
                if cuser_id <= 3: 
                    okay_href = '/publications_manage'
                else: 
                    okay_href = '/my_publications'
            
            elif mode == 'edit': 
                parsed = urlparse(search)
                form_p_editmodeid = parse_qs(parsed.query)['id'][0]
                
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
                to_delete =  bool(removerecord)
                
                values_update_publications = [p_tag, p_title, to_delete, p_timestamp_time, p_username_modifier, form_p_editmodeid]
                db.modifydatabase(sql_update_publications,values_update_publications)
                
            #PRESENTER EDIT

                if type(p_pres) == int: 
                    p_pres = [p_pres]
                
                sql_pres_del = """DELETE FROM pres_authors
                    WHERE pub_id = %s """
                pres_values_del = [int(form_p_editmodeid)]
                db.modifydatabase(sql_pres_del, pres_values_del)
                
                for i in range(len(p_pres)): 
                    sql_pres = """INSERT INTO pres_authors(
                        pub_id, 
                        p_author_id
                    )
                    VALUES (%s, %s)
                    """
                    pres_values = [int(form_p_editmodeid), p_pres[i]]
                    db.modifydatabase(sql_pres, pres_values)

                    sql_pres_upd ="""update pres_authors
                        set
                        author_name = (select author_fn || ' ' || author_ln from authors where p_author_id=author_id)
                        where p_author_id>0;
                        """
                    val_pres_upd =[]
                    db.modifydatabase(sql_pres_upd, val_pres_upd)               
                
                    sql_update_presentations = """INSERT INTO presentations 
                        (pub_id,
                        p_author_id, 
                        p_conf, 
                        p_loc, 
                        p_start_date, 
                        p_end_date,
                        p_add_info, 
                        p_year, 
                        p_date_range)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s) 
                    """
                    
                    str_to_date = datetime.strptime(p_end_date, '%Y-%m-%d').date()
                    p_year = str_to_date.year
                    p_date_range = str(p_start_date + ' to ' + p_end_date )
                    
                    values_update_presentations = [int(form_p_editmodeid), p_pres[i], p_conf, p_loc, p_start_date, p_end_date, p_addinfo, p_year, p_date_range]
                    db.modifydatabase(sql_update_presentations, values_update_presentations)
                
                feedbackmessage = 'Presentation details updated.'
                if cuser_id <= 3: 
                    okay_href = '/publications_manage'
                else: 
                    okay_href = '/my_publications'
            else: 
                raise PreventUpdate
    elif eventid == 'form_p_closebtn2' and close_btn: 
        pass
    else: 
        raise PreventUpdate
    return [addauthoropenmodal, openmodal, feedbackmessage, okay_href, all_inputsalert]

#Add Presenter Submit process
@app.callback(
    [
        Output('p_add_inputs_alert', 'is_open'),
        Output('p_add_success_alert', 'is_open'),
    ], 
    [
        Input('form_p_submit_author_submitbtn', 'n_clicks'), 
    ], 
    [
        State('form_p_add_author_fn', 'value'),
        State('form_p_add_author_ln', 'value'),
        State('form_p_add_author_up_aff_dropdown', 'value'),
        State('form_p_up_aff_others', 'value'),
        State('form_p_upd_unit_dropdown', 'value'),
        State('form_p_engg_dept_dropdown', 'value'),
        State('form_p_iefacind_dropdown', 'value'),
        State('form_p_add_author_mail', 'value'),
        State('form_p_add_author_contact', 'value'),
        State('url', 'search' ),
        # State('currentuserid', 'data')
    ]
)
def form_p_submitprocess (add_submit_btn,
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
    
    if eventid == 'form_p_submit_author_submitbtn' and add_submit_btn:     
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
