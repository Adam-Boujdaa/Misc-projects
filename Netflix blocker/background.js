////////// The following program was written by Adam B following this tutorial : https://youtu.be/f0Fw9yskETs //////////


// Listen for web requests on Chrome (takes in 3 arguments):
chrome.webRequest.onBeforeRequest.addListener(
  //The first is the callback function that needs details about the request that is supposed to get sent :
    function(details) {return {cancel : true}},
  // Filtering argument because otherwise it will block all requests from the browser : Here we want to block netflix requests so 
    {urls: ["://.netflix.com/" , "https://www.netflix.com/"]}
  //Block "function"
    [blocking]
)    