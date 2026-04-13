// Inject shared footer into all pages
const footerHTML = `
<footer>
  <div class="footer-top">
    <div>
      <p class="footer-tagline">ENTER THE<br>BLVCKOUT.</p>
      <div class="footer-newsletter">
        <input type="email" placeholder="Your Email Here" />
        <button>Subscribe</button>
      </div>
      <p class="footer-newsletter-note">Subscribe to our newsletter for the latest features and updates.</p>
    </div>
    <div class="footer-col">
      <h4>Shop</h4>
      <ul>
        <li><a href="collections.html">Women</a></li>
        <li><a href="collections.html">Men</a></li>
        <li><a href="collections.html">Unisex</a></li>
        <li><a href="custom.html">Custom</a></li>
      </ul>
    </div>
    <div class="footer-col">
      <h4>Contact</h4>
      <ul>
        <li><a href="#footer-newsletter">Join Us</a></li>
        <li><a href="contact.html#ticketForm">Contact Us</a></li>
        <li><a href="policies.html">Terms &amp; Conditions</a></li>
      </ul>
    </div>
    <div class="footer-col">
      <h4>Follow Us</h4>
      <div class="footer-social">
        <div class="footer-social-item">
          <span class="footer-social-icon">✕</span> Instagram
        </div>
        <div class="footer-social-item">
          <span class="footer-social-icon">𝕏</span> X
        </div>
        <div class="footer-social-item">
          <span class="footer-social-icon">▶</span> YouTube
        </div>
      </div>
    </div>
  </div>
  <div class="footer-bottom">
    <span>© 2026 BLVKOUT. All rights reserved.</span>
    <span><a href="policies.html" style="color:inherit;">Privacy Policy</a> · <a href="policies.html" style="color:inherit;">Terms of Service</a></span>
  </div>
  <div class="footer-watermark">BLV.K</div>
</footer>
`;

document.querySelectorAll('footer').forEach(f => f.outerHTML = footerHTML);
