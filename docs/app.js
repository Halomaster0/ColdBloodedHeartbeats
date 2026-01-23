/**
 * Cold Blooded Heartbeats - Application Logic
 * Architecture: Unified Initialization
 */

const App = {
    currentStep: 1,
    cart: [],
    emailJS: {
        publicKey: 'tjFiVTG59iT5vLlQm',
        serviceID: 'service_jshwbap',
        templateID: 'template_8yplknt'
    },

    /**
     * Initialize all components and event listeners
     */
    init() {
        console.log("🚀 Cold Blooded Heartbeats Framework Initialized");

        this.loadCart();
        this.setupEventListeners();
        this.loadInventory(); // Dynamic stock loading
        this.updateConfiguratorUI();
        this.toggleMenu(); // Initialize mobile menu
    },

    /**
     * Fetch and render inventory from JSON
     */
    async loadInventory() {
        const containers = {
            'index': document.querySelector('#live-animals .grid'),
            'animals': document.querySelector('#browse-animals .grid'),
            'pantry': document.querySelector('#browse-pantry .grid'),
            'habitats': document.querySelector('#browse-habitats .grid'),
            'den': document.querySelector('#the-den-collection .grid')
        };

        // Determine which page we are on
        let currentPage = 'index';
        const path = window.location.pathname;
        if (path.includes('animals.html')) currentPage = 'animals';
        else if (path.includes('pantry.html')) currentPage = 'pantry';
        else if (path.includes('habitats.html')) currentPage = 'habitats';
        else if (path.includes('den.html')) currentPage = 'den';

        const container = containers[currentPage];
        if (!container) return;

        try {
            const response = await fetch('inventory.json');
            if (!response.ok) throw new Error("Failed to load inventory");
            const inventory = await response.json();

            // Filter by category
            let category = currentPage;
            if (currentPage === 'index' || currentPage === 'animals') category = 'animals';

            let items = inventory.filter(item => item.category === category && item.status !== 'sold');

            // Limit to 2 for homepage if needed, or keep all
            if (currentPage === 'index') items = items.slice(0, 2);

            if (items.length > 0) {
                container.innerHTML = items.map(item => this.createCardHTML(item)).join('');

                // Re-initialize buttons and animations after injection
                this.initProductButtons();
                this.revealOnScroll();
            }
        } catch (error) {
            console.error("📦 Inventory Load Error:", error);
        }
    },

    createCardHTML(item) {
        const isAnimal = item.category === 'animals';
        const badge = (isAnimal && item.verified_feeder) ? '<div class="badge-verified">Verified Feeder</div>' : '';

        let feedingLog = '';
        if (isAnimal && item.feeding_log && item.feeding_log.length > 0) {
            feedingLog = `
                <div class="meal-log">
                    <p>Last ${item.feeding_log.length} Meals:</p>
                    <ul>
                        ${item.feeding_log.map(log => `<li>${log.date} - ${log.food_type}</li>`).join('')}
                    </ul>
                </div>
            `;
        }

        const buyBtnText = isAnimal ? 'Buy Now' : (item.variant.includes('Subscribe') ? 'Subscribe' : 'Add to Cart');
        const buyBtnClass = isAnimal ? 'btn-buy' : (item.variant.includes('Subscribe') ? 'btn-subscribe' : 'btn-buy');

        const qtyControl = (!isAnimal && !item.variant.includes('Subscribe')) ? `
            <div class="qty-control">
                <button class="qty-btn qty-minus">-</button>
                <input type="number" value="1" min="1" class="qty-input">
                <button class="qty-btn qty-plus">+</button>
            </div>
        ` : '';

        const cardClass = isAnimal ? 'card glass-panel animal-card' : 'card glass-panel';

        return `
            <div class="${cardClass}" id="${item.id}">
                ${badge}
                <img src="${item.image}" alt="${item.name} ${item.variant}" class="${item.category === 'animals' ? 'animal-img' : item.category + '-img'}">
                <div class="animal-info">
                    <h3>${item.name} <span class="morph">${item.variant}</span></h3>
                    <p class="sku">SKU: ${item.id}</p>
                    ${feeding_log || `<p>${item.description || ''}</p>`}
                    <div class="card-footer">
                        <span class="price">$${item.price.toFixed(2)}</span>
                        ${qtyControl}
                        <button class="btn btn-sm ${buyBtnClass}">${buyBtnText}</button>
                    </div>
                    ${isAnimal ? '<a href="coming-soon.html" class="care-link">Download Care Guide (PDF)</a>' : ''}
                </div>
            </div>
        `;
    },

    initEmailJS() {
        if (window.emailjs) {
            emailjs.init(this.emailJS.publicKey);
        }
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

        // Checkout Modal Close
        document.querySelectorAll('.checkout-close').forEach(btn => {
            btn.addEventListener('click', () => this.closeCheckoutModal());
        });

        // Cart Toggle
        const cartTrigger = document.querySelector('.cart-trigger');
        const cartClose = document.querySelector('.cart-close');
        if (cartTrigger) cartTrigger.addEventListener('click', () => this.toggleCart(true));
        if (cartClose) cartClose.addEventListener('click', () => this.toggleCart(false));

        // Checkout Button
        const btnCheckout = document.querySelector('.btn-checkout');
        if (btnCheckout) {
            btnCheckout.addEventListener('click', () => {
                if (this.cart.length === 0) return alert("Your cart is empty!");
                this.toggleCart(false);
                this.openCheckoutModal();
            });
        }

        // Form Submission Overload
        const leadForm = document.getElementById('lead-form');
        if (leadForm) {
            leadForm.addEventListener('submit', (e) => {
                e.preventDefault();
                this.handleLeadSubmit();
            });
        }

        // Checkout Form Submission
        const checkoutForm = document.getElementById('checkout-form');
        if (checkoutForm) {
            checkoutForm.addEventListener('submit', (e) => {
                e.preventDefault();
                // Prevent double submission
                if (checkoutForm.dataset.submitting === 'true') return;
                checkoutForm.dataset.submitting = 'true';
                this.handleCheckoutSubmit().finally(() => {
                    checkoutForm.dataset.submitting = 'false';
                });
            });
        }

        // Payment method change listener
        document.querySelectorAll('input[name="payment-method"]').forEach(radio => {
            radio.addEventListener('change', (e) => this.handlePaymentMethodChange(e.target.value));
        });

        // Quantity Selector Logic (+ / - buttons)
        document.addEventListener('click', (e) => {
            if (e.target.classList.contains('qty-plus')) {
                const input = e.target.previousElementSibling;
                input.value = parseInt(input.value) + 1;
            }
            if (e.target.classList.contains('qty-minus')) {
                const input = e.target.nextElementSibling;
                if (parseInt(input.value) > 1) {
                    input.value = parseInt(input.value) - 1;
                }
            }
        });
    },

    /**
     * Cart Management
     */
    loadCart() {
        this.cart = JSON.parse(localStorage.getItem('cbh_cart') || '[]');
        this.updateCartUI();
    },

    saveCart() {
        localStorage.setItem('cbh_cart', JSON.stringify(this.cart));
        this.updateCartUI();
    },

    addToCart(product, quantity = 1) {
        const existingItem = this.cart.find(item => item.name === product.name && item.price === product.price);
        if (existingItem) {
            existingItem.quantity += quantity;
        } else {
            this.cart.push({ ...product, quantity });
        }
        this.saveCart();
        this.showToast(`${quantity} x ${product.name} added to cart!`);
    },

    removeFromCart(index) {
        this.cart.splice(index, 1);
        this.saveCart();
    },

    showToast(message) {
        // Create toast notification
        const toast = document.createElement('div');
        toast.className = 'toast-notification';
        toast.innerText = message;
        document.body.appendChild(toast);

        setTimeout(() => toast.classList.add('show'), 10);
        setTimeout(() => {
            toast.classList.remove('show');
            setTimeout(() => toast.remove(), 300);
        }, 2000);
    },

    updateCartUI() {
        const cartItemsContainer = document.querySelector('.cart-items');

        if (!cartItemsContainer) return;

        cartItemsContainer.innerHTML = '';
        let total = 0;

        this.cart.forEach((item, index) => {
            const itemElement = document.createElement('div');
            itemElement.className = 'cart-item';
            itemElement.innerHTML = `
                <div class="cart-item-info">
                    <h4>${item.name}</h4>
                    <p>$${item.price.toFixed(2)}</p>
                    <div class="cart-item-qty">
                        <button class="cart-qty-btn" onclick="App.updateItemQuantity(${index}, -1)">-</button>
                        <span class="cart-qty-val">${item.quantity}</span>
                        <button class="cart-qty-btn" onclick="App.updateItemQuantity(${index}, 1)">+</button>
                    </div>
                </div>
                <button class="cart-item-remove" onclick="App.removeFromCart(${index})">&times;</button>
            `;
            cartItemsContainer.appendChild(itemElement);
            total += (item.price * item.quantity);
        });

        const totalAmount = document.querySelector('.total-amount');
        if (totalAmount) totalAmount.innerText = `$${total.toFixed(2)}`;

        const countBadge = document.querySelector('.cart-count');
        if (countBadge) {
            const totalItems = this.cart.reduce((sum, item) => sum + item.quantity, 0);
            countBadge.innerText = totalItems;
        }
    },

    updateItemQuantity(index, delta) {
        this.cart[index].quantity += delta;
        if (this.cart[index].quantity < 1) {
            this.removeFromCart(index);
        } else {
            this.saveCart();
        }
    },

    /**
     * Mobile Cart Toggle
     */
    toggleCart(force) {
        const cartSidebar = document.querySelector('.cart-sidebar');
        if (cartSidebar) {
            if (force !== undefined) {
                force ? cartSidebar.classList.add('active') : cartSidebar.classList.remove('active');
            } else {
                cartSidebar.classList.toggle('active');
            }
        }
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
    openModal(title, subtitle, prefillMessage = '') {
        document.getElementById('modal-title').innerText = title;
        document.getElementById('modal-subtitle').innerText = subtitle;
        const modal = document.getElementById('lead-modal');
        modal.classList.remove('hidden');
        // Small delay to allow display change before opacity transition
        setTimeout(() => modal.classList.add('active'), 10);

        document.getElementById('modal-form-content').classList.remove('hidden');
        document.getElementById('modal-success').classList.add('hidden');

        // Pre-fill message if provided
        // Pre-fill message if provided, otherwise clear it
        const messageField = document.getElementById('message');
        if (messageField) {
            messageField.value = prefillMessage || '';
        }
    },

    openCheckoutModal() {
        // Build order summary
        const total = this.cart.reduce((sum, item) => sum + (item.price * item.quantity), 0);

        // Open checkout modal
        const checkoutModal = document.getElementById('checkout-modal');
        if (!checkoutModal) return;

        // Reset UI state (ensure form is shown, success is hidden)
        const checkoutContent = document.getElementById('checkout-content');
        const checkoutSuccess = document.getElementById('checkout-success');
        if (checkoutContent) checkoutContent.classList.remove('hidden');
        if (checkoutSuccess) checkoutSuccess.classList.add('hidden');

        // Update order summary display
        const orderList = checkoutModal.querySelector('.checkout-order-list');
        if (orderList) {
            orderList.innerHTML = this.cart.map(item => `
                <div class="checkout-order-item">
                    <span>${item.name} (x${item.quantity})</span>
                    <span>$${(item.price * item.quantity).toFixed(2)}</span>
                </div>
            `).join('');
        }

        const totalDisplay = checkoutModal.querySelector('.checkout-total-amount');
        if (totalDisplay) totalDisplay.innerText = `$${total.toFixed(2)}`;

        checkoutModal.classList.remove('hidden');
        setTimeout(() => checkoutModal.classList.add('active'), 10);
    },

    closeModal() {
        const modal = document.getElementById('lead-modal');
        if (modal) {
            modal.classList.remove('active');
            // Wait for transition to finish before hiding display
            setTimeout(() => modal.classList.add('hidden'), 400);
        }
    },

    closeCheckoutModal() {
        const checkoutModal = document.getElementById('checkout-modal');
        if (checkoutModal) {
            checkoutModal.classList.remove('active');
            setTimeout(() => checkoutModal.classList.add('hidden'), 400);
        }
    },

    async handleLeadSubmit() {
        const leadForm = document.getElementById('lead-form');
        if (!leadForm) return;

        const name = document.getElementById('name').value;
        const email = document.getElementById('email').value;
        const message = document.getElementById('message').value;

        // 1. Submit to Formspree
        try {
            const formData = new FormData(leadForm);
            const response = await fetch(leadForm.action, {
                method: 'POST',
                body: formData,
                headers: { 'Accept': 'application/json' }
            });

            if (response.ok) {
                // 2. Send EmailJS Confirmation (optional for inquiries)
                if (window.emailjs) {
                    await emailjs.send(this.emailJS.serviceID, this.emailJS.templateID, {
                        to_name: name,
                        to_email: email,
                        order_details: message,
                        reply_to: 'info@coldbloodedheartbeats.com'
                    });
                }

                // Switch UI state
                document.getElementById('modal-form-content').classList.add('hidden');
                document.getElementById('modal-success').classList.remove('hidden');

                leadForm.reset();
            } else {
                alert("Submission failed. Please try again.");
            }
        } catch (error) {
            console.error("Error submitting form:", error);
            alert("An error occurred. Please try again.");
        }
    },

    async handleCheckoutSubmit() {
        const checkoutForm = document.getElementById('checkout-form');
        const customerEmail = document.getElementById('checkout-email').value;
        const paymentMethod = document.querySelector('input[name="payment-method"]:checked')?.value;

        if (!paymentMethod) {
            return alert("Please select a payment method");
        }

        const orderSummary = this.cart.map(item => `- ${item.name} (x${item.quantity}) at $${item.price.toFixed(2)} each = $${(item.price * item.quantity).toFixed(2)}`).join('\n');
        const total = this.cart.reduce((sum, item) => sum + (item.price * item.quantity), 0);

        try {
            // 1. Submit to Formspree (owner notification)
            const checkoutForm = document.getElementById('checkout-form');
            if (!checkoutForm) throw new Error("Checkout form not found");

            const formData = new FormData(checkoutForm);

            // Add order details to form
            formData.set('email', customerEmail);
            formData.set('payment_method', paymentMethod);
            formData.set('order_summary', `${orderSummary}\n\nTotal: $${total.toFixed(2)}`);
            formData.set('total', total.toFixed(2));

            // Add card details if applicable
            if (paymentMethod === 'Card') {
                const cardholderName = document.getElementById('cardholder-name')?.value;
                if (cardholderName) {
                    formData.set('cardholder_name', cardholderName);
                }
            }

            const response = await fetch(checkoutForm.action, {
                method: 'POST',
                body: formData,
                headers: { 'Accept': 'application/json' }
            });

            if (response.ok) {
                // 2. Send EmailJS confirmation to customer
                if (window.emailjs) {
                    const emailData = {
                        to_name: customerEmail.split('@')[0],
                        to_email: customerEmail,
                        order_details: `${orderSummary}\n\nTotal: $${total.toFixed(2)}\nPayment Method: ${paymentMethod}`,
                        reply_to: 'info@coldbloodedheartbeats.com'
                    };

                    // Add payment-specific info
                    if (paymentMethod === 'Card') {
                        const cardholderName = document.getElementById('cardholder-name')?.value;
                        if (cardholderName) {
                            emailData.order_details += `\nCardholder: ${cardholderName}`;
                        }
                    }

                    await emailjs.send(this.emailJS.serviceID, this.emailJS.templateID, emailData);
                }

                // Show success message
                const checkoutContent = document.getElementById('checkout-content');
                const checkoutSuccess = document.getElementById('checkout-success');

                if (checkoutContent) checkoutContent.classList.add('hidden');
                if (checkoutSuccess) checkoutSuccess.classList.remove('hidden');

                // Clear cart
                this.cart = [];
                this.saveCart();

                checkoutForm.reset();
            } else {
                console.error("Formspree response error:", response.status, response.statusText);
                alert("Checkout failed. Please try again.");
            }
        } catch (error) {
            console.error("Error during checkout:", error);
            alert("An error occurred. Please try again.");
        }
    },

    handlePaymentMethodChange(method) {
        const paymentDetailsSection = document.getElementById('payment-details');
        if (!paymentDetailsSection) return;

        let detailsHTML = '';

        switch (method) {
            case 'E-Transfer':
                detailsHTML = `
                    <div class="payment-detail-box">
                        <p class="payment-info">📧 E-Transfer instructions will be sent to your email after order confirmation.</p>
                    </div>
                `;
                break;
            case 'PayPal':
                detailsHTML = `
                    <div class="payment-detail-box">
                        <p class="payment-info">💡 Invoice will be sent to your email. You'll receive a PayPal payment link.</p>
                    </div>
                `;
                break;
            case 'Card':
                detailsHTML = `
                    <div class="card-payment-fields">
                        <div class="form-group">
                            <label for="cardholder-name">Cardholder Name</label>
                            <input type="text" id="cardholder-name" name="cardholder_name" placeholder="Full Name" required>
                        </div>
                        <div class="form-group">
                            <label for="card-number">Card Number</label>
                            <input type="text" id="card-number" name="card_number" placeholder="XXXX XXXX XXXX XXXX" maxlength="19" required>
                        </div>
                        <div class="card-details-row">
                            <div class="form-group">
                                <label for="card-expiry">Expiration</label>
                                <input type="text" id="card-expiry" name="card_expiry" placeholder="MM/YY" maxlength="5" required>
                            </div>
                            <div class="form-group">
                                <label for="card-cvv">CVV</label>
                                <input type="text" id="card-cvv" name="card_cvv" placeholder="***" maxlength="3" required>
                            </div>
                        </div>
                        <p class="payment-info">💳 Card will be processed securely. You'll receive confirmation via email.</p>
                    </div>
                `;
                break;
        }

        paymentDetailsSection.innerHTML = detailsHTML;

        // Add input formatting for card fields
        if (method === 'Card') {
            this.initCardFormatting();
        }
    },

    initCardFormatting() {
        // Format card number with spaces
        const cardNumberInput = document.getElementById('card-number');
        if (cardNumberInput) {
            cardNumberInput.addEventListener('input', (e) => {
                let value = e.target.value.replace(/\s/g, '');
                let formattedValue = value.match(/.{1,4}/g)?.join(' ') || value;
                e.target.value = formattedValue;
            });
        }

        // Format expiry date
        const expiryInput = document.getElementById('card-expiry');
        if (expiryInput) {
            expiryInput.addEventListener('input', (e) => {
                let value = e.target.value.replace(/\D/g, '');
                if (value.length >= 2) {
                    value = value.slice(0, 2) + '/' + value.slice(2, 4);
                }
                e.target.value = value;
            });
        }

        // Only allow numbers in CVV
        const cvvInput = document.getElementById('card-cvv');
        if (cvvInput) {
            cvvInput.addEventListener('input', (e) => {
                e.target.value = e.target.value.replace(/\D/g, '');
            });
        }
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
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px'
        };

        const observer = new IntersectionObserver((entries) => {
            entries.forEach((entry, index) => {
                if (entry.isIntersecting) {
                    // Staggered reveal for grid items
                    const delay = (entry.target.classList.contains('card')) ? (index % 3) * 100 : 0;
                    setTimeout(() => {
                        entry.target.style.opacity = '1';
                        entry.target.style.transform = 'translateY(0)';
                    }, delay);
                    observer.unobserve(entry.target);
                }
            });
        }, observerOptions);

        document.querySelectorAll('.glass-panel, .section-title, .hero-content').forEach(el => {
            el.style.opacity = '0';
            el.style.transform = 'translateY(30px)';
            el.style.transition = 'all 0.8s cubic-bezier(0.165, 0.84, 0.44, 1)';
            observer.observe(el);
        });
    },

    /**
     * Combined Buy/Inquiry logic
     */
    initProductButtons() {
        document.querySelectorAll('.btn-buy, .btn-subscribe, .btn-sm').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const card = e.target.closest('.card');
                if (!card) return;

                const name = card.querySelector('h3').innerText;
                const priceMatch = card.querySelector('.price').innerText.match(/\d+\.?\d*/);
                const price = priceMatch ? parseFloat(priceMatch[0]) : 0;

                // Determine if it's a direct buy or inquiry
                const isDirectBuy = btn.classList.contains('btn-buy') || btn.classList.contains('btn-subscribe');
                const isLive = card.classList.contains('animal-card');

                if (isLive) {
                    // Pre-fill inquiry with animal details
                    const sku = card.querySelector('.sku')?.innerText || '';
                    const prefillText = `I'm interested in: ${name}\n${sku}\nPrice: $${price.toFixed(2)}\n\nAdditional questions:\n`;
                    this.openModal(`Inquiry: ${name}`, 'Live animals require a brief consultation before purchase.', prefillText);
                } else if (isDirectBuy) {
                    const qtyInput = card.querySelector('.qty-input');
                    const quantity = qtyInput ? parseInt(qtyInput.value) : 1;
                    this.addToCart({ name, price }, quantity);
                }
            });
        });
    },

    /**
     * Mobile Menu Toggle
     */
    toggleMenu() {
        const menuToggle = document.querySelector('.menu-toggle');
        const navLinks = document.querySelector('.nav-links');

        // Add backdrop element if it doesn't exist
        let backdrop = document.querySelector('.nav-backdrop');
        if (!backdrop) {
            backdrop = document.createElement('div');
            backdrop.className = 'nav-backdrop';
            backdrop.style.cssText = `
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background: rgba(0,0,0,0.5);
                backdrop-filter: blur(5px);
                z-index: 950;
                opacity: 0;
                visibility: hidden;
                transition: all 0.4s ease;
            `;
            document.body.appendChild(backdrop);
        }

        if (menuToggle && navLinks) {
            const toggle = () => {
                const isActive = menuToggle.classList.toggle('active');
                navLinks.classList.toggle('active');

                if (isActive) {
                    backdrop.style.opacity = '1';
                    backdrop.style.visibility = 'visible';
                    document.body.style.overflow = 'hidden';
                } else {
                    backdrop.style.opacity = '0';
                    backdrop.style.visibility = 'hidden';
                    document.body.style.overflow = '';
                }
            };

            menuToggle.addEventListener('click', toggle);
            backdrop.addEventListener('click', toggle);

            // Close menu when a link is clicked
            document.querySelectorAll('.nav-item a').forEach(link => {
                link.addEventListener('click', () => {
                    if (menuToggle.classList.contains('active')) {
                        toggle();
                    }
                });
            });
        }
    }
};

// Start application when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    App.init();
});
