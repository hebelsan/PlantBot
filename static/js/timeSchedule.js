let addButton = document.getElementById('add-button');
let list = document.getElementById('scheduleList');

function handleAddTimeTemplate() {
    let timeTemplateElement = generateTimeTemplate();
    list.appendChild(timeTemplateElement);
    addButton.disabled = true;
}

function handleRemoveTimeTemplate(el) {
    el.remove();
    // TODO remove time scheduler job
    addButton.disabled = false;
}

function handleAddTime(timeField, durationField, crossIcon, checkIcon, configureIcon, errorSpan) {
    // check timeField and durationField is not empty
    if (!timeField.value) {
        errorSpan.style.display = '';
        errorSpan.innerHTML = 'time required <span class="closebtn">&times;</span>';
        return
    } else if(!durationField.value) {
        errorSpan.style.display = '';
        errorSpan.innerHTML = 'duration required <span class="closebtn">&times;</span>';
        return
    } else {
        errorSpan.style.display = 'none';
    }
    // TODO add time scheduler job
    addButton.disabled = false;
    crossIcon.style.display = 'none';
    checkIcon.style.display = 'none';
    timeField.disabled = true;
    durationField.disabled = true;
    configureIcon.style.display = ''
}

function handleConfigureTime(timeField, durationField, crossIcon, checkIcon, configureIcon) {
    addButton.disabled = true;
    configureIcon.style.display = 'none';
    crossIcon.style.display = '';
    checkIcon.style.display = '';
    timeField.disabled = false;
    durationField.disabled = false;
}

function generateTimeTemplate() {
    let timeTemplate = document.createElement('li');
    let timeField = document.createElement('input');
    let durationLabel = document.createElement('label');
    let durationField = document.createElement('input');
    let crossIcon = document.createElement('span');
    let checkIcon = document.createElement('span');
    let configureIcon = document.createElement('span');
    let errorSpan = document.createElement('span');
    // time field
    timeField.setAttribute('type', 'time');
    timeTemplate.appendChild(timeField);
    // duration label
    durationLabel.appendChild(document.createTextNode('duration(sek):'))
    timeTemplate.appendChild(durationLabel);
    // duration field
    durationField.setAttribute('type', 'number');
    durationField.classList.add('durSecInput');
    timeTemplate.appendChild(durationField);
    // cross icon
    crossIcon.appendChild(document.createTextNode('\u2716'))
    crossIcon.classList.add('cross');
    crossIcon.onclick = function() { handleRemoveTimeTemplate(this.parentNode); };
    timeTemplate.appendChild(crossIcon);
    // check icon
    checkIcon.appendChild(document.createTextNode('\u2714'))
    checkIcon.classList.add('check');
    checkIcon.onclick = function() { handleAddTime(timeField, durationField, crossIcon, checkIcon, configureIcon, errorSpan); };
    timeTemplate.appendChild(checkIcon);
    // configure icon
    configureIcon.appendChild(document.createTextNode('\u2699'));
    configureIcon.classList.add('configure');
    configureIcon.onclick = function() { handleConfigureTime(timeField, durationField, crossIcon, checkIcon, configureIcon); };
    configureIcon.style.display = 'none';
    timeTemplate.appendChild(configureIcon);
    // error span
    errorSpan.classList.add('error');
    errorSpan.style.display = 'none';
    errorSpan.onclick = function() { errorSpan.style.display = 'none'; }
    timeTemplate.appendChild(errorSpan);

    timeTemplate.classList.add('timeItem');
    return timeTemplate;
}