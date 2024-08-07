
let typesDiv = document.getElementById('typeSelect');

let btnMale = document.getElementById('btnMale');
let btnFemale = document.getElementById('btnFemale');

let inputSexo = document.getElementById('pjSexo');
let inputType = document.getElementById('pjType');

function loadMaleTypes() {
    typesDiv.innerHTML = "";
    let maleTypeTemplate = document.getElementById('maleTypesTemplate').content.cloneNode(true);
    let types = maleTypeTemplate.getElementById('maleTypes');
    
    typesDiv.append(types);
    inputType.value = 'null';

    let btnFighter = document.getElementById('btnFighter');
    let btnAventurer = document.getElementById('btnAventurer');
    let btnHechizero = document.getElementById('btnHechizero');


    btnFighter.addEventListener('click', () => {
        btnFighter.disabled = true;
        btnAventurer.disabled = false;
        btnHechizero.disabled = false;

        btnFighter.classList.add('selected');
        btnAventurer.classList.remove('selected');
        btnHechizero.classList.remove('selected');

        inputType.value = 'Guerrero';
    });
    btnAventurer.addEventListener('click', () => {
        btnAventurer.disabled = true;
        btnFighter.disabled = false;
        btnHechizero.disabled = false;

        btnAventurer.classList.add('selected');
        btnFighter.classList.remove('selected');
        btnHechizero.classList.remove('selected');

        inputType.value = 'Aventurero';
    });
    btnHechizero.addEventListener('click', () => {
        btnHechizero.disabled = true;
        btnFighter.disabled = false;
        btnAventurer.disabled = false;

        btnHechizero.classList.add('selected');
        btnFighter.classList.remove('selected');
        btnAventurer.classList.remove('selected');

        inputType.value = 'Hechizero';
    });  
}

function loadFemaleTypes() {
    typesDiv.innerHTML = "";
    inputType.value = 'null';
    let femaleTypeTemplate = document.getElementById('femaleTypesTemplate').content.cloneNode(true);
    let types = femaleTypeTemplate.getElementById('femaleTypes');

    typesDiv.append(types);

    let btnFighter = document.getElementById('btnFighter');
    let btnAventurer = document.getElementById('btnAventurer');
    let btnHechizero = document.getElementById('btnHechizero');

    btnFighter.addEventListener('click', () => {
        btnFighter.disabled = true;
        btnAventurer.disabled = false;
        btnHechizero.disabled = false;

        btnFighter.classList.add('selected');
        btnAventurer.classList.remove('selected')
        btnHechizero.classList.remove('selected');
        inputType.value = 'Guerrero';
    });
    btnAventurer.addEventListener('click', () => {
        btnAventurer.disabled = true;
        btnFighter.disabled = false;
        btnHechizero.disabled = false;

        btnAventurer.classList.add('selected');
        btnHechizero.classList.remove('selected');
        btnFighter.classList.remove('selected');

        inputType.value = 'Aventurero';
    });
    btnHechizero.addEventListener('click', () => {
        btnHechizero.disabled = true;
        btnFighter.disabled = false;
        btnAventurer.disabled = false;

        btnHechizero.classList.add('selected');
        btnFighter.classList.remove('selected');
        btnAventurer.classList.remove('selected');

        inputType.value = 'Hechizero';
    });
}

btnMale.addEventListener('click', ()=> {
    btnMale.disabled = true;
    btnFemale.disabled = false;
    inputSexo.value = 'm';
    loadMaleTypes();
});
btnFemale.addEventListener('click', ()=> {
    btnMale.disabled = false;
    btnFemale.disabled = true;
    inputSexo.value = 'f';
    loadFemaleTypes();
});