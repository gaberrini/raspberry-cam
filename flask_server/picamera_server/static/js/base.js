function showErrorNotChrome(){
    /**
     * Show the error-message hidden when the navigator is not chrome
     */
    if(!/chrom(e|ium)/.test(navigator.userAgent.toLowerCase())) {
        document.getElementById('chrome-error-message').hidden = false;
    }
}

window.addEventListener("load", function(){
    showErrorNotChrome();
});
