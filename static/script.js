document.addEventListener("DOMContentLoaded", function() {
    // Handle contact form submission
    const contactForm = document.getElementById("contactForm");
    if (contactForm) {
        contactForm.addEventListener("submit", async function(event) {
            event.preventDefault();
            
            const formData = new FormData(contactForm);
            const response = await fetch("/contact", {
                method: "POST",
                body: formData
            });

            if (response.ok) {
                alert("Message sent successfully!");
                contactForm.reset();
            } else {
                alert("Failed to send message. Please try again.");
            }
        });
    }

    // Handle resume upload form submission
    const resumeForm = document.getElementById("resumeUploadForm");
    if (resumeForm) {
        resumeForm.addEventListener("submit", async function(event) {
            event.preventDefault();
            
            const formData = new FormData(resumeForm);
            const response = await fetch("/resume_review", {
                method: "POST",
                body: formData
            });

            if (response.ok) {
                const result = await response.json();
                const matchesList = document.getElementById('matchesList');
                const resultsSection = document.getElementById('resultsSection');
                
                // Clear previous results
                matchesList.innerHTML = '';
                
                // Add each match to the list
                result.matches.forEach(match => {
                    const matchItem = document.createElement('div');
                    matchItem.className = 'match-item';
                    matchItem.innerHTML = `
                        ${match[0]}
                        <span class="match-score">Score: ${match[1].toFixed(2)}</span>
                    `;
                    matchesList.appendChild(matchItem);
                });
                
                // Show results section
                resultsSection.style.display = 'block';
                resumeForm.reset();
            } else {
                const error = await response.json();
                alert(`Error: ${error.error || 'Failed to process resume'}`);
            }
        });
    }
});
