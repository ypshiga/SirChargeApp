# SirChargeApp
<h2>Overview</h2>
Sir Charge A Lot is a web app to help people find and compare hospital costs in California. Hospital pricing information is usually pretty tough to find for any one individual hospital - it is even harder to compare costs across hospitals. For California, this data is collected by the State and <a href="https://data.chhs.ca.gov/dataset/chargemasters/resource/95e415ee-5c11-40b9-b693-ff9af7985a94">hosted publicly</a> but the data is not accessible to the average person. That's why I created Sir Charge A Lot - a web app to make healthcare pricing data accessible. The app is deployed via <a href="https://www.heroku.com/">Heroku</a> using <a href="https://streamlit.io/">Streamlit</a> with interactive plots made using <a href="https://plotly.com/">Plotly</a>.


<h2>App link here! </h2>
Find the app here: https://sirchargealot.herokuapp.com/

<h2>Data </h2>
The <a href="https://data.chhs.ca.gov/dataset/chargemasters/resource/95e415ee-5c11-40b9-b693-ff9af7985a94">data</a> is from CA hospital "Chargemasters" for 2020.

<h2>Details</h2>
The costs for the top ~25 services per hospital for ~300 hospitals are collected by the State of California and hosted at the link above. For this project I processes, cleaned and standardized the data and loaded it into a [Pandas](https://pandas.pydata.org) DataFrame. I then used [Plotly](https://plotly.com) + [Streamlit](https://streamlit.io) to make interactive visuals to help people discover and compare the costs at hospitals near them. I also used this [Plotly Events Component](https://github.com/null-jones/streamlit-plotly-events) to use points selected on the map to create additional plots/tables.<br><br>

As described on the app page, these costs do not neccesarily reflect "out-of-pocket" expenses. The costs listed here do not factor in insurance and can therefore be higher or lower depending on the negogiated rates of any particular insurer. The goal of this app is to help people make informed healthcare decisions and hopefully save money. Healthcare costs transparancey is a notoriously complicated issue, read more about it here: [WSJ: Hospitals hide pricing data](https://www.wsj.com/articles/hospitals-hide-pricing-data-from-search-results-11616405402) and [NPR: Hospitals have started posting their prices](https://www.npr.org/sections/health-shots/2021/07/02/1012317032/hospitals-have-started-posting-their-prices-online-heres-what-they-reveal).

If you have any questions or comments feel free to reach out: <yoichishiga@gmail.com>

This web app was developed for the [TDI Data Science Fellowship](https://www.thedataincubator.com/programs/data-science-fellowship).

<h2>Demo videos </h2>
Check out a few demo clips:


https://user-images.githubusercontent.com/44503923/130150720-46528d8d-9bd7-4d8e-9886-2485b8726a6f.mp4



https://user-images.githubusercontent.com/44503923/130150731-016d706d-3018-4280-8b56-aac7dd9e3aa7.mp4



https://user-images.githubusercontent.com/44503923/130150761-4431ec4d-4cc6-43c2-b5f7-d77109d891cb.mp4



https://user-images.githubusercontent.com/44503923/130150749-c3910dfe-409b-4599-a318-5d6cb5f433ba.mp4


