from dash import dcc 
from dash import html 
import dash_bootstrap_components as dbc 
import dash 
from dash.dependencies import Input, Output, State 
from dash.exceptions import PreventUpdate 
import pandas as pd 

from app import app 
from apps import dbconnect as db 

layout = html.Div( 
    [ 
        html.H2('Publication Authors Management'), 
        html.Hr(), 
        dbc.Card( 
            [ 
                dbc.CardHeader(html.H3('Authors')), 
                dbc.CardBody( 
                    [ 
                        dbc.Button("Add Author", color='danger', href='/author_profile?mode=add'), 
                        html.Hr(), 
                        html.Div( 
                            [ 
                                html.H5 ("List of Authors", style={'font-weight':'bold'}), 
                                dbc.Row( 
                                    [ 
                                        dbc.Label(
                                            html.Div([
                                                html.Img(src=app.get_asset_url('search.png'), height="20px", width="18px", style={'position':'left','vertical-align':'middle'}),
                                                html.Span("Search", style={'vertical-align': 'right', 'padding-left':'5px', 'font-size':'20px'}),
                                            ]),
                                        width=1),
                                        dbc.Col( 
                                            [
                                                dbc.FormText("Search author or email", style = {"font-style": "italic", 'font-size':'13px'}), 
                                                dbc.Input(type="text", id="authors_filter", placeholder="Enter Keyword"),
                                            ],
                                            style={'min-width': '22%', 'padding-left': '0.5rem', 'padding-right': '0.5rem'}
                                        ),
                                        dbc.Col(
                                            [
                                                dbc.FormText("Filter by UP Affiliation", style={"font-style": "italic"}),
                                                dcc.Dropdown(
                                                    options=[
                                                    {'label': 'UP Baguio', 'value': 'UP Baguio'},
                                                    {'label': 'UP Cebu', 'value': 'UP Cebu'},
                                                    {'label': 'UP Diliman', 'value': 'UP Diliman'},
                                                    {'label': 'UP Los Baños', 'value': 'UP Los Baños'},
                                                    {'label': 'UP Manila', 'value': 'UP Manila'},
                                                    {'label': 'UP Mindanao', 'value': 'UP Mindanao'},
                                                    {'label': 'UP Open University', 'value': 'UP Open University'},
                                                    {'label': 'UP Visayas', 'value': 'UP Visayas'},
                                                    {'label': 'Others', 'value': 'Others'},
                                                    ],
                                                    id='up_aff_dropdown', clearable=True, searchable=True, placeholder="UP Affiliation"),
                                            ],
                                            width = 2,
                                        ),
                                        html.Div(
                                            dbc.Col(
                                                [
                                                    dbc.FormText("Filter by UPD Unit", style={"font-style": "italic"}),
                                                    dcc.Dropdown(
                                                        options=[
                                                        {'label': 'College of Arts and Letters', 'value': 'College of Arts and Letters'},
                                                        {'label': 'College of Fine Arts', 'value': 'College of Fine Arts'},
                                                        {'label': 'College of Human Kinetics', 'value': 'College of Human Kinetics'},
                                                        {'label': 'College of Mass Communication', 'value': 'College of Mass Communication'},
                                                        {'label': 'College of Music', 'value': 'College of Music'},
                                                        {'label': 'Asian Institute of Tourism', 'value': 'Asian Institute of Tourism'},
                                                        {'label': 'Cesar E.A. Virata School of Business', 'value': 'Cesar E.A. Virata School of Business'},
                                                        {'label': 'School of Economics', 'value': 'School of Economics'},
                                                        {'label': 'School of Labor and Industrial Relations', 'value': 'School of Labor and Industrial Relations'},
                                                        {'label': 'National College of Public Administration and Governance', 'value': 'National College of Public Administration and Governance'},
                                                        {'label': 'School of Urban and Regional Planning', 'value': 'School of Urban and Regional Planning'},
                                                        {'label': 'Technology Management Center', 'value': 'Technology Management Center'},
                                                        {'label': 'UPD Extension Program in Pampanga and Olongapo', 'value': 'UPD Extension Program in Pampanga and Olongapo'},
                                                        {'label': 'School of Archaeology', 'value': 'chool of Archaeology'},
                                                        {'label': 'College of Architecture', 'value': 'College of Architecture'},
                                                        {'label': 'College of Engineering', 'value': 'College of Engineering'},
                                                        {'label': 'College of Science', 'value': 'College of Science'},
                                                        {'label': 'School of Library and Information Studies', 'value': 'School of Library and Information Studies'},
                                                        {'label': 'School of Labor and Industrial Relations', 'value': 'School of Labor and Industrial Relations'},
                                                        {'label': 'School of Statistics', 'value': 'School of Statistics'},
                                                        {'label': 'Asian Center', 'value': 'Asian Center'},
                                                        {'label': 'College of Education', 'value': 'College of Education'},
                                                        {'label': 'Institute of Islamic Studies', 'value': 'Institute of Islamic Studies'},
                                                        {'label': 'College of Law', 'value': 'College of Law'},
                                                        {'label': 'College of Social Sciences and Philosophy', 'value': 'College of Social Sciences and Philosophy'},
                                                        {'label': 'College of Social Work and Community Development', 'value': 'College of Social Work and Community Development'},
                                                        {'label': 'Others', 'value': 'Others'},
                                                        ],
                                                        id='upd_unit_dropdown', clearable=True, searchable=True, placeholder="UP Diliman Unit"),
                                                ],
                                                width = 2,
                                            ),
                                            id='authorman_upd_unit_div'
                                        ), 
                                        html.Div(
                                            dbc.Col(
                                                [
                                                    dbc.FormText("Filter by UPD Engineering Department", style={"font-style": "italic"}),
                                                    dcc.Dropdown(
                                                        options=[
                                                        {'label': 'Department of Chemical Engineering', 'value': 'Department of Chemical Engineering'},
                                                        {'label': 'Institute of Civil Engineering', 'value': 'Institute of Civil Engineering'},
                                                        {'label': 'Department of Computer Science', 'value': 'Department of Computer Science'},
                                                        {'label': 'Electrical and Electronics Institute', 'value': 'Electrical and Electronics Institute'},
                                                        {'label': 'Department of Geodetic Engineering', 'value': 'Department of Geodetic Engineering'},
                                                        {'label': 'Department of Industrial Engineering and Operations Research', 'value': 'Department of Industrial Engineering and Operations Research'},
                                                        {'label': 'Department of Mechanical Engineering', 'value': 'Department of Mechanical Engineering'},
                                                        {'label': 'Department of Mining Metallurgical and Materials Engineering', 'value': 'Department of Mining Metallurgical and Materials Engineering'},
                                                        {'label': 'Energy Engineering Program', 'value': 'Energy Engineering Program'},
                                                        {'label': 'Environmental Engineering Program', 'value': 'Environmental Engineering Program'},
                                                        {'label': 'Others', 'value': 'Others'},
                                                        ],
                                                        id='upd_engg_dropdown', clearable=True, searchable=True, placeholder="Affiliation"),
                                                ],
                                                width = 2,
                                            ),
                                            id='authorman_engg_dept_div'
                                        ),
                                        # dbc.Col(
                                        #     [
                                        #         dbc.FormText("Filter by UPD Unit", style={"font-style": "italic"}),
                                        #         dcc.Dropdown(
                                        #             options=[
                                        #             {'label': 'UPD IE Faculty', 'value': True},
                                        #             {'label': 'Non-UPD IE Faculty', 'value': False},
                                        #             {'label': 'N/A: Non-UPD Affiliated', 'value': "Non-UP"},
                                        #             ],
                                        #             id='ie_faculty_dropdown', clearable=True, placeholder="Faculty Indicator"),
                                        #     ],
                                        #     width = 2,
                                        # ),
                                    ], 
                                    className="mb-3", 
                                ), 
                                html.Div( 
                                    id='authorslist' 
                                ) 
                            ] 
                        ) 
                    ] 
                ) 
            ] 
        ) 
    ] 
) 

# UP Criteria Style       
@app.callback(
    [
        Output('authorman_upd_unit_div', 'style'),
        Output('authorman_engg_dept_div', 'style'),
        # Output('authorman_iefacind_div', 'style'),
    ], 
    [
        Input('url', 'pathname'), 
        Input('up_aff_dropdown', 'value'),
        Input('upd_unit_dropdown', 'value'),
        # Input('authorprof_engg_dept_dropdown', 'value'),
    ]
)
def facinddiv (pathname, up_aff, upd_unit): 
    if pathname == '/author_manage':
        if up_aff == '':
            up_aff = None
        if up_aff == None:
            upd_unit_div = {'display': 'none'}
            engg_dept_div = {'display': 'none'}
        elif up_aff == 'Others':
            upd_unit_div = {'display': 'none'}
            engg_dept_div = {'display': 'none'}
        elif up_aff == 'UP Diliman':
            upd_unit_div = {'display': 'contents'}
            engg_dept_div = {'display': 'none'}
            if upd_unit == '':
                upd_unit = None
            if upd_unit == None:
                engg_dept_div = {'display': 'none'}
            elif upd_unit == 'College of Engineering':
                engg_dept_div = {'display': 'contents'}
            else:
                engg_dept_div = {'display': 'none'}
        else:
            upd_unit_div = {'display': 'none'}
            engg_dept_div = {'display': 'none'}
    else:
        raise PreventUpdate
    return(upd_unit_div, engg_dept_div)



@app.callback( 
    [ 
        Output('authorslist', 'children') 
    ], 
    [ 
        Input('url', 'pathname'), 
        Input('authors_filter', 'value'),
        Input('up_aff_dropdown', 'value'),
        Input('upd_unit_dropdown', 'value'),
        Input('upd_engg_dropdown', 'value'),
        # Input('faculty_dropdown', 'value')
    ] 
) 

def authors_loadauthorslist(pathname, searchterm, upfilter, updfilter, enggfilter):
    if pathname == '/author_manage':
        sql = """SELECT
                author_id,
                author_ln || ', '|| author_fn as author_full_name,
                CASE
                    WHEN author_up_constituent = 'Others' THEN author_up_constituent || ' (' || author_other_aff ||') '
                    ELSE author_up_constituent
                END as specified_aff,
                author_upd_unit,
                author_engg_dept,
                author_fac_ind,
                author_mail,
                author_contact,
                to_char(author_last_upd::timestamp, 'Month DD YYYY HH24:MI:SS')
            FROM 
                authors 
            WHERE
                author_delete_ind = false
            """
        values = []
        cols = ['authorID', 'Full Name', 'Affiliation', 'UPD Unit', 'UPD Engineering Dept.', 'IE Faculty Indication', 'Email', 'Contact #', 'Last Updated']         

        # if facfilter:
        #     sql += """AND (author_fac_ind ILIKE %s)"""

        if upfilter:
            sql += """AND (author_up_constituent ILIKE %s)"""
            values += [f"%{upfilter}%"]
            if updfilter:
                sql += """AND (author_upd_unit ILIKE %s)"""
                values += [f"%{updfilter}%"]
                if enggfilter:
                    sql += """AND (author_engg_dept ILIKE %s)"""
                    values += [f"%{enggfilter}%"]
                    if searchterm:
                        sql += """AND (((author_fn || ' ' || author_ln) ILIKE %s)
                        OR (author_mail ILIKE %s))"""
                        values += [f"%{searchterm}%", f"%{searchterm}%"]
        #     elif enggfilter:
        #         sql += """AND (author_engg_dept ILIKE %s)"""
        #         values += [f"%{enggfilter}%"]
        #         if searchterm:
        #             sql += """((author_fn || ' ' || faculty_ln) ILIKE %s)
        #                 OR (author_mail ILIKE %s))"""
        #             values += [f"%{searchterm}%", f"%{searchterm}%"]
        #     elif searchterm:
        #         sql += """((author_fn || ' ' || faculty_ln) ILIKE %s)
        #         OR (author_mail ILIKE %s))"""
        #         values += [f"%{searchterm}%", f"%{searchterm}%"]
            

        # if updfilter:
        #     sql += """AND (author_upd_unit ILIKE %s)"""
        #     values += [f"%{updfilter}%"]
        #     # if upfilter:
        #     #     sql += """AND (author_up_constituent ILIKE %s)"""
        #     if enggfilter:
        #         sql += """AND (author_engg_dept ILIKE %s)"""
        #         values += [f"%{enggfilter}%"]
        #         if searchterm:
        #             sql += """((author_fn || ' ' || faculty_ln) ILIKE %s)
        #             OR (author_mail ILIKE %s))"""
        #             values += [f"%{searchterm}%", f"%{searchterm}%"]

        # if enggfilter:
        #     sql += """AND (author_engg_dept ILIKE %s)"""
        #     values += [f"%{enggfilter}%"]
        #     if searchterm:
        #         sql += """((author_fn || ' ' || faculty_ln) ILIKE %s)
        #         OR (author_mail ILIKE %s))"""
        #         values += [f"%{searchterm}%", f"%{searchterm}%"]

        if searchterm:
            sql += """AND (((author_fn || ' ' || author_ln) ILIKE %s)
            OR (author_mail ILIKE %s))"""
            values += [f"%{searchterm}%", f"%{searchterm}%"]
            if upfilter:
                sql += """AND (author_up_constituent ILIKE %s)"""
                values += [f"%{upfilter}%"]
                if updfilter:
                    sql += """AND (author_upd_unit ILIKE %s)"""
                    values += [f"%{upfilter}%"]
                    if enggfilter:
                        sql += """AND (author_engg_dept ILIKE %s)"""
                        values += [f"%{enggfilter}%"]
            # elif updfilter:
            #     sql += """AND (author_upd_unit ILIKE %s)"""
            #     values += [f"%{updfilter}%"]
            #     # if upfilter:
            #     #     sql += """AND (author_up_constituent ILIKE %s)"""
            #     if enggfilter:
            #         sql += """AND (author_engg_dept ILIKE %s)"""
            #         values += [f"%{enggfilter}%"]
            # elif enggfilter:
            #     sql += """AND (author_engg_dept ILIKE %s)"""
            #     values += [f"%{enggfilter}%"]
        sql += """ORDER BY author_last_upd DESC"""  
        authors = db.querydatafromdatabase(sql, values, cols)

        if authors.shape[0]: 
            buttons = []
            for idnumber in authors['authorID']: 
                buttons += [ 
                    html.Div( 
                        dbc.Button('Edit/Delete', href=f"/author_profile?mode=edit&id={idnumber}", size='sm', color='secondary', ), 
                        style={'text-align': 'center'} 
                    ) 
                ] 
            authors['Modify'] = buttons 
            
            authors.drop(['authorID'],axis=1,inplace=True) 
            table = dbc.Table.from_dataframe(authors, striped=True, bordered=True, hover=True, size='sm') 
            return [table] 
        else:
            return ["No records to display."]
    else: 
        return ["No records to display."]        