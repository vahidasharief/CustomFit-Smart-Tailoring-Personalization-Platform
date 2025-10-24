// Form validation and error handling
document.addEventListener('DOMContentLoaded', function() {
    console.log('DOM Content Loaded - Initializing form handlers');
    
    // Handle form submissions with loading state
    const forms = document.querySelectorAll('form');
    console.log(`Found ${forms.length} forms on the page`);
    
    forms.forEach((form, index) => {
        console.log(`Setting up form handler for form ${index + 1}`);
        
        form.addEventListener('submit', function(event) {
            console.log(`Form ${index + 1} submission triggered`);
            
            const submitButton = form.querySelector('button[type="submit"]');
            if (submitButton) {
                console.log('Submit button found, updating state');
                const originalText = submitButton.innerHTML;
                submitButton.disabled = true;
                submitButton.innerHTML = `
                    <svg class="animate-spin -ml-1 mr-3 h-5 w-5 inline-block" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                        <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                        <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                    </svg>
                    Processing...
                `;
            }
        });
    });

    // Initialize error handling
    const bookingForm = document.querySelector('form');
    const errorDiv = document.getElementById('form-errors') || document.createElement('div');
    
    if (!errorDiv.id) {
        errorDiv.id = 'form-errors';
        errorDiv.className = 'hidden p-4 mb-4 text-red-700 bg-red-100 rounded-lg';
        if (bookingForm) {
            bookingForm.insertBefore(errorDiv, bookingForm.firstChild);
        }
    }

    function showError(message) {
        errorDiv.textContent = message;
        errorDiv.classList.remove('hidden');
        setTimeout(() => {
            errorDiv.classList.add('hidden');
        }, 5000);
    }

    if (bookingForm) {
        bookingForm.addEventListener('submit', async function(e) {
            e.preventDefault();
            errorDiv.classList.add('hidden');

            const dateInput = document.getElementById('appointment_date');
            const timeInput = document.getElementById('appointment_time');
            
            // Basic date validation
            const selectedDate = new Date(dateInput.value);
            const today = new Date();
            today.setHours(0, 0, 0, 0);
            
            if (selectedDate < today) {
                showError('Please select a future date');
                return;
            }
            
            // Measurement validation
            const measurements = ['chest', 'waist', 'hips', 'length'];
            for (const measurement of measurements) {
                const value = parseFloat(document.getElementById(measurement).value);
                if (value <= 0 || value > 100) {
                    showError(`Please enter a valid ${measurement} measurement (between 0 and 100 inches)`);
                    return;
                }
            }

            // Submit form
            try {
                const formData = new FormData(bookingForm);
                const response = await fetch('/api/book', {
                    method: 'POST',
                    body: formData
                });
                
                const result = await response.json();
                
                if (!response.ok) {
                    showError(result.errors ? result.errors.join(', ') : 'Booking failed. Please try again.');
                    return;
                }
                
                window.location.href = '/?success=1';
            } catch (error) {
                showError('An error occurred. Please try again.');
            }
        });

        // Dynamic time slot validation
        const timeInput = document.getElementById('appointment_time');
        if (timeInput) {
            timeInput.addEventListener('change', function() {
                const time = this.value;
                const [hours] = time.split(':');
                
                // Assume business hours are 9 AM to 6 PM
                if (hours < 9 || hours >= 18) {
                    showError('Please select a time between 9 AM and 6 PM');
                    this.value = '';
                }
            });
        }
    }
});