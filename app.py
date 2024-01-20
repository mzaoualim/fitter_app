'''
Interactive app to identify and visualize stocks
probability distribution approximation and characteristics
'''

from datetime import date
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import yfinance as yf
from fitter import Fitter, get_distributions

from helper_functions import data_loader
st.set_option('deprecation.showPyplotGlobalUse', False)

def main():
        st.write("""
        # 
        """)
        st.markdown("<h1 style='text-align: center;'> Discover the best probability distribution fit to stock market data </h1>", unsafe_allow_html=True)

        st.write('---')

        ## dataset
        st.markdown("<h2 style='text-align: center;'> Pick the Data </h2>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns(3)

        with col1:
                ticker = st.text_input('Type your ticker:', 'AAPL')

        
        with col2:
                period = st.selectbox('Closing Prices Period',
                                ('1d', '5d', '1mo', '3mo', '6mo','1y', '2y', '5y', '10y', 'ytd', 'max'))

        with col3:
                interval = st.selectbox('Closing Prices intervals',
                                ('1m', '2m', '5m', '15m', '30m', '60m', '90m', '1h', '1d', '5d', '1wk', '1mo', '3mo'))
                
        
        a, b = st.columns(2)
        with a:
                st.info('Check out the tickers list [here](https://stockanalysis.com/stocks/)', icon="ℹ️")

        with b:
                st.info('Please consider these interval limitations: 1m data is only for available for last 7 days and data interval < 1d for the last 60 days', icon="ℹ️")


        
        submit = st.button('Retrieve the Data', use_container_width=True)

        if submit:
                #loading closing price
                dataset = data_loader(ticker, period, interval)

                # plot histogram
                fig, ax = plt.subplots()
                ax.hist(dataset.values, density=True)
                ax.set_xlabel('Closing Price')
                ax.set_ylabel('Probability density')
                ax.set_title('Closing Price Histogram')
                st.pyplot(fig)
                        
                #fitting data
                st.markdown("<h2 style='text-align: center;'> Fit the Data </h2>", unsafe_allow_html=True)

                f = Fitter(dataset, distributions = get_distributions())
                
                with st.spinner('Looking for the best fit...'):
                        f.fit(progress = True)
                st.success("Fitting's Done!")

                #plot data + approx distributions
                st.markdown("<h2 style='text-align: center;'> Approximate the Data Distribution </h2>", unsafe_allow_html=True)
                st.write(f.summary(Nbest = 1), use_container_width=True)
                fig = f.plot_pdf(Nbest = 1, lw = 1)
                st.pyplot(fig, use_container_width=True)
                                
                st.markdown("<h2 style='text-align: center;'> Best Distribution Parameters </h2>", unsafe_allow_html=True)
                st.write(pd.DataFrame(f.get_best()), use_container_width=True)
                
                st.balloons()



if __name__ == "__main__":
    main()
