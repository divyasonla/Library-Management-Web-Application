<input type="file" id="fileInput">
<button onclick="uploadFile()">Upload aur Import karo</button>

<script>
function uploadFile() {
    let fileInput = document.getElementById("fileInput");
    let file = fileInput.files[0];

    if (!file) {
        alert("Please select a file!");
        return;
    }

    let formData = new FormData();
    formData.append("file", file);

    fetch("/api/method/your_app.api.import_books", {
        method: "POST",
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message || data.error);
    })
    .catch(error => {
        console.error("Error:", error);
    });
}
</script>
