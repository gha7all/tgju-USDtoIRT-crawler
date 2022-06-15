# tgju website crawler and visualizer
This project basically crawls data from tgju website by using selenium and visualizes the results with plotly.

## How to run
1. Change config.py file to your local information
2. Download and setup chromedriver
3. Activate virtual environment and run
```
pip install -r requirements.txt
```
<b> Do steps below by the following order: </b>
```
python crawler.py
```
Wait for it so that it crawls all data, then
```
python plot.py
```

<b>NOTE</b>: If there is any problem while executing(early stop, etc) check your internet connection and repeat above steps again.

## Demo
Daily Close Price
![](https://github.com/gha7all/Images/blob/master/Screenshot%20from%202022-06-16%2001-59-55.png)

Candlesticks
![](https://github.com/gha7all/Images/blob/master/Screenshot%20from%202022-06-16%2002-00-18.png)
