// Popup script for the extension

// Load user data from Chrome storage
chrome.storage.sync.get(['userData'], function(result) {
    const userData = result.userData || {
        name: 'Abraham Kuriakose',
        email: 'abrahamkuriakosevit@gmail.com',
        phone: '+61494395881',
        location: 'Ashfield, NSW, Australia',
        linkedin: 'abraham13202',
        github: 'abraham13202',
        visaStatus: 'Visa Subclass 500'
    };

    // Display user info
    document.getElementById('userName').textContent = userData.name;
    document.getElementById('userEmail').textContent = userData.email;
    document.getElementById('userPhone').textContent = userData.phone;

    // Store in local storage for easy access
    if (!result.userData) {
        chrome.storage.sync.set({ userData: userData });
    }
});

// Fill button click handler
document.getElementById('fillButton').addEventListener('click', async function() {
    const button = this;
    const status = document.getElementById('status');

    button.disabled = true;
    button.textContent = '⏳ Filling...';
    status.className = 'status filling';
    status.textContent = '⏳ Auto-filling form...';

    try {
        // Get the active tab
        const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });

        // Send message to content script to fill the form
        chrome.tabs.sendMessage(tab.id, { action: 'fillForm' }, function(response) {
            if (chrome.runtime.lastError) {
                status.className = 'status ready';
                status.textContent = '❌ Error: ' + chrome.runtime.lastError.message;
                button.disabled = false;
                button.textContent = '✨ Auto-Fill This Page';
                return;
            }

            if (response && response.success) {
                status.className = 'status ready';
                status.textContent = '✅ Form filled! Fields: ' + response.fieldsFilledcount;

                // Show filled fields
                if (response.filledFields && response.filledFields.length > 0) {
                    const fieldList = document.getElementById('fieldList');
                    const fieldsDetected = document.getElementById('fieldsDetected');

                    fieldsDetected.innerHTML = response.filledFields.map(field =>
                        `<div class="field-item filled">✓ ${field}</div>`
                    ).join('');

                    fieldList.style.display = 'block';
                }

                setTimeout(() => {
                    status.textContent = '✓ Ready to auto-fill';
                    button.disabled = false;
                    button.textContent = '✨ Auto-Fill This Page';
                }, 2000);
            } else {
                status.className = 'status ready';
                status.textContent = '⚠️ No form fields found on this page';
                button.disabled = false;
                button.textContent = '✨ Auto-Fill This Page';
            }
        });
    } catch (error) {
        status.className = 'status ready';
        status.textContent = '❌ Error: ' + error.message;
        button.disabled = false;
        button.textContent = '✨ Auto-Fill This Page';
    }
});

// Settings button
document.getElementById('settingsButton').addEventListener('click', function() {
    chrome.runtime.openOptionsPage();
});
