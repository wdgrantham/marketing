function setCssVar(cssSelector, cssValue, cssVar, newCssVar) {
    let getElem = document.querySelector(cssSelector);
    //console.log(getElem);
    let elemStyles = getComputedStyle(getElem);
    let getElemStyle = elemStyles.getPropertyValue(cssValue);
    let root = document.querySelector(':root');
    let rootStyles = getComputedStyle(root);
    let getRootStyle = rootStyles.getPropertyValue(cssVar);
    console.log(getRootStyle);
    root.style.setProperty(cssVar, newCssVar)
    console.log(getRootStyle);
}
    
setCssVar('.font-cursive-1','font-family','--cursive-font', '"Muli", sans-serif')

var styleSelector = document.getElementsByClassName("style-selector");

var myFunction = function() {
    let cssVarValue = this.getAttribute("css-var-name");
    let newCssVarValue = this.getAttribute("new-css-var-value");
    let root = document.querySelector(':root')
    let rootStyles = getComputedStyle(root);
    root.style.setProperty(cssVarValue, newCssVarValue);
    alert(cssVarValue + newCssVarValue);
};

for (var i = 0; i < styleSelector.length; i++) {
    styleSelector[i].addEventListener('click', myFunction, false);
}



//let selectClass = document.querySelector('.font-cursive-1');
//let classStyles = getComputedStyle(selectClass);
//console.log(classStyles.fontFamily);