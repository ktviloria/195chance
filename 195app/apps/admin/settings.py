
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
                dbc.CardHeader(html.H2("Settings")),
                dbc.CardBody(
                    [
                        dbc.Row(
                            [
                                # tabs
                                dbc.Col(
                                    [
                                        dcc.Tabs(
                                            children =[
                                                dcc.Tab(label="Criteria", value="tab_pc", style={"color": "#800000"}, selected_style={'font-weight': 'bold', "color": "#800000"}),
                                                dcc.Tab(label="Faculty Rank", value="tab_ra", style={"color": "#800000"}, selected_style={'font-weight': 'bold', "color": "#800000"}),
                                                dcc.Tab(label="Faculty Authorship Role", value="tab_ro", style={"color": "#800000"}, selected_style={'font-weight': 'bold', "color": "#800000"}),
                                                dcc.Tab(label="Faculty Authorship Involvement", value="tab_i", style={"color": "#800000"}, selected_style={'font-weight': 'bold', "color": "#800000"}),
                                                dcc.Tab(label="UP Constituent", value="tab_up_cons", style={"color": "#800000"}, selected_style={'font-weight': 'bold', "color": "#800000"}),
                                                dcc.Tab(label="UP Diliman Unit", value="tab_upd_unit", style={"color": "#800000"}, selected_style={'font-weight': 'bold', "color": "#800000"}),
                                                dcc.Tab(label="UPD Engineering Departments", value="tab_engg_dept", style={"color": "#800000"}, selected_style={'font-weight': 'bold', "color": "#800000"}),
                                            ],
                                            id='tabs',
                                            value='tab_pc',
                                            vertical = True,
                                        ),
                                    ],
                                    width=2,
                                ),
                                dbc.Col(
                                    [
                                        html.Div(id='settings'),
                                        html.Br(),
                                        html.Div(id='list',
                                                #  style={'border-left':'1px', 'height':'500px'}
                                                )
                                    ],    
                                    width=10
                                ),
                            ],
                            className="mb-3",
                        ),
                    ],
                )
            ]
        ),     
    ]
)

@app.callback(
    [
        Output('settings', 'children'),
        Output('list', 'children'),
    ],
    [
        Input('url', 'pathname'),
        Input('tabs', 'value'),
    ]
)

def settings_page(pathname, tab):
    if pathname == '/settings':
        if tab == 'tab_pc':
            #publication criteria 
            sql_pc = """SELECT 
                tag_id, 
                tag_title, 
                tag_sub, 
                tag_short_title, 
                tag_modified_by, 
                to_char(tag_last_upd::timestamp, 'Month DD YYYY HH24:MI:SS')
            FROM tags 
            WHERE 
                not tag_delete_ind  
            Order By tag_id 
            """
            values_pc = []
            cols_pc = ['tag_id', 'Criteria', 'Type', "Shortened Criteria Title", 'Last Modified By', 'Last Modified']
            criteria = db.querydatafromdatabase(sql_pc, values_pc, cols_pc)
            
            if criteria.shape[0]: 
                buttons = []
                for i in criteria['tag_id']: 
                    buttons += [ 
                        html.Div(
                            dbc.Button('Edit/Delete', href = f"/form_criteria?mode=edit&id={i}", size = 'sm', color = 'secondary'), 
                            style = {'text-align': 'center'}
                        )
                    ]
                criteria['Action'] = buttons 
            
            for i in range(len(criteria['Type'])): 
                if criteria['Type'][i] == 'A': 
                    criteria['Type'][i] = 'Publications/Authorships'
                elif criteria['Type'][i] == 'P': 
                    criteria['Type'][i] = 'Presentations'
                elif criteria['Type'][i] == 'R': 
                    criteria['Type'][i] = 'Projects'
                elif criteria['Type'][i] == 'O': 
                    criteria['Type'][i] = 'Other Academic Merits'
            
            add = [
                html.Div(
                    [
                        html.Div( 
                        [ 
                            html.H5("Criteria"),
                            html.Hr(),
                        ],
                        id = 'form_pc' 
                        ),
                        html.Div(
                            [
                                dbc.Button('Add Criteria', href= "/form_criteria?mode=add",color="danger", id='form_pc_submitbtn', className="me-md-2"),
                            ],
                            className="d-grid d-md-flex justify-content-md-end",
                        ),
                    ]
                )
            ]
            criteria.drop(['tag_id'],axis=1,inplace=True) 
            list = dbc.Table.from_dataframe(criteria, striped=True, bordered=True, hover=True, size='sm') 

        elif tab == 'tab_ra':
            #rank
            sql_pc = """SELECT 
                rank_id, 
                rank_title, 
                ranks_modified_by, 
                to_char(ranks_last_upd::timestamp, 'Month DD YYYY HH24:MI:SS')
            from ranks
            WHERE not ranks_delete_ind
            order by rank_id
            """
            values_pc = []
            cols_pc = ['rank_id','Ranks', 'Last Modified By', 'Last Modified']
            rank = db.querydatafromdatabase(sql_pc, values_pc, cols_pc) 
            
            if rank.shape[0]: 
                buttons = []
                for i in rank['rank_id']: 
                    buttons += [ 
                        html.Div(
                            dbc.Button('Edit/Delete', href = f"/form_faculty_rank?mode=edit&id={i}", size = 'sm', color = 'secondary'), 
                            style = {'text-align': 'center'}
                        )
                    ]
                rank['Action'] = buttons 
            add = [
                html.Div(
                    [
                        html.Div( 
                        [ 
                            html.H5("Faculty Rank"),
                            html.Hr(),
                        ],
                        ),
                        html.Div(
                            [
                                dbc.Button('Add Faculty Rank', href= "/form_faculty_rank?mode=add",color="danger", id='form_ra_submitbtn', className="me-md-2"),
                            ],
                            className="d-grid d-md-flex justify-content-md-end",
                        ),
                    ]
                )
            ]
            rank.drop(['rank_id'],axis=1,inplace=True) 
            list = dbc.Table.from_dataframe(rank, striped=True, bordered=True, hover=True, size='sm')

        elif tab == 'tab_ro':
            #role
            sql_pc = """SELECT 
                a_label_id, 
                a_label, 
                role_modified_by, 
                to_char(role_last_upd::timestamp, 'Month DD YYYY HH24:MI:SS')
                 
            from authorship_role
            WHERE not role_delete_ind
            ORDER BY a_label_id
            """
            values_pc = []
            cols_pc = ['a_labelid','Roles', 'Last Modified By', 'Last Modified']
            role = db.querydatafromdatabase(sql_pc, values_pc, cols_pc)
            
            if role.shape[0]: 
                buttons = []
                for i in role['a_labelid']: 
                    buttons += [ 
                        html.Div(
                            dbc.Button('Edit/Delete', href = f"/form_role?mode=edit&id={i}", size = 'sm', color = 'secondary'), 
                            style = {'text-align': 'center'}
                        )
                    ]
                role['Action'] = buttons 
            
            add = [
                html.Div(
                    [
                        html.Div( 
                        [ 
                            html.H5("Faculty Authorship Role"),
                            html.Hr(),
                        ],
                        ),
                        html.Div(
                            [
                                dbc.Button('Add Faculty Authorship Role',  href= "/form_role?mode=add",color="danger", id='form_ro_submitbtn', className="me-md-2"),
                            ],
                            className="d-grid d-md-flex justify-content-md-end",
                        ),
                    ]
                )
            ]
            role.drop(['a_labelid'],axis=1,inplace=True) 
            list = dbc.Table.from_dataframe(role, striped=True, bordered=True, hover=True, size='sm') 

        elif tab == 'tab_i':
            #involvement
            sql_pc = """SELECT 
                a_author_subcat_id,
                a_author_subcat_label, 
                sub_modified_by, 
                to_char(sub_last_upd::timestamp, 'Month DD YYYY HH24:MI:SS')
            from authorship_subcategory
            WHERE not sub_delete_ind
            ORDER BY a_author_subcat_id
            """
            values_pc = []
            cols_pc = ['subcat_id','Involvement', 'Last Modified By', 'Last Modified']
            inv = db.querydatafromdatabase(sql_pc, values_pc, cols_pc)
            
            if inv.shape[0]: 
                buttons = []
                for i in inv['subcat_id']: 
                    buttons += [ 
                        html.Div(
                            dbc.Button('Edit/Delete', href = f"/form_involvement?mode=edit&id={i}", size = 'sm', color = 'secondary'), 
                            style = {'text-align': 'center'}
                        )
                    ]
                inv['Action'] = buttons 

            add = [
                html.Div(
                    [
                        html.Div( 
                        [ 
                            html.H5("Faculty Authorship Involvement"),
                            html.Hr(),
                        ],
                        ),
                        html.Div(
                            [
                                dbc.Button('Add Faculty Authorship Involvement', href= "/form_involvement?mode=add",color="danger", id='form_i_submitbtn', className="me-md-2"),
                            ],
                            className="d-grid d-md-flex justify-content-md-end",
                        ),
                    ]
                )
            ]
            inv.drop(['subcat_id'],axis=1,inplace=True) 
            list = dbc.Table.from_dataframe(inv, striped=True, bordered=True, hover=True, size='sm')

        elif tab == 'tab_up_cons':
            #up constituent
            sql_pc = """SELECT 
                cons_id,
                cons_name 
            from up_system
            WHERE not cons_delete_ind
            ORDER BY cons_id
            """
            values_pc = []
            cols_pc = ['cons_id','UP Constituent']
            cons = db.querydatafromdatabase(sql_pc, values_pc, cols_pc)
            
            if cons.shape[0]: 
                buttons = []
                for i in cons['cons_id']: 
                    buttons += [ 
                        html.Div(
                            dbc.Button('Edit/Delete', href = f"/form_up_constituent?mode=edit&id={i}", size = 'sm', color = 'secondary'), 
                            style = {'text-align': 'center'}
                        )
                    ]
                cons['Action'] = buttons 

            add = [
                html.Div(
                    [
                        html.Div( 
                        [ 
                            html.H5("UP Constituents"),
                            html.Hr(),
                        ],
                        ),
                        html.Div(
                            [
                                dbc.Button('Add UP Constituent', href= "/form_up_constituent?mode=add",color="danger", id='form_up_cons_submitbtn', className="me-md-2"),
                            ],
                            className="d-grid d-md-flex justify-content-md-end",
                        ),
                    ]
                )
            ]
            cons.drop(['cons_id'],axis=1,inplace=True) 
            list = dbc.Table.from_dataframe(cons, striped=True, bordered=True, hover=True, size='sm') 
            
        elif tab == 'tab_upd_unit':
            #upd unit
            sql_pc = """SELECT 
                college_id,
                college_name 
            from up_diliman
            WHERE not college_delete_ind
            ORDER BY college_id
            """
            values_pc = []
            cols_pc = ['college_id','UP Diliman Unit']
            unit = db.querydatafromdatabase(sql_pc, values_pc, cols_pc)
            
            if unit.shape[0]: 
                buttons = []
                for i in unit['college_id']: 
                    buttons += [ 
                        html.Div(
                            dbc.Button('Edit/Delete', href = f"/form_upd_unit?mode=edit&id={i}", size = 'sm', color = 'secondary'), 
                            style = {'text-align': 'center'}
                        )
                    ]
                unit['Action'] = buttons 

            add = [
                html.Div(
                    [
                        html.Div( 
                        [ 
                            html.H5("UP Diliman Units"),
                            html.Hr(),
                        ],
                        ),
                        html.Div(
                            [
                                dbc.Button('Add UP Diliman Unit', href= "/form_upd_unit?mode=add",color="danger", id='form_upd_unit_submitbtn', className="me-md-2"),
                            ],
                            className="d-grid d-md-flex justify-content-md-end",
                        ),
                    ]
                )
            ]
            unit.drop(['college_id'],axis=1,inplace=True) 
            list = dbc.Table.from_dataframe(unit, striped=True, bordered=True, hover=True, size='sm') 

        elif tab == 'tab_engg_dept':
            #upd engineering department
            sql_pc = """SELECT 
                dept_id,
                dept_name 
            from upd_engg_depts
            WHERE not dept_delete_ind
            ORDER BY dept_id
            """
            values_pc = []
            cols_pc = ['dept_id','UP Diliman Engineering Department']
            enggdept = db.querydatafromdatabase(sql_pc, values_pc, cols_pc)
            
            if enggdept.shape[0]: 
                buttons = []
                for i in enggdept['dept_id']: 
                    buttons += [ 
                        html.Div(
                            dbc.Button('Edit/Delete', href = f"/form_engg_dept?mode=edit&id={i}", size = 'sm', color = 'secondary'), 
                            style = {'text-align': 'center'}
                        )
                    ]
                enggdept['Action'] = buttons 

            add = [
                html.Div(
                    [
                        html.Div( 
                        [ 
                            html.H5("UP Diliman Engineering Departments"),
                            html.Hr(),
                        ],
                        ),
                        html.Div(
                            [
                                dbc.Button('Add UP Diliman Engineering Department', href= "/form_engg_dept?mode=add",color="danger", id='form_engg_dept_submitbtn', className="me-md-2"),
                            ],
                            className="d-grid d-md-flex justify-content-md-end",
                        ),
                    ]
                )
            ]
            enggdept.drop(['dept_id'],axis=1,inplace=True) 
            list = dbc.Table.from_dataframe(enggdept, striped=True, bordered=True, hover=True, size='sm') 

        return [add,list]
    else: 
        return ['',"No records to display."]  
