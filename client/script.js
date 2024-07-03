document.addEventListener("DOMContentLoaded", () => {
  const urlInput = document.getElementById("url-input");
  const createButton = document.getElementById("create-button");
  const resultContainer = document.getElementsByClassName("result");

  createButton.addEventListener("click", () => {
    const url = urlInput.value.trim();
    if (!url) {
      alert("Please enter a URL");
      return;
    }
    const host = "http://0.0.0.0:8000";
    fetch("http://0.0.0.0:8000", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ url: url }),
    })
      .then((response) => response.json())
      .then((data) => {
        resultContainer[0].style.display = "block";
        resultContainer[0].innerHTML = `
                              <p class="text-center">
        Your shorten link:
                                <a href="${host}/${data.data.url}" class="text-decoration-none">${data.data.url}</a>
      </p>
                    `;
      })
      .catch((error) => {
        console.error("Error:", error);
        resultContainer[0].style.display = "block";
        resultContainer[0].innerHTML = `<p>Error: ${error.message}</p>`;
      });
  });
});
