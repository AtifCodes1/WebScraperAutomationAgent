console.log("JavaScript file loaded");
const urlInput = document.getElementById("url");
const scrapeButton = document.querySelector("button");
const results = document.getElementById("results");
scrapeButton.addEventListener("click", async () => {
    const url = urlInput.value;

    const response = await fetch("/scrape", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            url: url
        })
    });
    const data = await response.json();
    console.log(data);
    results.innerHTML = "";
    data.books.forEach(book => {
        const bookElement = document.createElement("div");
        bookElement.innerHTML = `
        <h3>${book.title}</h3>
        <p>Price: ${book.price}</p>
        <p>Rating: ${book.rating}</p>
        `;
        results.appendChild(bookElement);
    });
});