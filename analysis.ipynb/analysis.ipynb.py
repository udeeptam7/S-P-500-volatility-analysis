import sys
import subprocess
import importlib
from pathlib import Path

# --- Ensure required packages are installed ---
def ensure_package(package_name):
    try:
        importlib.import_module(package_name)
    except ModuleNotFoundError:
        print(f"{package_name} not found. Installing...")
        subprocess.run([sys.executable, "-m", "pip", "install", package_name], check=True)
        importlib.invalidate_caches()
    finally:
        return importlib.import_module(package_name)

# Core packages
pd = ensure_package('pandas')
np = ensure_package('numpy')
yf = ensure_package('yfinance')
plt = None
plotting_enabled = True
try:
    plt = ensure_package('matplotlib.pyplot')
except Exception:
    plotting_enabled = False
    print("Warning: matplotlib is not available. Plots will be skipped.")

# --- Download S&P 500 data ---
try:
    print("Downloading S&P 500 historical data...")
    df = yf.download("^GSPC", start="2010-01-01", end="2025-12-31", interval="1d", progress=False)
    df = df.reset_index()[['Date', 'Close']]
except Exception as e:
    print("Error downloading data:", e)
    sys.exit(1)

# --- Save data ---
Path("data").mkdir(parents=True, exist_ok=True)
df.to_csv("data/index_prices.csv", index=False)
print("Data saved to 'data/index_prices.csv'")

# --- Compute log returns and rolling volatility ---
df['log_return'] = np.log(df['Close'] / df['Close'].shift(1))
df.dropna(inplace=True)
df['rolling_volatility'] = df['log_return'].rolling(window=30).std() * np.sqrt(252)

# --- Classify volatility regime ---
median_vol = df['rolling_volatility'].median()
df['volatility_regime'] = np.where(df['rolling_volatility'] <= median_vol, 'Low Volatility', 'High Volatility')

# --- Statistics per regime ---
stats = df.groupby('volatility_regime')['log_return'].agg(
    mean_return='mean',
    volatility='std'
)
stats['annualized_return'] = stats['mean_return'] * 252
stats['annualized_volatility'] = stats['volatility'] * np.sqrt(252)

# --- Maximum drawdown ---
def max_drawdown(returns):
    cumulative = (1 + returns).cumprod()
    peak = cumulative.cummax()
    drawdown = (cumulative - peak) / peak
    return drawdown.min()

mdd = df.groupby('volatility_regime')['log_return'].apply(max_drawdown)

print("\nAnnualized statistics by volatility regime:")
print(stats)
print("\nMaximum drawdown by regime:")
print(mdd)

# --- Plotting ---
if plotting_enabled:
    # Figure 1: S&P 500 Price
    fig1 = plt.figure(figsize=(12,5))
    plt.plot(df['Date'], df['Close'], color='blue')
    plt.title("S&P 500 Index Price Over Time")
    plt.xlabel("Date")
    plt.ylabel("Close Price")

    # Figure 2: Rolling 30-day Volatility
    fig2 = plt.figure(figsize=(12,5))
    plt.plot(df['Date'], df['rolling_volatility'], color='orange')
    plt.title("Rolling 30-Day Volatility (Annualized)")
    plt.xlabel("Date")
    plt.ylabel("Volatility")

    # Figure 3: Return Distribution by Volatility Regime
    fig3 = plt.figure(figsize=(8,5))
    df[df['volatility_regime']=="Low Volatility"]['log_return'].hist(alpha=0.6, bins=50, label='Low Volatility', color='green')
    df[df['volatility_regime']=="High Volatility"]['log_return'].hist(alpha=0.6, bins=50, label='High Volatility', color='red')
    plt.title("Return Distribution by Volatility Regime")
    plt.xlabel("Log Return")
    plt.ylabel("Frequency")
    plt.legend()

    # Display all figures at once
    plt.show()
else:
    print("Plotting skipped because matplotlib is not installed.")
