import json

with open('extracted_scripts.txt', 'r', encoding='utf-8') as f:
    scripts = f.read()

html = """<!doctype html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Dashboard - Qunix</title>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet" />
  <script src="https://unpkg.com/lucide@latest"></script>
  <style>
    :root {
      --background: 0 0% 100%;
      --foreground: 240 10% 3.9%;
      --muted: 240 4.8% 95.9%;
      --muted-foreground: 240 3.8% 46.1%;
      --border: 240 5.9% 90%;
      --primary: 240 5.9% 10%;
      --primary-foreground: 0 0% 98%;
      --radius: 0.5rem;
    }
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body { font-family: 'Inter', sans-serif; background-color: hsl(var(--background)); color: hsl(var(--foreground)); -webkit-font-smoothing: antialiased; }

    /* Layout */
    .app-layout { display: flex; height: 100vh; overflow: hidden; }
    .sidebar { width: 250px; border-right: 1px solid hsl(var(--border)); display: flex; flex-direction: column; background: hsl(var(--background)); }
    .sidebar-header { height: 4rem; display: flex; align-items: center; padding: 0 1.5rem; border-bottom: 1px solid hsl(var(--border)); font-weight: 600; font-size: 1.125rem; gap: 0.5rem; }
    .sidebar-nav { flex: 1; padding: 1.5rem 1rem; display: flex; flex-direction: column; gap: 0.5rem; }
    .sidebar-link { display: flex; align-items: center; gap: 0.75rem; padding: 0.5rem 0.75rem; border-radius: var(--radius); font-size: 0.875rem; font-weight: 500; color: hsl(var(--muted-foreground)); transition: 0.2s; cursor: pointer; text-decoration: none; }
    .sidebar-link.active { background-color: hsl(var(--muted)); color: hsl(var(--foreground)); }
    .sidebar-link:hover { background-color: hsl(var(--muted)); color: hsl(var(--foreground)); }
    
    .sidebar-footer { padding: 1.5rem 1rem; border-top: 1px solid hsl(var(--border)); }

    .main-content { flex: 1; display: flex; flex-direction: column; overflow: hidden; background: #fafafa; }
    .top-header { height: 4rem; display: flex; align-items: center; justify-content: flex-end; padding: 0 2rem; border-bottom: 1px solid hsl(var(--border)); background: hsl(var(--background)); }
    .scroll-area { flex: 1; overflow-y: auto; padding: 2rem; }
    .max-w-6xl { max-width: 1152px; margin: 0 auto; }

    /* Typography & Utilities */
    .text-sm { font-size: 0.875rem; }
    .text-lg { font-size: 1.125rem; }
    .text-2xl { font-size: 1.5rem; line-height: 2rem; }
    .text-3xl { font-size: 1.875rem; line-height: 2.25rem; }
    .text-muted { color: hsl(var(--muted-foreground)); }
    .font-semibold { font-weight: 600; }
    .font-medium { font-weight: 500; }
    .mb-2 { margin-bottom: 0.5rem; }
    .mb-4 { margin-bottom: 1rem; }
    .mb-6 { margin-bottom: 1.5rem; }
    .mb-8 { margin-bottom: 2rem; }
    .flex { display: flex; }
    .items-center { align-items: center; }
    .justify-between { justify-content: space-between; }
    .gap-2 { gap: 0.5rem; }
    .gap-4 { gap: 1rem; }
    .gap-6 { gap: 1.5rem; }
    .grid { display: grid; }
    .grid-4 { grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); }
    
    /* Components */
    .btn { display: inline-flex; align-items: center; justify-content: center; gap: 0.5rem; border-radius: var(--radius); font-size: 0.875rem; font-weight: 500; height: 2.5rem; padding: 0 1rem; border: none; cursor: pointer; transition: 0.2s; text-decoration: none; }
    .btn-primary { background-color: hsl(var(--primary)); color: hsl(var(--primary-foreground)); }
    .btn-primary:hover { opacity: 0.9; }
    .btn-primary:disabled { opacity: 0.5; cursor: not-allowed; }
    .btn-secondary { background-color: transparent; border: 1px solid hsl(var(--border)); color: hsl(var(--foreground)); }
    .btn-secondary:hover:not(:disabled) { background-color: hsl(var(--muted)); }
    
    .card { background: hsl(var(--background)); border: 1px solid hsl(var(--border)); border-radius: calc(var(--radius) + 2px); padding: 1.5rem; box-shadow: 0 1px 2px rgba(0,0,0,0.05); }
    .card-header { margin-bottom: 1rem; padding-bottom: 1rem; border-bottom: 1px solid hsl(var(--border)); display: flex; justify-content: space-between; align-items: center; }
    .card-title { font-weight: 600; font-size: 1rem; }

    /* Modal */
    .modal { position: fixed; top: 0; left: 0; right: 0; bottom: 0; background-color: rgba(0,0,0,0.4); display: none; align-items: center; justify-content: center; z-index: 100; backdrop-filter: blur(4px); }
    .modal-content { background: hsl(var(--background)); width: 100%; max-width: 800px; max-height: 90vh; overflow-y: auto; border-radius: calc(var(--radius) + 4px); box-shadow: 0 10px 15px -3px rgba(0,0,0,0.1); border: 1px solid hsl(var(--border)); }
    .modal-header { padding: 1.5rem; border-bottom: 1px solid hsl(var(--border)); display: flex; justify-content: space-between; align-items: center; position: sticky; top: 0; background: hsl(var(--background)); z-index: 10; }
    .modal-body { padding: 2rem; }
    .modal-close { background: none; border: none; cursor: pointer; color: hsl(var(--muted-foreground)); }
    .modal-close:hover { color: hsl(var(--foreground)); }
    
    /* Wizard Steps */
    .step-header { text-align: center; margin-bottom: 2rem; }
    .step-actions { display: flex; justify-content: space-between; margin-top: 2rem; border-top: 1px solid hsl(var(--border)); padding-top: 1.5rem; }
    
    .upload-area { border: 2px dashed hsl(var(--border)); border-radius: var(--radius); padding: 3rem 2rem; text-align: center; cursor: pointer; transition: 0.2s; background: hsl(var(--background)); }
    .upload-area:hover { border-color: hsl(var(--primary)); background: #fafafa; }
    
    .progress-bar { width: 100%; height: 6px; background: hsl(var(--muted)); border-radius: 3px; overflow: hidden; margin: 1rem 0; }
    .progress-fill { height: 100%; background: hsl(var(--primary)); width: 0%; transition: width 0.3s; }
    
    /* Config layout */
    .config-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 2rem; }
    .form-group { margin-bottom: 1.5rem; }
    .label { display: block; font-size: 0.875rem; font-weight: 500; margin-bottom: 0.5rem; }
    .input { display: flex; height: 2.5rem; width: 100%; border-radius: var(--radius); border: 1px solid hsl(var(--border)); background: transparent; padding: 0 0.75rem; font-size: 0.875rem; }
    .input:focus { outline: none; border-color: hsl(var(--primary)); box-shadow: 0 0 0 1px hsl(var(--primary)); }
    
    /* Config Preview */
    .preview-box { border: 1px solid hsl(var(--border)); border-radius: var(--radius); background: #fafafa; height: 400px; position: relative; overflow: hidden; display: flex; align-items: center; justify-content: center; }
    
    .bubble-preview { position: absolute; display: flex; align-items: center; justify-content: center; cursor: pointer; transition: 0.2s; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
    .bubble-preview.size-small { width: 50px; height: 50px; border-radius: 25px; }
    .bubble-preview.size-medium { width: 60px; height: 60px; border-radius: 30px; }
    .bubble-preview.size-large { width: 70px; height: 70px; border-radius: 35px; }
    .bubble-preview.position-bottom-right { bottom: 20px; right: 20px; }
    .bubble-preview.position-bottom-left { bottom: 20px; left: 20px; }
    .bubble-preview.position-top-right { top: 20px; right: 20px; }
    .bubble-preview.position-top-left { top: 20px; left: 20px; }
    
    /* Chat Widget Preview */
    .chat-widget-preview { width: 300px; height: 420px; border-radius: calc(var(--radius) + 4px); box-shadow: 0 10px 25px rgba(0,0,0,0.1); overflow: hidden; display: flex; flex-direction: column; border: 1px solid hsl(var(--border)); background: hsl(var(--background)); }
    .chat-header-preview { padding: 0.75rem 1rem; color: white; display: flex; justify-content: space-between; align-items: center; font-size: 0.875rem; font-weight: 500; }
    .chat-messages-preview { flex: 1; padding: 1rem; overflow-y: auto; background: #fafafa; display: flex; flex-direction: column; gap: 0.75rem; }
    .msg-bot, .msg-user { max-width: 85%; font-size: 0.875rem; padding: 0.6rem 0.8rem; line-height: 1.4; border-radius: var(--radius); box-shadow: 0 1px 2px rgba(0,0,0,0.05); }
    .msg-bot { background: white; align-self: flex-start; border: 1px solid hsl(var(--border)); }
    .msg-user { background: hsl(var(--primary)); color: white; align-self: flex-end; }
    .msg-bot.style-square, .msg-user.style-square { border-radius: 0; }
    .msg-bot.style-minimal { background: transparent; border: none; border-left: 2px solid hsl(var(--primary)); border-radius: 0; box-shadow: none; padding-left: 1rem; }
    .msg-user.style-minimal { background: transparent; color: hsl(var(--foreground)); border: none; border-right: 2px solid hsl(var(--primary)); border-radius: 0; box-shadow: none; padding-right: 1rem; text-align: right; }
    
    .chat-input-preview-box { padding: 0.75rem; border-top: 1px solid hsl(var(--border)); background: background; display: flex; gap: 0.5rem; align-items: center; }
    
    .chat-widget-preview.theme-dark { background: #09090b; border-color: #27272a; }
    .chat-widget-preview.theme-dark .chat-messages-preview { background: #121212; }
    .chat-widget-preview.theme-dark .msg-bot { background: #27272a; border-color: #27272a; color: #fff; }
    .chat-widget-preview.theme-dark .chat-input-preview-box { border-color: #27272a; background: #09090b; }
    
    /* Code bloc */
    pre { background: hsl(var(--primary)); color: hsl(var(--muted)); padding: 1rem; border-radius: var(--radius); overflow-x: auto; font-family: monospace; font-size: 0.875rem; }
  </style>
</head>
<body>
  
  <div class="app-layout">
    <!-- Sidebar -->
    <aside class="sidebar">
      <div class="sidebar-header">
        <i data-lucide="brain-circuit"></i> Qunix
      </div>
      <nav class="sidebar-nav">
        <a class="sidebar-link active" href="#"><i data-lucide="layout-dashboard"></i> Dashboard</a>
        <a class="sidebar-link" href="#" onclick="viewDocumentation()"><i data-lucide="book-open"></i> Documentation</a>
        <a class="sidebar-link" href="#" onclick="viewExamples()"><i data-lucide="images"></i> Examples</a>
        <a class="sidebar-link" href="#" onclick="contactSupport()"><i data-lucide="headphones"></i> Support</a>
      </nav>
      <div class="sidebar-footer">
        <button class="btn btn-secondary" style="width: 100%; justify-content: flex-start" onclick="openSettings()">
          <i data-lucide="settings"></i> Settings
        </button>
      </div>
    </aside>

    <!-- Main Content -->
    <main class="main-content">
      <header class="top-header">
        <div class="flex items-center gap-4">
          <span class="text-sm font-medium" id="user-email">Loading...</span>
          <button class="btn btn-secondary" style="height: 2rem; padding: 0 0.5rem;" onclick="logout()">
            <i data-lucide="log-out" width="16" height="16"></i> Logout
          </button>
        </div>
      </header>

      <div class="scroll-area flex-1">
        <div class="max-w-6xl">
          
          <div id="loading-screen" class="text-center" style="padding: 4rem 0;">
            <i data-lucide="loader-2" class="lucide-spin" width="32" height="32" style="margin: 0 auto; animation: spin 1s linear infinite;"></i>
            <h2 class="text-xl mt-4 font-semibold">Loading dashboard...</h2>
          </div>

          <div id="dashboard-content" style="display: none;">
            <div class="mb-8">
              <h1 class="text-3xl font-semibold mb-2">Dashboard</h1>
              <p class="text-muted">Welcome back to your Qunix Smart Support console.</p>
            </div>

            <!-- Stats Grid -->
            <div class="grid grid-4 gap-6 mb-8">
              <div class="card">
                <p class="text-sm text-muted mb-2 font-medium">Messages Used</p>
                <div class="text-3xl font-semibold" id="message-count">0</div>
              </div>
              <div class="card">
                <p class="text-sm text-muted mb-2 font-medium">Active Widgets</p>
                <div class="text-3xl font-semibold" id="widget-count">0</div>
              </div>
              <div class="card">
                <p class="text-sm text-muted mb-2 font-medium">Messages</p>
                <div class="text-3xl font-semibold" id="messages-remaining">100%</div>
              </div>
              <div class="card">
                <p class="text-sm text-muted mb-2 font-medium">Days Active</p>
                <div class="text-3xl font-semibold" id="days-active">0</div>
              </div>
            </div>

            <!-- 2 Col Layout -->
            <div style="display: grid; grid-template-columns: 2fr 1fr; gap: 1.5rem;">
              <div class="card">
                <div class="card-header">
                  <h3 class="card-title">Your Chatbot Widget</h3>
                </div>
                <div id="widget-section">
                  <!-- Dynamically populated -->
                </div>
              </div>

              <div class="card">
                <div class="card-header">
                  <h3 class="card-title">Quick Actions</h3>
                </div>
                <div id="quick-actions" class="flex" style="flex-direction: column; gap: 0.5rem;">
                  <!-- Dynamically populated -->
                </div>
              </div>
            </div>
          </div>

        </div>
      </div>
    </main>
  </div>

  <!-- Wizard Modal -->
  <div class="modal" id="widget-creation-modal">
    <div class="modal-content">
      <div class="modal-header">
        <h3 id="modal-title" class="font-semibold text-lg">Create Your Chatbot</h3>
        <button class="modal-close" onclick="closeWidgetModal()"><i data-lucide="x"></i></button>
      </div>
      <div class="modal-body">
        
        <!-- Step 1 Upload -->
        <div id="step-upload">
          <div class="step-header">
            <h4 class="text-xl font-semibold mb-2">Upload Your Documents</h4>
            <p class="text-muted text-sm">Upload PDF files that your chatbot will use to answer questions.</p>
          </div>
          
          <div class="upload-area mb-6" id="pdf-upload-area" onclick="document.getElementById('pdf-file-input').click()">
            <i data-lucide="file-up" width="32" height="32" class="mb-2" style="margin: 0 auto; color: hsl(var(--muted-foreground));"></i>
            <p class="font-medium text-sm">Drag & drop your PDF files here</p>
            <p class="text-muted text-xs mt-1">or click to browse</p>
            <input type="file" id="pdf-file-input" accept=".pdf" multiple style="display: none" />
          </div>

          <div id="file-list" style="display: none;" class="mb-6">
            <h5 class="text-sm font-semibold mb-2">Selected Files</h5>
            <div id="files-container" class="flex" style="flex-direction: column; gap: 0.5rem;"></div>
          </div>

          <div id="upload-progress" style="display: none;" class="mb-6 card bg-slate-50">
            <div class="flex justify-between text-sm font-medium mb-1">
              <span id="progress-status">Uploading...</span>
            </div>
            <div class="progress-bar">
              <div class="progress-fill" id="progress-fill"></div>
            </div>
            <p class="text-xs text-muted" id="progress-details">Extracting text...</p>
          </div>

          <div class="step-actions">
            <button class="btn btn-secondary" onclick="closeWidgetModal()">Cancel</button>
            <button class="btn btn-primary" id="upload-next-btn" onclick="processDocuments()" disabled>Process Documents</button>
          </div>
        </div>

        <!-- Step 2 Processing Complete -->
        <div id="step-processing-complete" style="display: none;">
          <div class="step-header">
            <div style="display: flex; justify-content: center; margin-bottom: 1rem;"><i data-lucide="check-circle-2" width="48" height="48" style="color: hsl(var(--primary));"></i></div>
            <h4 class="text-xl font-semibold mb-2">Embedding Generated Successfully</h4>
            <p class="text-muted text-sm">Your documents have been processed and converted into AI-readable format.</p>
          </div>

          <div class="card mb-6" id="processing-summary"></div>
          
          <div class="grid grid-4 gap-4 mb-6">
            <div class="card p-4">
              <h5 class="font-semibold text-sm mb-1">Vector DB</h5>
              <p class="text-xs text-muted">Stored as high-dimensional vectors</p>
            </div>
            <div class="card p-4">
              <h5 class="font-semibold text-sm mb-1">AI Model</h5>
              <p class="text-xs text-muted">Configured for your content</p>
            </div>
          </div>

          <div class="step-actions">
            <button class="btn btn-secondary" onclick="closeWidgetModal()">Cancel</button>
            <button class="btn btn-primary" onclick="goToCustomization()">Customize Chat Bubble <i data-lucide="arrow-right" width="16" height="16"></i></button>
          </div>
        </div>

        <!-- Step 3 Bubble Customization -->
        <div id="step-bubble-customization" style="display: none;">
          <div class="step-header">
            <h4 class="text-xl font-semibold mb-2">Customize Chat Bubble</h4>
            <p class="text-muted text-sm">Design how your chat bubble appears on your website.</p>
          </div>

          <div class="config-grid">
            <div>
              <div class="form-group">
                <label class="label">Bubble Color</label>
                <div class="flex gap-2">
                  <input type="color" id="bubble-color" value="#09090b" class="input" style="padding: 0; width: 40px;" oninput="updateBubblePreview()" />
                  <input type="text" id="bubble-color-text" value="#09090b" class="input" oninput="updateBubbleColorFromText()" />
                </div>
              </div>

              <div class="form-group">
                <label class="label">Icon</label>
                <select id="bubble-icon" class="input" onchange="updateBubblePreview()">
                  <option value="💬">💬 Chat</option>
                  <option value="🤖">🤖 Robot</option>
                  <option value="💡">💡 Help</option>
                  <option value="●">● Minimal</option>
                </select>
              </div>

              <div class="form-group">
                <label class="label">Position</label>
                <select id="bubble-position" class="input" onchange="updateBubblePreview()">
                  <option value="bottom-right">Bottom Right</option>
                  <option value="bottom-left">Bottom Left</option>
                  <option value="top-right">Top Right</option>
                  <option value="top-left">Top Left</option>
                </select>
              </div>

              <div class="form-group">
                <label class="label">Size</label>
                <select id="bubble-size" class="input" onchange="updateBubblePreview()">
                  <option value="small">Small (50px)</option>
                  <option value="medium" selected>Medium (60px)</option>
                  <option value="large">Large (70px)</option>
                </select>
              </div>

              <div class="form-group">
                <label class="label">Hover Tooltip</label>
                <input type="text" id="bubble-text" class="input" value="Chat with us!" oninput="updateBubblePreview()"/>
              </div>

              <div class="flex gap-4">
                <label class="flex items-center gap-2 text-sm"><input type="checkbox" id="bubble-pulse" checked onchange="updateBubblePreview()"> Pulse</label>
                <label class="flex items-center gap-2 text-sm"><input type="checkbox" id="bubble-shadow" checked onchange="updateBubblePreview()"> Shadow</label>
              </div>
            </div>

            <div>
              <div class="preview-box" id="bubble-preview-wrapper">
                <div class="bubble-preview" id="chat-bubble-preview">
                  <span id="bubble-icon-preview">💬</span>
                </div>
                <div id="bubble-tooltip" style="display:none;"></div>
              </div>
            </div>
          </div>

          <div class="step-actions">
            <button class="btn btn-secondary" onclick="goBackToProcessing()"><i data-lucide="arrow-left" width="16" height="16"></i> Back</button>
            <button class="btn btn-primary" onclick="goToChatCustomization()">Customize Window <i data-lucide="arrow-right" width="16" height="16"></i></button>
          </div>
        </div>

        <!-- Step 4 Chat Interface -->
        <div id="step-chat-customization" style="display: none;">
          <div class="step-header">
            <h4 class="text-xl font-semibold mb-2">Customize Chat Window</h4>
            <p class="text-muted text-sm">Design the chat window that opens when users click.</p>
          </div>

          <div class="config-grid">
            <div>
              <div class="form-group">
                <label class="label">Window Title</label>
                <input type="text" id="chat-title" class="input" value="AI Assistant" oninput="updateChatPreview()" />
              </div>
              <div class="form-group">
                <label class="label">Welcome Message</label>
                <textarea id="welcome-message" class="input" style="height: auto; padding: 0.5rem 0.75rem" rows="3" oninput="updateChatPreview()">Hello! How can I help you today?</textarea>
              </div>
              <div class="form-group">
                <label class="label">Header Color</label>
                <div class="flex gap-2">
                  <input type="color" id="header-color" value="#09090b" class="input" style="padding: 0; width: 40px;" oninput="updateChatPreview()" />
                  <input type="text" id="header-color-text" value="#09090b" class="input" oninput="updateHeaderColorFromText()" />
                </div>
              </div>
              <div class="form-group">
                <label class="label">Theme</label>
                <select id="chat-theme" class="input" onchange="updateChatPreview()">
                  <option value="light">Light</option>
                  <option value="dark">Dark</option>
                </select>
              </div>
              <div class="form-group">
                <label class="label">Message Style</label>
                <select id="message-style" class="input" onchange="updateChatPreview()">
                  <option value="rounded">Rounded</option>
                  <option value="square">Square</option>
                  <option value="minimal">Minimal</option>
                </select>
              </div>
              <label class="flex items-center gap-2 text-sm"><input type="checkbox" id="show-branding" checked onchange="updateChatPreview()"> Show branding</label>
            </div>

            <div class="flex items-center justify-center">
              <div id="chat-preview-wrapper" class="preview-box" style="padding: 1rem; height: 100%; width: 100%; border:none; background: transparent;">
                <div class="chat-widget-preview" id="chat-widget-preview">
                  <div class="chat-header-preview" id="chat-header-preview">
                    <span id="chat-title-preview">AI Assistant</span>
                    <i data-lucide="x" width="16" height="16"></i>
                  </div>
                  <div class="chat-messages-preview" id="chat-messages-preview">
                    <div class="msg-bot" id="welcome-message-preview">Hello! How can I help you today?</div>
                    <div class="msg-user">Can you help me with pricing?</div>
                    <div class="msg-bot">I'd be happy to help you with pricing information! Let me find that for you.</div>
                  </div>
                  <div class="chat-input-preview-box" id="chat-input-container">
                    <input type="text" class="input" style="height: 2rem;" id="chat-input" placeholder="Type a message..." disabled />
                    <button id="chat-send-preview" class="btn btn-primary" style="height: 2rem; width: 2rem; padding: 0; border-radius: 50%;"><i data-lucide="arrow-right" width="14" height="14"></i></button>
                  </div>
                  <div id="chat-branding-preview" style="text-align: center; font-size: 0.65rem; padding: 0.25rem; border-top: 1px solid var(--border);">
                    Powered by Qunix
                  </div>
                </div>
              </div>
            </div>
          </div>

          <div class="step-actions">
            <button class="btn btn-secondary" onclick="goBackToBubbleCustomization()"><i data-lucide="arrow-left" width="16" height="16"></i> Back</button>
            <button class="btn btn-primary" onclick="goToEmbedCodeStep()">Generate Embed Code <i data-lucide="arrow-right" width="16" height="16"></i></button>
          </div>
        </div>

        <!-- Step 5 Embed Code -->
        <div id="step-embed-code" style="display: none;">
          <div class="step-header">
            <div style="display: flex; justify-content: center; margin-bottom: 1rem;"><i data-lucide="code-2" width="48" height="48" style="color: hsl(var(--primary));"></i></div>
            <h4 class="text-xl font-semibold mb-2">Your Chatbot is Ready!</h4>
            <p class="text-muted text-sm">Copy the embed code and paste it into your website.</p>
          </div>

          <div class="card mb-6 bg-slate-50">
            <div class="flex justify-between border-b pb-2 mb-2 text-sm">
              <span class="text-muted">Widget ID:</span> <span class="font-medium font-mono" id="widget-id-display">Loading...</span>
            </div>
            <div class="flex justify-between border-b pb-2 mb-2 text-sm">
              <span class="text-muted">Status:</span> <span class="font-medium text-green-600">Active</span>
            </div>
            <div class="flex justify-between text-sm">
              <span class="text-muted">API Endpoint:</span> <span class="font-medium font-mono">http://localhost:8001</span>
            </div>
          </div>

          <div class="mb-6 relative" id="embed-code-content">
            <button class="btn btn-secondary" id="copy-btn" onclick="copyEmbedCode()" style="position: absolute; top: 0.5rem; right: 0.5rem; height: 2rem; font-size: 0.75rem;"><i data-lucide="copy" width="14" height="14"></i> Copy</button>
            <pre><code style="white-space: pre-wrap;"></code></pre>
          </div>

          <div class="step-actions">
            <button class="btn btn-secondary" onclick="goBackToChatCustomization()"><i data-lucide="arrow-left" width="16" height="16"></i> Back</button>
            <button class="btn btn-primary" onclick="finishWidgetCreation()"><i data-lucide="check" width="16" height="16"></i> Complete Setup</button>
          </div>
        </div>

      </div>
    </div>
  </div>

  <style>
    @keyframes spin { 100% { transform: rotate(360deg); } }
  </style>
"""

html += scripts

html += """
  <script>lucide.createIcons();</script>
</body>
</html>
"""

with open('dashboard.html', 'w', encoding='utf-8') as f:
    f.write(html)

print('dashboard.html reconstructed successfully.')
