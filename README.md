# Summary
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Collectible card games such as Magic the Gathering or the Pokemon Trading Card Game have been a longtime hobby of mine, but they were very expensive as a kid with no income. Therefore, I developed a basic application integrating Python's data collection and visualization and Google Sheets' data storage to track the prices of cards I was interested in and notify me when they passed certain thresholds.
  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;This was one of my first projects with Python, so while it had enormous room for improvement it was amazing to see the prices appearing on the sheet in front of me, and exciting to get automated emails when a card passed a predetermined threshold. I quickly moved on to develop a much more robust and extensive application ([mtg-goose](https://coltonglasgow13.github.io/mtg_goose/)), but as an initial project, mtg-python showed the potential of automated data collection in this market.

# Exploration
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;The cost of individual cards can range from pennies to hundreds of dollars, with constantly fluctuating markets. That got me thinking - if investing in the stock market can make you money, why couldn't the same thing work with collectible cards? So I started researching card prices, and quickly found a major roadblock to this idea: unlike the stock market, there are not well-developed sources of data for collectible cards.

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;By this point, I had begin to buy a variety of cards that I hoped to sell for a profit, mostly based on speculation, and I was tracking my inventory in a large Google Sheets file. Problem was, if I wanted to see how my investment was doing, I would have to go look up the price of a card manually, possibly across multiple different websites, which is very time-consuming with enough cards. 

> Manually checking the price of hundreds of cards in a cluttered, non-standardized document was not sustainable.
> 
> ![image alt ><](/images/mtg-sales-screenshot.png)

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;As a solution, I realized that automation would be necessary, and because there were no established resources publicly providing card price data, I would have to start from scratch.

# The First Scraper
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;I wanted to start by taking data from [Card Kingdom's Buylist](https://www.cardkingdom.com/purchasing/mtg_singles?filter[sort]=price_desc "Card Kingdom Buylist"), because it is relatively static and therefore easier to scrape, and because buylists are an important reference point for an investment. Larger companies create buylists to represent the cards they are willing to buy from individuals immediately for the posted price, and selling to them not only locks in money for your cards, but allows you to sell large amounts of the same card immediately rather than waiting for them to sell gradually on retail platforms. Therefore, they are the safest and most reliable way to value your cards.

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Using the [Google Sheets API](https://developers.google.com/sheets/api "Google Sheets API"), I integrated a spreadsheet with a small Python application. On one sheet I could manually list the cards I wanted to track the price of, which python could then read and then use to scrape the desired prices. After it goes to the website and gets each price, it would enter this data into another sheet.

> An example of data collected for a certain card over two days.
> 
> ![image alt ><](/images/scraper-screenshot-2.png)

An issue that soon emerged (and that was a critical failing point of the project overall) was that Google Sheets doesn't have the ability to efficiently store and access larger amounts of data, especially when using the API. Once the sheet started to fill with thousands of lines of data as the scraper ran automatically each day, access became impossible, so I had to routinely store the data in csv files on my computer rather than  

# Applications of the Data
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Because I wanted to use this system to automate as much as possible, I also set it up so that cards I wanted to track could have a price target. If the scraper found that a card had reached it's price target, it would automatically send me an email so I would know that I could sell my cards for a profit.

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Furthermore, now that I had access to all this data, I could visualize it to provide more context for my decisions and a more intuitive way to consider my investments. I established a simple [MatPlotLib](https://matplotlib.org/stable/index.html "MatPlotLib") script that would display the tracked prices over time for any particular card.
