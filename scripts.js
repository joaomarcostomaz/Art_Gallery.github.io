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
        const text = 'A ideia do trabalho é focada no problema da galeria de arte. Imagine a seguinte situação: Você é dono de uma galeria em que vários quadros artísticos e grandes antiguidades são expostas. Sabendo dos perigos existentes, você precisa ter alguma forma de segurança dentro do espaço, como câmeras por exemplo. A ideia do algoritmo é encontrar o menor número de câmeras que vigie toda a sua galeria, sendo esta representada por um polígono.';
        const content = `<h2>Descrição do problema</h2><p>${text}</p>`;
        polygonGraph.innerHTML = content;
    });

    triangulationDescriptionButton.addEventListener('click', function() {
        const text = 'O algoritmo de triangulação utilizado “é chamado ear-clipping”. A ideia é dividir um polígono simples em triângulos. Ele funciona identificando "orelhas" no polígono, onde uma "orelha" é um triângulo formado por três vértices consecutivos que não contém outros vértices do polígono em seu interior. O processo começa verificando se o polígono é simples e, em seguida, identifica e remove iterativamente essas "orelhas", adicionando os triângulos formados à lista de resultados. Cada vez que uma "orelha" é removida, a lista de vértices do polígono é atualizada, como pode ser visto na animação. Esse procedimento continua até que o polígono seja reduzido a três vértices, formando o último triângulo. É importante ressaltar que caso o polígono não seja simples, o algoritmo não funcionará corretamente.';
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
