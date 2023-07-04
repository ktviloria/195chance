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
                                                dbc.FormText("Search author, UP constituent, UPD Unit, UPD Engineering Department", style = {"font-style": "italic", 'font-size':'13px'}), 
                                                dbc.Input(type="text", id="authors_filter", placeholder="Enter Keyword"),
                                            ],
                                            style={'min-width': '22%', 'padding-left': '0.5rem', 'padding-right': '0.5rem'}
                                        ),
                                        dbc.Col(
                                            [
                                                dbc.FormText("Filter by UP Affiliation", style={"font-style": "italic"}),
                                                dcc.Dropdown(
                                                    options=[
                                                    {'label': 'UP Baguio', 'value': '1'},
                                                    {'label': 'UP Cebu', 'value': '2'},
                                                    {'label': 'UP Diliman', 'value': '3'},
                                                    {'label': 'UP Los Baños', 'value': '4'},
                                                    {'label': 'UP Manila', 'value': '5'},
                                                    {'label': 'UP Mindanao', 'value': '6'},
                                                    {'label': 'UP Open University', 'value': '7'},
                                                    {'label': 'UP Visayas', 'value': '8'},
                                                    {'label': 'Others', 'value': None},
                                                    ],
                                                    id='up_aff_dropdown', clearable=True, searchable=True, placeholder="Affiliation"),
                                            ],
                                                width = 2,
                                        ),
                                        dbc.Col(
                                            [
                                                dbc.FormText("Filter by UPD Unit", style={"font-style": "italic"}),
                                                dcc.Dropdown(
                                                    options=[
                                                    {'label': 'College of Arts and Letters', 'value': '1'},
                                                    {'label': 'College of Fine Arts', 'value': '2'},
                                                    {'label': 'College of Human Kinetics', 'value': '3'},
                                                    {'label': 'College of Mass Communication', 'value': '4'},
                                                    {'label': 'College of Music', 'value': '5'},
                                                    {'label': 'Asian Institute of Tourism', 'value': '6'},
                                                    {'label': 'Cesar E.A. Virata School of Business', 'value': '7'},
                                                    {'label': 'School of Economics', 'value': '8'},
                                                    {'label': 'School of Labor and Industrial Relations', 'value': '9'},
                                                    {'label': 'National College of Public Administration and Governance', 'value': '10'},
                                                    {'label': 'School of Urban and Regional Planning', 'value': '11'},
                                                    {'label': 'Technology Management Center', 'value': '12'},
                                                    {'label': 'UPD Extension Program in Pampanga and Olongapo', 'value': '13'},
                                                    {'label': 'School of Archaeology', 'value': '14'},
                                                    {'label': 'College of Architecture', 'value': '15'},
                                                    {'label': 'College of Engineering', 'value': '16'},
                                                    {'label': 'College of Science', 'value': '17'},
                                                    {'label': 'School of Library and Information Studies', 'value': '18'},
                                                    {'label': 'School of Labor and Industrial Relations', 'value': '19'},
                                                    {'label': 'School of Statistics', 'value': '20'},
                                                    {'label': 'Asian Center', 'value': '21'},
                                                    {'label': 'College of Education', 'value': '22'},
                                                    {'label': 'Institute of Islamic Studies', 'value': '23'},
                                                    {'label': 'College of Law', 'value': '24'},
                                                    {'label': 'College of Social Sciences and Philosophy', 'value': '25'},
                                                    {'label': 'College of Social Work and Community Development', 'value': '26'},
                                                    {'label': 'Others', 'value': None},
                                                    ],
                                                    id='upd_unit_dropdown', clearable=True, searchable=True, placeholder="UP Diliman Unit"),
                                            ],
                                                width = 2,
                                        ),
                                        dbc.Col(
                                            [
                                                dbc.FormText("Filter by UPD Engineering Department", style={"font-style": "italic"}),
                                                dcc.Dropdown(
                                                    options=[
                                                    {'label': 'Department of Chemical Engineering', 'value': '1'},
                                                    {'label': 'Institute of Civil Engineering', 'value': '2'},
                                                    {'label': 'Department of Computer Science', 'value': '3'},
                                                    {'label': 'Electrical and Electronics Institute', 'value': '4'},
                                                    {'label': 'Department of Geodetic Engineering', 'value': '5'},
                                                    {'label': 'Department of Industrial Engineering and Operations Research', 'value': '6'},
                                                    {'label': 'Department of Mechanical Engineering', 'value': '7'},
                                                    {'label': 'Department of Mining Metallurgical and Materials Engineering', 'value': '8'},
                                                    {'label': 'Energy Engineering Program', 'value': '9'},
                                                    {'label': 'Environmental Engineering Program', 'value': '10'},
                                                    {'label': 'Others', 'value': None},
                                                    ],
                                                    id='upd_engg_dropdown', clearable=True, searchable=True, placeholder="Affiliation"),
                                            ],
                                                width = 2,
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
                author_up_constituent,
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
        cols = ['authorID', 'Full Name', 'UP Affiliation', 'UPD Unit', 'UPD Engineering Dept.', 'IE Faculty Indication', 'Email', 'Contact #', 'Last Updated']         

        # if afffilter == True:
        #     sql += """ AND author_aff = 'true' """ 
        #     if facultyfilter == True:
        #         sql += """ AND author_fac_ind = 'true' """ 
        #         if searchterm:
        #             sql += """ AND (((author_fn || ' ' || author_ln) ILIKE %s) OR (author_mail ILIKE %s) OR (author_contact ILIKE %s))"""
        #             values += [f"%{searchterm}%", f"%{searchterm}%"]
        #     elif facultyfilter == False:
        #         sql += """ AND author_fac_ind = 'false' """
        #         if searchterm:
        #             sql += """ AND (((author_fn || ' ' || author_ln) ILIKE %s) OR (author_mail ILIKE %s) OR (author_contact ILIKE %s))"""
        #             values += [f"%{searchterm}%", f"%{searchterm}%"]
        # elif afffilter == False: 
        #     sql += """ AND author_aff = 'false' """
        #     # sql += """ AND author_fac_ind = 'N/A' """
        #     if searchterm:
        #         sql += """ AND (((author_fn || ' ' || author_ln) ILIKE %s) OR (author_mail ILIKE %s) OR (author_contact ILIKE %s))"""
        #         values += [f"%{searchterm}%", f"%{searchterm}%"]
        # elif facultyfilter == True:
        #     sql += """ AND author_fac_ind = 'true' """
        #     if afffilter == True:
        #         sql += """ AND author_aff = 'true' """
        #         if searchterm:
        #             sql += """ AND (((author_fn || ' ' || author_ln) ILIKE %s) OR (author_mail ILIKE %s) OR (author_contact ILIKE %s))"""
        #             values += [f"%{searchterm}%", f"%{searchterm}%"]
        # elif facultyfilter == False:
        #     sql += """ AND author_fac_ind = 'false' """
        #     if afffilter == True:
        #         sql += """ AND author_aff = 'true' """
        #         if searchterm:
        #             sql += """ AND (((author_fn || ' ' || author_ln) ILIKE %s) OR (author_mail ILIKE %s) OR (author_contact ILIKE %s))"""
        #             values += [f"%{searchterm}%", f"%{searchterm}%"]
        #     elif afffilter == False:
        #         sql += """ AND author_aff = 'false' """
        #         if searchterm:
        #             sql += """ AND (((author_fn || ' ' || author_ln) ILIKE %s) OR (author_mail ILIKE %s) OR (author_contact ILIKE %s))"""
        #             values += [f"%{searchterm}%", f"%{searchterm}%"]
        # elif facultyfilter == "N/A":
        #     sql += """ AND author_fac_ind = '' """
        #     if afffilter == False:
        #         sql += """ AND author_aff = 'false' """
        #         if searchterm:
        #             sql += """ AND (((author_fn || ' ' || author_ln) ILIKE %s) OR (author_mail ILIKE %s) OR (author_contact ILIKE %s))"""
        #             values += [f"%{searchterm}%", f"%{searchterm}%"]
        # elif searchterm:
        #     sql += """ AND (((author_fn || ' ' || author_ln) ILIKE %s) OR (author_mail ILIKE %s) OR (author_contact ILIKE %s))"""
        #     values += [f"%{searchterm}%", f"%{searchterm}%"]
        #     if afffilter == True:
        #         sql += """ author_aff = 'true' """   
        #         if facultyfilter == True: 
        #             sql += """ AND author_fac_ind = 'true' """
        #         elif facultyfilter == False: 
        #             sql += """ AND author_fac_ind = 'false' """ 
        #     if afffilter == False:
        #         sql += """ AND author_aff = 'false' """
        #         # sql += """ AND author_fac_ind = 'N/A' """

        # sql += """ORDER BY authors.author_aff DESC, authors.author_fac_ind"""
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
            
            # for i in range(len(authors['Author Affiliation'])): 
            #     if authors['Author Affiliation'][i] == 'true' : 
            #         authors['Author Affiliation'][i] = 'UP'
            #     else: 
            #         authors['Author Affiliation'][i] = 'Non-UP'

            
            # for i in range(len(authors['IE Faculty Indication'])): 
            #     if authors['Author Affiliation'][i] == 'UP' and authors['IE Faculty Indication'][i] == 'true': 
            #         authors['IE Faculty Indication'][i] = 'IE Faculty'
            #     elif authors['Author Affiliation'][i] == 'UP' and authors['IE Faculty Indication'][i] == 'false': 
            #         authors['IE Faculty Indication'][i] = 'Non-IE Faculty'
            #     elif authors['Author Affiliation'][i] == 'UP' and authors['IE Faculty Indication'][i] == None: 
            #         authors['IE Faculty Indication'][i] = 'To be updated'
            #     else:
            #         authors['IE Faculty Indication'][i] = 'N/A'
                
        authors.drop(['authorID'],axis=1,inplace=True) 
        table = dbc.Table.from_dataframe(authors, striped=True, bordered=True, hover=True, size='sm') 
        return [table] 
    else: 
        return ["No records to display."]        