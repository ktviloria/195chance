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
from dateutil import relativedelta
 
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
                dcc.Store(id='form_r_toload', storage_type='memory', data=0), 
            ] 
        ), 
        html.H2("Project Details"), 
        html.H6("* Indicates required field", style={"color": "#d9534f", "font-style": "italic"}),
        dbc.Alert('Please supply required fields.', color="danger", id='r_inputs_alert', is_open=False),
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
                                    id='form_r_fac', multi = True 
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
                                    id='form_r_tag', optionHeight=60
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
                                id="form_r_title", placeholder="Enter publication title" 
                            ), 
                            width=6, 
                        ), 
                    ], 
                    className="mb-3", 
                ), 
            ],
            id='form_r_gen'
        ),
        html.Div(
            dbc.Row( 
                [   
                    dbc.Col(
                        [
                        dbc.Label("Role"),
                        ], width=2, style={'display': 'flex', 'align-items': 'center'}
                        ), 
                    dbc.Col( 
                        dbc.Input( 
                            type="text", id="form_r_role", placeholder="Enter role in project" 
                        ), 
                        width=6,
                    ), 
                ], 
                className="mb-3", 
            ), id = 'r_role_div'
            ), 
        
        # projects
        html.Div(
            [
                #roles
                
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
                                id='form_r_start_date',
                                placeholder="MM/DD/YYYY",
                                display_format="MM/DD/YYYY",
                                min_date_allowed=date(2014, 1, 1),
                                max_date_allowed=date.today(),
                                initial_visible_month=date.today(),
                                #note: I couldn't adjust the width of the box to fit the placeholder
                            ), className="DateInput_input_1"
                                    #html.Div(id='output-container-date-picker-range')
                                #type="text", id="form_r_presdate", placeholder="Enter date(s) of presentation YYYY or MM/DD/YYYY" 
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
                                id='form_r_end_date',
                                placeholder="MM/DD/YYYY",
                                display_format="MM/DD/YYYY",
                                min_date_allowed=date(2014, 1, 1),
                                max_date_allowed=date.today(),
                                initial_visible_month=date.today(),
                                #note: I couldn't adjust the width of the box to fit the placeholder
                            ), className="DateInput_input_1"
                                    #html.Div(id='output-container-date-picker-range')
                                #type="text", id="form_r_presdate", placeholder="Enter date(s) of presentation YYYY or MM/DD/YYYY" 
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
                #             id='r_date_range',
                #             min_date_allowed=date(2014, 1, 1),
                #             max_date_allowed=date.today(),
                #             initial_visible_month=date.today(),
                #             start_date_placeholder_text="MM/DD/YYYY",
                #             end_date_placeholder_text="MM/DD/YYYY",
                #                 #note: I couldn't adjust the width of the box to fit the placeholder
                #             ),
                #                     #html.Div(id='output-container-date-picker-range')
                #                 #type="text", id="form_r_presdate", placeholder="Enter date(s) of presentation YYYY or MM/DD/YYYY" 
                #         ), 
                #     ], 
                #     className="mb-3", 
                # ),
                #fund org
                dbc.Row( 
                    [ 
                        dbc.Label("Funding Organization", width=2, style={'display': 'flex', 'align-items': 'center'}), 
                        dbc.Col( 
                            dbc.Textarea(
                                #type="text", 
                                id="form_r_fundorg", placeholder="Enter funding organization", style={"height":"15px"} 
                            ), 
                            width=6,
                        ), 
                    ], 
                    className="mb-3", 
                ),
                
            ],
            id='form_r'
        ),
        html.Div( 
                dbc.Row( 
                    [ 
                        dbc.Label("Link to Copy of Contract", width=2, style={'display': 'flex', 'align-items': 'center'}), 
                        dbc.Col( 
                            dbc.Textarea(
                                #type="text", 
                                id="form_r_contract_link", placeholder="Please save link to GDrive and insert link here",
                                style={"min-height":"80px"}
                                #style={"height":"15px"} 
                            ), 
                            width=6,
                        ), 
                    ], 
                    className="mb-3", 
                ), id = 'r_contract_div'), 
        html.Div( 
            dbc.Row( 
                [ 
                    dbc.Label("Wish to delete?", width=2), 
                    dbc.Col( 
                        dbc.Checklist( 
                            id='form_r_removerecord', 
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
            id = 'form_r_removerecord_div' 
        ), 
        html.Hr(), 
        dbc.Button('Submit', color='danger', id='form_r_submitbtn'), 
        dbc.Modal( 
            [    
                dbc.ModalHeader(dbc.ModalTitle("Saving Progress"), style=mod_style), 
                dbc.ModalBody("tempmessage", id='form_r_feedback_message'), 
                dbc.ModalFooter( 
                    dbc.Button("Okay", color='secondary', id="form_r_closebtn", className="ms-auto", n_clicks=0) 
                ),           
            ], 
            centered=True, 
            id="form_r_modal", 
            is_open=False, 
        ),  
    ]
)   


@app.callback (
    [
        Output('r_role_div', 'style'), 
        Output('r_contract_div', 'style'), 
    ], 
    [
        Input('url', 'pathname'), 
    ], 
    [
        State('currentuserid', 'data'),
        State('url', 'search')
    ]
)

def loaddivs (pathname, currentuserid, search): 
    if pathname == '/form_projects':
        parsed = urlparse(search)
        mode = parse_qs(parsed.query)['mode'][0]
    if pathname == '/form_projects' and currentuserid <3 and mode != 'edit':  
        removethis = {'display': 'none'}
    elif pathname == '/form_projects' and currentuserid <3 and mode == 'edit': 
        removethis = None
    else: 
        removethis = None
        
    return[removethis, removethis]
        
@app.callback(

    Output('form_r_fac', 'disabled'), 
    [Input('url', 'pathname')], 
    [State('url', 'search'),]
    
)
def diablefacoptions (pathname, search):
    if pathname == '/form_projects':
        parsed = urlparse(search)
        mode = parse_qs(parsed.query)['mode'][0]
        
        if mode == 'edit': 
            return (True)
        else: 
            raise PreventUpdate
    else: 
        raise PreventUpdate 
    

@app.callback (
    [
        Output('form_r_toload', 'data'), 
        Output('form_r_removerecord_div', 'style'),
        Output ('form_r_fac', 'options'), 
        Output ('form_r_tag', 'options')
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
    if pathname == '/form_projects': 
        sql_faculty_involved = """ SELECT DISTINCT (faculty.faculty_fn ||' '|| faculty.faculty_ln) as label, user_id as value
            from faculty
            WHERE faculty_delete_ind = false and faculty_active_ind = true
            ORDER BY value 
        """
        values_faculty = []
        cols_faculty = ['label', 'value']
        faculty_involved = db.querydatafromdatabase(sql_faculty_involved,values_faculty, cols_faculty)
        
        # if currentuserid > 3:
        # for i in range (len(faculty_involved)): 
        #     if faculty_involved['value'][i] != int (currentuserid): 
        #         faculty_involved = faculty_involved.drop(i)
        #     else: 
        #         pass
        
        faculty_opts = faculty_involved.to_dict('records')
        
        sql_tags = """SELECT DISTINCT (tag_title) AS label, tag_id AS value 
            from tags 
            WHERE tag_sub = 'R' and not tag_delete_ind 
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
        Output('form_r_fac', 'value'),
        Output('form_r_tag', 'value'),
        Output('form_r_title', 'value'),
        Output('form_r_role', 'value'),
        Output('form_r_start_date', 'date'),
        Output('form_r_end_date', 'date'),
        Output('form_r_fundorg', 'value'), 
        Output('form_r_contract_link', 'value')
    ],
    [
        Input('form_r_toload', 'modified_timestamp')
    ],
    [
        State('form_r_toload', 'data'),
        State('url', 'search'), 
        State('currentuserid', 'data')
    ],
)

def form_r_load (timestamp, to_load, search, currentuserid):
    if to_load == 1: 
        form_r_sql = """SELECT 
            publications.pub_id,
            publications.tag_id,
            publications.pub_title,
            projects.r_start_date,
            projects.r_end_date, 
            projects.r_fund_org,
            projects_users.r_roles, 
            projects_users.r_contract_link
            FROM publications 
                LEFT OUTER JOIN faculty on publications.user_id = faculty.user_id 
                RIGHT OUTER JOIN projects on publications.pub_id = projects.pub_id 
                RIGHT OUTER JOIN projects_users on publications.pub_id = projects_users.pub_id
            WHERE 
                publications.pub_delete_ind = false 
            AND publications.pub_id =%s AND projects_users.user_id = %s
			ORDER BY publications.pub_id
        """
    
        parsed = urlparse(search)
        form_r_id = parse_qs(parsed.query)['id'][0]
        form_r_id2 = parse_qs(parsed.query)['key'][0]
        
        form_r_val = [int(form_r_id), int(form_r_id2)]
        form_r_colname = ['form_r_pub_id', 'form_r_tag_id', 
            'form_r_pub_title', 'form_r_start_date', 'form_r_end_date',
            'form_r_fund_org', 'form_r_roles', 'form_r_contract']
        form_r_df = db.querydatafromdatabase(form_r_sql, form_r_val,form_r_colname)

        
        
        form_r_pub_id = form_r_df['form_r_pub_id'][0]
        # form_r_user_id = form_r_df['form_r_user_id'][0]
        form_r_tag_id = form_r_df['form_r_tag_id'][0]
        form_r_pub_title = form_r_df['form_r_pub_title'][0]
        # form_r_roles = form_r_df['form_r_roles'][0]
        form_r_start_date = form_r_df['form_r_start_date'][0]
        form_r_end_date = form_r_df['form_r_end_date'][0]
        form_r_fund_org = form_r_df['form_r_fund_org'][0]
        # form_r_contract_link = form_r_df['contract link'][0]
        form_r_roles = form_r_df['form_r_roles'][0]
        form_r_contract_link = form_r_df['form_r_contract'][0]
        
        form_r_us = """SELECT
            projects_users.user_id, 
            projects_users.r_roles, 
            projects_users.r_contract_link 
        FROM projects_users
        WHERE projects_users.pub_id = %s
        """
        
        form_r_us_val = [int(form_r_id)]
        form_r_us_col = ['userids', 'roles', 'contract']
        form_r_us_df = db.querydatafromdatabase(form_r_us,  form_r_us_val, form_r_us_col)
        
        projec = []
        if len(form_r_us_df['userids']) > 1: 
            for i in range(len(form_r_us_df['userids'])): 
                projec.append(form_r_us_df['userids'][i])
        else: 
            pass
        if len(form_r_us_df['userids']) > 1:
                form_r_user_id = projec
        else: 
            form_r_user_id = form_r_us_df['userids'][0]
        
        # form_r_roles = None
        # form_r_contract_link = None 
        # if currentuserid <= 3: 
        #     form_r_roles = None
        #     form_r_contract_link = None 
        # else: 
        #     for i in range(len(form_r_us_df['userids'])): 
        #         if form_r_us_df['userids'][i] == currentuserid: 
        #             form_r_roles = form_r_us_df['roles'][i]
        #             form_r_contract_link = form_r_us_df['contract'][i]
        #         else: 
        #             pass 
                
            
    
    else: 
        raise PreventUpdate
    return[form_r_user_id, form_r_tag_id, form_r_pub_title, 
           form_r_roles, form_r_start_date, form_r_end_date, 
           form_r_fund_org, form_r_contract_link]

@app.callback (
    [
        Output('form_r_modal', 'is_open'), 
        Output('form_r_feedback_message', 'children'), 
        Output('form_r_closebtn', 'href'), 
        Output('r_inputs_alert', 'is_open')
    ], 
    [
        Input('form_r_submitbtn', 'n_clicks'), 
        Input('form_r_closebtn', 'n_clicks')
    ], 
    [
        State('form_r_fac', 'value'),
        State('form_r_tag', 'value'),
        State('form_r_title', 'value'),
        State('form_r_role', 'value'),
        State('form_r_start_date', 'date'),
        State('form_r_end_date', 'date'),
        State('form_r_fundorg', 'value'),
        State('url', 'search' ),
        State('form_r_removerecord', 'value'), 
        State('form_r_contract_link', 'value'), 
        State('currentuserid', 'data')
    ]
)
     
def form_r_submitprocess(submit_btn, close_btn, r_faculty, r_tag, r_title, 
                         r_role, r_start_date, r_end_date, r_fundorg, search, removerecord, r_contract,  cuser_id): 
    
    ctx = dash.callback_context
    if ctx.triggered: 
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]
        openmodal = False 
        feedbackmessage  = ' '
        all_inputsalert = False
        okay_href = None 
    else: 
        raise PreventUpdate
    
    if eventid == 'form_r_submitbtn' and submit_btn: 
        
        inputs = [
            r_faculty, 
            r_tag, 
            r_title, 
            r_start_date, 
            r_end_date, 
            # r_fundorg
        ]
        
        if not all(inputs): 
            all_inputsalert = True
        else: 
            openmodal = True
            parsed = urlparse(search)
            mode = parse_qs(parsed.query)['mode'][0]
            
            r_sqlcode_modifiedby = """SELECT
            user_id,
            user_un
            FROM users
            """
            r_vals_modifiedby = []
            r_cols_modifiedby = ['id', 'un']
            r_username = db.querydatafromdatabase(r_sqlcode_modifiedby, r_vals_modifiedby, r_cols_modifiedby)
            
            r_username_modifier = ""
            for i in range(len(r_username['id'])):
                if int(r_username['id'][i]) == cuser_id:
                    r_username_modifier = r_username['un'][i]
            
            r_timestamp = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            r_timestamp_time = dt.datetime.strptime(r_timestamp,'%Y-%m-%d %H:%M:%S')
            
            if mode == "add": 
                sql_max_inquiry  = """SELECT MAX(pub_id) from publications
                """
                sql_max_val = []
                max_colname = ['max']
                pub_max_value_db = db.querydatafromdatabase (sql_max_inquiry, sql_max_val, max_colname)
                sql_pub_max = int(pub_max_value_db['max'][0]) + 1
            
                form_r_sqlcode_add_publications = """INSERT INTO publications(
                    pub_id,  
                    tag_id, 
                    pub_title, 
                    pub_delete_ind, 
                    pub_last_upd,
                    modified_by
                )
                VALUES (%s, %s, %s, %s, %s, %s)
                """
                form_r_values_addpub = [sql_pub_max, r_tag, r_title, False,  r_timestamp_time, r_username_modifier]
                db.modifydatabase(form_r_sqlcode_add_publications,form_r_values_addpub)
                
                
                
                form_r_sqlcode_add_projects = """INSERT INTO projects(
                    pub_id, 
                    r_start_date, 
                    r_end_date, 
                    r_fund_org, 
                    r_year, 
                    r_timeframe
                )
                VALUES (%s, %s, %s, %s, %s, %s)
                """
                str_to_date_start = datetime.strptime(r_start_date, '%Y-%m-%d').date()
                str_to_date_end = datetime.strptime(r_end_date, '%Y-%m-%d').date()
                r_year = str(str_to_date_end.year)
                
                delta = relativedelta.relativedelta(str_to_date_end, str_to_date_start)
                r_timeframe = f"{delta.years} Years, {delta.months} Months, {delta.days} Days" 
                
                form_r_values_addprojects = [sql_pub_max, r_start_date, r_end_date, r_fundorg, r_year, r_timeframe ]
                
                db.modifydatabase(form_r_sqlcode_add_projects, form_r_values_addprojects)
                
                
                
                if type(r_faculty) == int: 
                    r_faculty = [r_faculty]
                
                for i in range(len(r_faculty)): 
                    sql_projects_users = """INSERT INTO projects_users(
                        pub_id, 
                        user_id 
                    )
                    VALUES (%s, %s)
                    """
                    
                    projects_users_values = [sql_pub_max, r_faculty[i]]
                    db.modifydatabase(sql_projects_users,projects_users_values )
                
                if cuser_id > 3: 
                    sql_projects_users2 = """UPDATE projects_users
                    SET 
                        r_roles = %s, 
                        r_contract_link = %s
                    WHERE 
                        pub_id = %s AND user_id = %s
                    """
                    
                    projects_users_values2 = [r_role, r_contract, sql_pub_max, cuser_id]
                    db.modifydatabase(sql_projects_users2, projects_users_values2)
                                 
                
                feedbackmessage = 'Project entry added to database.'
                if cuser_id <= 3: 
                    okay_href = '/publications_manage'
                else: 
                    okay_href = '/my_publications'
            
            
            elif mode == 'edit':
                parsed = urlparse(search)
                form_r_editmodeid = parse_qs(parsed.query)['id'][0]
                form_r_editmodekey = parse_qs(parsed.query)['key'][0]
                
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
                
                values_update_publications = [ r_tag, r_title, to_delete,  r_timestamp_time, r_username_modifier, form_r_editmodeid]
                db.modifydatabase(sql_update_publications, values_update_publications)
                

                sql_update_projects  = """UPDATE projects
                SET  
                    r_start_date = %s, 
                    r_end_date = %s, 
                    r_fund_org = %s, 
                    r_year = %s, 
                    r_timeframe = %s 
                WHERE
                    pub_id = %s 
                """
                
                str_to_date_start = datetime.strptime(r_start_date, '%Y-%m-%d').date()
                str_to_date_end = datetime.strptime(r_end_date, '%Y-%m-%d').date()
                r_year = str_to_date_end.year
                
                delta = relativedelta.relativedelta(str_to_date_end, str_to_date_start)
                r_timeframe = f"{delta.years} Years, {delta.months} Months, {delta.days} Days" 
                
                values_update_projects = [r_start_date, r_end_date, r_fundorg, r_year, r_timeframe, form_r_editmodeid]
                
                
                if cuser_id > 3: 
                    sql_projects_users2 = """UPDATE projects_users
                    SET 
                        r_roles = %s, 
                        r_contract_link = %s
                    WHERE 
                        pub_id = %s AND user_id = %s
                    """
                    
                    projects_users_values2 = [r_role, r_contract, form_r_editmodeid, cuser_id]
                    db.modifydatabase(sql_projects_users2, projects_users_values2)
                
                elif cuser_id < 3: 
                    sql_projects_users2 = """UPDATE projects_users
                    SET 
                        r_roles = %s, 
                        r_contract_link = %s
                    WHERE 
                        pub_id = %s AND user_id = %s
                    """
                    
                    projects_users_values2 = [r_role, r_contract, form_r_editmodeid, form_r_editmodekey]
                    db.modifydatabase(sql_projects_users2, projects_users_values2)
                
                
                
                
                
                db.modifydatabase(sql_update_projects, values_update_projects)
                feedbackmessage = 'Project details updated.'
                if cuser_id <= 3: 
                    okay_href = '/publications_manage'
                else: 
                    okay_href = '/my_publications'
            
            
            else: 
                raise PreventUpdate
    elif eventid == 'form_r_closebtn' and close_btn: 
        pass
    else: 
        raise PreventUpdate
    return [openmodal, feedbackmessage, okay_href, all_inputsalert]
                
