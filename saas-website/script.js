// Global variables
let currentUser = null;

// DOM Content Loaded
document.addEventListener("DOMContentLoaded", function () {
  initializeWebsite();
});

// Initialize website functionality
function initializeWebsite() {
  // Initialize pricing toggle
  initializePricingToggle();

  // Initialize smooth scrolling
  initializeSmoothScrolling();

  // Initialize navbar scroll effect
  initializeNavbarScroll();

  // Initialize demo animations
  initializeDemoAnimations();

  console.log("ChatMongo website initialized successfully!");
}

// Pricing toggle functionality
function initializePricingToggle() {
  const toggle = document.getElementById("pricing-toggle");
  const monthlyPrices = document.querySelectorAll(".amount.monthly");
  const annualPrices = document.querySelectorAll(".amount.annual");

  if (toggle) {
    toggle.addEventListener("change", function () {
      if (this.checked) {
        // Show annual prices
        monthlyPrices.forEach((price) => (price.style.display = "none"));
        annualPrices.forEach((price) => (price.style.display = "inline"));
      } else {
        // Show monthly prices
        monthlyPrices.forEach((price) => (price.style.display = "inline"));
        annualPrices.forEach((price) => (price.style.display = "none"));
      }
    });
  }
}

// Smooth scrolling for navigation links
function initializeSmoothScrolling() {
  document.querySelectorAll('a[href^="#"]').forEach((anchor) => {
    anchor.addEventListener("click", function (e) {
      e.preventDefault();
      const target = document.querySelector(this.getAttribute("href"));
      if (target) {
        target.scrollIntoView({
          behavior: "smooth",
          block: "start",
        });
      }
    });
  });
}

// Navbar scroll effect
function initializeNavbarScroll() {
  const navbar = document.querySelector(".navbar");

  window.addEventListener("scroll", function () {
    if (window.scrollY > 100) {
      navbar.style.background = "rgba(255, 255, 255, 0.98)";
      navbar.style.boxShadow = "0 2px 20px rgba(0, 0, 0, 0.1)";
    } else {
      navbar.style.background = "rgba(255, 255, 255, 0.95)";
      navbar.style.boxShadow = "none";
    }
  });
}

// Demo animations
function initializeDemoAnimations() {
  // Animate demo chat widget
  const demoChatBubble = document.querySelector(".demo-chat-bubble");
  const demoChatWindow = document.querySelector(".demo-chat-window");

  if (demoChatBubble && demoChatWindow) {
    // Auto-open demo chat after 3 seconds
    setTimeout(() => {
      demoChatWindow.style.display = "block";
      demoChatWindow.style.animation = "slideUp 0.5s ease-out forwards";
    }, 3000);

    // Click to toggle demo chat
    demoChatBubble.addEventListener("click", function () {
      if (
        demoChatWindow.style.display === "none" ||
        !demoChatWindow.style.display
      ) {
        demoChatWindow.style.display = "block";
        demoChatWindow.style.animation = "slideUp 0.5s ease-out forwards";
      } else {
        demoChatWindow.style.animation = "slideDown 0.5s ease-out forwards";
        setTimeout(() => {
          demoChatWindow.style.display = "none";
        }, 500);
      }
    });
  }
}

// Mobile menu toggle
function toggleMobileMenu() {
  const navMenu = document.querySelector(".nav-menu");
  const navToggle = document.querySelector(".nav-toggle");

  navMenu.classList.toggle("active");
  navToggle.classList.toggle("active");
}

// Scroll to demo section
function scrollToDemo() {
  const demoSection = document.getElementById("demo");
  if (demoSection) {
    demoSection.scrollIntoView({
      behavior: "smooth",
      block: "start",
    });
  }
}

// Modal functionality
function openSignupModal() {
  const modal = document.getElementById("signup-modal");
  if (modal) {
    modal.style.display = "block";
    document.body.style.overflow = "hidden";
  }
}

function closeSignupModal() {
  const modal = document.getElementById("signup-modal");
  if (modal) {
    modal.style.display = "none";
    document.body.style.overflow = "auto";
  }
}

function openWidgetModal() {
  const modal = document.getElementById("widget-modal");
  if (modal) {
    modal.style.display = "block";
    document.body.style.overflow = "hidden";
  }
}

function closeWidgetModal() {
  const modal = document.getElementById("widget-modal");
  if (modal) {
    modal.style.display = "none";
    document.body.style.overflow = "auto";
  }
}

// Handle signup form submission
function handleSignup(event) {
  event.preventDefault();

  const email = document.getElementById("email").value;
  const company = document.getElementById("company").value;
  const industry = document.getElementById("industry").value;
  const useCase = document.getElementById("use-case").value;

  // Generate unique bot ID (in real app, this would be from your backend)
  const botId = generateBotId();

  // Store user data (in real app, this would be sent to your backend)
  currentUser = {
    email,
    company,
    industry,
    useCase,
    botId,
    plan: "starter",
    createdAt: new Date().toISOString(),
  };

  // Show success message
  showSignupSuccess(currentUser);

  // Track signup event
  trackEvent("signup", {
    email,
    company,
    industry,
    useCase,
  });
}

// Generate unique bot ID
function generateBotId() {
  return "bot_" + Math.random().toString(36).substr(2, 16);
}

// Show signup success
function showSignupSuccess(user) {
  closeSignupModal();

  // Create success modal
  const successModal = document.createElement("div");
  successModal.className = "modal";
  successModal.style.display = "block";
  successModal.innerHTML = `
    <div class="modal-content">
      <div class="modal-header">
        <h3>🎉 Welcome to SmartChat AI!</h3>
        <button class="modal-close" onclick="this.parentElement.parentElement.parentElement.remove(); document.body.style.overflow='auto';">&times;</button>
      </div>
      <div class="modal-body">
        <div style="text-align: center; margin-bottom: 2rem;">
          <div style="font-size: 4rem; margin-bottom: 1rem;">🤖</div>
          <h4 style="margin-bottom: 1rem;">Your AI Chatbot is Being Created!</h4>
          <p style="color: #6b7280; margin-bottom: 2rem;">
            We're setting up your personalized chatbot for <strong>${user.company}</strong> in the <strong>${user.industry}</strong> industry.
          </p>
        </div>
        
        <div style="background: #f9fafb; padding: 1.5rem; border-radius: 12px; margin-bottom: 2rem;">
          <h5 style="margin-bottom: 1rem;">Next Steps:</h5>
          <ol style="margin-left: 1rem; color: #6b7280;">
            <li style="margin-bottom: 0.5rem;">Check your email for login credentials</li>
            <li style="margin-bottom: 0.5rem;">Upload your documents and data</li>
            <li style="margin-bottom: 0.5rem;">Customize your chatbot's appearance</li>
            <li>Deploy to your website with one line of code</li>
          </ol>
        </div>
        
        <div style="text-align: center;">
          <button class="btn btn-primary" onclick="openDashboard('${user.botId}')">
            Go to Dashboard
          </button>
        </div>
      </div>
    </div>
  `;

  document.body.appendChild(successModal);
  document.body.style.overflow = "hidden";
}

// Generate widget embed code
function generateWidgetCode(widgetKey, website) {
  const domain =
    window.location.hostname === "localhost"
      ? "http://localhost:3000"
      : "https://cdn.chatmongo.com";

  return `<script 
  src="${domain}/widget.js"
  data-key="${widgetKey}"
  data-website="${website}">
</script>`;
}

// Copy widget code to clipboard
function copyWidgetCode() {
  const codeElement = document.getElementById("widget-code");
  const code = codeElement.textContent;

  navigator.clipboard
    .writeText(code)
    .then(() => {
      const copyBtn = document.querySelector(".copy-btn");
      const originalText = copyBtn.textContent;

      copyBtn.textContent = "Copied!";
      copyBtn.style.background = "#28a745";

      setTimeout(() => {
        copyBtn.textContent = originalText;
        copyBtn.style.background = "#00A86B";
      }, 2000);

      // Track copy event
      trackEvent("widget_code_copied", {
        widgetKey: currentUser?.widgetKey,
      });
    })
    .catch((err) => {
      console.error("Failed to copy code:", err);

      // Fallback: select text
      const range = document.createRange();
      range.selectNode(codeElement);
      window.getSelection().removeAllRanges();
      window.getSelection().addRange(range);
    });
}

// Open dashboard (placeholder)
function openDashboard(botId) {
  // In a real app, this would redirect to the user dashboard
  alert(
    `Dashboard for Bot ID: ${
      botId || "new"
    }\n\nYou'll be able to:\n\n• Upload and manage your data\n• Train your AI chatbot\n• Customize appearance and behavior\n• View conversation analytics\n• Generate embed codes\n• Manage billing and settings`
  );

  // Track dashboard click
  trackEvent("dashboard_clicked", {
    botId: botId || currentUser?.botId,
  });
}

// Plan selection
function selectPlan(planName) {
  if (planName === "starter") {
    openSignupModal();
  } else if (planName === "professional") {
    // In real app, this would start the checkout process
    alert(
      "Professional Plan Selected!\n\nFeatures:\n• 5 chatbots\n• 10,000 conversations/month\n• 500MB data upload\n• 50+ languages\n• Full customization\n• Analytics dashboard\n• API access\n• Priority support\n\nCheckout coming soon!"
    );
  } else if (planName === "enterprise") {
    // In real app, this would open contact form
    alert(
      "Enterprise Plan Selected!\n\nOur sales team will contact you within 24 hours to discuss:\n• Unlimited chatbots and conversations\n• White-label solutions\n• Custom integrations\n• Dedicated support\n• SLA guarantees\n• On-premise deployment options"
    );
  }

  // Track plan selection
  trackEvent("plan_selected", {
    plan: planName,
  });
}

// Event tracking (placeholder for analytics)
function trackEvent(eventName, properties = {}) {
  console.log("Event tracked:", eventName, properties);

  // In a real app, you would send this to your analytics service
  // Example: analytics.track(eventName, properties);
}

// Close modals when clicking outside
window.addEventListener("click", function (event) {
  const signupModal = document.getElementById("signup-modal");
  const widgetModal = document.getElementById("widget-modal");

  if (event.target === signupModal) {
    closeSignupModal();
  }

  if (event.target === widgetModal) {
    closeWidgetModal();
  }
});

// Keyboard shortcuts
document.addEventListener("keydown", function (event) {
  // Close modals with Escape key
  if (event.key === "Escape") {
    closeSignupModal();
    closeWidgetModal();
  }

  // Open signup with Ctrl/Cmd + K
  if ((event.ctrlKey || event.metaKey) && event.key === "k") {
    event.preventDefault();
    openSignupModal();
  }
});

// Intersection Observer for animations
const observerOptions = {
  threshold: 0.1,
  rootMargin: "0px 0px -50px 0px",
};

const observer = new IntersectionObserver((entries) => {
  entries.forEach((entry) => {
    if (entry.isIntersecting) {
      entry.target.style.opacity = "1";
      entry.target.style.transform = "translateY(0)";
    }
  });
}, observerOptions);

// Observe elements for scroll animations
document.addEventListener("DOMContentLoaded", function () {
  const animatedElements = document.querySelectorAll(
    ".feature-card, .step, .pricing-card"
  );

  animatedElements.forEach((el) => {
    el.style.opacity = "0";
    el.style.transform = "translateY(30px)";
    el.style.transition = "opacity 0.6s ease, transform 0.6s ease";
    observer.observe(el);
  });
});

// Performance monitoring
window.addEventListener("load", function () {
  // Track page load time
  const loadTime =
    performance.timing.loadEventEnd - performance.timing.navigationStart;

  trackEvent("page_loaded", {
    loadTime: loadTime,
    userAgent: navigator.userAgent,
    viewport: {
      width: window.innerWidth,
      height: window.innerHeight,
    },
  });
});

// Error handling
window.addEventListener("error", function (event) {
  console.error("JavaScript error:", event.error);

  trackEvent("javascript_error", {
    message: event.message,
    filename: event.filename,
    lineno: event.lineno,
    colno: event.colno,
  });
});

// Service worker registration (for PWA features)
if ("serviceWorker" in navigator) {
  window.addEventListener("load", function () {
    navigator.serviceWorker
      .register("/sw.js")
      .then(function (registration) {
        console.log("ServiceWorker registration successful");
      })
      .catch(function (err) {
        console.log("ServiceWorker registration failed");
      });
  });
}
