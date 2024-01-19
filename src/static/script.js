const posterImage = document.querySelector('.banner-image');
const logoImage = document.querySelector('.logo-image');
const colorThief = new ColorThief();

function extractDominantColor(image) {
    return colorThief.getColor(image);
}

function convertToRGBColor(colorArray) {
    return `rgb(${colorArray.join(', ')})`;
}

function applyDynamicColor(rgbColor, variableName) {
    document.documentElement.style.setProperty(variableName, rgbColor);
}

function applyDefaultColor(variableName, defaultValue) {
    const defaultColor = localStorage.getItem(variableName) || defaultValue;
    document.documentElement.style.setProperty(variableName, defaultColor);
}

function saveDynamicColor(rgbColor, variableName) {
    localStorage.setItem(variableName, rgbColor);
}

const posterImageObj = new Image();
posterImageObj.crossOrigin = 'Anonymous';
posterImageObj.src = posterImage.src;

const logoImageObj = new Image();
logoImageObj.crossOrigin = 'Anonymous';
logoImageObj.src = logoImage.src;

if (posterImageObj.complete && logoImageObj.complete) {
    handleImageLoad();
} else {
    applyDefaultColor('--dominantColor', 'rgb(3, 0, 28)');
    applyDefaultColor('--dominantColorLogo', 'rgb(3, 0, 28)'); // Valor padrão para a cor do logo
    posterImageObj.addEventListener('load', handleImageLoad);
    logoImageObj.addEventListener('load', handleImageLoad);
}

window.addEventListener('beforeunload', () => {
    saveDynamicColor(getComputedStyle(document.documentElement).getPropertyValue('--dominantColor'), '--dominantColor');
    saveDynamicColor(getComputedStyle(document.documentElement).getPropertyValue('--dominantColorLogo'), '--dominantColorLogo');
});

function handleImageLoad() {
    const dominantColor = extractDominantColor(posterImageObj);
    const rgbColor = convertToRGBColor(dominantColor);
    applyDynamicColor(rgbColor, '--dominantColor');
    saveDynamicColor(rgbColor, '--dominantColor');
    
    const logoDominantColor = extractDominantColor(logoImageObj);
    const rgbLogoColor = convertToRGBColor(logoDominantColor);
    applyDynamicColor(rgbLogoColor, '--dominantColorLogo');
    saveDynamicColor(rgbLogoColor, '--dominantColorLogo');
    console.log(rgbColor, rgbLogoColor)
}
