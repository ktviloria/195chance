#for viewing all publications of the department
#all users have access to this page

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

mod_style = { 
 'color': '#fff',
 'background-color': '#b22222',
 'font-size': '25px'
} 

layout= html.Div( 
    [ 
        html.Div( 
            [ 
                dcc.Store(id='pubdet_toload', storage_type='memory', data=0), 
            ],
            # [
            #     html.Button("Download CSV", id="btn_csv"),
            #     dcc.Download(id="download-dataframe-csv"),
            # ] 
        ),
        html.Div('', id = 'modals_holder',  style={'display': 'none'}), 
        dbc.Card(
            [
                dbc.CardHeader(html.H2("Departmental Publications")),
                dbc.CardBody(
                    [
                        dbc.Row(
                            [
                                # tabs
                                dbc.Col(
                                    [
                                        dbc.Tabs(
                                            children=[
                                                dbc.Tab(label="Authorships", tab_id="tab_a", label_style={"color": "#800000"}, active_tab_style={'font-weight': 'bold'}),
                                                dbc.Tab(label="Presentations", tab_id="tab_p", label_style={"color": "#800000"}, active_tab_style={'font-weight': 'bold'}),
                                                dbc.Tab(label="Projects", tab_id="tab_r", label_style={"color": "#800000"}, active_tab_style={'font-weight': 'bold'}),
                                                dbc.Tab(label="Others", tab_id="tab_o", label_style={"color": "#800000"}, active_tab_style={'font-weight': 'bold'})
                                            ],
                                            id='tabs',
                                            active_tab='tab_a',
                                            #vertical=True
                                        ),
                                    ],
                                    width=7
                                ),
                                #date filter
                                dbc.Col(
                                    html.Div(
                                        dcc.Dropdown(id='pubhome_date_filter', clearable=True, searchable=True, placeholder="LOWER YYYY"),
                                        className="dash-bootstrap" 
                                    ),
                                    style={'min-width': '8%', 'padding-left': '0.5rem', 'padding-right': '0.5rem'}
                                ),
                                dbc.Col(
                                    html.Div(
                                        dcc.Dropdown(id='pubhome_date_filter_upper', clearable=True, searchable=True, placeholder="UPPER YYYY"),
                                        className="dash-bootstrap" 
                                    ),
                                    style={'min-width': '8%', 'padding-left': '0.5rem', 'padding-right': '0.5rem'}
                                ),
                                
                                #search filter
                                dbc.Col(
                                    [
                                        dbc.Input(
                                            type="text", id="pub_filter", placeholder="Search"
                                        ),
                                    ],
                                    style={'min-width': '22%', 'padding-left': '0.5rem', 'padding-right': '0.5rem'}
                                ),
                            ],
                            className="mb-3",
                        ),
                        #publist
                        html.Div(id='publist')
                    ]
                )
            ]
        )
    ]
)

# df = pd.DataFrame({"a": [1, 2, 3, 4], "b": [2, 1, 5, 6], "c": ["x", "x", "y", "y"]})
# @app.callback(
#     Output("download-dataframe-csv", "data"),
#     Input("btn_csv", "n_clicks"),
#     prevent_initial_call=True,
# )

# def func(n_clicks):
#     return dcc.send_data_frame(df.to_csv, "mydf.csv")

@app.callback(
    [
        Output('pubhome_date_filter', 'options'),
        Output('pubhome_date_filter_upper', 'options')
    ],
    [
        Input('url', 'pathname'),
        Input('tabs', 'active_tab'),
        Input('pubhome_date_filter', 'value'),
    ]
) 

def pubhome_loaddropdown(pathname, tab, initial_date):
    if pathname == '/publications_home':
        if tab == 'tab_a':
            pubhome_sql_date_filter = """SELECT DISTINCT (a_year) as label, (a_year) as value
                                from authorships
                                ORDER BY value DESC"""
        elif tab == 'tab_p':
            pubhome_sql_date_filter = """SELECT DISTINCT (p_year) as label, (p_year) as value
                                from presentations
                                ORDER BY value DESC"""
        elif tab == 'tab_r':
            pubhome_sql_date_filter = """SELECT DISTINCT (r_year) as label, (r_year) as value
                                from projects
                                ORDER BY value DESC"""
        elif tab == 'tab_o':
            pubhome_sql_date_filter = """SELECT DISTINCT (o_year) as label, (o_year) as value
                                from others
                                ORDER BY value DESC"""
        else:
            raise PreventUpdate
        
        pubhome_values_date_filter = []
        pubhome_cols_date_filter = ['label', 'value']
        pubhome_date_filter_included = db.querydatafromdatabase(pubhome_sql_date_filter, pubhome_values_date_filter, pubhome_cols_date_filter)
        pubhome_date_filter_options = pubhome_date_filter_included.to_dict('records')

        if initial_date: 
            if tab == 'tab_a':
                pubhome_sql_date_filter_upper = """SELECT DISTINCT (a_year) as label, (a_year) as value
                                from authorships
                                WHERE cast(a_year as int) >=  %s 
                                ORDER BY value DESC"""
            elif tab == 'tab_p':
                pubhome_sql_date_filter_upper = """SELECT DISTINCT (p_year) as label, (p_year) as value
                                    from presentations
                                    WHERE cast(p_year as int) >=  %s 
                                    ORDER BY value DESC"""
            elif tab == 'tab_r':
                pubhome_sql_date_filter_upper = """SELECT DISTINCT (r_year) as label, (r_year) as value
                                    from projects
                                    WHERE cast(r_year as int) >=  %s 
                                    ORDER BY value DESC"""
            elif tab == 'tab_o':
                pubhome_sql_date_filter_upper = """SELECT DISTINCT (o_year) as label, (o_year) as value
                                    from others
                                    WHERE cast(o_year as int) >=  %s 
                                    ORDER BY value DESC"""
            
            pubhome_values_filter_upper = [initial_date]
            pubhome_cols_date_filter_upper = ['label', 'value']
            
            pubhome_date_filter_included_upper = db.querydatafromdatabase(pubhome_sql_date_filter_upper, pubhome_values_filter_upper, pubhome_cols_date_filter_upper)
            pubome_date_filter_options_upper = pubhome_date_filter_included_upper.to_dict('records')
        else: 
            pubome_date_filter_options_upper = pubhome_date_filter_options
    
    
    
    else:
        raise PreventUpdate
    
    return [pubhome_date_filter_options, pubome_date_filter_options_upper]    


@app.callback(
    [
        Output('publist', 'children'), 
        Output('modals_holder', 'children')
    ],
    [
        Input('url', 'pathname'),
        Input('tabs', 'active_tab'),
        Input('pub_filter', 'value'),
        Input('pubhome_date_filter', 'value'), 
        Input('pubhome_date_filter_upper', 'value')
    ]
)

def pubhome_loadpublist(pathname, tab, searchterm, datefilter, datefilter_u):
    if pathname == '/publications_home':
        
        if tab == 'tab_a':
            sql_a = """SELECT
                    a_year,
                    publications.pub_id,
                    faculty_fn || ' ' || faculty_ln AS faculty_full_name,
                    tag_short_title,
                    pub_title,
                    a_authors,
                    authorship_role.a_label,
                    authorship_subcategory.a_author_subcat_label,
                    To_char(a_date, 'Month YYYY'), 
                    a_pub_name, 
                    a_publisher, 
                    a_doi, 
                    a_isxn, 
                    a_scopus
                FROM authorships
                    INNER JOIN publications on authorships.pub_id = publications.pub_id
                    INNER JOIN faculty on publications.user_id = faculty.user_id
                    INNER JOIN tags on publications.tag_id = tags.tag_id
                    FULL JOIN authorship_role on authorships.authorship_role = authorship_role.a_label_id
                    FULL JOIN authorship_subcategory on authorships.authorship_subcategory = authorship_subcategory.a_author_subcat_id
                WHERE
                    pub_delete_ind = false
                
                """
            values_a = []
            cols_a = ['Year','id', 'Faculty Involved', 'Publication Criteria', 'Title', 'All Authors', 'Involvement', 'Involvement2', 'Date', 'Publication', 'Publisher', 'DOI','ISXN', 'Scopus'] 
            
            #fix additivity of searchterms and filters
            if datefilter:
                sql_a += """AND (cast (a_year as int) >= %s)"""
                values_a += [datefilter]
                if datefilter_u:
                    sql_a += """AND (cast (a_year as int) <= %s)"""
                    values_a += [datefilter_u]
                    if searchterm:
                        sql_a += """ AND (
                            ((faculty_fn || ' ' || faculty_ln) ILIKE %s) OR (pub_title ILIKE %s) OR (a_year ILIKE %s)
                            OR (a_authors ILIKE %s) OR (a_pub_name ILIKE %s) OR ((To_char(a_date, 'Month YYYY')) ILIKE %s)
                            OR (a_publisher ILIKE %s) OR (a_doi ILIKE %s) OR (a_isxn ILIKE %s) OR (a_scopus ILIKE %s) OR (tag_short_title ILIKE %s)
                            )"""
                        values_a += [f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%",
                                f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%",
                                f"%{searchterm}%", f"%{searchterm}%"]
                if searchterm:
                    sql_a += """ AND (
                        ((faculty_fn || ' ' || faculty_ln) ILIKE %s) OR (pub_title ILIKE %s) OR (a_year ILIKE %s)
                        OR (a_authors ILIKE %s) OR (a_pub_name ILIKE %s) OR ((To_char(a_date, 'Month YYYY')) ILIKE %s)
                        OR (a_publisher ILIKE %s) OR (a_doi ILIKE %s) OR (a_isxn ILIKE %s) OR (a_scopus ILIKE %s) OR (tag_short_title ILIKE %s)
                        )"""
                    values_a += [f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%",
                            f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%",
                            f"%{searchterm}%", f"%{searchterm}%"]
                    if datefilter_u:
                        sql_a += """AND (cast (a_year as int) <= %s)"""
                        values_a += [datefilter_u]
                else:
                    sql_a += """"""
                    values_a += [] 
                    
            elif datefilter_u: 
                sql_a += """AND (cast (a_year as int) <= %s)"""
                values_a += [datefilter_u]
                if datefilter:
                    sql_a += """AND (cast (a_year as int) >= %s)"""
                    values_a += [datefilter]
                    if searchterm:
                        sql_a += """ AND (
                            ((faculty_fn || ' ' || faculty_ln) ILIKE %s) OR (pub_title ILIKE %s) OR (a_year ILIKE %s)
                            OR (a_authors ILIKE %s) OR (a_pub_name ILIKE %s) OR ((To_char(a_date, 'Month YYYY')) ILIKE %s)
                            OR (a_publisher ILIKE %s) OR (a_doi ILIKE %s) OR (a_isxn ILIKE %s) OR (a_scopus ILIKE %s) OR (tag_short_title ILIKE %s)
                            )"""
                        values_a += [f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%",
                                f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%",
                                f"%{searchterm}%", f"%{searchterm}%"]
                if searchterm:
                    sql_a += """ AND (
                        ((faculty_fn || ' ' || faculty_ln) ILIKE %s) OR (pub_title ILIKE %s) OR (a_year ILIKE %s)
                        OR (a_authors ILIKE %s) OR (a_pub_name ILIKE %s) OR ((To_char(a_date, 'Month YYYY')) ILIKE %s)
                        OR (a_publisher ILIKE %s) OR (a_doi ILIKE %s) OR (a_isxn ILIKE %s) OR (a_scopus ILIKE %s) OR (tag_short_title ILIKE %s)
                        )"""
                    values_a += [f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%",
                            f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%",
                            f"%{searchterm}%", f"%{searchterm}%"]
                    if datefilter:
                        sql_a += """AND (cast (a_year as int) >= %s)"""
                        values_a += [datefilter]
                else:
                    sql_a += """"""
                    values_a += [] 
            
            elif searchterm:
                sql_a += """ AND (
                    ((faculty_fn || ' ' || faculty_ln) ILIKE %s) OR (pub_title ILIKE %s) OR (a_year ILIKE %s)
                    OR (a_authors ILIKE %s) OR (a_pub_name ILIKE %s) OR ((To_char(a_date, 'Month YYYY')) ILIKE %s)
                    OR (a_publisher ILIKE %s) OR (a_doi ILIKE %s) OR (a_isxn ILIKE %s) OR (a_scopus ILIKE %s) OR (tag_short_title ILIKE %s)
                    )"""
                values_a += [f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%",
                        f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", 
                        f"%{searchterm}%", f"%{searchterm}%"]
                if datefilter:
                    sql_a += """AND (cast (a_year as int) >= %s)"""
                    values_a += [datefilter]
                    if datefilter_u:
                        sql_a += """AND (cast (a_year as int) <= %s)"""
                        values_a += [datefilter_u]
                elif datefilter_u:
                    sql_a += """AND (cast (a_year as int) <= %s)"""
                    values_a += [datefilter_u]
                    if datefilter:
                        sql_a += """AND (cast (a_year as int) >= %s)"""
                        values_a += [datefilter]
                else:
                    sql_a += """"""
                    values_a += []     
            else:
                sql_a += """"""
                values_a += []
                
            sql_a += """ORDER BY authorships.a_year DESC"""
            pub_a = db.querydatafromdatabase(sql_a, values_a, cols_a) 
            
            modals_a = []
            if pub_a.shape[0]: 
                buttons_a = [] 
                # pub_details = []
                # other_info = []
                
                
                for ids in pub_a['id']: 
                    buttons_a += [
                        html.Div(
                            # dbc.Button('View', id = f"modal_button_{ids}", href=f"/publication_details_a?mode=view&id={ids}", size='sm', color='primary', ), 
                            dbc.Button('View', id = f"modal_button_{ids}", size='sm', color='danger', ), 
                            style={'text-align': 'center'} 
                        ) 
                    ]
                
                for i in range(len(pub_a)): 
                    ids = pub_a['id'][i]
                    pub_title = pub_a['Title'][i]
                    pub_faculty_assoc = pub_a['Faculty Involved'][i]
                    pub_category = pub_a['Publication Criteria'][i]
                    pub_authors = pub_a['All Authors'][i]
                    pub_involvement = pub_a['Involvement'][i]
                    pub_involvement2 = pub_a['Involvement2'][i]
                    pub_date = pub_a['Date'][i]
                    pub_publication = pub_a['Publication'][i]
                    pub_publisher = pub_a['Publisher'][i]
                    pub_DOI = pub_a['DOI'][i]
                    pub_ISXN = pub_a['ISXN'][i]
                    pub_Scopus = pub_a['Scopus'][i]
                    
                    modals_a += [
                        html.Div(
                            dbc.Modal(
                                [
                                    dbc.ModalHeader(dbc.ModalTitle("Publication Details"), style=mod_style), 
                                    dbc.ModalBody([
                                        html.Div([
                                            html.Strong("Title: "),
                                            html.Span(f"{pub_title}"), ], id = f"modal_title_{ids}"
                                        ),
                                        html.Div([
                                            html.Strong("Faculty Involved: "),  
                                            html.Span(f"{pub_faculty_assoc}"),], id = f"modal_pub_faculty_{ids}"
                                        ),       
                                        html.Div([
                                            html.Strong("Publication Category: "), 
                                            html.Span(f"{pub_category}"),], id = f"modal_pub_category_{ids}"
                                        ), 
                                        html.Div([
                                            html.Strong("Authors: "),
                                            html.Span(f"{pub_authors}"),], id = f"modal_authors_{ids}"),
                                        html.Div([
                                            html.Strong("Involvement: "), 
                                            html.Span(f"{pub_involvement} ({pub_involvement2})"),], id = f"modal_involvement_{ids}"),
                                        html.Div([
                                            html.Strong("Date of Publication: "), 
                                            html.Span(f"{pub_date}"),], id = f"modal_date_{ids}"),
                                        html.Div([
                                            html.Strong("Publication: "),
                                            html.Span(f"{pub_publication}"),], id = f"modal_publication_{ids}"),
                                        html.Div([
                                            html.Strong("Publishing House: "),
                                            html.Span(f"{pub_publisher}"),], id = f"modal_publisher_{ids}"),
                                        html.Div([
                                            html.Strong("DOI: "),
                                            html.Span(f"{pub_DOI}"),], id = f"modal_DOI_{ids}"),
                                        html.Div([
                                            html.Strong("ISXN: "), 
                                            html.Span(f"{pub_ISXN}"),], id = f"modal_ISXN_{ids}"),
                                        html.Div([
                                            html.Strong("Scopus: "), 
                                            html.Span(f"{pub_Scopus}"),], id = f"modal_scopus_{ids}"), 
                                    ],), 
                                    # dbc.ModalFooter(
                                    #     dbc.Button("Close", id= f'modal_close_{ids}', n_clicks = 0)
                                    # )
                                ], 
                                id = f"modal_a_{ids}", size ='lg',
                                centered=True, is_open = False
                            ),  id= f'div_modal_{ids}', style={'display': 'none'}
                        )
                    ]
                
                # for i in range(len(pub_a)): 
                #     inputs_1 = [pub_a['Date'][i], pub_a['Publication'][i], pub_a['Publisher'][i]]
                #     if not all (inputs_1) :  
                #         pub_details += " "
                #     else: 
                #         pub_details += [("Published in/on: %s in %s by %s" % (pub_a['Date'][i], pub_a['Publication'][i], pub_a['Publisher'][i]))] 
                #     # inputs_2 = [pub_a['DOI'][i], pub_a['ISXN'][i], pub_a['Scopus'][i]]
                #     # if not all (inputs_2): 
                #     #     other_info += " "
                #     # else: 
                #     other_info += [("DOI: %s \n Issue Number: %s \n Scopus: %s"  % (pub_a['DOI'][i], pub_a['ISXN'][i], pub_a['Scopus'][i]) or " " )]
                # pub_a['Publication Details'] = pub_details
                # pub_a['Other Information'] = other_info
                pub_a['More Details'] = buttons_a 
                # pub_a['Modals'] = modals_a

            pub_a.drop(['id'],axis=1,inplace=True)
            pub_a.drop(['Date'],axis=1,inplace=True)
            pub_a.drop(['Publication'],axis=1,inplace=True)
            pub_a.drop(['Publisher'],axis=1,inplace=True)
            pub_a.drop(['DOI'],axis=1,inplace=True)
            pub_a.drop(['ISXN'],axis=1,inplace=True)
            pub_a.drop(['Scopus'],axis=1,inplace=True)
            pub_a.drop(['Involvement2'],axis=1,inplace=True)
            
            if pub_a.shape[0]:
                table_a = dbc.Table.from_dataframe(pub_a, striped=True, bordered=True, hover=True, size='sm', style={"whiteSpace": "pre-line"}) 
            else:
                table_a = "No records to display"
            return [table_a, modals_a]
        
        elif tab == 'tab_p':
            sql_p = """SELECT
                    p_year,
                    publications.pub_id,
                    faculty_fn || ' ' || faculty_ln AS faculty_full_name,
                    tag_short_title,
                    pub_title,
                    p_authors,
                    to_char(p_start_date, 'Month DD, YYYY'), 
                    to_char(p_end_date, 'Month DD, YYYY'), 
                    p_conf, 
                    p_loc, 
                    p_add_info
                FROM presentations
                    INNER JOIN publications on presentations.pub_id = publications.pub_id
                    INNER JOIN faculty on publications.user_id = faculty.user_id
                    INNER JOIN tags on publications.tag_id = tags.tag_id
                WHERE
                    pub_delete_ind = false
                """
            values_p = []
            cols_p = ['Year', 'id', 'Faculty Involved', 'Publication Criteria', 'Title', 'Presenter/s', 'Start Date', 'End Date', 'Conference',
                      'Location', 'Other Info'] 
            
            if datefilter:
                sql_p += """AND (cast (p_year as int) >= %s)"""
                values_p += [datefilter]
                if datefilter_u:
                    sql_p += """AND (cast (p_year as int) <= %s)"""
                    values_p += [datefilter_u]
                    if searchterm:
                        sql_p += """ AND (
                            ((faculty_fn || ' ' || faculty_ln) ILIKE %s) OR (pub_title ILIKE %s) 
                            OR (p_authors ILIKE %s) OR (p_year ILIKE %s) OR (p_conf ILIKE %s)
                            OR (p_loc ILIKE %s) OR (p_add_info ILIKE %s) OR (tag_short_title ILIKE %s)
                            OR (to_char(p_start_date, 'Month DD, YYYY') ILIKE %s) OR (to_char(p_end_date, 'Month DD, YYYY')ILIKE %s)
                            )"""
                        values_p += [f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", 
                                f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%",
                                f"%{searchterm}%", f"%{searchterm}%",]
                if searchterm:
                    sql_p += """ AND (
                        ((faculty_fn || ' ' || faculty_ln) ILIKE %s) OR (pub_title ILIKE %s) 
                        OR (p_authors ILIKE %s) OR (p_year ILIKE %s) OR (p_conf ILIKE %s)
                        OR (p_loc ILIKE %s) OR (p_add_info ILIKE %s) OR (tag_short_title ILIKE %s)
                        OR (to_char(p_start_date, 'Month DD, YYYY') ILIKE %s) OR (to_char(p_end_date, 'Month DD, YYYY')ILIKE %s)
                        )"""
                    values_p += [f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", 
                            f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%",
                            f"%{searchterm}%", f"%{searchterm}%",]
                    if datefilter_u:
                        sql_p += """AND (cast (p_year as int) <= %s)"""
                        values_p += [datefilter_u]
                else:
                    sql_p += """"""
                    values_p += [] 
            
            elif datefilter_u: 
                sql_p += """AND (cast (p_year as int) <= %s)"""
                values_p += [datefilter_u]
                if datefilter:
                    sql_p += """AND (cast (p_year as int) >= %s)"""
                    values_p += [datefilter]
                    if searchterm:
                        sql_p += """ AND (
                            ((faculty_fn || ' ' || faculty_ln) ILIKE %s) OR (pub_title ILIKE %s) 
                            OR (p_authors ILIKE %s) OR (p_year ILIKE %s) OR (p_conf ILIKE %s)
                            OR (p_loc ILIKE %s) OR (p_add_info ILIKE %s) OR (tag_short_title ILIKE %s)
                            OR (to_char(p_start_date, 'Month DD, YYYY') ILIKE %s) OR (to_char(p_end_date, 'Month DD, YYYY')ILIKE %s)
                            )"""
                        values_p += [f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", 
                                f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%",
                                f"%{searchterm}%", f"%{searchterm}%",]
                if searchterm:
                    sql_p += """ AND (
                        ((faculty_fn || ' ' || faculty_ln) ILIKE %s) OR (pub_title ILIKE %s) 
                        OR (p_authors ILIKE %s) OR (p_year ILIKE %s) OR (p_conf ILIKE %s)
                        OR (p_loc ILIKE %s) OR (p_add_info ILIKE %s) OR (tag_short_title ILIKE %s)
                        OR (to_char(p_start_date, 'Month DD, YYYY') ILIKE %s) OR (to_char(p_end_date, 'Month DD, YYYY')ILIKE %s)
                        )"""
                    values_p += [f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", 
                            f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%",
                            f"%{searchterm}%", f"%{searchterm}%",]
                    if datefilter:
                        sql_p += """AND (cast (p_year as int) >= %s)"""
                        values_p += [datefilter]
                        
                else:
                    sql_p += """"""
                    values_p += [] 
            
            elif searchterm:
                sql_p += """ AND (
                    ((faculty_fn || ' ' || faculty_ln) ILIKE %s) OR (pub_title ILIKE %s) 
                    OR (p_authors ILIKE %s) OR (p_year ILIKE %s) OR (p_conf ILIKE %s)
                    OR (p_loc ILIKE %s) OR (p_add_info ILIKE %s) OR (tag_short_title ILIKE %s)
                    OR (to_char(p_start_date, 'Month DD, YYYY') ILIKE %s) OR (to_char(p_end_date, 'Month DD, YYYY')ILIKE %s)
                    )"""
                values_p += [f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", 
                        f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%",
                        f"%{searchterm}%", f"%{searchterm}%",]
                if datefilter:
                    sql_p += """AND (cast (p_year as int) >= %s)"""
                    values_p += [datefilter]
                    if datefilter_u:
                        sql_p += """AND (cast (p_year as int) <= %s)"""
                        values_p += [datefilter_u]
                if datefilter_u:
                        sql_p += """AND (cast (p_year as int) <= %s)"""
                        values_p += [datefilter_u]
                        if datefilter:
                            sql_p += """AND (cast (p_year as int) >= %s)"""
                            values_p += [datefilter]
                else:
                    sql_p += """"""
                    values_p += []     
            else:
                sql_p += """"""
                values_p += []
                
            sql_p += """ORDER BY presentations.p_year DESC"""
            pub_p = db.querydatafromdatabase(sql_p, values_p, cols_p)

            modals_p = []
            if pub_p.shape[0]:
                buttons_p = [] 
                # pres_details = []
                # other_details = []
                
                
                for id in pub_p['id']: 
                    buttons_p += [
                        html.Div(
                            dbc.Button('View', id = f"modal_button_{id}", size='sm', color='danger', ), 
                            style={'text-align': 'center'} 
                        ) 
                    ]
                
                for i in range(len(pub_p)): 
                    ids = pub_p['id'][i]
                    pub_title = pub_p['Title'][i]
                    pres_fac = pub_p['Faculty Involved'][i]
                    pres_category = pub_p['Publication Criteria'][i]
                    pres_conf = pub_p['Conference'][i]
                    pres_start = pub_p['Start Date'][i]
                    pres_end = pub_p['End Date'][i]
                    pres_loc = pub_p['Location'][i]
                    pres_other = pub_p['Other Info'][i]
                    
                    modals_p += [
                        html.Div(
                            dbc.Modal(
                                [
                                    dbc.ModalHeader(dbc.ModalTitle("Publication Details"), style=mod_style), 
                                    dbc.ModalBody([
                                        html.Div([
                                            html.Strong("Title: "), 
                                            html.Span(f"{pub_title}"),],id = f"modal_title_{ids}"),
                                        html.Div([
                                            html.Strong("Faculty Involved: "), 
                                            html.Span(f"{pres_fac}"),], id = f"modal_pres_fac_{ids}"),
                                        html.Div([
                                            html.Strong("Presentation Category: "), 
                                            html.Span(f"{pres_category}"),],  id = f"modal_pres_cat_{ids}"),
                                        html.Div([
                                            html.Strong("Conference: "), 
                                            html.Span(f"{pres_conf}"),], id = f"modal_pres_conf_{ids}"),
                                        html.Div([
                                            html.Strong("Presentation Date: "),
                                            html.Span(f"{pres_start} to {pres_end}"),], id = f"modal_pres_date_{ids}"),
                                        html.Div([
                                            html.Strong("Presentation Location: "),
                                            html.Span(f"{pres_loc}"),], id = f"modal_pres_loc_{ids}"),
                                        html.Div([
                                            html.Strong("Additional Information: "), 
                                            html.Span(f"{pres_other}"),], id = f"modal_pres_other_{ids}")
                                    ],), 
                                    # dbc.ModalFooter(
                                    #     dbc.Button("Close", id= f'modal_close_{ids}', n_clicks = 0)
                                    # )
                                ], 
                                id = f"modal_a_{ids}", size ='lg',
                                centered=True, is_open = False
                            ),  id= f'div_modal_{ids}', style={'display': 'none'}
                        )
                    ]

                # for i in range(len(pub_p)): 
                #     pres_details += [("Presented from: %s to %s \n Presented at: %s (%s)" % (pub_p['Start Date'][i], pub_p['End Date'][i], pub_p['Conference'][i], pub_p['Location'][i]) or "No Details Provided")]
                #     other_details += [pub_p['Other Info'][i]] 
            
                # pub_p['Presentation Details'] = pres_details
                # pub_p['Additional Info'] = other_details
                pub_p['More Details'] = buttons_p
                
            pub_p.drop(['id'],axis=1,inplace=True)
            pub_p.drop(['Start Date'],axis=1,inplace=True)
            pub_p.drop(['End Date'],axis=1,inplace=True)
            pub_p.drop(['Conference'],axis=1,inplace=True)
            pub_p.drop(['Location'],axis=1,inplace=True)
            pub_p.drop(['Other Info'],axis=1,inplace=True)
            
            if pub_p.shape[0]:
                table_p = dbc.Table.from_dataframe(pub_p, striped=True, bordered=True, hover=True, size='sm', style={"whiteSpace": "pre-line"}) 
            else:
                table_p = "No records to display"
            return [table_p, modals_p]
    
        elif tab == 'tab_r':
            sql_r = """SELECT
                    r_year,
                    publications.pub_id,
                    faculty_fn || ' ' || faculty_ln AS faculty_full_name,
                    tag_short_title,
                    pub_title,
                    r_roles, 
                    r_timeframe, 
                    to_char(r_start_date, 'Month DD, YYYY'),
                    to_char(r_end_date, 'Month DD, YYYY'), 
                    r_fund_org, 
                    r_contract_link 
                FROM projects
                    INNER JOIN publications on projects.pub_id = publications.pub_id
                    INNER JOIN faculty on publications.user_id = faculty.user_id
                    INNER JOIN tags on publications.tag_id = tags.tag_id
                WHERE
                    pub_delete_ind = false
                
                """
            values_r = []
            cols_r = ['Year', 'id', 'Faculty Involved', 'Publication Criteria', 'Title', 'Role', 'Timeframe', 'Start Date', 'End Date', 'Funding Organization', 'Contract'] 
            
            if datefilter:
                sql_r += """AND (cast (r_year as int) >= %s)"""
                values_r += [datefilter]
                if datefilter_u:
                    sql_r += """AND (cast (r_year as int) <= %s)"""
                    values_r += [datefilter_u]
                    if searchterm:
                        sql_r += """ AND (
                            (r_year ILIKE %s) OR ((faculty_fn || ' ' || faculty_ln) ILIKE %s) OR (pub_title ILIKE %s) 
                            OR (r_roles ILIKE %s) OR (r_timeframe ILIKE %s) OR (r_fund_org ILIKE %s) OR (tag_short_title ILIKE %s)
                            OR ((To_char(r_start_date, 'Month DD, YYYY')) ILIKE %s) OR ((To_char(r_end_date, 'Month DD, YYYY')) ILIKE %s)
                            )"""
                        values_r += [f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", 
                            f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%",
                            ]  
                if searchterm:
                    sql_r += """ AND (
                        (r_year ILIKE %s) OR ((faculty_fn || ' ' || faculty_ln) ILIKE %s) OR (pub_title ILIKE %s) 
                        OR (r_roles ILIKE %s) OR (r_timeframe ILIKE %s) OR (r_fund_org ILIKE %s) OR (tag_short_title ILIKE %s)
                        OR ((To_char(r_start_date, 'Month DD, YYYY')) ILIKE %s) OR ((To_char(r_end_date, 'Month DD, YYYY')) ILIKE %s)
                        )"""
                    values_r += [f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", 
                        f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%",
                    ]  
                    if datefilter_u:
                        sql_r += """AND (cast (r_year as int) <= %s)"""
                        values_r += [datefilter_u]
                else:
                    sql_r += """"""
                    values_r += [] 
                    
            elif datefilter_u: 
                sql_r += """AND (cast (r_year as int) <= %s)"""
                values_r += [datefilter_u]
                if datefilter:
                    sql_r += """AND (cast (r_year as int) >= %s)"""
                    values_r += [datefilter]
                    if searchterm:
                        sql_r += """ AND (
                            (r_year ILIKE %s) OR ((faculty_fn || ' ' || faculty_ln) ILIKE %s) OR (pub_title ILIKE %s) 
                            OR (r_roles ILIKE %s) OR (r_timeframe ILIKE %s) OR (r_fund_org ILIKE %s) OR (tag_short_title ILIKE %s)
                            OR ((To_char(r_start_date, 'Month DD, YYYY')) ILIKE %s) OR ((To_char(r_end_date, 'Month DD, YYYY')) ILIKE %s)
                            )"""
                        values_r += [f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%",
                                f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%"]
                if searchterm:
                    sql_r += """ AND (
                        (r_year ILIKE %s) OR ((faculty_fn || ' ' || faculty_ln) ILIKE %s) OR (pub_title ILIKE %s) 
                        OR (r_roles ILIKE %s) OR (r_timeframe ILIKE %s) OR (r_fund_org ILIKE %s) OR (tag_short_title ILIKE %s)
                        OR ((To_char(r_start_date, 'Month DD, YYYY')) ILIKE %s) OR ((To_char(r_end_date, 'Month DD, YYYY')) ILIKE %s)
                        )"""
                    values_r += [f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%",
                            f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%"]
                    if datefilter:
                        sql_r += """AND (cast (r_year as int) >= %s)"""
                        values_r += [datefilter]

                else:
                    sql_r += """"""
                    values_r += [] 
                    
            elif searchterm:
                sql_r += """ AND (
                        (r_year ILIKE %s) OR ((faculty_fn || ' ' || faculty_ln) ILIKE %s) OR (pub_title ILIKE %s) 
                        OR (r_roles ILIKE %s) OR (r_timeframe ILIKE %s) OR (r_fund_org ILIKE %s) OR (tag_short_title ILIKE %s)
                        OR ((To_char(r_start_date, 'Month DD, YYYY')) ILIKE %s) OR ((To_char(r_end_date, 'Month DD, YYYY')) ILIKE %s)
                        )"""
                values_r += [f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", 
                        f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%",
                        ]  
                if datefilter:
                    sql_r += """AND (cast (r_year as int) >= %s)"""
                    values_r += [datefilter]
                    if datefilter_u:
                        sql_r += """AND (cast (r_year as int) <= %s)"""
                        values_r += [datefilter_u]
                if datefilter_u:
                    sql_r += """AND (cast (r_year as int) <= %s)"""
                    values_r += [datefilter_u]
                    if datefilter:
                        sql_r += """AND (cast (r_year as int) >= %s)"""
                        values_r += [datefilter]
                    
                else:
                    sql_r += """"""
                    values_r += []     
            else:
                sql_r += """"""
                values_r += []    
            
            sql_r += """ORDER BY projects.r_year DESC"""
            pub_r = db.querydatafromdatabase(sql_r, values_r, cols_r)
            
            modals_r = []
            if pub_r.shape[0]:
                buttons_r=[] 
                # proj_details1 = []
                # proj_details2 = [] 
                # proj_details = []
                

                for id in pub_r['id']: 
                    buttons_r += [
                        html.Div(
                            dbc.Button('View', id = f"modal_button_{id}", size='sm', color='danger', ), 
                            style={'text-align': 'center'} 
                        ) 
                    ]
                
                for i in range(len(pub_r)): 
                    ids = pub_r['id'][i]
                    pub_title = pub_r['Title'][i]
                    proj_fac = pub_r['Faculty Involved'][i]
                    proj_role = pub_r['Role'][i]
                    proj_tag = pub_r['Publication Criteria'][i]
                    proj_start = pub_r ['Start Date'][i]
                    proj_end = pub_r['End Date'][i]
                    proj_timeframe = pub_r['Timeframe'][i]
                    proj_org = pub_r['Funding Organization'][i]
                    proj_contract = pub_r['Contract'][i]
                    
                    modals_r += [
                        html.Div(
                            dbc.Modal(
                                [
                                    dbc.ModalHeader(dbc.ModalTitle("Publication Details"), style=mod_style), 
                                    dbc.ModalBody([
                                        html.Div([
                                            html.Strong("Title: "),
                                            html.Span(f"{pub_title}"),], id = f"modal_title_{ids}"),
                                        html.Div([
                                            html.Strong("Faculty Involved: "), 
                                            html.Span(f"{proj_fac}"),], id = f"modal_proj_fac_{ids}"),
                                        html.Div([
                                            html.Strong("Project Role: "), 
                                            html.Span(f"{proj_role}"),], id = f"modal_proj_role_{ids}"),
                                        html.Div([
                                            html.Strong("Project Category: "), 
                                            html.Span(f"{proj_tag}"),], id = f"modal_proj_tag_{ids}"),
                                        html.Div([
                                            html.Strong("Project Duration: "), 
                                            html.Span(f"{proj_start} to {proj_end}. Completed in {proj_timeframe}"),], id = f"modal_proj_duration_{ids}"),
                                        html.Div([
                                            html.Strong("Funding Organization: "), 
                                            html.Span(f"{proj_org}"),], id = f"modal_proj_org_{ids}"),
                                        html.Div([
                                            html.Strong("Contract Copy: "), 
                                            html.Span(f"{proj_contract}"),], id = f"modal_proj_contract_{ids}"),
                                    ],), 
                                    # dbc.ModalFooter(
                                    #     dbc.Button("Close", id= f'modal_close_{ids}', n_clicks = 0)
                                    # )
                                ], 
                                id = f"modal_a_{ids}", size ='lg',
                                centered=True, is_open = False
                            ),  id= f'div_modal_{ids}', style={'display': 'none'}
                        )
                    ]

                pub_r['More Details'] = buttons_r

            pub_r.drop(['id'],axis=1,inplace=True)
            pub_r.drop(['Contract'],axis=1,inplace=True)
            pub_r.drop(['Start Date'],axis=1,inplace=True)
            pub_r.drop(['End Date'],axis=1,inplace=True)
            pub_r.drop(['Timeframe'],axis=1,inplace=True)
            pub_r.drop(['Role'],axis=1,inplace=True)
            pub_r.drop(['Funding Organization'],axis=1,inplace=True)
            
            if pub_r.shape[0]:
                table_r = dbc.Table.from_dataframe(pub_r, striped=True, bordered=True, hover=True, size='sm', style={"whiteSpace": "pre-line"}) 
            else:
                table_r = "No records to display"
            return [table_r, modals_r] 
            
        elif tab == 'tab_o':
            sql_o = """SELECT
                    o_year,
                    publications.pub_id,
                    faculty_fn || ' ' || faculty_ln AS faculty_full_name,
                    tag_short_title,
                    pub_title,
                    To_char(o_date, 'Month DD, YYYY'),
                    o_add_info
                FROM others
                    INNER JOIN publications on others.pub_id = publications.pub_id
                    INNER JOIN faculty on publications.user_id = faculty.user_id
                    INNER JOIN tags on publications.tag_id = tags.tag_id
                WHERE
                    pub_delete_ind = false
                """
            values_o = []
            cols_o = ['Year', 'id', 'Faculty Involved', 'Publication Criteria', 'Title', 'Date', 'Other Info'] 
            
            if datefilter:
                sql_o += """AND (cast (o_year as int) >= %s)"""
                values_o += [datefilter]
                if datefilter_u:
                    sql_o += """AND (cast (o_year as int) <= %s)"""
                    values_o += [datefilter_u]
                    if searchterm:
                        sql_o += """ AND (
                            (o_year ILIKE %s) OR (pub_title ILIKE %s) OR ((To_char(o_date, 'Month DD, YYYY')) ILIKE %s)
                            OR (o_add_info ILIKE %s) OR ((faculty_fn || ' ' || faculty_ln) ILIKE %s) OR (tag_short_title ILIKE %s)
                            )"""
                        values_o += [f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", 
                            f"%{searchterm}%",]
                if searchterm:
                    sql_o += """ AND (
                        (o_year ILIKE %s) OR (pub_title ILIKE %s) OR ((To_char(o_date, 'Month DD, YYYY')) ILIKE %s)
                        OR (o_add_info ILIKE %s) OR ((faculty_fn || ' ' || faculty_ln) ILIKE %s) OR (tag_short_title ILIKE %s)
                        )"""
                    values_o += [f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", 
                        f"%{searchterm}%",]
                    if datefilter_u:
                        sql_o += """AND (cast (o_year as int) <= %s)"""
                        values_o += [datefilter_u]
                else:
                    sql_o += """"""
                    values_o += [] 
                    
            elif datefilter_u: 
                sql_o += """AND (cast (o_year as int) <= %s)"""
                values_o += [datefilter_u]
                if datefilter: 
                    sql_o += """AND (cast (o_year as int) >= %s)"""
                    values_o += [datefilter]
                    if searchterm:
                        sql_o += """ AND (
                            (o_year ILIKE %s) OR (pub_title ILIKE %s) OR ((To_char(o_date, 'Month DD, YYYY')) ILIKE %s)
                            OR (o_add_info ILIKE %s) OR ((faculty_fn || ' ' || faculty_ln) ILIKE %s) OR (tag_short_title ILIKE %s)
                            )"""
                        values_o += [f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", 
                            f"%{searchterm}%",]
                if searchterm:
                    sql_o += """ AND (
                        (o_year ILIKE %s) OR (pub_title ILIKE %s) OR ((To_char(o_date, 'Month DD, YYYY')) ILIKE %s)
                        OR (o_add_info ILIKE %s) OR ((faculty_fn || ' ' || faculty_ln) ILIKE %s) OR (tag_short_title ILIKE %s)
                        )"""
                    values_o += [f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", 
                        f"%{searchterm}%",]
                    if datefilter: 
                        sql_o += """AND (cast (o_year as int) >= %s)"""
                        values_o += [datefilter]
                else:
                    sql_o += """"""
                    values_o += [] 
                    
            elif searchterm:
                sql_o += """ AND (
                        (o_year ILIKE %s) OR (pub_title ILIKE %s) OR ((To_char(o_date, 'Month DD, YYYY')) ILIKE %s)
                        OR (o_add_info ILIKE %s) OR ((faculty_fn || ' ' || faculty_ln) ILIKE %s) OR (tag_short_title ILIKE %s)
                        )"""
                values_o += [f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", 
                        f"%{searchterm}%",]
                if datefilter:
                    sql_o += """AND (cast (o_year as int) >= %s)"""
                    values_o += [datefilter]
                    if datefilter_u:
                        sql_o += """AND (cast (o_year as int) <= %s)"""
                        values_o += [datefilter_u]
                if datefilter_u:
                    sql_o += """AND (cast (o_year as int) <= %s)"""
                    values_o += [datefilter_u]
                    if datefilter:
                        sql_o += """AND (cast (o_year as int) >= %s)"""
                        values_o += [datefilter]
                    
                else:
                    sql_o += """"""
                    values_o += []    
            else:
                sql_o += """"""
                values_o += []
 
            
            sql_o += """ORDER BY others.o_year DESC"""
            pub_o = db.querydatafromdatabase(sql_o, values_o, cols_o)

            modals_o = []           
            if pub_o.shape[0]:
                buttons_o=[]
                

                for id in pub_o['id']: 
                    buttons_o += [
                        html.Div(
                            dbc.Button('View', id = f"modal_button_{id}", size='sm', color='danger' ), 
                            style={'text-align': 'center'} 
                        ) 
                    ]
                pub_o['More Details'] = buttons_o
                
                for i in range(len(pub_o)): 
                    ids = pub_o['id'][i]
                    pub_title = pub_o['Title'][i]
                    other_fac = pub_o['Faculty Involved'][i]
                    other_cat = pub_o['Publication Criteria'][i]
                    other_date = pub_o['Date'][i]
                    other_other = pub_o['Other Info'][i]
                    
                    modals_o += [
                        html.Div(
                            dbc.Modal(
                                [
                                    dbc.ModalHeader(dbc.ModalTitle("Publication Details"), style=mod_style), 
                                    dbc.ModalBody([
                                        html.Div([
                                            html.Strong("Title: "),
                                            html.Span(f"{pub_title}"),], id = f"modal_title_{ids}"), 
                                        html.Div([
                                            html.Strong("Faculty Involved: "), 
                                            html.Span(f"{other_fac}"),], id = f"modal_other_fac{ids}" ),
                                        html.Div([
                                            html.Strong("Category: "), 
                                            html.Span(f"{other_cat}"),], id = f"modal_other_cat{ids}" ),
                                        html.Div([
                                            html.Strong("Date: "), 
                                            html.Span(f"{other_date}"),], id = f"modal_other_date{ids}" ),
                                        html.Div([
                                            html.Strong("Additional Information: "), 
                                            html.Span(f"{other_other}"),], id = f"modal_other_other{ids}" ),
                                    ],), 
                                    # dbc.ModalFooter(
                                    #     dbc.Button("Close", id= f'modal_close_{ids}', n_clicks = 0)
                                    # )
                                ], 
                                id = f"modal_a_{ids}", size ='lg',
                                centered=True, is_open = False
                            ),  id= f'div_modal_{ids}', style={'display': 'none'}
                        )
                    ]

            pub_o.drop(['id'],axis=1,inplace=True)
            pub_o.drop(['Date'],axis=1,inplace=True)
            pub_o.drop(['Other Info'],axis=1,inplace=True)

            if pub_o.shape[0]:
                table_o = dbc.Table.from_dataframe(pub_o, striped=True, bordered=True, hover=True, size='sm', style={"whiteSpace": "pre-line"}) 
                
            else:
                table_o = "No records to display."
            return [table_o, modals_o]    
             
    else: 
        raise PreventUpdate      

sql_aa = """SELECT
        publications.pub_id
        
    FROM publications
    WHERE
        pub_delete_ind = false
    
    """
values_aa = []
cols_aa = ['id'] 

pub_aa = db.querydatafromdatabase(sql_aa, values_aa, cols_aa)

for ids in pub_aa['id']: 
    modal_a = f"modal_a_{ids}"
    modal_button = f"modal_button_{ids}"
    modal_close = f'modal_close_{ids}'
    div_modal = f'div_modal_{ids}'
    @app.callback(
        
        Output(modal_a, 'is_open'), 
        
        [
            Input(modal_button, 'n_clicks'), 
            # Input(modal_close, 'n_clicks')
        ], 
        [
            State(modal_button, 'is_open')
        ]
    )
    
    def ihopethisworks(n_clicks, open): 
        if n_clicks: 
            return True
        else: 
            return False

    