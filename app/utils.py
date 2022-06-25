"""
This is a utils module that contains helper functions for the dashboard.
"""
from dash import html, dcc, dash_table


def header(app):
    """
    This is a header function that returns the header and menu of the dashboard.

    Args:
        app (Dash): Dash application object.

    Returns:
        html.Div: html.Div object containing the header and menu.
    """
    return html.Div([get_header(app), html.Br([]), get_menu()])


def get_header(app):
    """
    This is header function that returns the header of the dashboard.

    Args:
        app (Dash): Dash application object.

    Returns:
        html.Div: html.Div object containing the header.
    """
    header_content = html.Div(
        [
            html.Div(
                [
                    html.A(
                        html.Img(
                            src=app.get_asset_url(
                                "PortfolioTrackerLogos/Portfolio Tracker Rectangle.png"
                            ),
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
    return header_content


def get_menu():
    """
    This is a menu function that returns the menu of the dashboard.

    Returns:
        html.Div: html.Div object containing the menu.
    """
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


def make_html_table(table_df):
    """
    Return a dash definition of an HTML table for a Pandas dataframe.
    """
    table = []
    for _, row in table_df.iterrows():
        html_row = []
        for _, value in enumerate(row):
            html_row.append(html.Td([value]))
        table.append(html.Tr(html_row))
    return table

def make_dash_table(
    table_df,
    editable=False,
    page_size=10,
    **kwargs
):
    """
    Return a dash table for a Pandas dataframe.
    """
    sort_mode=kwargs.get("sort_mode", "single")
    style_cell=kwargs.get('style_cell', {'padding':'4px'})
    style_cell_conditional=kwargs.get('style_cell_conditional', {})
    hidden_columns=kwargs.get('style_cell_conditional', []),
    return dash_table.DataTable(
        data=table_df.to_dict('records'),
        columns=[{"name": i, "id": i} for i in table_df.columns],
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
    