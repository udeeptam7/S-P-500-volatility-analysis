# analysis.ipynb
# S&P 500 Volatility Analysis

Analyzed 15+ years of S&P 500 historical data to uncover trends in price, volatility, and risk. This project demonstrates **financial data analysis** using Python and visualization of volatility regimes.

---

# Project Overview
- Downloaded historical S&P 500 index data using `yfinance` (2010–2025).  
- Calculated **log returns** for daily price changes.  
- Computed **rolling 30-day volatility** (annualized).  
- Classified periods into **Low Volatility** and **High Volatility** regimes based on median volatility.  
- Calculated **annualized returns**, **annualized volatility**, and **maximum drawdowns** per regime.  
- Visualized:
  1. S&P 500 price over time  
  2. Rolling 30-day volatility  
  3. Return distribution by volatility regime  

---

#  Tools & Libraries
- **Python 3.x**  
- **pandas** – Data manipulation  
- **numpy** – Numerical calculations  
- **yfinance** – Download historical stock data  
- **matplotlib** – Plotting and visualizations  

---


