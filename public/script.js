const title = document.getElementById('main-title');
const description = document.getElementById('main-desc');
const myLink = document.getElementById('my-link'); 

function addHoverEffect(element, scaleValue) {
    element.style.transition = "transform 0.3s ease";
    element.style.display = "inline-block"; 

    element.addEventListener('mouseenter', () => {
        element.style.transform = `scale(${scaleValue})`;
    });

    element.addEventListener('mouseleave', () => {
        element.style.transform = "scale(1)";
    });
}

addHoverEffect(title, 1.5);
addHoverEffect(description, 1.5);
addHoverEffect(myLink, 1.5);