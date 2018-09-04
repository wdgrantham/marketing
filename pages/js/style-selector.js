let styleSelector = document.getElementsByClassName("style-selector");

let styleSelectorToggle = document.getElementsByClassName("style-selector-toggle");

let openStyleSelector = function(){
    
    let styleSelectorCanvas = document.getElementById('canvas');

    let openStylesBtn = document.getElementById('open-styles');
    
    if (styleSelectorCanvas.classList.contains('opened')) {
        openStylesBtn.classList.remove('opened');
        styleSelectorCanvas.classList.remove('opened');
        console.log('You removed the opened class');
    } else {
        openStylesBtn.classList.add('opened');
        styleSelectorCanvas.classList.add('opened');
        console.log('You added the opened class');
    };
    
};

let changeCssVar = function() {
    let cssVarValue = this.getAttribute("css-var-name");
    let newCssVarValue = this.getAttribute("new-css-var-value");
    let root = document.querySelector(':root')
    let rootStyles = getComputedStyle(root);
    root.style.setProperty(cssVarValue, newCssVarValue);
    console.log('Changed the CSS Variable ' + cssVarValue + ' to ' + newCssVarValue);
};

for (var i = 0; i < styleSelector.length; i++) {
    styleSelector[i].addEventListener('click', changeCssVar, false);
};

for (var j = 0; j < styleSelectorToggle.length; j++) {
    styleSelectorToggle[j].addEventListener('click', openStyleSelector, false);
};
