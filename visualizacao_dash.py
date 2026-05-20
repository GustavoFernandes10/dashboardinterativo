import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output

df = pd.read_csv('ecommerce_estatistica.csv')
print(df.head())
print(df.describe())
print(df.info())
pd.isnull(df).sum()

lista_qtd_vendidos = df['Qtd_Vendidos'].unique()
options = [{'label': Qtd_Vendidos, 'value': Qtd_Vendidos} for Qtd_Vendidos in lista_qtd_vendidos]

def cria_graficos(selecao_Qtd_Vendidos):
    # Gráfico de barra
    filtro_df = df[df['Qtd_Vendidos'].isin(selecao_Qtd_Vendidos)]

    fig1 = px.bar(filtro_df, x='Qtd_Vendidos', y='Marca', color='Qtd_Vendidos', barmode='group', color_discrete_sequence=px.colors.qualitative.Pastel)
    fig1.update_layout(title='Marca por Quantidade Vendida', xaxis_title='Quantidade Vendida', yaxis_title='Marca')

    fig2 = px.scatter_3d(filtro_df, x='Qtd_Vendidos', y='Marca', z='Preço', color='Qtd_Vendidos', color_discrete_sequence=px.colors.qualitative.Pastel)
    fig2.update_layout(title='Relação quantidade vendida e marca', scene=dict(xaxis_title='Quantidade Vendida', yaxis_title='Marca', zaxis_title='Desconto'))
    return fig1, fig2

def cria_app():
    app = Dash(__name__)
    app.layout = html.Div([
        html.H1('Análise de Clientes - Visualização Interativa'),
        dcc.Checklist(
            id='qtd-vendidos-Checklist',
            options=[
        {'label': Qtd_Vendidos, 'value': Qtd_Vendidos}
        for Qtd_Vendidos in df['Qtd_Vendidos'].unique()
        ],
            value=df['Qtd_Vendidos'].unique().tolist(),
            inline=False
        ),
        dcc.Graph(id='grafico-barra'),
        dcc.Graph(id='grafico-3d')
    ])

    @app.callback(
        [Output('grafico-barra', 'figure'), Output('grafico-3d', 'figure')],
        [Input('qtd-vendidos-Checklist', 'value')]
    )
    def atualizar_graficos(selecao_Qtd_Vendidos):
        if selecao_Qtd_Vendidos is None or len(selecao_Qtd_Vendidos) == 0:
            selecao_Qtd_Vendidos = lista_qtd_vendidos
        fig1, fig2 = cria_graficos(selecao_Qtd_Vendidos)
        return fig1, fig2

    return app

if __name__ == '__main__':    
    app = cria_app()
    
app.run(debug=True, port=8050)