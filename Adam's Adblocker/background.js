// The code runs in a browser extension, using the WebExtension API.
// It will run on every page the user visits, and block ads and trackers.

// This script is intended to run in the context of the web page.
// It blocks requests to known ad and tracker domains using the WebRequest API.

  // List of known ad and tracker domains
  var blockList = [
    "doubleclick.net",
    "adnxs.com",
    "adservice.google.com",
    "advertising.com",
    "exampletracker.com",
    // ...
  ];

  // Block requests to known ad and tracker domains
  chrome.webRequest.onBeforeRequest.addListener(
    function(details) {
      // Check if the request URL matches any of the domains in the block list
      for (var i = 0; i < blockList.length; i++) {
        if (details.url.includes(blockList[i])) {
          // Block the request
          return {cancel: true};
        }
      }
    },
    {urls: ["<all_urls>"]},
    ["blocking"]


  
);