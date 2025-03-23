import tkinter as tk
from tkinter import messagebox
import requests

# Define the API Key (use your provided API key here)
FOREX_API_KEY = 'b0cb64a792fccf134ce4c005e02af3b2'  # Your Forex API key

# Function to get the latest currency exchange rate for a country
def get_forex_rate(currency_code):
    url = f"https://api.exchangerate-api.com/v4/latest/{currency_code}"  # Correct endpoint for latest rates
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if 'rates' in data:
                return data['rates']  # Get the exchange rates
            else:
                print(f"Error fetching data: {data.get('error', 'Unknown error')}")
                return None
        else:
            print(f"Error: HTTP {response.status_code}")
            return None
    except Exception as e:
        print(f"Error: {e}")
        return None

# Function to fetch news related to currency (optional)
def get_currency_news(currency_code):
    url = f"https://newsapi.org/v2/everything?q={currency_code} currency&apiKey=033d3481bbc04385b06c80328696fe11"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if data['status'] == 'ok':
                return data['articles']
            else:
                print("Error fetching news")
                return None
        else:
            print(f"Error: HTTP {response.status_code}")
            return None
    except Exception as e:
        print(f"Error: {e}")
        return None

# Function to display Forex rate and Currency News
def display_forex_and_news(currency_code):
    forex_rates = get_forex_rate(currency_code)
    if forex_rates:
        # Get the exchange rate for USD (or any other currency you specify)
        if 'USD' in forex_rates:
            result_text = f"Exchange Rate for {currency_code.upper()}:\nUSD: {forex_rates['USD']}\n"
            result_label.config(text=result_text)
        else:
            messagebox.showerror("Error", f"Currency code '{currency_code}' not found.")
    else:
        messagebox.showerror("Error", "Failed to fetch Forex rates")

    # Optionally, display currency news
    news = get_currency_news(currency_code)
    if news:
        news_text = f"\nLatest News for {currency_code.upper()} currency:\n"
        for article in news[:3]:  # Limit to top 3 news articles
            title = article['title']
            description = article['description']
            news_text += f"\n{title}\n{description}\n"
        
        # Update the text widget with news content
        news_text_widget.delete(1.0, tk.END)  # Clear existing text
        news_text_widget.insert(tk.END, news_text)  # Insert new news text
    else:
        news_text_widget.delete(1.0, tk.END)  # Clear existing text
        news_text_widget.insert(tk.END, "No news available")

# Function to handle button click event
def on_button_click():
    currency_code = currency_entry.get().strip().upper()
    if not currency_code:
        messagebox.showwarning("Input Error", "Please enter a currency code")
    else:
        display_forex_and_news(currency_code)

# Create the main window using Tkinter
root = tk.Tk()
root.title("Currency Exchange Rates & News")

# Create and place widgets (entry, button, labels)
currency_label = tk.Label(root, text="Enter Currency Code (e.g., USD, EUR):")
currency_label.pack(pady=10)

currency_entry = tk.Entry(root, width=20)
currency_entry.pack(pady=10)

search_button = tk.Button(root, text="Get Forex Data", command=on_button_click)
search_button.pack(pady=10)

result_label = tk.Label(root, text="", justify=tk.LEFT)
result_label.pack(pady=10)

# Create a frame to hold the Text widget and Scrollbar for the news box
news_frame = tk.Frame(root)
news_frame.pack(pady=10)

# Create a Text widget to display the news (with scrollbar)
news_text_widget = tk.Text(news_frame, width=50, height=10, wrap=tk.WORD, bd=2, relief=tk.GROOVE)
news_text_widget.pack(side=tk.LEFT)

# Create a Scrollbar for the Text widget
news_scrollbar = tk.Scrollbar(news_frame, command=news_text_widget.yview)
news_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# Link the scrollbar to the Text widget
news_text_widget.config(yscrollcommand=news_scrollbar.set)

# Run the Tkinter event loop
root.mainloop()
