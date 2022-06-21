from dash import html, dcc, dash_table


def header(app):
    return html.Div([get_header(app), html.Br([]), get_menu()])


def get_header(app):
    header = html.Div(
        [
            html.Div(
                [
                    html.A(
                        html.Img(
                            src=app.get_asset_url("PortfolioTrackerLogos/Portfolio Tracker Rectangle.png"),
                            className="logo",
                        ),
                        href="#",
                    ),
                ],
                className="row",
            ),
        ],
        className="row",
    )
    return header


def get_menu():
    menu = html.Div(
        [
            dcc.Link(
                "Binance Overview",
                href="/",
                className="tab first",
            ),
        ],
        className="row all-tabs",
    )
    return menu


def make_html_table(df):
    """ Return a dash definition of an HTML table for a Pandas dataframe """
    table = []
    for index, row in df.iterrows():
        html_row = []
        for i in range(len(row)):
            html_row.append(html.Td([row[i]]))
        table.append(html.Tr(html_row))
    return table

def make_dash_table(df, editable=False, hidden_columns=[],page_size=10,sort_mode='single', style_cell={'padding':'4px'},style_cell_conditional={}):
    """ Return a dash table for a Pandas dataframe """
    return dash_table.DataTable(
        data=df.to_dict('records'),
        columns=[{"name": i, "id": i} for i in df.columns],
        editable=editable,
        hidden_columns=hidden_columns,
        export_format='xlsx',
        page_size=page_size,
        sort_action='native',
        sort_mode=sort_mode,
        style_cell=style_cell,
        style_cell_conditional=style_cell_conditional,
        style_as_list_view=True,
        style_header={'fontWeight':'bold'}
    )