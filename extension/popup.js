document.addEventListener('DOMContentLoaded', function() {
  const findButton = document.getElementById('findButton');
  const searchInput = document.getElementById('searchText');

  findButton.addEventListener('click', async () => {
    const searchText = searchInput.value.trim();
    if (!searchText) return;

    // Get the active tab
    // const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
    
    // Send message to content script
    chrome.runtime.sendMessage({
      action: 'findText',
      text: searchText
    });
  });
}); 