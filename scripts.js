document.addEventListener("DOMContentLoaded", function() {
    const polygonSelect = document.getElementById('polygon-select');
    const seePolygonButton = document.getElementById('see-polygon-button');
    const triangulateButton = document.getElementById('triangulate-button');
    const finalTriangulateButton = document.getElementById('final-triangulate-button');
    const colorButton = document.getElementById('color-button');
    const finalColoringButton = document.getElementById('final-coloring-button');
    const cameraButton = document.getElementById('camera-button');
    const problemDescriptionButton = document.getElementById('problem-description-button');
    const triangulationDescriptionButton = document.getElementById('triangulation-description-button');
    const coloringDescriptionButton = document.getElementById('coloring-description-button');
    const camerasDescriptionButton = document.getElementById('cameras-description-button');
    const polygonGraph = document.getElementById('polygon-graph');

    function loadContent(file) {
        fetch(file)
            .then(response => response.text())
            .then(data => {
                const parser = new DOMParser();
                const htmlDoc = parser.parseFromString(data, 'text/html');
                const content = htmlDoc.body.innerHTML;
                polygonGraph.innerHTML = content;

                const scripts = polygonGraph.querySelectorAll('script');
                scripts.forEach(script => {
                    const newScript = document.createElement('script');
                    newScript.type = script.type;
                    if (script.src) {
                        newScript.src = script.src;
                    } else {
                        newScript.textContent = script.textContent;
                    }
                    document.body.appendChild(newScript);
                    document.body.removeChild(newScript);
                });
            })
            .catch(error => console.error('Error loading the content:', error));
    }

    seePolygonButton.addEventListener('click', function() {
        const polygon = polygonSelect.value;
        loadContent(`data/${polygon}/polygon.html`);
    });

    triangulateButton.addEventListener('click', function() {
        const polygon = polygonSelect.value;
        loadContent(`data/${polygon}/triangulation.html`);
    });

    finalTriangulateButton.addEventListener('click', function() {
        const polygon = polygonSelect.value;
        loadContent(`data/${polygon}/final-triangulation.html`);
    });

    colorButton.addEventListener('click', function() {
        const polygon = polygonSelect.value;
        loadContent(`data/${polygon}/coloring.html`);
    });

    finalColoringButton.addEventListener('click', function() {
        const polygon = polygonSelect.value;
        loadContent(`data/${polygon}/final-coloring.html`);
    });

    cameraButton.addEventListener('click', function() {
        const polygon = polygonSelect.value;
        loadContent(`data/${polygon}/cameras.html`);
    });

    problemDescriptionButton.addEventListener('click', function() {
        const text = 'a completar';
        const content = `<h2>Descrição do problema</h2><p>${text}</p>`;
        polygonGraph.innerHTML = content;
    });

    triangulationDescriptionButton.addEventListener('click', function() {
        const text = 'a completar';
        const content = `<h2>Descrição da triangulação</h2><p>${text}</p>`;
        polygonGraph.innerHTML = content;
    });

    coloringDescriptionButton.addEventListener('click', function() {
        const text = 'a completar';
        const content = `<h2>Descrição da coloração</h2><p>${text}</p>`;
        polygonGraph.innerHTML = content;
    });

    camerasDescriptionButton.addEventListener('click', function() {
        const text = 'a completar';
        const content = `<h2>Descrição da distribuição de câmeras</h2><p>${text}</p>`;
        polygonGraph.innerHTML = content;
    });
});
