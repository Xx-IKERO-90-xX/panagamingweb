let optionDiv = document.getElementById("optionsUserEdit");
let brTag = document.createElement("br");

function clearOptionsDiv() {
    optionDiv.innerHTML = "";
    optionDiv.append(brTag);
    optionDiv.append(brTag);
}

function loadDefaultThemes(){
    clearOptionsDiv();

    let defaultTemplate = document.getElementById("defaultTemplate").content.cloneNode(true);
    let themes = defaultTemplate.getElementById("defaultThemes");
    optionDiv.append(themes);
}

function loadBlueThemes() {
    clearOptionsDiv();
    
    let blueThemeTemplate = document.getElementById("blueTemplate").content.cloneNode(true);
    let blueThemes = blueThemeTemplate.getElementById("blueThemes");
    optionDiv.append(blueThemes);
}

function loadGreenThemes() {
    clearOptionsDiv();

    let greenThemeTemplate = document.getElementById("greenTemplate").content.cloneNode(true);
    let greenThemes = greenThemeTemplate.getElementById("greenThemes");
    optionDiv.append(greenThemes);
}

function loadRedThemes() {
    clearOptionsDiv();

    let redThemeTemplate = document.getElementById("redTemplate").content.cloneNode(true);
    let redThemes = redThemeTemplate.getElementById("redThemes");
    optionDiv.append(redThemes);
}

function loadYellowThemes() {
    clearOptionsDiv();

    let yellowThemeTemplate = document.getElementById("yellowTemplate").content.cloneNode(true);
    let yellowThemes = yellowThemeTemplate.getElementById("yellowThemes");
    optionDiv.append(yellowThemes);
}

function loadPurpleThemes() {
    clearOptionsDiv();

    let purpleThemeTemplate = document.getElementById("purpleTemplate").content.cloneNode(true);
    let purpleThemes = purpleThemeTemplate.getElementById("purpleThemes");
    optionDiv.append(purpleThemes);
}

let everyBtn = document.getElementById("everyDefaultBtn");
let btnFilterBlue = document.getElementById("blueFilterBtn");
let btnFilterGreen = document.getElementById("greenFilterBtn");
let btnFilterRed = document.getElementById("redFilterBtn");
let btnFilterYellow = document.getElementById("yellowFilterBtn");
let btnFilterPurple = document.getElementById("purpleFilterBtn");

everyBtn.addEventListener("click", loadDefaultThemes);
btnFilterBlue.addEventListener("click", loadBlueThemes);
btnFilterGreen.addEventListener("click", loadGreenThemes);
btnFilterRed.addEventListener("click", loadRedThemes);
btnFilterYellow.addEventListener("click", loadYellowThemes);
btnFilterPurple.addEventListener("click", loadPurpleThemes);


loadDefaultThemes();
