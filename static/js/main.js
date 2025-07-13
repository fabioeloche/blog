/**
 * Main JavaScript file for The Tennis Time
 */

document.addEventListener('DOMContentLoaded', function() {
    
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // Initialize popovers
    var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });
    
    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
    
    // Auto-hide alerts after 5 seconds
    setTimeout(function() {
        const alerts = document.querySelectorAll('.alert');
        alerts.forEach(function(alert) {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        });
    }, 5000);
    
    // Add loading state to forms
    document.querySelectorAll('form').forEach(form => {
        form.addEventListener('submit', function() {
            const submitBtn = this.querySelector('button[type="submit"]');
            if (submitBtn) {
                const originalText = submitBtn.innerHTML;
                submitBtn.innerHTML = '<span class="loading"></span> Loading...';
                submitBtn.disabled = true;
                
                // Re-enable button after 10 seconds as fallback
                setTimeout(() => {
                    submitBtn.innerHTML = originalText;
                    submitBtn.disabled = false;
                }, 10000);
            }
        });
    });
    
    // Search functionality enhancement
    const searchInput = document.querySelector('input[name="search"]');
    if (searchInput) {
        let searchTimeout;
        searchInput.addEventListener('input', function() {
            clearTimeout(searchTimeout);
            searchTimeout = setTimeout(() => {
                if (this.value.length >= 3) {
                    this.form.submit();
                }
            }, 500);
        });
    }
    
    // Comment form enhancement
    const commentForm = document.querySelector('.comment-form');
    if (commentForm) {
        const textarea = commentForm.querySelector('textarea');
        if (textarea) {
            // Auto-resize textarea
            textarea.addEventListener('input', function() {
                this.style.height = 'auto';
                this.style.height = (this.scrollHeight) + 'px';
            });
            
            // Character counter
            const charCounter = document.createElement('small');
            charCounter.className = 'text-muted mt-1 d-block';
            textarea.parentNode.appendChild(charCounter);
            
            textarea.addEventListener('input', function() {
                const remaining = 1000 - this.value.length;
                charCounter.textContent = `${remaining} characters remaining`;
                
                if (remaining < 100) {
                    charCounter.className = 'text-warning mt-1 d-block';
                } else if (remaining < 0) {
                    charCounter.className = 'text-danger mt-1 d-block';
                } else {
                    charCounter.className = 'text-muted mt-1 d-block';
                }
            });
        }
    }
    
    // Lazy loading for images
    if ('IntersectionObserver' in window) {
        const imageObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    img.src = img.dataset.src;
                    img.classList.remove('lazy');
                    imageObserver.unobserve(img);
                }
            });
        });
        
        document.querySelectorAll('img[data-src]').forEach(img => {
            imageObserver.observe(img);
        });
    }
    
    // Back to top button
    const backToTopBtn = document.createElement('button');
    backToTopBtn.innerHTML = '<i class="fas fa-arrow-up"></i>';
    backToTopBtn.className = 'btn btn-primary position-fixed';
    backToTopBtn.style.cssText = 'bottom: 20px; right: 20px; z-index: 1000; border-radius: 50%; width: 50px; height: 50px; display: none;';
    document.body.appendChild(backToTopBtn);
    
    window.addEventListener('scroll', function() {
        if (window.pageYOffset > 300) {
            backToTopBtn.style.display = 'block';
        } else {
            backToTopBtn.style.display = 'none';
        }
    });
    
    backToTopBtn.addEventListener('click', function() {
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    });
    
    // Keyboard shortcuts
    document.addEventListener('keydown', function(e) {
        // Ctrl/Cmd + K for search
        if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
            e.preventDefault();
            const searchInput = document.querySelector('input[name="search"]');
            if (searchInput) {
                searchInput.focus();
            }
        }
        
        // Escape to close modals
        if (e.key === 'Escape') {
            const modals = document.querySelectorAll('.modal.show');
            modals.forEach(modal => {
                const modalInstance = bootstrap.Modal.getInstance(modal);
                if (modalInstance) {
                    modalInstance.hide();
                }
            });
        }
    });
    
    // Copy link functionality
    document.querySelectorAll('.copy-link').forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            const url = window.location.href;
            
            if (navigator.clipboard) {
                navigator.clipboard.writeText(url).then(() => {
                    this.innerHTML = '<i class="fas fa-check"></i> Copied!';
                    setTimeout(() => {
                        this.innerHTML = '<i class="fas fa-link"></i> Copy Link';
                    }, 2000);
                });
            } else {
                // Fallback for older browsers
                const textArea = document.createElement('textarea');
                textArea.value = url;
                document.body.appendChild(textArea);
                textArea.select();
                document.execCommand('copy');
                document.body.removeChild(textArea);
                
                this.innerHTML = '<i class="fas fa-check"></i> Copied!';
                setTimeout(() => {
                    this.innerHTML = '<i class="fas fa-link"></i> Copy Link';
                }, 2000);
            }
        });
    });
    
    // Reading time calculator
    function calculateReadingTime() {
        const postContent = document.querySelector('.post-content');
        if (postContent) {
            const text = postContent.textContent || postContent.innerText;
            const wordCount = text.trim().split(/\s+/).length;
            const readingTime = Math.ceil(wordCount / 200); // Average reading speed: 200 words per minute
            
            const readingTimeElement = document.createElement('div');
            readingTimeElement.className = 'text-muted small';
            readingTimeElement.innerHTML = `<i class="fas fa-clock me-1"></i>${readingTime} min read`;
            
            const postHeader = document.querySelector('.d-flex.justify-content-between.align-items-center');
            if (postHeader) {
                postHeader.appendChild(readingTimeElement);
            }
        }
    }
    
    calculateReadingTime();
    
    // Social sharing
    function sharePost() {
        if (navigator.share) {
            navigator.share({
                title: document.title,
                url: window.location.href
            });
        } else {
            // Fallback: copy to clipboard
            const url = window.location.href;
            if (navigator.clipboard) {
                navigator.clipboard.writeText(url);
                alert('Link copied to clipboard!');
            }
        }
    }
    
    // Add share button to post detail pages
    const shareBtn = document.createElement('button');
    shareBtn.innerHTML = '<i class="fas fa-share-alt"></i> Share';
    shareBtn.className = 'btn btn-outline-primary btn-sm';
    shareBtn.addEventListener('click', sharePost);
    
    const postActions = document.querySelector('.d-flex.justify-content-between.align-items-center');
    if (postActions) {
        postActions.appendChild(shareBtn);
    }
    
    console.log('The Tennis Time - JavaScript loaded successfully!');
}); 