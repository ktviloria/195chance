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
        dbc.Alert('Please supply required fields.', color="danger", id='p_inputs_alert2', is_open=False),
        html.Hr(), 
        # General pub info needed
        html.Div(
            [
                #Faculty involved
                dbc.Row( 
                    [   
                        dbc.Col(
                            [
                            dbc.Label("Presentation Role"),
                            dbc.Label("*", style={"color": "#d9534f", "font-style": "bold"})
                            ], width=2, style={'display': 'flex', 'align-items': 'center'}
                        ), 
                        dbc.Col( 
                            html.Div( 
                                dcc.Dropdown( 
                                    options=[
                                            {'label': 'Presenter', 'value': 'Presenter'},
                                            {'label': 'Co-Presenter', 'value': 'Co-Presenter'}
                                        ], 
                                    id= 'form_prole_fac2', 
                                ),
                                className="dash-bootstrap" 
                            ), 
                            width=4,
                        ), 
                        dbc.Col(
                            [
                            dbc.Label("Faculty Involved"),
                            dbc.Label("*", style={"color": "#d9534f", "font-style": "bold"})
                            ], width=2, style={'display': 'flex', 'align-items': 'center'}
                            ), 
                        dbc.Col( 
                            html.Div( 
                                dcc.Dropdown( 
                                    id= 'form_p_fac2', 
                                ),
                                className="dash-bootstrap" 
                            ), 
                            width=4,
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
                            dbc.Textarea( 
                                #type="text", 
                                id="form_p_title2", placeholder="Enter publication title" 
                            ), 
                            width=6, 
                        ), 
                    ], 
                    className="mb-3", 
                ), 
            ],
            id='form_p_gen2'
        ),
        # presentations
        html.Div(
            [
                #authors
                dbc.Row( 
                    [ 
                        dbc.Col(
                            [
                            dbc.Label("Authors"),
                            dbc.Label("*", style={"color": "#d9534f", "font-style": "bold"})
                            ], width=2, style={'display': 'flex', 'align-items': 'center'}
                            ), 
                        dbc.Col( 
                            dbc.Textarea( 
                                #type="text", 
                                id="form_p_authors2", placeholder="Enter all authors of presentation/publication" 
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
                            dbc.Textarea( 
                                #type="text", 
                                id="form_p_conf2", placeholder="Enter conference", style={"height":"15px"} 
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
                            dbc.Textarea( 
                                #type="text", 
                                id="form_p_loc2", placeholder="Enter location of conference", style={"height":"15px"}  
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
                            width=6,
                        ), 
                    ], 
                    className="mb-3", 
                )
            ],
            id='form_p2'
            
        ),
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
    ] 
) 

@app.callback(
     [
        Output('form_p_toload2', 'data'), 
        Output('form_p_removerecord_div2', 'style'),
        Output ('form_p_fac2', 'options'), 
        Output ('form_p_tag2', 'options') 
    ], 
    [
        Input('url', 'pathname'), 
        Input('form_prole_fac2', 'value')
    ], 
    [
        State('url', 'search'),
        State('currentuserid', 'data'), 
        
    ] 
)

def form_a_load_dropdown(pathname, role,  search, currentuserid): 
    if pathname == '/form_presentations': 
        sql_faculty_involved = """ SELECT DISTINCT (faculty.faculty_fn ||' '|| faculty.faculty_ln) as label, user_id as value
            from faculty
            WHERE not faculty_delete_ind  and faculty_active_ind = true 
            ORDER BY value 
        """
        values_faculty = []
        cols_faculty = ['label', 'value']
        faculty_involved = db.querydatafromdatabase(sql_faculty_involved,values_faculty, cols_faculty)
        
        if currentuserid > 3 and role == 'Presenter':
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


@app.callback(
        Output('form_p_fac2', 'multi'),
     
    [
        Input('form_prole_fac2', 'value'), 
        Input('url', 'pathname')
    ]
)
def multi_fac (role, pathname): 
    if pathname == '/form_presentations': 
        if role == "Co-Presenter": 
            multi = True 
        else: 
            multi = False
    else: 
        raise PreventUpdate
    return (multi)    


@app.callback (
    [
        Output('form_p_fac2', 'value'),
        Output('form_prole_fac2', 'value'), 
        Output('form_p_tag2', 'value'),
        Output('form_p_title2', 'value'),
        Output('form_p_authors2', 'value'),
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
    if loadonce == 1: 
        if to_load == 1: 
            form_p_sql = """SELECT 
                publications.pub_id,
                publications.tag_id,
                publications.pub_title, 
                presentations.p_authors, 
                presentations.p_conf, 
                presentations.p_loc, 
                presentations.p_start_date, 
                presentations.p_end_date,
                presentations.p_add_info 
            FROM publications 
                LEFT OUTER JOIN faculty on publications.user_id = faculty.user_id 
				LEFT OUTER JOIN presentations on presentations.pub_id = publications.pub_id            WHERE 
                publications.pub_delete_ind = false
                and publications.pub_id = %s
            ORDER BY publications.pub_id
            """
            
            parsed = urlparse(search)
            form_p_id = parse_qs(parsed.query)['id'][0]
            
            form_p_val = [int(form_p_id)]
            form_p_colname = ['form_p_pub_id', 'form_p_tag_id', 
                            'form_p_pub_title', 'form_p_authors', 'form_p_conf', 
                            'form_p_loc', 'form_p_start_date', 'form_p_end_date', 
                            'form_p_add_info']
            form_p_df = db.querydatafromdatabase(form_p_sql, form_p_val, form_p_colname)
            
            form_p_us = """SELECT 
                presentations_users.user_id, 
                presentations_users.pres_role
                
            
            FROM presentations_users
            WHERE presentations_users.pub_id = %s
            """
            
            presenters = []
            form_p_us_val = [int(form_p_id)]
            form_p_us_col = ['user_ids', 'roles']
            form_p_us_df = db.querydatafromdatabase(form_p_us,  form_p_us_val, form_p_us_col)
            
            
            if form_p_us_df['roles'][0] == 'Co-Presenter': 
                if len(form_p_us_df['user_ids']) > 1: 
                    for i in range(len(form_p_us_df['user_ids'])): 
                        presenters.append(form_p_us_df['user_ids'][i])
 
                else: 
                    pass
            else: 
                pass
            
            form_p_role = form_p_us_df['roles'][0]
            if len(form_p_us_df['user_ids']) > 1:
                form_p_presenters = presenters
            else: 
                form_p_presenters = form_p_us_df['user_ids'][0]
            
            

            form_p_pub_id = form_p_df['form_p_pub_id'][0]
            form_p_tag_id = form_p_df['form_p_tag_id'][0]
            form_p_pub_title = form_p_df['form_p_pub_title'][0]
            form_p_authors = form_p_df['form_p_authors'][0]
            form_p_conf = form_p_df['form_p_conf'][0]
            form_p_loc = form_p_df['form_p_loc'][0]
            form_p_start_date = form_p_df['form_p_start_date'][0]
            form_p_end_date = form_p_df['form_p_end_date'][0]
            form_p_add_info = form_p_df['form_p_add_info'][0]
        else: 
            raise PreventUpdate
        loadonce +=1
    else: 
        raise PreventUpdate    
    return [form_p_presenters, form_p_role, form_p_tag_id, form_p_pub_title, form_p_authors, 
            form_p_conf, form_p_loc, form_p_start_date,  form_p_end_date, 
            form_p_add_info, loadonce]
    
@app.callback(
    [
        Output('form_p_modal2', 'is_open'), 
        Output('form_p_feedback_message2', 'children'), 
        Output('form_p_closebtn2', 'href'), 
        Output('p_inputs_alert2', 'is_open')
    ], 
    [
        Input('form_p_submitbtn2', 'n_clicks'), 
        Input('form_p_closebtn2', 'n_clicks')
    ], 
    [
        State('form_p_fac2', 'value'),
        State('form_prole_fac2', 'value'), 
        State('form_p_tag2', 'value'),
        State('form_p_title2', 'value'),
        State('form_p_authors2', 'value'),
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

def form_p_submitprocess (submit_btn, close_btn, p_faculty, p_role,
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
    
    if eventid == 'form_p_submitbtn2' and submit_btn: 
        
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
                
                
                if type(p_faculty) == int: 
                    p_faculty = [p_faculty]
                
                for i in range(len(p_faculty)): 
                    sql_presentations_users = """INSERT INTO presentations_users(
                        pub_id, 
                        user_id, 
                        pres_role
                    )
                    VALUES (%s, %s, %s)
                    """
                    
                    presentations_users_values = [sql_pub_max, p_faculty[i], p_role]
                    db.modifydatabase(sql_presentations_users, presentations_users_values)
                
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
                
                if type(p_faculty) == int: 
                    p_faculty = [p_faculty]
                
                sql_presentations_users_del = """DELETE FROM presentations_users
                    WHERE pub_id = %s 
                """
                presentations_users_values_del = [int(form_p_editmodeid) ]
                db.modifydatabase(sql_presentations_users_del,presentations_users_values_del)
                
                for i in range(len(p_faculty)): 
                    sql_presentations_users = """INSERT INTO presentations_users(
                        pub_id, 
                        user_id, 
                        pres_role
                    )
                    VALUES (%s, %s, %s)
                    """
                    
                    presentations_users_values = [int(form_p_editmodeid), p_faculty[i], p_role]
                    db.modifydatabase(sql_presentations_users, presentations_users_values)                
                
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
    elif eventid == 'form_p_closebtn2' and close_btn: 
        pass
    else: 
        raise PreventUpdate
    return [openmodal, feedbackmessage, okay_href, all_inputsalert]
