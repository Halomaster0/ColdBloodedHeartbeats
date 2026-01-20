/**
 * Cold Blooded Heartbeats - Application Logic
 * Architecture: Unified Initialization
 */

const App = {
    currentStep: 1,

    /**
     * Initialize all components and event listeners
     */
    init() {
        console.log("🚀 Cold Blooded Heartbeats Framework Initialized");

        this.setupEventListeners();
        this.revealOnScroll();
        this.updateConfiguratorUI();
        this.initBuyButtons(); // Initialize product interaction logic
        this.toggleMenu(); // Initialize mobile menu
    },

    /**
     * Centralized Event Listener Management
     */
    setupEventListeners() {
        // CTA Buttons
        const ctaPrimary = document.getElementById('cta-primary');
        const ctaSecondary = document.getElementById('cta-secondary');

        if (ctaPrimary) {
            ctaPrimary.addEventListener('click', () => {
                this.handleNavigation('#live-animals');
            });
        }

        if (ctaSecondary) {
            ctaSecondary.addEventListener('click', () => {
                this.openModal('Specialty Consultation', 'Our expert keepers will help you find the perfect match.');
            });
        }

        // Modal Hooks
        document.querySelectorAll('.btn-consult').forEach(btn => {
            btn.addEventListener('click', (e) => {
                e.preventDefault();
                this.openModal('Specialty Consultation', 'Our expert keepers will help you find the perfect match.');
            });
        });

        // Configurator logic extension for quote
        const btnNext = document.getElementById('btn-next');
        const btnPrev = document.getElementById('btn-prev');

        if (btnNext) {
            btnNext.addEventListener('click', () => {
                if (this.currentStep === 3) {
                    this.openModal('Enclosure Quote Request', 'Specify your requirements and we will send a detailed blueprint.');
                } else {
                    this.handleStep(1);
                }
            });
        }
        if (btnPrev) {
            btnPrev.addEventListener('click', () => this.handleStep(-1));
        }

        // Modal Close
        document.querySelectorAll('.modal-close, .modal-close-btn').forEach(btn => {
            btn.addEventListener('click', () => this.closeModal());
        });

    },

    /**
     * Handle Step Transitions
     */
    handleStep(direction) {
        this.currentStep += direction;
        this.updateConfiguratorUI();
    },

    /**
     * Update Configurator UI Visibility
     */
    updateConfiguratorUI() {
        // Update Steps
        document.querySelectorAll('.config-step').forEach((step, index) => {
            if (index + 1 === this.currentStep) {
                step.classList.remove('hidden');
                step.style.opacity = '0';
                setTimeout(() => {
                    step.style.opacity = '1';
                    step.style.transition = 'opacity 0.3s ease';
                }, 10);
            } else {
                step.classList.add('hidden');
            }
        });

        // Update Indicators
        document.querySelectorAll('.step-indicator .step').forEach((step, index) => {
            if (index + 1 === this.currentStep) {
                step.classList.add('active');
            } else if (index + 1 < this.currentStep) {
                step.classList.add('completed');
                step.classList.remove('active');
            } else {
                step.classList.remove('active', 'completed');
            }
        });

        // Update Buttons
        const btnPrev = document.getElementById('btn-prev');
        const btnNext = document.getElementById('btn-next');

        if (btnPrev) btnPrev.disabled = this.currentStep === 1;
        if (btnNext) {
            btnNext.innerText = this.currentStep === 3 ? 'Request Quote' : 'Next Step';
        }
    },

    /**
     * Modal Management
     */
    openModal(title, subtitle) {
        document.getElementById('modal-title').innerText = title;
        document.getElementById('modal-subtitle').innerText = subtitle;
        const modal = document.getElementById('lead-modal');
        modal.classList.remove('hidden');
        // Small delay to allow display change before opacity transition
        setTimeout(() => modal.classList.add('active'), 10);

        document.getElementById('modal-form-content').classList.remove('hidden');
        document.getElementById('modal-success').classList.add('hidden');
    },

    closeModal() {
        const modal = document.getElementById('lead-modal');
        modal.classList.remove('active');
        // Wait for transition to finish before hiding display
        setTimeout(() => modal.classList.add('hidden'), 400);
    },

    handleLeadSubmit() {
        const leadForm = document.getElementById('lead-form');
        const name = document.getElementById('name').value;
        const email = document.getElementById('email').value;
        const message = document.getElementById('message').value;

        console.log(`📡 Handoff to Layer 3: Lead for ${name} (${email})`);

        // Simulated Persistence for Local Demo
        const leads = JSON.parse(localStorage.getItem('cbh_leads') || '[]');
        leads.push({
            timestamp: new Date().toISOString(),
            name,
            email,
            message,
            status: 'NEW'
        });
        localStorage.setItem('cbh_leads', JSON.stringify(leads));

        // Switch UI state
        document.getElementById('modal-form-content').classList.add('hidden');
        document.getElementById('modal-success').classList.remove('hidden');

        // IMPORTANT: Reset form fields for next use
        leadForm.reset();
    },

    /**
     * Smooth scroll navigation
     */
    handleNavigation(selector) {
        const element = document.querySelector(selector);
        if (element) {
            element.scrollIntoView({ behavior: 'smooth' });
        }
    },

    /**
     * Subtle entrance reveal animations
     */
    revealOnScroll() {
        const observerOptions = {
            threshold: 0.1
        };

        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.style.opacity = '1';
                    entry.target.style.transform = 'translateY(0)';
                }
            });
        }, observerOptions);

        document.querySelectorAll('.glass-panel').forEach(panel => {
            panel.style.opacity = '0';
            panel.style.transform = 'translateY(20px)';
            panel.style.transition = 'all 0.6s cubic-bezier(0.165, 0.84, 0.44, 1)';
            observer.observe(panel);
        });
    },

    /**
     * Initialize Product Interaction (Buy/Subscribe)
     */
    initBuyButtons() {
        document.querySelectorAll('.btn-buy, .btn-subscribe').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const card = e.target.closest('.card');
                const title = card ? card.querySelector('h3').innerText : 'Product Inquiry';
                const action = e.target.classList.contains('btn-subscribe') ? 'Subscription' : 'Purchase';

                this.openModal(`${action} Inquiry: ${title}`, 'Specify your preferences and our specialist will finalize the order with you.');
            });
        });
    },

    /**
     * Mobile Menu Toggle
     */
    toggleMenu() {
        const menuToggle = document.querySelector('.menu-toggle');
        const navLinks = document.querySelector('.nav-links');

        if (menuToggle && navLinks) {
            menuToggle.addEventListener('click', () => {
                menuToggle.classList.toggle('active');
                navLinks.classList.toggle('active');
            });

            // Close menu when a link is clicked
            document.querySelectorAll('.nav-item a').forEach(link => {
                link.addEventListener('click', () => {
                    menuToggle.classList.remove('active');
                    navLinks.classList.remove('active');
                });
            });
        }
    }
};

// Start application when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    App.init();
});
