import dash
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate
from dash.dependencies import Input, Output, State

import webbrowser

from app import app
from apps import commonmodules as cm
from apps import login
from apps.admin import dashboard, faculty_manage, faculty_profile, publications_manage, settings, reports, author_manage, author_profile
from apps.faculty import edit_my_profile, my_profile, my_publications
from apps.general import faculty_details, faculty_home, home, publications_home
from apps.forms import edit_password, form_authorships, form_presentations, form_projects, form_others, form_criteria, form_facrank, form_involvement, form_role, edit_username, form_presentations_copy, form_up_constituent, form_upd_unit, form_engg_dept

CONTENT_STYLE = { 
 "margin-left": "1em", 
 "margin-right": "1em", 
 "padding": "1em 1em", 
 "margin-top": "0em",
 "margin-bottom": "0em",
} 

app.layout = html.Div( 
    [ 
        dcc.Location(id='url', refresh=True), 
        dcc.Store(id='sessionlogout', data=True, storage_type='session'), 
        dcc.Store(id='currentuserid', data=-1, storage_type='session'), 
        dcc.Store(id='currentrole', data=-1, storage_type='session'), 
        
        html.Div( 
            cm.navbar, 
            id='navbar_div' 
        ),
        html.Div(id='page-content', style=CONTENT_STYLE), 
    ],
) 

#content callback for changed urls 
@app.callback( 
    [ 
        Output('page-content', 'children'),
        Output('navbar_div', 'style'), 
        Output('sessionlogout', 'data'), 
    ], 
    [ 
        Input('url', 'pathname') 
    ],
    [ 
        State('sessionlogout', 'data'), 
        State('currentuserid', 'data'),
        State('currentrole', 'data')
    ]  
) 
def displaypage(pathname,
                sessionlogout, currentuserid, currentrole
                ): 
    ctx = dash.callback_context 
    if ctx.triggered: 
        eventid = ctx.triggered[0]['prop_id'].split('.')[0] 
    else: 
        raise PreventUpdate 

    if eventid == 'url':
        print(currentuserid, currentrole, pathname, sessionlogout)
        if currentuserid == '': 
            currentuserid = -1
        if int(currentuserid) < 0:
            if pathname in ['/']:
                returnlayout = login.layout
            else: 
                returnlayout = '404: request not found. User not logged in.'
            navbar_div = {'display': 'none'}
        else:
            sessionlogout = False    

            if pathname == '/home':
                returnlayout = home.layout
            elif pathname == '/faculty_details':
                returnlayout = faculty_details.layout
            elif pathname == '/faculty_home': 
                returnlayout = faculty_home.layout
            elif pathname == '/publications_home':
                returnlayout = publications_home.layout
            
            elif pathname == '/my_profile': 
                returnlayout = my_profile.layout
            elif pathname == '/edit_my_profile': 
                returnlayout = edit_my_profile.layout
            elif pathname == '/my_publications': 
                returnlayout = my_publications.layout

            elif pathname == '/dashboard': 
                returnlayout = dashboard.layout
            elif pathname == '/faculty_manage':
                returnlayout = faculty_manage.layout
            elif pathname == '/faculty_profile':
                returnlayout = faculty_profile.layout
            elif pathname == '/publications_manage': 
                returnlayout = publications_manage.layout
            elif pathname == '/settings':
                returnlayout = settings.layout
            elif pathname == '/reports':
                returnlayout = reports.layout
            elif pathname == '/author_manage':
                returnlayout = author_manage.layout
            elif pathname == '/author_profile':
                returnlayout = author_profile.layout

            elif pathname == '/form_authorships':
                returnlayout = form_authorships.layout
            elif pathname == '/form_presentations':
                returnlayout = form_presentations.layout
            elif pathname == '/form_projects':
                returnlayout = form_projects.layout
            elif pathname == '/form_others':
                returnlayout = form_others.layout
            elif pathname == '/form_criteria': 
                returnlayout = form_criteria.layout
            elif pathname == '/form_role': 
                returnlayout = form_role.layout
            elif pathname == '/form_faculty_rank': 
                returnlayout = form_facrank.layout
            elif pathname == '/form_involvement': 
                returnlayout = form_involvement.layout
            elif pathname == '/edit_password':
                returnlayout = edit_password.layout
            elif pathname == '/edit_username':
                returnlayout = edit_username.layout
            elif pathname == '/form_up_constituent':
                returnlayout = form_up_constituent.layout
            elif pathname == '/form_upd_unit':
                returnlayout = form_upd_unit.layout
            elif pathname == '/form_engg_dept':
                returnlayout = form_engg_dept.layout


            elif pathname == '/form_presentations_copy':
                returnlayout = form_presentations_copy.layout
            


            elif pathname == '/login':
                returnlayout = login.layout 
                sessionlogout = True

            else:
                returnlayout = '404: request not found. URL does not exist.'
            navbar_div = {'display': 'none' if sessionlogout else 'unset'}
        
    else: 
        raise PreventUpdate 
    return [returnlayout, navbar_div, sessionlogout]


if __name__ == '__main__': 
    webbrowser.open('http://127.0.0.1:8050/', new=0, autoraise=True) 
    app.run_server(debug=False)
