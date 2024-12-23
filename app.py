import streamlit as st
import pandas as pd
import requests
import yfinance as yf
import matplotlib.pyplot as plt
from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.foreignexchange import ForeignExchange

# Function to call the World Bank API
def fetch_nominal_gdp(country_code):
    url = f'http://api.worldbank.org/v2/country/{country_code}/indicator/NY.GDP.MKTP.CD?format=json'
    try:
        response = requests.get(url)
        data = response.json()
        if len(data) > 1:
            df = pd.json_normalize(data[1])  # Flatten the nested JSON
            df = df[['country.value', 'date', 'value']]  # Extract relevant columns
            df.columns = ['Country', 'Date', 'Номинальный ВВП']  # Rename columns
            return df
        else:
            st.error("No Номинальный ВВП data found")
            return None
    except Exception as e:
        st.error(f"Error fetching Номинальный ВВП data: {e}")
        return None

# Function to fetch Темпы роста реального ВВП
def fetch_real_gdp_growth(country_code):
    url = f'http://api.worldbank.org/v2/country/{country_code}/indicator/NY.GDP.MKTP.KD.ZG?format=json'
    try:
        response = requests.get(url)
        data = response.json()
        if len(data) > 1:
            df = pd.json_normalize(data[1])  # Flatten the nested JSON
            df = df[['country.value', 'date', 'value']]  # Extract relevant columns
            df.columns = ['Country', 'Date', 'Темпы роста реального ВВП']  # Rename columns
            return df
        else:
            st.error("No Темпы роста реального ВВП data found")
            return None
    except Exception as e:
        st.error(f"Error fetching Темпы роста реального ВВП data: {e}")
        return None

# Function to fetch ВВП на душу населения
def fetch_gdp_per_capita(country_code):
    url = f'http://api.worldbank.org/v2/country/{country_code}/indicator/NY.GDP.PCAP.CD?format=json'
    try:
        response = requests.get(url)
        data = response.json()
        if len(data) > 1:
            df = pd.json_normalize(data[1])  # Flatten the nested JSON
            df = df[['country.value', 'date', 'value']]  # Extract relevant columns
            df.columns = ['Country', 'Date', 'ВВП на душу населения']  # Rename columns
            return df
        else:
            st.error("No ВВП на душу населения data found")
            return None
    except Exception as e:
        st.error(f"Error fetching ВВП на душу населения data: {e}")
        return None

# Function to fetch Государственные расходы (% от ВВП)
def fetch_government_expenditure(country_code):
    url = f'http://api.worldbank.org/v2/country/{country_code}/indicator/NE.CON.GOVT.ZS?format=json'
    try:
        response = requests.get(url)
        data = response.json()
        if len(data) > 1:
            df = pd.json_normalize(data[1])  # Flatten the nested JSON
            df = df[['country.value', 'date', 'value']]  # Extract relevant columns
            df.columns = ['Country', 'Date', 'Государственные расходы (% от ВВП)']  # Rename columns
            return df
        else:
            st.error("No Государственные расходы data found")
            return None
    except Exception as e:
        st.error(f"Error fetching Государственные расходы data: {e}")
        return None
    
# Function to fetch Real GDP (Actual Values)
def fetch_real_gdp_actual(country_code):
    url = f'http://api.worldbank.org/v2/country/{country_code}/indicator/NY.GDP.MKTP.KD?format=json'
    try:
        response = requests.get(url)
        data = response.json()
        if len(data) > 1:
            df = pd.json_normalize(data[1])  # Flatten the nested JSON
            df = df[['country.value', 'date', 'value']]  # Extract relevant columns
            df.columns = ['Country', 'Date', 'Реальный ВВП (фактический)']  # Rename columns
            return df
        else:
            st.error("No Real GDP data found")
            return None
    except Exception as e:
        st.error(f"Error fetching Real GDP data: {e}")
        return None
    
# Function to fetch Inflation (Consumer Prices, annual %)
def fetch_inflation(country_code):
    url = f'http://api.worldbank.org/v2/country/{country_code}/indicator/FP.CPI.TOTL.ZG?format=json'
    try:
        response = requests.get(url)
        data = response.json()
        if len(data) > 1:
            df = pd.json_normalize(data[1])  # Flatten the nested JSON
            df = df[['country.value', 'date', 'value']]  # Extract relevant columns
            df.columns = ['Country', 'Date', 'Инфляция (%)']  # Rename columns
            return df
        else:
            st.error("No Inflation data found")
            return None
    except Exception as e:
        st.error(f"Error fetching Inflation data: {e}")
        return None

# Main function to aggregate all data
def fetch_world_bank_data(country_code):
    # Fetch data from each indicator function
    nominal_gdp_df = fetch_nominal_gdp(country_code)
    real_gdp_growth_df = fetch_real_gdp_growth(country_code)
    gdp_per_capita_df = fetch_gdp_per_capita(country_code)
    government_expenditure_df = fetch_government_expenditure(country_code)
    real_gdp_df = fetch_real_gdp_actual(country_code)  # Real GDP (Actual values)
    inflation_df = fetch_inflation(country_code)  # Inflation data

    # Combine all the dataframes on 'Date'
    if nominal_gdp_df is not None and real_gdp_growth_df is not None and gdp_per_capita_df is not None and government_expenditure_df is not None and real_gdp_df is not None and inflation_df is not None:
        combined_df = nominal_gdp_df
        combined_df = pd.merge(combined_df, real_gdp_growth_df[['Date', 'Темпы роста реального ВВП']], on='Date', how='outer')
        combined_df = pd.merge(combined_df, gdp_per_capita_df[['Date', 'ВВП на душу населения']], on='Date', how='outer')
        combined_df = pd.merge(combined_df, government_expenditure_df[['Date', 'Государственные расходы (% от ВВП)']], on='Date', how='outer')
        combined_df = pd.merge(combined_df, real_gdp_df[['Date', 'Реальный ВВП (фактический)']], on='Date', how='outer')
        combined_df = pd.merge(combined_df, inflation_df[['Date', 'Инфляция (%)']], on='Date', how='outer')
        
        # Ensure Date is in the correct format
        combined_df['Date'] = pd.to_datetime(combined_df['Date'], errors='coerce')

        # Return the combined DataFrame
        return combined_df
    else:
        return None


# Function to call the Alpha Vantage API
def fetch_alpha_vantage_data(symbol):
    api_key = 'your_alpha_vantage_api_key'  # Replace with your actual key
    ts = TimeSeries(key=api_key, output_format='pandas')
    try:
        data, meta_data = ts.get_daily(symbol=symbol, outputsize='compact')
        return data
    except Exception as e:
        st.error(f"Error fetching data from Alpha Vantage: {e}")
        return None

# Function to call the Yahoo Finance API
def fetch_yahoo_finance_data(symbol):
    try:
        data = yf.download(symbol, period='1y', interval='1d')
        return data
    except Exception as e:
        st.error(f"Error fetching data from Yahoo Finance: {e}")
        return None

# Function to call the OECD API (example for GDP data)
def fetch_oecd_data(country_code):
    url = f'https://stats.oecd.org/SDMX-JSON/data/NAAGDP/{country_code}.json'
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors
        data = response.json()

        if "dataSets" in data and data["dataSets"]:
            # Normalize and clean the data if available
            df = pd.json_normalize(data['dataSets'][0]['series'])
            return df
        else:
            st.error(f"No GDP data available for country code {country_code} from OECD.")
            return None
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching data from OECD: {e}")
        return None

# Function to fetch currency exchange rate data using Alpha Vantage
def fetch_currency_data(from_currency, to_currency):
    api_key = 'your_alpha_vantage_api_key'  # Replace with your actual API key
    fx = ForeignExchange(key=api_key, output_format='pandas')
    
    try:
        # Fetch the historical exchange rate data for the given currency pair
        data, meta_data = fx.get_currency_exchange_daily(
            from_symbol=from_currency,
            to_symbol=to_currency,
            outputsize='full'  # This gives the full historical data
        )
        return data
    except Exception as e:
        st.error(f"Error fetching currency data from Alpha Vantage: {e}")
        return None

# Function to plot exchange rate data
def plot_currency_data(df, from_currency, to_currency):
    if df is not None:
        fig, ax = plt.subplots(figsize=(10, 6))
        # Plot the '4. close' column (daily closing exchange rate) without markers for a smoother line
        ax.plot(df.index, df['4. close'], color='b', linestyle='-', linewidth=1.5, label=f'{from_currency}/{to_currency} Exchange Rate')
        
        ax.set_title(f"Currency Exchange Rate: {from_currency}/{to_currency} Over Time")
        ax.set_xlabel('Date')
        ax.set_ylabel(f'Exchange Rate ({from_currency}/{to_currency})')
        ax.grid(True)
        
        # Rotate date labels for better readability
        plt.xticks(rotation=45)
        
        st.pyplot(fig)


# Function to plot GDP data
# def plot_gdp_data(df):
#     if df is not None:
#         df['date'] = pd.to_datetime(df['date'], format='%Y')
#         fig, ax = plt.subplots()
#         ax.plot(df['date'], df['value'], marker='o', color='b', linestyle='-', label='Номинальный ВВП')
#         ax.set_title("Номинальный ВВП Over Time")
#         ax.set_xlabel('Year')
#         ax.set_ylabel('GDP in USD')
#         ax.grid(True)
#         st.pyplot(fig)

# Function to plot Номинальный ВВП
def plot_without_dates(df, column, title, ylabel):
    if df is not None:
        # Ensure 'Date' column is in datetime format
        df['Date'] = pd.to_datetime(df['Date'], errors='coerce')  # Convert 'Date' column to datetime
        df = df.dropna(subset=['Date'])  # Drop rows with invalid or missing 'Date' values
        
        # Set 'Date' column as the index
        df.set_index('Date', inplace=True)

        # Now plot using df.index (which is the Date column) as x-axis
        fig, ax = plt.subplots()
        ax.plot(df.index, df[column], marker='o', linestyle='-', label=title)

        # Set plot titles and labels
        ax.set_title(title)
        ax.set_xlabel('Date')  # This will now correctly label the x-axis as 'Date'
        ax.set_ylabel(ylabel)
        ax.grid(True)

        # Rotate date labels for better readability
        plt.xticks(rotation=45)

        st.pyplot(fig)

# Function to plot Номинальный ВВП
def plot_nominal_gdp(df):
    plot_without_dates(df, 'Номинальный ВВП', "Номинальный ВВП Over Time", 'Номинальный ВВП in USD')

# Function to plot Темпы роста реального ВВП
def plot_real_gdp_growth(df):
    plot_without_dates(df, 'Темпы роста реального ВВП', "Темпы роста реального ВВП Over Time", 'Темпы роста реального ВВП (%)')

# Function to plot Real GDP
def plot_real_gdp(df):
    plot_without_dates(df, 'Реальный ВВП (фактический)', "Реальный ВВП (фактический) Over Time", 'Real GDP (Constant Prices)')

# Function to plot Inflation
def plot_inflation(df):
    plot_without_dates(df, 'Инфляция (%)', "Инфляция (%) Over Time", 'Инфляция (%) Rate (%)')

# Function to plot Государственные расходы
def plot_government_expenditure(df):
    plot_without_dates(df, 'Государственные расходы (% от ВВП)', "Государственные расходы Over Time", 'Expenditure (% of GDP)')



# def display_economic_indicators(country_code):
#     # Fetch data
#     world_bank_data = fetch_world_bank_data(country_code)
    
#     if world_bank_data is not None:
#         # Plot each indicator
#         plot_nominal_gdp(world_bank_data)
#         plot_real_gdp_growth(world_bank_data)
#         plot_real_gdp(world_bank_data)
#         plot_inflation(world_bank_data)
#         plot_government_expenditure(world_bank_data)
#     else:
#         st.error("Error fetching World Bank data.")

# Function to plot Alpha Vantage stock data
def plot_alpha_stock_data(df, symbol):
    if df is not None:
        fig, ax = plt.subplots()
        ax.plot(df.index, df['4. close'], marker='o', color='g', linestyle='-', label=f'{symbol} Stock Price')  # Alpha Vantage's "4. close"
        ax.set_title(f"Stock Price of {symbol} Over Time")
        ax.set_xlabel('Date')
        ax.set_ylabel('Stock Price (USD)')
        ax.grid(True)
        st.pyplot(fig)

# Function to plot Yahoo Finance stock data
def plot_yahoo_stock_data(df, symbol):
    if df is not None:
        fig, ax = plt.subplots()
        ax.plot(df.index, df['Close'], marker='o', color='b', linestyle='-', label=f'{symbol} Stock Price')  # Yahoo's "Close"
        ax.set_title(f"Stock Price of {symbol} Over Time")
        ax.set_xlabel('Date')
        ax.set_ylabel('Stock Price (USD)')
        ax.grid(True)
        st.pyplot(fig)

# Streamlit app setup
st.title("Загрузчик Экономических и Финансовых Данных")

# Ввод пользователя для кода страны, символа акции или валютной пары
country_code = st.text_input("Введите код страны (например, 'USA', 'ARG')")
symbol = st.text_input("Введите символ акции (например, 'AAPL', 'GOOG')")
from_currency = st.text_input("Введите код валюты 'из' (например, 'USD', 'EUR')")
to_currency = st.text_input("Введите код валюты 'в' (например, 'EUR', 'GBP')")



# Buttons to fetch data
if st.button("Загрузить данные Всемирного банка"):
    world_bank_data = fetch_world_bank_data(country_code)
    if world_bank_data is not None:
        st.write("Данные Всемирного банка:")
        st.dataframe(world_bank_data)
        
        # Построение всех графиков (без дат)
        plot_nominal_gdp(world_bank_data)
        plot_real_gdp_growth(world_bank_data)
        plot_real_gdp(world_bank_data)
        plot_inflation(world_bank_data)
        plot_government_expenditure(world_bank_data)


if st.button("Загрузить данные Alpha Vantage"):
    alpha_vantage_data = fetch_alpha_vantage_data(symbol)
    if alpha_vantage_data is not None:
        st.write(f"Данные Alpha Vantage для {symbol}:")
        st.dataframe(alpha_vantage_data)
        plot_alpha_stock_data(alpha_vantage_data, symbol)  # Построение графика акций с использованием функции Alpha Vantage

if st.button("Загрузить данные Yahoo Finance"):
    yahoo_finance_data = fetch_yahoo_finance_data(symbol)
    if yahoo_finance_data is not None:
        st.write(f"Данные Yahoo Finance для {symbol}:")
        st.dataframe(yahoo_finance_data)
        plot_yahoo_stock_data(yahoo_finance_data, symbol)  # Построение графика акций с использованием функции Yahoo Finance

if st.button("Загрузить данные OECD"):
    oecd_data = fetch_oecd_data(country_code)
    if oecd_data is not None:
        st.write("Данные OECD:")
        st.dataframe(oecd_data)

if st.button("Загрузить данные валют"):
    if from_currency and to_currency:
        currency_data = fetch_currency_data(from_currency, to_currency)
        if currency_data is not None:
            st.write(f"Данные валют для {from_currency}/{to_currency}:")
            st.dataframe(currency_data)  # Отображение сырых данных
            plot_currency_data(currency_data, from_currency, to_currency)  # Построение графика валют
    else:
        st.error("Пожалуйста, введите коды валют 'из' и 'в'.")