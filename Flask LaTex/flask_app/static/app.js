async function convertLatex() {
    const latexInput = document.getElementById('latex-input').value;
    const response = await fetch('/convert', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: `latex=${encodeURIComponent(latexInput)}`,
    });

    const data = await response.json();
    const bulletPointsElement = document.getElementById('bullet-points');
    bulletPointsElement.innerHTML = '';

    data.bullet_points.forEach(point => {
        const li = document.createElement('li');
        li.textContent = point;
        bulletPointsElement.appendChild(li);
    });
}

async function exportDocx() {
    const bulletPoints = Array.from(document.getElementById('bullet-points').children).map(li => li.textContent);
    const formData = new FormData();
    bulletPoints.forEach(point => formData.append('bullet_points[]', point));

    const response = await fetch('/export', {
        method: 'POST',
        body: formData,
    });

    const blob = await response.blob();
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'bullet_points.docx';
    document.body.appendChild(a);
    a.click();
    a.remove();
}