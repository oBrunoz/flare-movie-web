const posterImage = document.querySelector('.banner-image');
const colorThief = new ColorThief();

function extractDominantColor(image) {
    return colorThief.getColor(image);
}

function convertToRGBColor(colorArray) {
    return `rgb(${colorArray.join(', ')})`;
}

function applyDynamicColor(rgbColor) {
    document.documentElement.style.setProperty('--dominantColor', rgbColor);
}

function applyDefaultColor() {
    const defaultColor = localStorage.getItem('dynamicColor') || 'rgb(3, 0, 28)';
    document.documentElement.style.setProperty('--dominantColor', defaultColor);
}

function saveDynamicColor(rgbColor) {
    localStorage.setItem('dynamicColor', rgbColor);
}

const image = new Image();
image.crossOrigin = 'Anonymous';
image.src = posterImage.src;

if (image.complete) {
    handleImageLoad();
} else {
    applyDefaultColor();
    image.addEventListener('load', handleImageLoad);
}

window.addEventListener('beforeunload', () => {
    saveDynamicColor(getComputedStyle(document.documentElement).getPropertyValue('rgb(3, 0, 28)'));
});

function handleImageLoad() {
    const dominantColor = extractDominantColor(image);
    const rgbColor = convertToRGBColor(dominantColor);
    console.log(rgbColor);
    applyDynamicColor(rgbColor);
    saveDynamicColor(rgbColor);
}
