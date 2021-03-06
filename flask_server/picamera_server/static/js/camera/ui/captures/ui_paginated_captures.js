// Expand capture on click
function expandCapture(image) {
    // Get the expanded image
    let expandImg = document.getElementById("expandedImg");
    // Get the image text
    let imgText = document.getElementById("imgtext");
    // Use the same src in the expanded image as the image being clicked on from the grid
    expandImg.src = image.src;
    // Use the value of the alt attribute of the clickable image as text inside the expanded image
    imgText.innerHTML = image.alt;
    // Show the container element (hidden with CSS)
    expandImg.parentElement.style.display = "block";

    // Place the expanded image after the grid in which the image is being expanded
    let expandedImgContainer = document.getElementById("expandedImgContainer");
    // Append after the row of the grid
    image.parentElement.parentElement.append(expandedImgContainer);
    expandedImgContainer.scrollIntoView();
}

// Close expanded capture with Escape
document.body.addEventListener("keydown", (event) => {
    if(event.code === 'Escape') {
        let expandedImgContainer = document.querySelector("#expandedImgContainer > div");
        expandedImgContainer.style.display = 'none';
    }
});

// Redirect to get apply date filters
function getCapturesFilteredByDate(){
    /**
     * Redirect with the datetime filters applied.
     * Action of button in datetime filter form
     *
     * @type {number}
     */
    let pageNumber = 1;
    let datetimeFrom = document.getElementById('datetime-from-input').value;
    let datetimeUntil = document.getElementById('datetime-until-input').value;
    let capturesEndpoint = document.getElementById('capturesEndpoint').value;
    let endpoint = `${window.location.origin}${capturesEndpoint}${pageNumber}/?datetimeFrom=${datetimeFrom}&datetimeUntil=${datetimeUntil}`;
    window.location.replace(endpoint);
    return false
}
