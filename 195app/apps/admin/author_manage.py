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
                                            dbc.Input( 
                                                value='',
                                                type='text', 
                                                id='authors_filter', 
                                                placeholder='Enter Filter' 
                                            ), 
                                            width=6 
                                        ),
                                        dbc.Col(
                                            dcc.Dropdown(
                                                options=[
                                                {'label': 'UP', 'value': True},
                                                {'label': 'Non-UP', 'value': False},
                                                ],
                                                id='aff_dropdown', clearable=True, placeholder="Affiliation"),
                                                width = 2,
                                        ),
                                        dbc.Col(
                                            dcc.Dropdown(
                                                options=[
                                                {'label': 'IE Faculty', 'value': True},
                                                {'label': 'Non-IE Faculty', 'value': False},
                                                {'label': 'N/A: Non-UP Affiliated', 'value': "Non-UP"},
                                                ],
                                                id='faculty_dropdown', clearable=True, placeholder="Faculty"),
                                                width = 2,
                                        ),
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
        Input('aff_dropdown', 'value'),
        Input('faculty_dropdown', 'value')
    ] 
) 

def authors_loadauthorslist(pathname, searchterm, afffilter, facultyfilter):
    if pathname == '/author_manage':
        sql = """SELECT
                author_id, 
                author_ln || ', '|| author_fn as author_full_name,
                author_mail,
                author_contact,
                author_aff,
                author_fac_ind,
                to_char(author_last_upd::timestamp, 'Month DD YYYY HH24:MI:SS')
            FROM 
                authors 
            WHERE
                author_delete_ind = false
            """
        values = []
        cols = ['authorID', 'Full Name', 'Email', 'Contact #', 'Author Affiliation', 'IE Faculty Indication', 'Last Updated']         

        if afffilter == True:
            sql += """ AND author_aff = 'true' """ 
            if facultyfilter == True:
                sql += """ AND author_fac_ind = 'true' """ 
                if searchterm:
                    sql += """ AND (((author_fn || ' ' || author_ln) ILIKE %s) OR (author_mail ILIKE %s) OR (author_contact ILIKE %s))"""
                    values += [f"%{searchterm}%", f"%{searchterm}%"]
            elif facultyfilter == False:
                sql += """ AND author_fac_ind = 'false' """
                if searchterm:
                    sql += """ AND (((author_fn || ' ' || author_ln) ILIKE %s) OR (author_mail ILIKE %s) OR (author_contact ILIKE %s))"""
                    values += [f"%{searchterm}%", f"%{searchterm}%"]
        elif afffilter == False: 
            sql += """ AND author_aff = 'false' """
            # sql += """ AND author_fac_ind = 'N/A' """
            if searchterm:
                sql += """ AND (((author_fn || ' ' || author_ln) ILIKE %s) OR (author_mail ILIKE %s) OR (author_contact ILIKE %s))"""
                values += [f"%{searchterm}%", f"%{searchterm}%"]
        elif facultyfilter == True:
            sql += """ AND author_fac_ind = 'true' """
            if afffilter == True:
                sql += """ AND author_aff = 'true' """
                if searchterm:
                    sql += """ AND (((author_fn || ' ' || author_ln) ILIKE %s) OR (author_mail ILIKE %s) OR (author_contact ILIKE %s))"""
                    values += [f"%{searchterm}%", f"%{searchterm}%"]
        elif facultyfilter == False:
            sql += """ AND author_fac_ind = 'false' """
            if afffilter == True:
                sql += """ AND author_aff = 'true' """
                if searchterm:
                    sql += """ AND (((author_fn || ' ' || author_ln) ILIKE %s) OR (author_mail ILIKE %s) OR (author_contact ILIKE %s))"""
                    values += [f"%{searchterm}%", f"%{searchterm}%"]
            elif afffilter == False:
                sql += """ AND author_aff = 'false' """
                if searchterm:
                    sql += """ AND (((author_fn || ' ' || author_ln) ILIKE %s) OR (author_mail ILIKE %s) OR (author_contact ILIKE %s))"""
                    values += [f"%{searchterm}%", f"%{searchterm}%"]
        elif facultyfilter == "N/A":
            sql += """ AND author_fac_ind = '' """
            if afffilter == False:
                sql += """ AND author_aff = 'false' """
                if searchterm:
                    sql += """ AND (((author_fn || ' ' || author_ln) ILIKE %s) OR (author_mail ILIKE %s) OR (author_contact ILIKE %s))"""
                    values += [f"%{searchterm}%", f"%{searchterm}%"]
        elif searchterm:
            sql += """ AND (((author_fn || ' ' || author_ln) ILIKE %s) OR (author_mail ILIKE %s) OR (author_contact ILIKE %s))"""
            values += [f"%{searchterm}%", f"%{searchterm}%"]
            if afffilter == True:
                sql += """ author_aff = 'true' """   
                if facultyfilter == True: 
                    sql += """ AND author_fac_ind = 'true' """
                elif facultyfilter == False: 
                    sql += """ AND author_fac_ind = 'false' """ 
            if afffilter == False:
                sql += """ AND author_aff = 'false' """
                # sql += """ AND author_fac_ind = 'N/A' """

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
            
            for i in range(len(authors['Author Affiliation'])): 
                if authors['Author Affiliation'][i] == 'true' : 
                    authors['Author Affiliation'][i] = 'UP'
                else: 
                    authors['Author Affiliation'][i] = 'Non-UP'

            
            for i in range(len(authors['IE Faculty Indication'])): 
                if authors['Author Affiliation'][i] == 'UP' and authors['IE Faculty Indication'][i] == 'true': 
                    authors['IE Faculty Indication'][i] = 'IE Faculty'
                elif authors['Author Affiliation'][i] == 'UP' and authors['IE Faculty Indication'][i] == 'false': 
                    authors['IE Faculty Indication'][i] = 'Non-IE Faculty'
                elif authors['Author Affiliation'][i] == 'UP' and authors['IE Faculty Indication'][i] == None: 
                    authors['IE Faculty Indication'][i] = 'To be updated'
                else:
                    authors['IE Faculty Indication'][i] = 'N/A'
                
        authors.drop(['authorID'],axis=1,inplace=True) 
        table = dbc.Table.from_dataframe(authors, striped=True, bordered=True, hover=True, size='sm') 
        return [table] 
    else: 
        return ["No records to display."]        