# 💰 Money Tracker

A simple, elegant web application for tracking your income and expenses. Built with vanilla JavaScript, HTML, and CSS.

## Features

- **Track Income & Expenses**: Easily add and categorize your financial transactions
- **Real-time Summary**: View your total income, expenses, and current balance at a glance
- **Transaction History**: See all your transactions in a clean, organized list
- **Categories**: Organize transactions with predefined categories (Salary, Food, Transport, etc.)
- **Filtering**: Filter transactions by type (All, Income, Expenses)
- **Data Persistence**: All data is saved locally in your browser using localStorage
- **Export to CSV**: Download your transaction history as a CSV file
- **Responsive Design**: Works perfectly on desktop, tablet, and mobile devices
- **Modern UI**: Clean, gradient-based interface with smooth animations

## How to Use

### Getting Started

1. Open `index.html` in your web browser
2. The app will load with empty transaction history

### Adding a Transaction

1. Fill in the transaction form:
   - **Description**: What the transaction is for (e.g., "Monthly Salary", "Grocery Shopping")
   - **Amount**: The monetary value (positive numbers only)
   - **Type**: Select either "Income" or "Expense"
   - **Category**: Choose from available categories
   - **Date**: Select the transaction date (defaults to today)

2. Click "Add Transaction" button

3. The transaction will appear in your history and the summary cards will update automatically

### Managing Transactions

- **View Transactions**: All transactions are displayed in the history section, sorted by date (newest first)
- **Delete Transaction**: Click the "×" button on any transaction to remove it
- **Filter Transactions**: Use the dropdown to show all transactions, only income, or only expenses
- **Export Data**: Click "Export CSV" to download your transactions as a spreadsheet
- **Clear All**: Click "Clear All" to delete all transactions (this action requires confirmation)

### Understanding the Summary Cards

- **Total Income**: Sum of all income transactions (green)
- **Total Expenses**: Sum of all expense transactions (red)
- **Balance**: Income minus expenses (green if positive, red if negative)

## Categories

### Income Categories
- Salary
- Freelance
- Investment

### Expense Categories
- Food
- Transport
- Utilities
- Entertainment
- Shopping
- Healthcare
- Other

## Data Storage

All transaction data is stored locally in your browser using localStorage. This means:
- ✅ Your data persists between sessions
- ✅ No server or internet connection required
- ✅ Your financial data stays private on your device
- ⚠️ Clearing browser data will delete your transactions
- ⚠️ Data is specific to the browser and device you're using

## Browser Compatibility

This app works on all modern browsers:
- Chrome/Edge (version 90+)
- Firefox (version 88+)
- Safari (version 14+)
- Opera (version 76+)

## Files

- `index.html` - Main HTML structure
- `styles.css` - Styling and responsive design
- `app.js` - Application logic and functionality

## Technologies Used

- HTML5
- CSS3 (with CSS Grid and Flexbox)
- Vanilla JavaScript (ES6+)
- LocalStorage API

## Privacy

This application runs entirely in your browser. No data is sent to any server or third party. All information is stored locally on your device.

## Tips

1. **Regular Updates**: Add transactions regularly to maintain accurate records
2. **Use Categories**: Proper categorization helps you understand spending patterns
3. **Export Regularly**: Download CSV backups of your data periodically
4. **Accurate Dates**: Use the correct date for each transaction for better tracking
5. **Detailed Descriptions**: Write clear descriptions to remember what each transaction was for

## Future Enhancements

Potential features for future versions:
- Monthly/yearly reports and analytics
- Charts and visualizations
- Budget setting and tracking
- Recurring transactions
- Import from CSV
- Multiple accounts
- Dark mode toggle

## License

This project is open source and available for personal and commercial use.

## Support

For issues or questions, please refer to the project repository.

---

**Happy Tracking! 📊**
