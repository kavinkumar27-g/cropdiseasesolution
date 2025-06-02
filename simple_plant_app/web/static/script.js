// Simple Plant Disease Solution - JavaScript

document.addEventListener('DOMContentLoaded', function() {
    console.log('🌱 Simple Plant Disease Solution loaded');
    
    // Auto-hide flash messages after 5 seconds
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            alert.style.opacity = '0';
            setTimeout(() => {
                alert.remove();
            }, 300);
        }, 5000);
    });
    
    // Search input focus enhancement
    const searchInput = document.querySelector('.search-input');
    if (searchInput) {
        searchInput.addEventListener('focus', function() {
            this.parentElement.style.transform = 'scale(1.02)';
        });
        
        searchInput.addEventListener('blur', function() {
            this.parentElement.style.transform = 'scale(1)';
        });
    }
    
    // Smooth scrolling for internal links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth'
                });
            }
        });
    });
    
    // Add loading state to forms
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function() {
            const submitBtn = this.querySelector('button[type="submit"]');
            if (submitBtn) {
                submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Processing...';
                submitBtn.disabled = true;
            }
        });
    });
});

// Dynamic solution addition for add disease form
let solutionCount = 0;

function addSolution() {
    const container = document.getElementById('solutions-container');
    if (!container) return;
    
    const solutionHtml = `
        <div class="solution-item" id="solution-${solutionCount}">
            <div class="solution-header">
                <h4>Solution ${solutionCount + 1}</h4>
                <button type="button" class="btn btn-danger btn-sm" onclick="removeSolution(${solutionCount})">
                    <i class="fas fa-trash"></i>
                </button>
            </div>
            
            <div class="form-row">
                <div class="form-group">
                    <label>Type</label>
                    <select name="solution_type" required>
                        <option value="">Select type...</option>
                        <option value="organic">🌱 Organic</option>
                        <option value="inorganic">🧪 Inorganic</option>
                    </select>
                </div>
                
                <div class="form-group">
                    <label>Effectiveness</label>
                    <select name="effectiveness">
                        <option value="Medium">Medium</option>
                        <option value="Low">Low</option>
                        <option value="High">High</option>
                        <option value="Very High">Very High</option>
                    </select>
                </div>
            </div>
            
            <div class="form-group">
                <label>Solution Description</label>
                <textarea name="solution_text" rows="2" required
                          placeholder="Describe the treatment method..."></textarea>
            </div>
            
            <div class="form-group">
                <label>Application Method</label>
                <input type="text" name="application" 
                       placeholder="How to apply this treatment...">
            </div>
        </div>
    `;
    
    container.insertAdjacentHTML('beforeend', solutionHtml);
    solutionCount++;
}

function removeSolution(index) {
    const solution = document.getElementById(`solution-${index}`);
    if (solution) {
        solution.remove();
    }
}

// Initialize with one solution if on add disease page
if (document.getElementById('solutions-container')) {
    addSolution();
}
