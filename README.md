# SirChargeApp

Sir Charge A Lot is a web app to help people find and compare hospital costs in California. Hospital pricing information is usually pretty tough to find - that's why I created Sir Charge A Lot - a web app to make healthcare pricing data accessible.

Find the app here: https://sirchargealot.herokuapp.com/

The app is deployed via [Heroku](https://www.heroku.com/) using [Streamlit](https://streamlit.io/) with interactive plots made using [Plotly](https://plotly.com/) .

It uses data from CA hospital "Chargemaster" for 2020 https://data.chhs.ca.gov/dataset/chargemasters/resource/95e415ee-5c11-40b9-b693-ff9af7985a94

The costs for the top ~25 services per hospital for ~300 hospitals are collected by the State of California and hosted at the link above. For this project I processes, cleaned and standardized the data and loaded it into a [Pandas](https://pandas.pydata.org/) DataFrame. I then used Plotly + Streamlit to make interactive visuals to help people discover and compare the costs at hospitals near them and help them save money.

Check out a few demo clips:


https://user-images.githubusercontent.com/44503923/130150720-46528d8d-9bd7-4d8e-9886-2485b8726a6f.mp4



https://user-images.githubusercontent.com/44503923/130150731-016d706d-3018-4280-8b56-aac7dd9e3aa7.mp4



https://user-images.githubusercontent.com/44503923/130150761-4431ec4d-4cc6-43c2-b5f7-d77109d891cb.mp4



https://user-images.githubusercontent.com/44503923/130150749-c3910dfe-409b-4599-a318-5d6cb5f433ba.mp4


This is a web app developed for the [TDI Data Science Fellowship](https://www.thedataincubator.com/programs/data-science-fellowship/) .
