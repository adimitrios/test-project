class MoneyTracker {
    constructor() {
        this.transactions = this.loadTransactions();
        this.init();
    }

    init() {
        this.setDefaultDate();
        this.attachEventListeners();
        this.renderTransactions();
        this.updateSummary();
    }

    setDefaultDate() {
        const dateInput = document.getElementById('date');
        const today = new Date().toISOString().split('T')[0];
        dateInput.value = today;
    }

    attachEventListeners() {
        document.getElementById('transactionForm').addEventListener('submit', (e) => {
            e.preventDefault();
            this.addTransaction();
        });

        document.getElementById('filterType').addEventListener('change', () => {
            this.renderTransactions();
        });

        document.getElementById('exportBtn').addEventListener('click', () => {
            this.exportToCSV();
        });

        document.getElementById('clearBtn').addEventListener('click', () => {
            this.clearAllTransactions();
        });
    }

    addTransaction() {
        const description = document.getElementById('description').value.trim();
        const amount = parseFloat(document.getElementById('amount').value);
        const type = document.getElementById('type').value;
        const category = document.getElementById('category').value;
        const date = document.getElementById('date').value;

        if (!description || !amount || !date) {
            alert('Please fill in all fields');
            return;
        }

        const transaction = {
            id: Date.now(),
            description,
            amount,
            type,
            category,
            date,
            timestamp: new Date().toISOString()
        };

        this.transactions.push(transaction);
        this.saveTransactions();
        this.renderTransactions();
        this.updateSummary();
        this.resetForm();
    }

    deleteTransaction(id) {
        if (confirm('Are you sure you want to delete this transaction?')) {
            this.transactions = this.transactions.filter(t => t.id !== id);
            this.saveTransactions();
            this.renderTransactions();
            this.updateSummary();
        }
    }

    renderTransactions() {
        const filterType = document.getElementById('filterType').value;
        const transactionsList = document.getElementById('transactionsList');

        let filteredTransactions = this.transactions;

        if (filterType !== 'all') {
            filteredTransactions = this.transactions.filter(t => t.type === filterType);
        }

        filteredTransactions.sort((a, b) => new Date(b.date) - new Date(a.date));

        if (filteredTransactions.length === 0) {
            transactionsList.innerHTML = '<p class="empty-state">No transactions found.</p>';
            return;
        }

        transactionsList.innerHTML = filteredTransactions.map(transaction => `
            <div class="transaction-item ${transaction.type}">
                <div class="transaction-info">
                    <div class="transaction-description">${this.escapeHtml(transaction.description)}</div>
                    <div class="transaction-details">
                        <span class="category-badge">${transaction.category}</span>
                        <span>${this.formatDate(transaction.date)}</span>
                    </div>
                </div>
                <div style="display: flex; align-items: center;">
                    <span class="transaction-amount ${transaction.type}">
                        ${transaction.type === 'income' ? '+' : '-'}$${transaction.amount.toFixed(2)}
                    </span>
                    <button class="delete-btn" onclick="tracker.deleteTransaction(${transaction.id})" title="Delete transaction">
                        &times;
                    </button>
                </div>
            </div>
        `).join('');
    }

    updateSummary() {
        const totalIncome = this.transactions
            .filter(t => t.type === 'income')
            .reduce((sum, t) => sum + t.amount, 0);

        const totalExpenses = this.transactions
            .filter(t => t.type === 'expense')
            .reduce((sum, t) => sum + t.amount, 0);

        const balance = totalIncome - totalExpenses;

        document.getElementById('totalIncome').textContent = `$${totalIncome.toFixed(2)}`;
        document.getElementById('totalExpenses').textContent = `$${totalExpenses.toFixed(2)}`;
        document.getElementById('balance').textContent = `$${balance.toFixed(2)}`;

        const balanceElement = document.getElementById('balance');
        if (balance >= 0) {
            balanceElement.style.color = 'var(--income-color)';
        } else {
            balanceElement.style.color = 'var(--expense-color)';
        }
    }

    resetForm() {
        document.getElementById('transactionForm').reset();
        this.setDefaultDate();
    }

    saveTransactions() {
        localStorage.setItem('moneyTrackerTransactions', JSON.stringify(this.transactions));
    }

    loadTransactions() {
        const saved = localStorage.getItem('moneyTrackerTransactions');
        return saved ? JSON.parse(saved) : [];
    }

    clearAllTransactions() {
        if (confirm('Are you sure you want to delete ALL transactions? This cannot be undone!')) {
            this.transactions = [];
            this.saveTransactions();
            this.renderTransactions();
            this.updateSummary();
        }
    }

    exportToCSV() {
        if (this.transactions.length === 0) {
            alert('No transactions to export');
            return;
        }

        const headers = ['Date', 'Description', 'Category', 'Type', 'Amount'];
        const rows = this.transactions.map(t => [
            t.date,
            `"${t.description}"`,
            t.category,
            t.type,
            t.amount.toFixed(2)
        ]);

        const csvContent = [
            headers.join(','),
            ...rows.map(row => row.join(','))
        ].join('\n');

        const blob = new Blob([csvContent], { type: 'text/csv' });
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `money-tracker-${new Date().toISOString().split('T')[0]}.csv`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        window.URL.revokeObjectURL(url);
    }

    formatDate(dateString) {
        const date = new Date(dateString + 'T00:00:00');
        return date.toLocaleDateString('en-US', {
            year: 'numeric',
            month: 'short',
            day: 'numeric'
        });
    }

    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
}

const tracker = new MoneyTracker();
