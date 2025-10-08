// Background service worker

// Initialize default user data on install
chrome.runtime.onInstalled.addListener(function() {
    const defaultUserData = {
        name: 'Abraham Kuriakose',
        email: 'abrahamkuriakosevit@gmail.com',
        phone: '+61494395881',
        location: 'Ashfield, NSW, Australia',
        linkedin: 'abraham13202',
        github: 'abraham13202',
        visaStatus: 'Visa Subclass 500'
    };

    chrome.storage.sync.set({ userData: defaultUserData }, function() {
        console.log('Job Auto-Filler initialized with default data');
    });
});

// Listen for messages from content scripts
chrome.runtime.onMessage.addListener(function(request, sender, sendResponse) {
    if (request.action === 'getUserData') {
        chrome.storage.sync.get(['userData'], function(result) {
            sendResponse({ userData: result.userData });
        });
        return true; // Keep the message channel open for async response
    }
});
