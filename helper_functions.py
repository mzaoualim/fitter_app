# helper functions
import yfinance as yf


def data_loader(ticker, period, interval):
    '''
    func to load the closing price of a the der
    '''
    # Getting stock Data from yahoo finance
    tickerData = yf.Ticker(ticker)
    tickerDf = tickerData.history(period=period, interval=interval)

    return tickerDf['Close']