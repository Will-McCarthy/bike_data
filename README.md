# bike_data

bike_data is a data science project focused on understanding the mountain bike market.

## Hi Linkedin,



In an effort to demonstrate my data science expertise, I turned my passion into a data science project, a "passion project" if you will.



As many of you know, I have a healthy obsession with mountain biking. Personally, I have four bikes. Although this would be enough for most people, the correct number of bikes is n+1, where n is the current number of bikes owned. I decided to find my next bike by doing some analysis on the mountain bike market.



1) The first step was to obtain a dataset, so I wrote a web scraper and pulled data on 41k mountain bikes from my favorite place to go shopping: Pinkbike's buy/sell market. This market is similar to craigslist for selling high-end, used mountain bikes. 

2) The second step was to get the data into a format that could be used. I used the title text to extract the model year and brand. Often the brand name was not explicity mentioned in the title, so I created a list of keywords that are used when refering to specific models in order to extract the brand.   

3) With that data, I created preliminary visualizations in Tableau to see what features may be useful in building models. I found that features like frame materials and brand had a significant impact, but features like frame size and location were not as correlated. 

4) I then trained and tested many different regression models using the most important features to find the best fit. I used a linear model, decision tree, random forrest, support vector machine and a polynomial model. 

Results: The linear model produced the fastest results, random forrest produced the most accurate and SVM and polynomial models were not fit for this application.The linear model and random forrest produced R^2 values of ~.67, meaning they were decent at estimating price, but often had large misses. The error in this model is likely due to 2 things: 
First is missing detail data. Pinkbike does not have accurate data on component spec or if the bike is an e-bike. Two bikes that have the same frame with different components can be thousands of dollars difference in price. 
The second source of error is the way these bikes are listed. Because private individuals list their bikes, there is variance between what two people think a bike is worth, making it harder to predict what the list price of a bike may be.   

Take a look at my project and the results on my github: https://github.com/Will-McCarthy/bike_data/tree/main.

Stay tuned on my account for more project updates!

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install the requirements for bike_data.

```bash
pip3 install -r requirements.txt
```


## Usage

```bash
python3 pinkbike_scraper.py
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

Please make sure to update tests as appropriate.
