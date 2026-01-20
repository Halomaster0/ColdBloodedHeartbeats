# Cold Blooded Heartbeats - Handover & Maintenance Guide

Congratulations! Your premium reptile e-commerce platform is ready. This guide covers how to manage your content, connect the lead forms to your email, and deploy the site to the web.

## 1. Connecting Forms to Email
Your website currently logs form submissions to the "console" and `localStorage` for demonstration purposes. To receive these inquiries directly in your inbox, we recommend using a free service like **Formspree.io**.

### Steps:
1.  Go to [Formspree.io](https://formspree.io/) and create a free account.
2.  Create a **New Form** and name it "Cold Blooded Leads".
3.  Copy the **Endpoint URL** provided (e.g., `https://formspree.io/f/xyza...`).
4.  Open `index.html` (and other HTML files) and locate the `<form id="lead-form">` section.
5.  Update the form tag to look like this:
    ```html
    <form id="lead-form" action="https://formspree.io/f/YOUR_ENDPOINT_HERE" method="POST">
    ```
6.  **Repeat** this for the modal forms on `animals.html`, `pantry.html`, and `habitats.html`.
7.  Now, when a user clicks "Submit", Formspree will handle the email delivery to you securely.

---

## 2. Adding Photos & products
Your platform is built on standard HTML/CSS, making it easy to update without complex tools.

### Adding Images:
1.  Save your new image-generated assets (from Nanobanana Pro) into the `Assets/` folder.
2.  Ensure filenames are simple, e.g., `banana_clown.jpg` or `pvc_tank_lg.png`.

### Adding a New Animal Card:
Open `animals.html` and copy an existing product card block:
```html
<div class="card glass-panel animal-card">
    <div class="badge-verified">Verified Feeder</div> <!-- Optional Badge -->
    <img src="Assets/YOUR_NEW_IMAGE.jpg" alt="Description" class="animal-img">
    <div class="animal-info">
        <h3>Species Name <span class="morph">Morph Name</span></h3>
        <p class="sku">SKU: CBH-2026-XX</p>
        <div class="card-footer">
            <span class="price">$XXX.00</span>
            <button class="btn btn-sm btn-buy">Buy Now</button>
        </div>
    </div>
</div>
```
Paste this new block inside the `<div class="grid">` container where you want it to appear.

---

## 3. GitHub Pages Deployment
To share your site with the world for free:

1.  **Repository**: Ensure all your files (`index.html`, `style.css`, `Assets/`, etc.) are committed to your GitHub repository.
2.  **Settings**: Go to your repository on GitHub.com → **Settings**.
3.  **Pages**: Scroll down/click on **Pages** in the sidebar.
4.  **Source**: Under "Build and deployment", select **Deploy from a branch**.
5.  **Branch**: Select `main` (or `master`) and folder `/docs`. Click **Save**.
6.  Wait 1-2 minutes. GitHub will provide a live URL (e.g., `yourusername.github.io/ColdBloodedHeartbeats`).

---

## 4. File Structure
Your project is organized for cleanliness:

- `index.html`: Home page.
- `animals.html` / `pantry.html` / `habitats.html`: Department pages.
- `style.css`: All visual styling, navigation properties, and glass effects.
- `app.js`: Logic for the configurator, modals, and product buttons.
- `Assets/`: Specific folder for all logos and product images. **Always put new images here.**

## 5. Debugging Tips
If something looks "off":
- **Images break?** Check that you put them in `Assets/` and the filename matches exactly (case-sensitive!).
- **Style weirdness?** If you edit `style.css`, you may need to "hard refresh" your browser (Ctrl+Shift+R) to see changes.
