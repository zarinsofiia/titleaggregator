document.addEventListener("DOMContentLoaded", function() {
    const headlineContainer = document.getElementById("headline-container");

    fetch('Article.json')
        .then(response => response.json())
        .then(data => {
            data.forEach(article => {
                const headlineBox = document.createElement("div");
                headlineBox.classList.add("headline-box");

                headlineBox.innerHTML = `<a href="${article.link}" target="_blank"><b>${article.title}</b></a><br><i>${article.pub_date}</i>`;
                headlineContainer.appendChild(headlineBox);
            });
        })
        .catch(error => console.error('Error fetching headlines:', error));
});
