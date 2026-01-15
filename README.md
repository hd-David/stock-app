# Stock Trading Application

A full-featured stock trading web application built with Flask that allows users to manage their stock portfolios, buy and sell stocks, and track market trends in real-time.

## Features

- **User Authentication**: Secure user registration and login system with password hashing
- **Portfolio Management**: View and manage your stock portfolio with real-time valuations
- **Stock Trading**: Buy and sell stocks with real-time price quotes
- **Market Data**: View trending stocks on the landing page with price change indicators
- **Stock Quotes**: Get real-time stock quotes and calculate order prices
- **Transaction History**: Track your trading history (in development)
- **Responsive UI**: Built with Bootstrap for a modern, responsive interface

## Technologies Used

- **Backend**: Flask (Python web framework)
- **Database**: MySQL/MariaDB with SQLAlchemy ORM
- **Authentication**: Flask-Login for session management
- **Forms**: Flask-WTF for form handling and validation
- **UI Framework**: Flask-Bootstrap for responsive design
- **API**: Alpha Vantage API for real-time stock data
- **Security**: Werkzeug for password hashing

## Prerequisites

Before running this application, ensure you have:

- Python 3.7 or higher
- MySQL or MariaDB database server
- Alpha Vantage API key (free at [alphavantage.co](https://www.alphavantage.co/))

## Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/hd-David/stock-app.git
   cd stock-app
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```
   
   **Note**: You may need to install `mysql-connector-python` separately if not included:
   ```bash
   pip install mysql-connector-python
   ```

4. **Set up the database**
   
   Create a MySQL/MariaDB database:
   ```sql
   CREATE DATABASE finance_app;
   ```
   
   Update the database connection string in `model.py` with your credentials:
   ```python
   DATABASE_URL = 'mysql+mysqlconnector://username:password@localhost/finance_app'
   ```
   
   **Security Note**: For production, use environment variables for database credentials instead of hardcoding them:
   ```python
   import os
   DATABASE_URL = os.environ.get('DATABASE_URL', 'mysql+mysqlconnector://root:@localhost/finance_app')
   ```

5. **Initialize the database tables**
   ```bash
   python init_db.py
   ```

6. **Set environment variables**
   
   Set your Alpha Vantage API key:
   ```bash
   export API_KEY="your_alpha_vantage_api_key"  # On Windows: set API_KEY=your_api_key
   ```

## Running the Application

1. **Start the Flask development server**
   ```bash
   python app.py
   ```

2. **Access the application**
   
   Open your web browser and navigate to:
   ```
   http://localhost:5000
   ```

## Project Structure

```
stock-app/
├── app.py                 # Main application file with routes
├── model.py              # Database models (User, Portfolio, Address)
├── forms.py              # WTForms for registration, login, and quotes
├── helpers.py            # Helper functions (lookup, usd formatting, etc.)
├── create.py             # User and portfolio creation utilities
├── init_db.py            # Database initialization script
├── requirements.txt      # Python dependencies
├── templates/            # HTML templates
│   ├── layout.html       # Base template
│   ├── landing.html      # Landing page with trending stocks
│   ├── page_login.html   # Login page
│   ├── register.html     # Registration page
│   ├── index.html        # User dashboard/portfolio view
│   ├── quote.html        # Stock quote form
│   ├── quoted.html       # Quote results
│   ├── buy.html          # Buy stocks form
│   └── ...
├── static/               # Static files (CSS, JavaScript, images)
│   └── js/              # JavaScript libraries
├── img/                  # Image assets
└── media/               # Media files (sounds, videos, data)
```

## Database Schema

### User Table
- `id`: Primary key
- `full_names`: User's full name
- `username`: Unique username
- `email`: User email address
- `password_hash`: Hashed password
- `cash`: Available cash balance (default: $10,000)
- `create_date`: Account creation timestamp

### Portfolio Table
- `id`: Primary key
- `user_id`: Foreign key to User
- `symbol`: Stock ticker symbol
- `quantity`: Number of shares owned
- `price`: Purchase price per share

### Address Table
- `id`: Primary key
- `user_id`: Foreign key to User

## Key Features Explained

### User Registration
- New users receive $10,000 starting cash
- Password hashing for security
- Email and username validation

### Stock Lookup
- Real-time stock data from Alpha Vantage API
- Quote multiple shares to calculate total order price
- Display company name, symbol, and current price

### Buying Stocks
- Validates sufficient funds before purchase
- Updates user cash balance
- Records transaction in portfolio

### Portfolio Dashboard
- Displays all stock holdings
- Shows current market value
- Calculates total portfolio value (stocks + cash)

### Landing Page
- Displays trending stocks (AAPL, TSLA, NVDA, SOFI)
- Shows price changes and percentage movements
- Updates dynamically

## API Key Setup

This application requires an Alpha Vantage API key for stock data:

1. Sign up for a free API key at [alphavantage.co](https://www.alphavantage.co/support/#api-key)
2. Set the environment variable:
   ```bash
   export API_KEY="your_api_key_here"
   ```
3. The application will raise a RuntimeError if the API key is not set

## Security Features

- Password hashing using Werkzeug
- Session management with Flask-Login
- CSRF protection with Flask-WTF
- Cache control headers to prevent sensitive data caching
- Login required decorators for protected routes

## Development

The application runs in debug mode by default when executed directly:
```python
if __name__ == '__main__':
    app.run(debug=True)
```

**⚠️ Security Warning**: Never run with `debug=True` in production as it can expose sensitive information and security vulnerabilities.

For production deployment:
1. Set `debug=False` in the code or use environment variables:
   ```python
   app.run(debug=os.environ.get('FLASK_DEBUG', 'False') == 'True')
   ```
2. Use a production-ready WSGI server like Gunicorn or uWSGI:
   ```bash
   pip install gunicorn
   gunicorn -w 4 -b 0.0.0.0:5000 app:app
   ```

## Future Enhancements

- Complete transaction history page
- Sell stocks functionality
- Real-time portfolio updates
- Stock price alerts
- Advanced charts and analytics
- Multiple currency support

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the MIT License.

## Acknowledgments

- Alpha Vantage for providing the stock market API
- Flask and its extensions for the web framework
- Bootstrap for the UI components