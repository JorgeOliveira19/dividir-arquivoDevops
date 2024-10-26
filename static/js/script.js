document.getElementById('csvForm').addEventListener('submit', function(event) {
    event.preventDefault(); // Impede o envio do formulário padrão

    var fileInput = document.getElementById('file');
    var file = fileInput.files[0];
    var loteInput = document.getElementById('tamanho_lote');
    var lote = parseInt(loteInput.value);

    if (!file || file.type !== 'text/csv') {
        document.getElementById('fileError').style.display = 'block';
        return;
    }
    if (isNaN(lote) || lote <= 0) {
        document.getElementById('loteError').style.display = 'block';
        return;
    }

    var formData = new FormData();
    formData.append('file', file);
    formData.append('tamanho_lote', lote);

    fetch('/', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        // Exibe os links para download
        var downloadLinks = document.getElementById('downloadLinks');
        var fileList = document.getElementById('fileList');
        fileList.innerHTML = '';
        data.forEach(function(link) {
            var listItem = document.createElement('li');
            var anchor = document.createElement('a');
            anchor.href = link;
            anchor.textContent = link.split('/').pop();
            listItem.appendChild(anchor);
            fileList.appendChild(listItem);
        });
        downloadLinks.style.display = 'block';
    })
    .catch(error => {
        console.error('Erro na requisição:', error);
    });
});