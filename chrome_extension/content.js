// Content script that runs on job application pages

// Listen for messages from the popup
chrome.runtime.onMessage.addListener(function(request, sender, sendResponse) {
    if (request.action === 'fillForm') {
        fillJobApplication();
        sendResponse({ success: true });
    }
    return true;
});

async function fillJobApplication() {
    // Get user data from Chrome storage
    const result = await chrome.storage.sync.get(['userData']);
    const userData = result.userData || {
        name: 'Abraham Kuriakose',
        email: 'abrahamkuriakosevit@gmail.com',
        phone: '+61494395881',
        location: 'Ashfield, NSW, Australia',
        linkedin: 'abraham13202',
        github: 'abraham13202'
    };

    let filledFields = [];

    // Common field patterns for job applications
    const fieldPatterns = {
        // Name fields
        name: ['name', 'full_name', 'fullname', 'applicant_name', 'firstname', 'first_name',
               'candidate_name', 'your_name', 'full-name'],
        firstName: ['firstname', 'first_name', 'first-name', 'fname', 'given_name'],
        lastName: ['lastname', 'last_name', 'last-name', 'lname', 'family_name', 'surname'],

        // Contact fields
        email: ['email', 'email_address', 'e-mail', 'emailaddress', 'mail', 'contact_email'],
        phone: ['phone', 'telephone', 'mobile', 'phone_number', 'phonenumber', 'contact_number',
                'tel', 'cell', 'contact_phone'],

        // Location fields
        location: ['location', 'address', 'city', 'current_location', 'residence', 'current_city'],
        country: ['country'],
        state: ['state', 'province', 'region'],

        // Professional fields
        linkedin: ['linkedin', 'linkedin_url', 'linkedin_profile', 'linkedin-url'],
        github: ['github', 'github_url', 'github_profile', 'github-url', 'portfolio'],
        website: ['website', 'portfolio', 'personal_website', 'url'],

        // Work authorization
        workAuth: ['work_authorization', 'visa', 'visa_status', 'work_permit', 'authorized_to_work',
                   'legal_to_work', 'work_eligibility']
    };

    // Function to check if field name matches pattern
    function matchesPattern(fieldName, patterns) {
        const lowerFieldName = fieldName.toLowerCase();
        return patterns.some(pattern => lowerFieldName.includes(pattern));
    }

    // Function to fill a field safely
    function fillField(element, value) {
        if (!element || element.value) return false; // Don't overwrite existing values

        element.value = value;
        element.dispatchEvent(new Event('input', { bubbles: true }));
        element.dispatchEvent(new Event('change', { bubbles: true }));
        element.dispatchEvent(new Event('blur', { bubbles: true }));

        return true;
    }

    // Find and fill input fields
    const inputs = document.querySelectorAll('input[type="text"], input[type="email"], input[type="tel"], input:not([type])');

    inputs.forEach(input => {
        const fieldName = (input.name || input.id || input.placeholder || '').toLowerCase();
        const ariaLabel = (input.getAttribute('aria-label') || '').toLowerCase();
        const label = findLabel(input);
        const combinedName = `${fieldName} ${ariaLabel} ${label}`.toLowerCase();

        let filled = false;

        // Try to match and fill based on field patterns
        if (matchesPattern(combinedName, fieldPatterns.name)) {
            filled = fillField(input, userData.name);
            if (filled) filledFields.push('Name');
        } else if (matchesPattern(combinedName, fieldPatterns.firstName)) {
            filled = fillField(input, 'Abraham');
            if (filled) filledFields.push('First Name');
        } else if (matchesPattern(combinedName, fieldPatterns.lastName)) {
            filled = fillField(input, 'Kuriakose');
            if (filled) filledFields.push('Last Name');
        } else if (matchesPattern(combinedName, fieldPatterns.email) || input.type === 'email') {
            filled = fillField(input, userData.email);
            if (filled) filledFields.push('Email');
        } else if (matchesPattern(combinedName, fieldPatterns.phone) || input.type === 'tel') {
            filled = fillField(input, userData.phone);
            if (filled) filledFields.push('Phone');
        } else if (matchesPattern(combinedName, fieldPatterns.location)) {
            filled = fillField(input, userData.location);
            if (filled) filledFields.push('Location');
        } else if (matchesPattern(combinedName, fieldPatterns.linkedin)) {
            filled = fillField(input, `https://linkedin.com/in/${userData.linkedin}`);
            if (filled) filledFields.push('LinkedIn');
        } else if (matchesPattern(combinedName, fieldPatterns.github)) {
            filled = fillField(input, `https://github.com/${userData.github}`);
            if (filled) filledFields.push('GitHub');
        } else if (matchesPattern(combinedName, fieldPatterns.workAuth)) {
            filled = fillField(input, userData.visaStatus || 'Visa Subclass 500');
            if (filled) filledFields.push('Visa Status');
        }

        if (filled) {
            input.style.backgroundColor = '#e8f5e9';
            setTimeout(() => {
                input.style.backgroundColor = '';
            }, 2000);
        }
    });

    // Handle file uploads for resume
    const fileInputs = document.querySelectorAll('input[type="file"]');
    fileInputs.forEach(input => {
        const fieldName = (input.name || input.id || '').toLowerCase();
        if (fieldName.includes('resume') || fieldName.includes('cv')) {
            // Highlight the upload button
            input.style.border = '2px solid #4caf50';
            filledFields.push('Resume Upload (highlighted)');

            setTimeout(() => {
                input.style.border = '';
            }, 3000);
        }
    });

    // Show notification
    if (filledFields.length > 0) {
        showNotification(`✅ Filled ${filledFields.length} fields!`);
    } else {
        showNotification('⚠️ No matching fields found on this page');
    }

    return { success: true, filledFields: filledFields, fieldsFilledCount: filledFields.length };
}

// Helper function to find associated label
function findLabel(input) {
    // Try to find label by 'for' attribute
    if (input.id) {
        const label = document.querySelector(`label[for="${input.id}"]`);
        if (label) return label.textContent;
    }

    // Try to find parent label
    const parentLabel = input.closest('label');
    if (parentLabel) return parentLabel.textContent;

    // Try to find preceding label
    let prevElement = input.previousElementSibling;
    while (prevElement) {
        if (prevElement.tagName === 'LABEL') {
            return prevElement.textContent;
        }
        prevElement = prevElement.previousElementSibling;
    }

    return '';
}

// Show temporary notification
function showNotification(message) {
    const notification = document.createElement('div');
    notification.textContent = message;
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: #667eea;
        color: white;
        padding: 15px 20px;
        border-radius: 5px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.3);
        z-index: 999999;
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        font-size: 14px;
        font-weight: 600;
        animation: slideIn 0.3s ease-out;
    `;

    document.body.appendChild(notification);

    setTimeout(() => {
        notification.style.animation = 'slideOut 0.3s ease-out';
        setTimeout(() => notification.remove(), 300);
    }, 3000);
}

// Add CSS for animations
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from {
            transform: translateX(400px);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    @keyframes slideOut {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(400px);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);

console.log('🚀 Job Auto-Filler extension loaded!');
