// Function to create an overlay element
function createOverlay(element) {
  const rect = element.getBoundingClientRect();
  const overlay = document.createElement('div');
  overlay.className = 'text-overlay';
  overlay.style.position = 'absolute';
  overlay.style.left = rect.left + window.scrollX + 'px';
  overlay.style.top = rect.top + window.scrollY + 'px';
  overlay.style.width = rect.width + 'px';
  overlay.style.height = rect.height + 'px';
  document.body.appendChild(overlay);
  return overlay;
}

// Function to find text and create overlays
function findAndOverlayText(searchText) {
  // Remove existing overlays
  document.querySelectorAll('.text-overlay').forEach(overlay => overlay.remove());

  // Create a tree walker to find text nodes
  const walker = document.createTreeWalker(
    document.body,
    NodeFilter.SHOW_TEXT,
    null,
    false
  );

  let node;
  while (node = walker.nextNode()) {
    const text = node.textContent;
    if (text.toLowerCase().includes(searchText.toLowerCase())) {
      // Create a span around the matching text
      const span = document.createElement('span');
      span.className = 'highlighted-text';
      node.parentNode.replaceChild(span, node);
      span.appendChild(document.createTextNode(text));
      
      // Create overlay for the span
      createOverlay(span);
    }
  }
}

// Listen for messages from the popup
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === 'findText') {
    findAndOverlayText(request.text);
  }
}); 