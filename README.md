# Summary
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Collectible card games such as Magic the Gathering or the Pokemon Trading Card Game have been a longtime hobby of mine, but they were very expensive as a kid with no income. Therefore, I developed a basic application integrating Python's data collection and visualization and Google Sheets' data storage to track the prices of cards I was interested in and notify me when they passed certain thresholds.
  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;This was one of my first projects with Python, so while it had enormous room for improvement it was amazing to see the prices appearing on the sheet in front of me, and exciting to get automated emails when a card passed a predetermined threshold. I quickly moved on to develop a much more robust and extensive application ([mtg-goose](https://coltonglasgow13.github.io/mtg_goose/)), but as an initial project, mtg-python showed the potential of automated data collection in this market.

## Exploration
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;The cost of individual cards can range from pennies to hundreds of dollars, with constantly fluctuating markets. That got me thinking - if investing in the stock market can make you money, why couldn't the same thing work with collectible cards? So I started researching card prices, and quickly found a major roadblock to this idea: unlike the stock market, there are not well-developed sources of data for collectible cards.

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;By this point, I had begin to buy a variety of cards that I hoped to sell for a profit, mostly based on speculation, and I was tracking my inventory in a large Google Sheets file. Problem was, if I wanted to see how my investment was doing, I would have to go look up the price of a card manually, possibly across multiple different websites, which is very time-consuming with enough cards. 

> Manually checking the price of hundreds of cards in a cluttered, non-standardized document was not sustainable.
> 
> ![image alt ><](/images/mtg-sales-screenshot.png)
