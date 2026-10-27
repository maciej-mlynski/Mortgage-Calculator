# Mortgage-Calculator

 Project available [here](https://kalkulator-financialmill.herokuapp.com/)
 
 I created it in the Python environment, using Stremlit framework. 
 However, I am not happy with this choice because despite its ease of use and clear documentation, streamlite is not the best tool for writing applications such as a calculator. 
 It's a fairly new framework and we have limited control over many things, especially when it comes to capturing user input.  
 
 I created the calculation algorithm for the calculator itself in 3 days. The longest part was designing the tabs, implementing the project and writing the data which took several months.  

For each stage through which the calculator leads I prepared an entry explaining particular issues related to mortgage credit. 

To sum up, the calculator is not an ordinary tool to analyze credit costs. It is more of an interactive presentation that allows the user to understand and consciously choose how to optimize the cost of their mortgage. 

Kod aktywacyjny do kalkulatora: FinancialMill2022

 
 

## Configuration

Database credentials are read from environment variables. Copy `.env.example` to `.env` and fill in the values (on Heroku, set them as Config Vars).
