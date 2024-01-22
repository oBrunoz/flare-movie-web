const posterImage = document.querySelector('.banner-image');
const logoImage = document.querySelector('.logo-image');
const colorThief = new ColorThief();

function extractDominantColor(image) {
    return colorThief.getColor(image);
}

function extractPaletteColor(image) {
    return colorThief.getPalette(image);
}

function getConstrast(rgbColor) {
    const luminance = (0.299 * rgbColor[0] + 0.587 * rgbColor[1] + 0.114 * rgbColor[2]) / 255;
    return luminance > 0.3 ? "black" : "white";
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
    if (dominantColor) {
        const rgbColor = convertToRGBColor(dominantColor);
        applyDynamicColor(rgbColor, '--dominantColor');
        saveDynamicColor(rgbColor, '--dominantColor');
        
        // Aplicar cor de texto baseado na cor de fundo
        try {
            const textColor = getConstrast(dominantColor);
            if (textColor) {
                document.documentElement.style.setProperty('--text-color', textColor);
                console.log('TEXT COLOR: ' + textColor);
                console.log(rgbColor);
            } else {
                document.documentElement.style.setProperty('--text-color', 'rgb(0,0,0)');
            }
        } catch (error) {
            console.error('Error getting color contrast: ', error);
        }
    } else {
        console.log('Dominant color is null. Using default color.');
        const defaultColor = 'rgb(0, 0, 0)';
        applyDynamicColor(defaultColor, '--dominantColor');
        saveDynamicColor(defaultColor, '--dominantColor');
        document.documentElement.style.setProperty('--text-color', 'rgb(0,0,0)');
    }

    const logoDominantColor = extractDominantColor(logoImageObj);
    if (logoDominantColor) {
        const rgbLogoColor = convertToRGBColor(logoDominantColor);
        applyDynamicColor(rgbLogoColor, '--dominantColorLogo');
        saveDynamicColor(rgbLogoColor, '--dominantColorLogo');
    } else {
        console.log('Logo dominant color is null. Using default color.');
        const defaultLogoColor = 'rgb(0, 0, 0)';
        applyDynamicColor(defaultLogoColor, '--dominantColorLogo');
        saveDynamicColor(defaultLogoColor, '--dominantColorLogo');
    }
}
