# Cold Blooded Heartbeats - Handover & Maintenance Guide

Congratulations! Your premium reptile e-commerce platform is ready. This guide covers how to manage your content, integrate payment services, and maintain your site.

---

## 1. Managing Products

### Adding/Editing Products in The Pantry or Habitats

Products are simple HTML blocks. To add a new product:

1. Open `pantry.html` or `habitats.html`
2. Find an existing product card (starts with `<div class="card glass-panel animal-card">`)
3. Copy the entire block and paste it where you want the new product
4. Update the details:

```html
<div class="card glass-panel animal-card">
    <img src="Assets/YOUR_IMAGE.jpg" alt="Product Name" class="pantry-img">
    <div class="animal-info">
        <h3>Product Name <span class="morph">Variant/Size</span></h3>
        <p>Product description here.</p>
        <div class="card-footer">
            <span class="price">$XX.XX</span>
            <button class="btn btn-sm btn-buy">Buy Now</button>
        </div>
    </div>
</div>
```

**Important**: 
- Use `class="pantry-img"` for Pantry products
- Use `class="habitat-img"` for Habitat products
- Price must include the `$` symbol
- Images should be placed in the `Assets/` folder

### Adding/Editing Live Animals

Live animals work slightly differently - they open an inquiry form instead of adding to cart:

1. Open `animals.html` or `index.html`
2. Copy an existing animal card
3. Update the details:

```html
<div class="card glass-panel animal-card" id="BP-2026-XX-XX">
    <div class="badge-verified">Verified Feeder</div>
    <img src="Assets/YOUR_ANIMAL.jpg" alt="Ball Python" class="animal-img">
    <div class="animal-info">
        <h3>Species Name <span class="morph">Morph Name</span></h3>
        <p class="sku">SKU: BP-2026-XX-XX</p>
        <div class="meal-log">
            <p>Last 3 Meals:</p>
            <ul>
                <li>Date - Food Type</li>
                <li>Date - Food Type</li>
                <li>Date - Food Type</li>
            </ul>
        </div>
        <div class="card-footer">
            <span class="price">$XXX.00</span>
            <button class="btn btn-sm btn-buy">Buy Now</button>
        </div>
    </div>
</div>
```

**Note**: Live animals automatically pre-fill the inquiry form with their details when users click "Buy Now".

---

## 2. Email & Form Integration

### Formspree Setup (Owner Notifications)

Formspree receives all customer orders and inquiries and forwards them to your email.

**Current Setup**: Using endpoint `https://formspree.io/f/mjggezoe`

**To Use Your Own Formspree Account**:

1. Go to [formspree.io](https://formspree.io) and create an account
2. Create a new form project
3. Copy your form endpoint (looks like `https://formspree.io/f/xxxxxxx`)
4. Update these files:
   - `index.html` - Line ~267: `<form id="lead-form" action="YOUR_ENDPOINT">`
   - `animals.html` - Update the form action
   - `pantry.html` - Update the form action
   - `habitats.html` - Update the form action
   - `app.js` - Line ~379: Update the fetch URL in `handleCheckoutSubmit()`

**What Formspree Receives**:
- Customer email
- Order items and total
- Payment method selected
- Any additional info (card holder name, etc.)

---

### EmailJS Setup (Customer Confirmations)

EmailJS sends automated confirmation emails to customers after they place an order.

**Current Setup**:
- Public Key: `tjFiVTG59iT5vLlQm`
- Service ID: `service_jshwbap`
- Template ID: `template_8yplknt`

**To Use Your Own EmailJS Account**:

1. Go to [emailjs.com](https://www.emailjs.com/) and create an account
2. **Add Email Service**:
   - Click "Email Services" → "Add New Service"
   - Choose your email provider (Gmail, Outlook, etc.)
   - Connect your email account
   - Copy the **Service ID**
3. **Create Email Template**:
   - Click "Email Templates" → "Create New Template"
   - Design your confirmation email with these variables:
     - `{{to_name}}` - Customer name
     - `{{to_email}}` - Customer email (auto-filled)
     - `{{order_details}}` - Full order summary
     - `{{reply_to}}` - Your business email
   - Example template:
     ```
     Hi {{to_name}},
     
     Thank you for your order at Cold Blooded Heartbeats!
     
     Order Details:
     {{order_details}}
     
     You'll receive payment instructions shortly.
     
     Best regards,
     Cold Blooded Heartbeats Team
     ```
   - Copy the **Template ID**
4. **Get Public Key**:
   - Go to "Account" → "General"
   - Copy your **Public Key**
5. **Update Your Site**:
   - Open `app.js`
   - Find lines 8-12 (the `emailJS` object):
   ```javascript
   emailJS: {
       publicKey: 'YOUR_PUBLIC_KEY',
       serviceID: 'YOUR_SERVICE_ID',
       templateID: 'YOUR_TEMPLATE_ID'
   }
   ```

---

## 3. Payment Method Integration

### E-Transfer (No Setup Required)
E-Transfer works out of the box. Customers receive instructions in their confirmation email. You just need to include your E-Transfer details in your EmailJS template.

### PayPal Integration

**Current Setup**: PayPal is selected as an option but invoices must be sent manually.

**To Enable Automatic PayPal Invoicing** (Future Enhancement):

PayPal requires a business account and API integration. When you're ready:

1. Create a [PayPal Business Account](https://www.paypal.com/business)
2. Get API credentials from PayPal Developer Dashboard
3. You'll need to add server-side code (not supported in static sites)
4. Alternative: Use PayPal's "Payment Buttons" feature:
   - Go to PayPal Business → "Checkout" → "Payments Buttons"
   - Create buttons for your products
   - Replace the checkout flow with PayPal buttons

**For now**: When customers select PayPal, send them a manual invoice using your PayPal account.

---

### Stripe Integration (Credit Card Processing)

**Current Setup**: Card fields are shown but not processed. Customer card details are collected for manual processing.

**To Enable Live Card Processing with Stripe**:

> **⚠️ Important**: Credit card processing requires a server-side component. GitHub Pages only supports static sites (no server). You have two options:

#### Option 1: Use Stripe Checkout (Recommended for Static Sites)

1. Create a [Stripe Account](https://stripe.com)
2. Get your **Publishable Key** and **Secret Key**
3. Use Stripe's hosted checkout page:
   - In `app.js`, modify the Card payment section to redirect to Stripe Checkout
   - Create checkout sessions via Stripe API
   - Requires minimal backend (can use serverless functions)

#### Option 2: Full Stripe Integration (Requires Server)

1. Set up a backend server (Node.js, Python, etc.)
2. Install Stripe SDK
3. Create payment intent on your server
4. Use Stripe.js on the frontend to collect card details securely
5. Process payment on backend using Stripe API

**Recommended Approach for Your Setup**:

Use **Stripe Payment Links**:
1. Go to your Stripe Dashboard
2. Create "Payment Links" for your products
3. When customer selects Card payment, redirect them to the payment link
4. Update `app.js` to generate the appropriate link based on cart contents

**Simple Implementation** (Temporary):
```javascript
// In handleCheckoutSubmit, when payment method is 'Card':
if (paymentMethod === 'Card') {
    // Send order to Formspree, then:
    window.location.href = 'YOUR_STRIPE_PAYMENT_LINK';
}
```

---

## 4. Updating Site Content

### Changing Colors/Styling

All visual styling is in `style.css`. Key color variables are at the top:

```css
:root {
    --clr-slate: #2C3333;    /* Dark background */
    --clr-forest: #1A3C40;   /* Darker accent */
    --clr-sage: #4E6E81;     /* Primary brand color */
    --clr-accent: #E7F6F2;   /* Light text */
}
```

Change these values to update your brand colors site-wide.

### Updating Homepage Text

1. Open `index.html`
2. Find the hero section (~line 122):
```html
<h1>Premium Reptiles.<br><span>Expertly Curated.</span></h1>
<p>Experience artisan genetics and professional husbandry...</p>
```
3. Edit the text directly

### Adding New Pages

1. Duplicate an existing HTML file (e.g., copy `pantry.html`)
2. Rename it (e.g., `care-guides.html`)
3. Update the content inside `<main>` tags
4. Add a navigation link in all HTML files:
```html
<li class="nav-item"><a href="care-guides.html">Care Guides</a></li>
```

---

## 5. Deployment to GitHub Pages

**Initial Setup**:

1. Ensure all files are in the `docs/` folder
2. Push to your GitHub repository
3. Go to GitHub repository → Settings → Pages
4. Source: Deploy from branch `main` → folder `/docs`
5. Save and wait 1-2 minutes

**Updating the Live Site**:

After making changes:
```bash
git add .
git commit -m "Updated products"
git push
```

GitHub Pages automatically rebuilds in ~1-2 minutes.

---

## 6. File Structure Reference

```
ColdBloodedHeartbeats/
├── docs/                    # All website files
│   ├── index.html          # Homepage
│   ├── animals.html        # Live Animals page
│   ├── pantry.html         # The Pantry page
│   ├── habitats.html       # Habitats page
│   ├── style.css           # All styling
│   ├── app.js              # All JavaScript logic
│   └── Assets/             # Images folder
│       └── *.jpg/png       # Product images
├── directives/             # Internal documentation
└── execution/              # Backend scripts (not used on live site)
```

---

## 7. Common Tasks Quick Reference

### Change a Product Price
1. Open the relevant HTML file
2. Find `<span class="price">$XX.XX</span>`
3. Update the price
4. Save and push to GitHub

### Update a Product Image
1. Add new image to `docs/Assets/`
2. Find the product's `<img src="Assets/OLD_IMAGE.jpg">` tag
3. Change to `<img src="Assets/NEW_IMAGE.jpg">`
4. Save and push

### Change Business Email for Forms
1. Update EmailJS template with your email
2. Update `reply_to` in `app.js` line ~401

### Test Changes Locally
1. Open any HTML file directly in your browser
2. Test the functionality
3. When satisfied, push to GitHub for live deployment

---

## 8. Troubleshooting

**Cart not working?**
- Check browser console (F12) for errors
- Ensure `app.js` is loading (check Network tab)

**Forms not sending?**
- Verify Formspree endpoint is correct
- Check EmailJS credentials in `app.js`
- TestEmailJS in their dashboard first

**Images not showing?**
- Check filename matches exactly (case-sensitive)
- Ensure image is in `Assets/` folder
- Try hard refresh (Ctrl+Shift+F5)

**Styling looks broken?**
- Hard refresh to clear cache
- Check `style.css` is loading
- Validate no syntax errors in CSS

---

## 9. Support & Resources

- **Formspree Docs**: https://help.formspree.io/
- **EmailJS Docs**: https://www.emailjs.com/docs/
- **Stripe Docs**: https://stripe.com/docs
- **GitHub Pages**: https://docs.github.com/pages

For code questions, the entire site uses standard HTML, CSS, and vanilla JavaScript - any web developer can help maintain it.

---

**Site Built By**: Halomaster Development  
**Technology Stack**: HTML5, CSS3, Vanilla JavaScript  
**Hosting**: GitHub Pages (Static Site)  
**Form Handling**: Formspree + EmailJS  
**Cart System**: Client-side localStorage
