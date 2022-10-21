from urllib import response
import yfinance as yf
import pandas as pd
import requests
from bs4 import BeautifulSoup
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def make_graph(stock_data, revenue_data, stock):
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, subplot_titles=("Historical Share Price", "Historical Revenue"), vertical_spacing = .3)
    stock_data_specific = stock_data[stock_data.Date <= '2021--06-14']
    revenue_data_specific = revenue_data[revenue_data.Date <= '2021-04-30']
    fig.add_trace(go.Scatter(x=pd.to_datetime(stock_data_specific.Date, infer_datetime_format=True), y=stock_data_specific.Close.astype("float"), name="Share Price"), row=1, col=1)
    fig.add_trace(go.Scatter(x=pd.to_datetime(revenue_data_specific.Date, infer_datetime_format=True), y=revenue_data_specific.Revenue.astype("float"), name="Revenue"), row=2, col=1)
    fig.update_xaxes(title_text="Date", row=1, col=1)
    fig.update_xaxes(title_text="Date", row=2, col=1)
    fig.update_yaxes(title_text="Price ($US)", row=1, col=1)
    fig.update_yaxes(title_text="Revenue ($US Millions)", row=2, col=1)
    fig.update_layout(showlegend=False,
    height=900,
    title=stock,
    xaxis_rangeslider_visible=True)
    fig.show()

tesla = yf.Ticker("TSLA")
tesla_stock_info = tesla.history("max")
tesla_stock_info.reset_index(inplace=True)
print(tesla_stock_info.head())

url = "https://www.macrotrends.net/stocks/charts/TSLA/tesla/revenue"
html_data = requests.get(url).text
soup = BeautifulSoup(html_data,"html5lib")
tesla_revenue_data = pd.DataFrame(columns=["Date","Revenue"])
for row in soup.find_all("tbody")[1].find_all("tr"):
    col = row.find_all("td")
    date = col[0].text
    revenue= col[1].text
    tesla_revenue_data = tesla_revenue_data.append({"Date":date,"Revenue":revenue},ignore_index=True)
tesla_revenue_data["Revenue"] = tesla_revenue_data["Revenue"].str.replace(',|\$',"")
tesla_revenue_data.dropna(True)
tesla_revenue_data = tesla_revenue_data[tesla_revenue_data['Revenue'] != ""]
print(tesla_revenue_data.tail())


gme = yf.Ticker("GME")
gme_data = gme.history("max")
gme_data.reset_index(inplace=True)
print(gme_data.head())



gme_url = " https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/labs/project/stock.html"
gme_html_data = requests.get(gme_url).text
gme_soup = BeautifulSoup(gme_html_data,"html5lib")
gme_revenue_data = pd.DataFrame(columns=["Date","Revenue"])
for gme_row in gme_soup.find_all("tbody")[1].find_all("tr"):
    gme_col = gme_row.find_all("td")
    gme_date = gme_col[0].text
    gme_revenue = gme_col[1].text
    gme_revenue_data = gme_revenue_data.append({"Date":gme_date,"Revenue":gme_revenue},ignore_index=True)
gme_revenue_data["Revenue"] = gme_revenue_data["Revenue"].str.replace(",|\$","")
print(gme_revenue_data.tail())

make_graph(tesla_stock_info,tesla_revenue_data,"Tesla")
make_graph(gme_data,gme_revenue_data,"GameStop")