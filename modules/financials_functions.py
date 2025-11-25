import pandas as pd 
import numpy as np
import scipy.stats as stats
from.backend import market_prices

def portfolio_volatility(
        df:pd.DataFrame,
        vector_w:np.array
    ) -> float:
    
    """
    Calculo de la volatilidad de un portfolio de 
    inversiones

    df(pd.DataFrame):
        DataFrame de retornos del portafolio.
    vector:w (np.array)
        vector de pesos de los instrumentos del portafolio

    Return (float): volatilidad de portafolio
    """

    # matriz varianza covarianza #
    m_cov = df.cov()

    #vector traspuesto 
    vector_w_t = np.array([vector_w])

    #varianza
    vector_cov = np.dot(m_cov,vector_w)
    varianza = np.dot(vector_w_t,vector_cov)

    #volatilidad
    vol = np.sqrt(varianza)

    return vol[0]

def porfafolio_returns(
        tickers: list,
        start: str,
        end: str,
        )   -> pd.DataFrame:

    '''

    Descarga desde la base de datos los precios de los instrumentos 
    indicados en el rango de fechas

    ticker (list):
        lista de menos instrumentos que componen
        el portafolio
    start (str):
        feche de inicio de precios
    end (str): 
    feche de termino de precios

    Return (pd.DataFrame): DataFrame de retornos diarios

    '''

    #descargar precios
    df = market_prices(
    start_date=start,
    end_date=end,
    tickers=tickers
    )

    df_pivot = pd.pivot_table(
    data=df, 
    index='FECHA', 
    columns='TICKER', 
    values='PRECIO_CIERRE', 
    aggfunc= 'max'
    )
    df_pivot = df_pivot.pct_change().dropna()
    return df_pivot

def VaR(sigma:float, confidence:float) -> float:
    '''
    Calculo del value at Risk al nivel de confianza indicado
    con supuesto de media cero
    '''

    #estadistico z al nivel de confianza
    z_score = stats.norm.ppf(confidence)

    #VaR
    var = z_score * sigma

    return var

