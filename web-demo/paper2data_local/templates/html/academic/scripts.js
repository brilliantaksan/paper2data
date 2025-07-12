// Paper2Data Academic Theme Interactive Scripts

document.addEventListener('DOMContentLoaded', function() {
    // Initialize all interactive features
    initializeTableOfContents();
    initializeSearchFunctionality();
    initializeFigureZoom();
    initializeTableEnhancements();
    initializeScrollToTop();
    initializeProgressIndicator();
    initializeAccessibilityFeatures();
    
    console.log('Paper2Data interactive features initialized');
});

// Table of Contents Enhancement
function initializeTableOfContents() {
    const toc = document.getElementById('table-of-contents');
    if (!toc) return;
    
    const tocLinks = toc.querySelectorAll('a');
    const sections = document.querySelectorAll('section[id]');
    
    // Add smooth scrolling and active state management
    tocLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const targetId = this.getAttribute('href').substring(1);
            const targetSection = document.getElementById(targetId);
            
            if (targetSection) {
                targetSection.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
                
                // Update active state
                updateActiveSection(targetId);
            }
        });
    });
    
    // Update active section on scroll
    window.addEventListener('scroll', debounce(updateActiveSection, 100));
}

// Search Functionality
function initializeSearchFunctionality() {
    // Create search box
    const searchBox = document.createElement('div');
    searchBox.className = 'search-box';
    searchBox.innerHTML = `
        <input type="text" id="paper-search" placeholder="Search in paper...">
        <button type="button" id="search-button">Search</button>
        <div id="search-results" class="search-results"></div>
    `;
    
    const nav = document.querySelector('.paper-nav');
    if (nav) {
        nav.appendChild(searchBox);
        
        const searchInput = document.getElementById('paper-search');
        const searchButton = document.getElementById('search-button');
        const searchResults = document.getElementById('search-results');
        
        searchInput.addEventListener('input', debounce(performSearch, 300));
        searchButton.addEventListener('click', performSearch);
        
        function performSearch() {
            const query = searchInput.value.trim();
            if (query.length < 2) {
                searchResults.innerHTML = '';
                return;
            }
            
            const results = searchInContent(query);
            displaySearchResults(results, searchResults);
        }
    }
}

// Figure Zoom Enhancement
function initializeFigureZoom() {
    const figures = document.querySelectorAll('.paper-figure img');
    
    figures.forEach(img => {
        img.addEventListener('click', function() {
            createImageModal(this);
        });
        
        // Add zoom cursor
        img.style.cursor = 'zoom-in';
        img.title = 'Click to zoom';
    });
}

// Table Enhancements
function initializeTableEnhancements() {
    const tables = document.querySelectorAll('.paper-table table');
    
    tables.forEach(table => {
        // Add sortable functionality
        makeTableSortable(table);
        
        // Add hover effects
        const rows = table.querySelectorAll('tr');
        rows.forEach(row => {
            row.addEventListener('mouseenter', function() {
                this.style.backgroundColor = '#e3f2fd';
            });
            
            row.addEventListener('mouseleave', function() {
                this.style.backgroundColor = '';
            });
        });
    });
}

// Scroll to Top Button
function initializeScrollToTop() {
    const scrollButton = document.createElement('button');
    scrollButton.className = 'scroll-to-top';
    scrollButton.innerHTML = '↑';
    scrollButton.title = 'Scroll to top';
    document.body.appendChild(scrollButton);
    
    scrollButton.addEventListener('click', function() {
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    });
    
    // Show/hide based on scroll position
    window.addEventListener('scroll', function() {
        if (window.pageYOffset > 300) {
            scrollButton.style.display = 'block';
        } else {
            scrollButton.style.display = 'none';
        }
    });
}

// Progress Indicator
function initializeProgressIndicator() {
    const progressBar = document.createElement('div');
    progressBar.className = 'reading-progress';
    document.body.appendChild(progressBar);
    
    window.addEventListener('scroll', function() {
        const scrollHeight = document.documentElement.scrollHeight - window.innerHeight;
        const scrolled = window.pageYOffset;
        const progress = (scrolled / scrollHeight) * 100;
        progressBar.style.width = progress + '%';
    });
}

// Accessibility Features
function initializeAccessibilityFeatures() {
    // Add skip links
    const skipLink = document.createElement('a');
    skipLink.href = '#main-content';
    skipLink.className = 'skip-link';
    skipLink.textContent = 'Skip to main content';
    document.body.insertBefore(skipLink, document.body.firstChild);
    
    // Add aria labels where needed
    const figures = document.querySelectorAll('.paper-figure');
    figures.forEach((figure, index) => {
        figure.setAttribute('aria-label', `Figure ${index + 1}`);
    });
    
    const tables = document.querySelectorAll('.paper-table');
    tables.forEach((table, index) => {
        table.setAttribute('aria-label', `Table ${index + 1}`);
    });
}

// Helper Functions
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

function updateActiveSection(targetId) {
    if (!targetId) {
        // Find current section based on scroll position
        const sections = document.querySelectorAll('section[id]');
        let currentSection = null;
        
        sections.forEach(section => {
            const rect = section.getBoundingClientRect();
            if (rect.top <= 100 && rect.bottom >= 100) {
                currentSection = section;
            }
        });
        
        if (currentSection) {
            targetId = currentSection.id;
        }
    }
    
    // Update TOC active state
    const tocLinks = document.querySelectorAll('#table-of-contents a');
    tocLinks.forEach(link => {
        link.classList.remove('active');
        if (link.getAttribute('href') === '#' + targetId) {
            link.classList.add('active');
        }
    });
}

function searchInContent(query) {
    const results = [];
    const sections = document.querySelectorAll('.content-sections section');
    
    sections.forEach(section => {
        const sectionText = section.textContent.toLowerCase();
        const queryLower = query.toLowerCase();
        
        if (sectionText.includes(queryLower)) {
            const sectionTitle = section.querySelector('h2')?.textContent || 'Unknown Section';
            const sectionId = section.id;
            
            // Find context around the match
            const index = sectionText.indexOf(queryLower);
            const start = Math.max(0, index - 50);
            const end = Math.min(sectionText.length, index + query.length + 50);
            const context = sectionText.substring(start, end);
            
            results.push({
                title: sectionTitle,
                id: sectionId,
                context: context,
                relevance: calculateRelevance(sectionText, queryLower)
            });
        }
    });
    
    return results.sort((a, b) => b.relevance - a.relevance);
}

function calculateRelevance(text, query) {
    const occurrences = (text.match(new RegExp(query, 'g')) || []).length;
    return occurrences / text.length * 1000;
}

function displaySearchResults(results, container) {
    if (results.length === 0) {
        container.innerHTML = '<div class="no-results">No results found</div>';
        return;
    }
    
    const resultsHtml = results.map(result => `
        <div class="search-result">
            <h4><a href="#${result.id}">${result.title}</a></h4>
            <p class="search-context">${result.context}</p>
        </div>
    `).join('');
    
    container.innerHTML = resultsHtml;
    
    // Add click handlers for search results
    const resultLinks = container.querySelectorAll('a');
    resultLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const targetId = this.getAttribute('href').substring(1);
            const targetSection = document.getElementById(targetId);
            
            if (targetSection) {
                targetSection.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
                container.innerHTML = '';
                document.getElementById('paper-search').value = '';
            }
        });
    });
}

function createImageModal(img) {
    const modal = document.createElement('div');
    modal.className = 'image-modal';
    modal.innerHTML = `
        <div class="modal-content">
            <span class="close-modal">&times;</span>
            <img src="${img.src}" alt="${img.alt}">
            <div class="modal-caption">${img.closest('figure')?.querySelector('figcaption')?.textContent || ''}</div>
        </div>
    `;
    
    document.body.appendChild(modal);
    
    // Add event listeners
    modal.addEventListener('click', function(e) {
        if (e.target === modal || e.target.classList.contains('close-modal')) {
            document.body.removeChild(modal);
        }
    });
    
    // Close on escape key
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape' && document.body.contains(modal)) {
            document.body.removeChild(modal);
        }
    });
}

function makeTableSortable(table) {
    const headers = table.querySelectorAll('th');
    
    headers.forEach((header, index) => {
        header.style.cursor = 'pointer';
        header.title = 'Click to sort';
        
        header.addEventListener('click', function() {
            sortTable(table, index);
        });
    });
}

function sortTable(table, column) {
    const tbody = table.querySelector('tbody');
    const rows = Array.from(tbody.querySelectorAll('tr'));
    
    // Determine sort direction
    const isAscending = !table.dataset.sortOrder || table.dataset.sortOrder === 'desc';
    table.dataset.sortOrder = isAscending ? 'asc' : 'desc';
    
    // Sort rows
    rows.sort((a, b) => {
        const aValue = a.cells[column].textContent.trim();
        const bValue = b.cells[column].textContent.trim();
        
        // Try to parse as numbers
        const aNum = parseFloat(aValue);
        const bNum = parseFloat(bValue);
        
        if (!isNaN(aNum) && !isNaN(bNum)) {
            return isAscending ? aNum - bNum : bNum - aNum;
        }
        
        // String comparison
        return isAscending ? aValue.localeCompare(bValue) : bValue.localeCompare(aValue);
    });
    
    // Update DOM
    rows.forEach(row => tbody.appendChild(row));
    
    // Update header indicators
    const headers = table.querySelectorAll('th');
    headers.forEach(h => h.classList.remove('sorted-asc', 'sorted-desc'));
    headers[column].classList.add(isAscending ? 'sorted-asc' : 'sorted-desc');
}

// Additional CSS for interactive elements
const additionalStyles = `
    .search-box {
        margin-top: 20px;
        padding: 15px;
        background-color: #f8f9fa;
        border-radius: 4px;
    }
    
    .search-box input {
        width: 70%;
        padding: 8px;
        border: 1px solid #ddd;
        border-radius: 4px;
    }
    
    .search-box button {
        padding: 8px 16px;
        margin-left: 10px;
        background-color: #3498db;
        color: white;
        border: none;
        border-radius: 4px;
        cursor: pointer;
    }
    
    .search-results {
        margin-top: 15px;
        max-height: 300px;
        overflow-y: auto;
    }
    
    .search-result {
        padding: 10px;
        border-bottom: 1px solid #eee;
    }
    
    .search-result h4 {
        margin: 0 0 5px 0;
        color: #3498db;
    }
    
    .search-context {
        color: #666;
        font-size: 0.9em;
    }
    
    .image-modal {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-color: rgba(0, 0, 0, 0.8);
        display: flex;
        align-items: center;
        justify-content: center;
        z-index: 1000;
    }
    
    .modal-content {
        position: relative;
        max-width: 90%;
        max-height: 90%;
        background-color: white;
        padding: 20px;
        border-radius: 8px;
    }
    
    .modal-content img {
        max-width: 100%;
        max-height: 70vh;
        object-fit: contain;
    }
    
    .close-modal {
        position: absolute;
        top: 10px;
        right: 15px;
        font-size: 28px;
        cursor: pointer;
        color: #999;
    }
    
    .modal-caption {
        margin-top: 10px;
        font-style: italic;
        color: #666;
        text-align: center;
    }
    
    .scroll-to-top {
        position: fixed;
        bottom: 20px;
        right: 20px;
        background-color: #3498db;
        color: white;
        border: none;
        width: 50px;
        height: 50px;
        border-radius: 50%;
        cursor: pointer;
        display: none;
        z-index: 100;
        font-size: 18px;
    }
    
    .reading-progress {
        position: fixed;
        top: 0;
        left: 0;
        height: 3px;
        background-color: #3498db;
        z-index: 100;
        transition: width 0.3s;
    }
    
    .skip-link {
        position: absolute;
        top: -40px;
        left: 6px;
        background: #000;
        color: white;
        padding: 8px;
        text-decoration: none;
        z-index: 100;
    }
    
    .skip-link:focus {
        top: 6px;
    }
    
    #table-of-contents a.active {
        color: #2980b9;
        font-weight: bold;
        background-color: #e8f4ff;
        padding: 2px 6px;
        border-radius: 3px;
    }
    
    th.sorted-asc::after {
        content: ' ↑';
    }
    
    th.sorted-desc::after {
        content: ' ↓';
    }
`;

// Add additional styles to the document
const styleSheet = document.createElement('style');
styleSheet.textContent = additionalStyles;
document.head.appendChild(styleSheet); 