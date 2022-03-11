function addTimeItem() {
    let list = document.getElementById('scheduleList');
    var item = document.createElement('li');
    item.appendChild(document.createTextNode('new entry'));
    list.appendChild(item);
}