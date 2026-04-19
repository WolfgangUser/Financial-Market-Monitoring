// Market Monitor - Main JavaScript

document.addEventListener('DOMContentLoaded', function() {
    console.log('Market Monitor initialized');
    
    // Add active class to current nav link
    const currentPath = window.location.pathname;
    document.querySelectorAll('.nav-link').forEach(link => {
        if (link.getAttribute('href') === currentPath) {
            link.classList.add('active');
        }
    });
    
    // Initialize any dynamic components
    initPriceUpdates();
    initTableSorting();
});

// Price update functionality
function initPriceUpdates() {
    const priceElements = document.querySelectorAll('[data-price-symbol]');
    if (priceElements.length > 0) {
        updatePrices(priceElements);
        // Update every 30 seconds
        setInterval(() => updatePrices(priceElements), 30000);
    }
}

function updatePrices(elements) {
    elements.forEach(el => {
        const symbol = el.getAttribute('data-price-symbol');
        fetch(`/api/asset/${symbol}/price/`)
            .then(response => response.json())
            .then(data => {
                el.textContent = '$' + data.price.toFixed(2);
                if (data.change_percent >= 0) {
                    el.classList.add('positive');
                    el.classList.remove('negative');
                } else {
                    el.classList.add('negative');
                    el.classList.remove('positive');
                }
            })
            .catch(err => console.error('Error updating price:', err));
    });
}

// Table sorting functionality
function initTableSorting() {
    const tables = document.querySelectorAll('.data-table[data-sortable="true"]');
    tables.forEach(table => {
        const headers = table.querySelectorAll('th[data-sort-key]');
        headers.forEach(header => {
            header.style.cursor = 'pointer';
            header.addEventListener('click', () => sortTable(table, header.dataset.sortKey));
        });
    });
}

function sortTable(table, key) {
    const tbody = table.querySelector('tbody');
    const rows = Array.from(tbody.querySelectorAll('tr'));
    
    rows.sort((a, b) => {
        const aVal = a.querySelector(`[data-key="${key}"]`)?.textContent || '';
        const bVal = b.querySelector(`[data-key="${key}"]`)?.textContent || '';
        return aVal.localeCompare(bVal, undefined, { numeric: true });
    });
    
    rows.forEach(row => tbody.appendChild(row));
}

// Format numbers as currency
function formatCurrency(value) {
    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD'
    }).format(value);
}

// Format numbers with commas
function formatNumber(value) {
    return new Intl.NumberFormat('en-US').format(value);
}

// Utility: Debounce function
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Export functions for global use
window.MarketMonitor = {
    formatCurrency,
    formatNumber,
    debounce
};
