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
                dcc.Store(id='form_p_toload', storage_type='memory', data=0), 
            ] 
        ), 
        html.H2("Presentation Details"), 
        html.H6("* Indicates required field", style={"color": "#d9534f", "font-style": "italic"}),
        dbc.Alert('Please supply required fields.', color="danger", id='p_inputs_alert', is_open=False),
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
                                    id='form_p_fac', 
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
                            dbc.Label("Criteria"),
                            dbc.Label("*", style={"color": "#d9534f", "font-style": "bold"})
                            ], width=2, style={'display': 'flex', 'align-items': 'center'}
                            ),  
                        dbc.Col( 
                            html.Div( 
                                dcc.Dropdown( 
                                    id='form_p_tag', 
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
                            dbc.Label("Presentation Title"),
                            dbc.Label("*", style={"color": "#d9534f", "font-style": "bold"})
                            ], width=2, style={'display': 'flex', 'align-items': 'center'}
                            ), 
                        dbc.Col( 
                            dbc.Input( 
                                type="text", id="form_p_title", placeholder="Enter title" 
                            ), 
                            width=6, 
                        ), 
                    ], 
                    className="mb-3", 
                ), 
            ],
            id='form_p_gen'
        ),
        # presentations
        html.Div(
            [
                #authors
                dbc.Row( 
                    [ 
                        dbc.Col(
                            [
                            dbc.Label("Presenter/s"),
                            dbc.Label("*", style={"color": "#d9534f", "font-style": "bold"})
                            ], width=2, style={'display': 'flex', 'align-items': 'center'}
                            ), 
                        dbc.Col( 
                            dbc.Input( 
                                type="text", id="form_p_authors", placeholder="Enter all presenter/s or authors of the presentation" 
                            ), 
                            width=6,
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
                            dbc.Input( 
                                type="text", id="form_p_conf", placeholder="Enter conference" 
                            ), 
                            width=6,
                        ), 
                    ], 
                    className="mb-3", 
                ),
                #location
                dbc.Row( 
                    [ 
                        dbc.Label("Location", width=2, style={'display': 'flex', 'align-items': 'center'}), 
                        dbc.Col( 
                            dbc.Input( 
                                type="text", id="form_p_loc", placeholder="Enter location of conference" 
                            ), 
                            width=6,
                        ), 
                    ], 
                    className="mb-3", 
                ),
                #pres year
                # dbc.Row( 
                #     [ 
                #         dbc.Label("Presentation Year", width=2), 
                #         dbc.Col( 
                #             dbc.Input(
                #                 type="text", id="form_p_presyear", placeholder="Enter year of presentation" 
                #             ), 
                #             width=6,
                #         ), 
                #     ], 
                #     className="mb-3", 
                # ),
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
                                id='form_p_start_date',
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
                                id='form_p_end_date',
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
                            dbc.Input( 
                                type="text", id="form_p_addinfo", placeholder="Enter any additional information" 
                            ), 
                            width=6,
                        ), 
                    ], 
                    className="mb-3", 
                )
            ],
            id='form_p'
            
        ),
        html.Div( 
            dbc.Row( 
                [ 
                    dbc.Label("Wish to delete?", width=2), 
                    dbc.Col( 
                        dbc.Checklist( 
                            id='form_p_removerecord', 
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
            id = 'form_p_removerecord_div' 
        ), 
        html.Hr(), 
        dbc.Button('Submit', color='danger', id='form_p_submitbtn'), 
        dbc.Modal( 
            [    
                dbc.ModalHeader(dbc.ModalTitle("Saving Progress"), style=mod_style), 
                dbc.ModalBody("tempmessage", id='form_p_feedback_message'), 
                dbc.ModalFooter( 
                    dbc.Button("Okay", color='secondary', id="form_p_closebtn", className="ms-auto", n_clicks=0) 
                ),           
            ], 
            centered=True, 
            id="form_p_modal", 
            is_open=False, 
        ),  
    ] 
) 


@app.callback (
    [
        Output('form_p_toload', 'data'), 
        Output('form_p_removerecord_div', 'style'),
        Output ('form_p_fac', 'options'), 
        Output ('form_p_tag', 'options')
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
    if pathname == '/form_presentations': 
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
    else: 
         raise PreventUpdate 
    return(to_load, removerecord_div,faculty_opts,tag_options )

@app.callback (
    [
        Output('form_p_fac', 'value'),
        Output('form_p_tag', 'value'),
        Output('form_p_title', 'value'),
        Output('form_p_authors', 'value'),
        Output('form_p_conf', 'value'),
        Output('form_p_loc', 'value'),
        Output('form_p_start_date', 'date'),
        Output('form_p_end_date', 'date'),
        Output('form_p_addinfo', 'value')
    ], 
    [
        Input('form_p_toload' , 'modified_timestamp')
    ], 
    [
        State('form_p_toload', 'data'),
        State('url', 'search')
    ]
)

def form_p_load (timestamp, to_load, search): 
    if to_load == 1: 
        form_p_sql = """SELECT 
            publications.pub_id,
			publications.user_id,
			publications.tag_id,
            publications.pub_title, 
            presentations.p_authors, 
            presentations.p_conf, 
            presentations.p_loc, 
            presentations.p_start_date, 
            presentations.p_end_date,
            presentations.p_add_info 
        FROM publications 
            INNER JOIN faculty on publications.user_id = faculty.user_id 
            INNER JOIN presentations on publications.pub_id = presentations.pub_id 
        WHERE 
            publications.pub_delete_ind = false
		ORDER BY publications.pub_id
        """
        
        parsed = urlparse(search)
        form_p_id = parse_qs(parsed.query)['id'][0]
        
        form_p_val = []
        form_p_colname = ['form_p_pub_id', 'form_p_user_id', 'form_p_tag_id', 
                          'form_p_pub_title', 'form_p_authors', 'form_p_conf', 
                          'form_p_loc', 'form_p_start_date', 'form_p_end_date', 
                          'form_p_add_info']
        form_p_df = db.querydatafromdatabase(form_p_sql, form_p_val, form_p_colname)
        
        counter = 0 
        counted = 0
        for i in range(len(form_p_df)): 
            if form_p_df['form_p_pub_id'][i] != int(form_p_id): 
                form_p_df = form_p_df.drop(i)
            else: 
                counted = counter 
            counter += 1

        form_p_pub_id = form_p_df['form_p_pub_id'][counted]
        form_p_user_id = form_p_df['form_p_user_id'][counted]
        form_p_tag_id = form_p_df['form_p_tag_id'][counted]
        form_p_pub_title = form_p_df['form_p_pub_title'][counted]
        form_p_authors = form_p_df['form_p_authors'][counted]
        form_p_conf = form_p_df['form_p_conf'][counted]
        form_p_loc = form_p_df['form_p_loc'][counted]
        form_p_start_date = form_p_df['form_p_start_date'][counted]
        form_p_end_date = form_p_df['form_p_end_date'][counted]
        form_p_add_info = form_p_df['form_p_add_info'][counted]
    
    else: 
        raise PreventUpdate
    return [form_p_user_id, form_p_tag_id, form_p_pub_title, form_p_authors, 
            form_p_conf, form_p_loc, form_p_start_date,  form_p_end_date, 
            form_p_add_info]
    
@app.callback(
    [
        Output('form_p_modal', 'is_open'), 
        Output('form_p_feedback_message', 'children'), 
        Output('form_p_closebtn', 'href'), 
        Output('p_inputs_alert', 'is_open')
    ], 
    [
        Input('form_p_submitbtn', 'n_clicks'), 
        Input('form_p_closebtn', 'n_clicks')
    ], 
    [
        State('form_p_fac', 'value'),
        State('form_p_tag', 'value'),
        State('form_p_title', 'value'),
        State('form_p_authors', 'value'),
        State('form_p_conf', 'value'),
        State('form_p_loc', 'value'),
        State('form_p_start_date', 'date'),
        State('form_p_end_date', 'date'),
        State('form_p_addinfo', 'value'), 
        State('url', 'search' ),
        State('form_p_removerecord', 'value'), 
        State('currentuserid', 'data')
    ]
)

def form_p_submitprocess (submit_btn, close_btn, p_faculty, 
                          p_tag, p_title, p_authors, p_conf, 
                          p_loc, p_start_date, p_end_date, p_addinfo, search, removerecord, cuser_id):
    
    ctx = dash.callback_context
    if ctx.triggered: 
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]
        openmodal = False 
        feedbackmessage  = ' '
        all_inputsalert = False
        okay_href = None 
    else: 
        raise PreventUpdate
    
    if eventid == 'form_p_submitbtn' and submit_btn: 
        
        inputs = [
            p_faculty, 
            p_tag,
            p_title, 
            p_authors, 
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
                    user_id, 
                    tag_id, 
                    pub_title, 
                    pub_delete_ind, 
                    pub_last_upd,
                    modified_by
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                """
                form_p_values_addpub = [sql_pub_max, p_faculty, p_tag, p_title, False, p_timestamp_time, p_username_modifier]
                db.modifydatabase(form_p_sqlcode_add_publications, form_p_values_addpub)
                
                form_p_sqlcode_add_presentations = """INSERT INTO presentations(
                    pub_id, 
                    p_authors, 
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

                form_p_values_addpresentations = [sql_pub_max, p_authors, p_conf, p_loc, p_start_date, p_end_date, p_addinfo, p_year, p_date_range]
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
                
                values_update_publications = [p_faculty, p_tag, p_title, to_delete, p_timestamp_time, p_username_modifier, form_p_editmodeid]
                db.modifydatabase(sql_update_publications,values_update_publications)
                
                sql_update_presentations = """UPDATE presentations
                SET 
                    p_authors = %s, 
                    p_conf = %s, 
                    p_loc = %s, 
                    p_start_date = %s, 
                    p_end_date = %s,
                    p_add_info = %s, 
                    p_year = %s, 
                    p_date_range = %s
                WHERE
                    pub_id = %s
                """
                
                str_to_date = datetime.strptime(p_end_date, '%Y-%m-%d').date()
                p_year = str_to_date.year
                p_date_range = str(p_start_date + ' to ' + p_end_date )
                
                values_update_presentations = [p_authors, p_conf, p_loc, p_start_date, p_end_date, p_addinfo, p_year, p_date_range, form_p_editmodeid]
                db.modifydatabase(sql_update_presentations, values_update_presentations)
                feedbackmessage = 'Presentation datials updated.'
                if cuser_id <= 3: 
                    okay_href = '/publications_manage'
                else: 
                    okay_href = '/my_publications'
            
                
            else: 
                raise PreventUpdate
    elif eventid == 'form_p_closebtn' and close_btn: 
        pass
    else: 
        raise PreventUpdate
    return [openmodal, feedbackmessage, okay_href, all_inputsalert]
