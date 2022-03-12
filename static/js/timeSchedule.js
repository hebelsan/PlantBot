let addButton = document.getElementById('add-button');
let list = document.getElementById('scheduleList');

function handleAddTimeTemplate() {
    let elements = generateEmptyTimeTemplate();
    elements.listItem.setAttribute('id', uuidv4());
    list.appendChild(elements.listItem);
    addButton.disabled = true;
}

function handleRemoveListItem(els) {
    fetch('/removeJobs', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ 'id': els.listItem.getAttribute('id') })
    }).then(() => {
        els.listItem.remove();
        addButton.disabled = false;
    }).catch((err) => {
        els.errorSpan.style.display = '';
        els.errorSpan.innerHTML = err.toString() + ' <span class="closebtn">&times;</span>';
    });
}

function handleAddTime(els) {
    let durationParsed = parseInt(els.durationField.value);
    // check timeField and durationField is not empty
    if (!els.timeField.value) {
        els.errorSpan.style.display = '';
        els.errorSpan.innerHTML = 'time required <span class="closebtn">&times;</span>';
        return
    } else if(!els.durationField.value) {
        els.errorSpan.style.display = '';
        els.errorSpan.innerHTML = 'duration required <span class="closebtn">&times;</span>';
        return
    } else if(isNaN(durationParsed)) {
        els.errorSpan.style.display = '';
        els.errorSpan.innerHTML = 'duration NaN <span class="closebtn">&times;</span>';
    } else {
        els.errorSpan.style.display = 'none';
    }

    addButton.disabled = false;

    fetch('/addJob', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ 'id': els.listItem.getAttribute('id'), 'time': els.timeField.value, 'duration': durationParsed })
    }).then(() => {
        els.crossIcon.style.display = 'none';
        els.checkIcon.style.display = 'none';
        els.timeField.disabled = true;
        els.durationField.disabled = true;
        els.configureIcon.style.display = ''
    }).catch((err) => {
        els.errorSpan.style.display = '';
        els.errorSpan.innerHTML = err.toString() + ' <span class="closebtn">&times;</span>';
    });
}

function handleConfigureTime(els) {
    addButton.disabled = true;
    els.configureIcon.style.display = 'none';
    els.crossIcon.style.display = '';
    els.checkIcon.style.display = '';
    els.timeField.disabled = false;
    els.durationField.disabled = false;
}

function generateEmptyTimeTemplate() {
    let els = {
        'listItem': document.createElement('li'),
        'timeField': document.createElement('input'),
        'durationLabel': document.createElement('label'),
        'durationField': document.createElement('input'),
        'crossIcon': document.createElement('span'),
        'checkIcon': document.createElement('span'),
        'configureIcon': document.createElement('span'),
        'errorSpan':  document.createElement('span')
    }
    // time field
    els.timeField.setAttribute('type', 'time');
    els.timeField.classList.add('timeField');
    els.listItem.appendChild(els.timeField);
    // duration label
    els.durationLabel.appendChild(document.createTextNode('duration(sek):'))
    els.listItem.appendChild(els.durationLabel);
    // duration field
    els.durationField.setAttribute('type', 'number');
    els.durationField.classList.add('durSecInput');
    els.listItem.appendChild(els.durationField);
    // cross icon
    els.crossIcon.appendChild(document.createTextNode('\u2716'))
    els.crossIcon.classList.add('cross');
    els.crossIcon.onclick = function() { handleRemoveListItem(els); };
    els.listItem.appendChild(els.crossIcon);
    // check icon
    els.checkIcon.appendChild(document.createTextNode('\u2714'))
    els.checkIcon.classList.add('check');
    els.checkIcon.onclick = function() { handleAddTime(els); };
    els.listItem.appendChild(els.checkIcon);
    // configure icon
    els.configureIcon.appendChild(document.createTextNode('\u2699'));
    els.configureIcon.classList.add('configure');
    els.configureIcon.onclick = function() { handleConfigureTime(els); };
    els.configureIcon.style.display = 'none'; // only via button
    els.listItem.appendChild(els.configureIcon);
    // error span
    els.errorSpan.classList.add('error');
    els.errorSpan.style.display = 'none';
    els.errorSpan.onclick = function() { els.errorSpan.style.display = 'none'; }
    els.listItem.appendChild(els.errorSpan);

    crypto.getRandomValues
    els.listItem.classList.add('timeItem');
    return els;
}

function fillTimeSchedule(data) {
    for (entry of data) {
        let elements = generateEmptyTimeTemplate();
        elements.configureIcon.style.display = '';
        elements.checkIcon.style.display = 'none';
        elements.crossIcon.style.display = 'none';
        elements.timeField.value = entry.time;
        elements.timeField.disabled = true;
        elements.durationField.value = entry.durationSek;
        elements.durationField.disabled = true;
        elements.listItem.setAttribute('id', entry.id);
        list.appendChild(elements.listItem);
    }
}

function uuidv4() {
    return ([1e7]+-1e3+-4e3+-8e3+-1e11).replace(/[018]/g, c =>
      (c ^ crypto.getRandomValues(new Uint8Array(1))[0] & 15 >> c / 4).toString(16)
    );
  }
  