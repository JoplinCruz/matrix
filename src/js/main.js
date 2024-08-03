const MATRIX = document.getElementById("matrix");

const SEQUENCE = ["a", "b", "c", "d", "e", " f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "t", "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"];
const NUMBER = [1, 2, 3, 4, 5, 6, 7, 8, 9, 0];

const maxLength = 32;
const minLength = 8;
const fps = 60;

const fontSize = 1;
const charSize = fontSize * 16;

var width = window.innerWidth;
var height = window.innerHeight;
var windowColumns = Math.floor(width / charSize);
var x = -charSize;
var y = NaN;

var velocity = NaN;
var trailLength = NaN;
var nodes = [];


// insert share array --->
var shareColumns = [];
var shadowColumns = [];
for (i = 0; i < windowColumns; i++) { shareColumns.push(i * charSize); }
// end insertion -------->


function changeLength() {
    return Math.floor(Math.random() * (maxLength - minLength) + minLength);
}


function changeVelocity() {
    let getVelocity = [];
    for (i = 1; i < Math.floor(charSize / 2); i++) {
        if (charSize % i == 0) {
            getVelocity.push(Math.floor(charSize / i));
        }
    }
    return getVelocity[Math.floor(Math.random() * getVelocity.length)];
}


function randomColumn() {
    // return Math.floor(Math.random() * columns) * charSize;
    // replace method ------>
    let choice = Math.floor(Math.random() * shareColumns.length);
    let getColumn = shareColumns[choice];
    shadowColumns.push(...shareColumns.splice(choice, 1));
    return getColumn;
    // end lines of code --->
}


function randomChar() {
    return SEQUENCE[Math.floor(Math.random() * SEQUENCE.length)];
}


function createChar(color, char, size, x, y, z) {
    let character = MATRIX.appendChild(document.createElement('p'));
    character.style.position = 'absolute';
    character.style.fontSize = size + 'rem';
    character.style.top = x + 'px';
    character.style.left = y + 'px';
    character.style.zIndex = z;
    character.style.color = color;
    character.innerHTML = char;

    return character;
}



function matrix(node) {
    let char = randomChar();

    if (node.x > height + charSize) {
        // swap code ---->
        shareColumns.push(node.y);
        shadowColumns.splice(shadowColumns.indexOf(node.y, 1));
        // end swap code --------------->
        node.x = -charSize;
        node.y = randomColumn();
        node.velocity = changeVelocity();
    }

    if (node.x / charSize == Math.floor(node.x / charSize)) {
        let trailLetter = createChar("darkgreen", char, fontSize, node.x, node.y, 0);
        node.trail.push(trailLetter);
        if (node.trail.length > node.trailLength) {
            node.trail[0].remove();
            node.trail.shift();
        }
        for (i = 0; i < node.trail.length; i++) {
            node.trail[i].style.opacity = i / (node.trail.length / 2);
        }
        node.trail[Math.floor(Math.random() * node.trail.length)].innerHTML = randomChar();
    }

    node.letter.innerHTML = char;
    node.letter.style.top = node.x + 'px';
    node.letter.style.left = node.y + 'px';

    node.x += node.velocity;
}



function mainframe() {

    if (nodes.length <= windowColumns * 0.9) {

        y = randomColumn();
        velocity = changeVelocity();
        trailLength = changeLength();

        nodes.push({
            letter: createChar("lightgreen", randomChar(), fontSize, x, y, 1),
            x: x,
            y: y,
            trail: [],
            trailLength: trailLength,
            velocity: velocity
        })
    }

    nodes.forEach(matrix);

    window.addEventListener("resize", function () {

        MATRIX.replaceChildren();

        width = window.innerWidth;
        height = window.innerHeight;

        windowColumns = Math.floor(width / charSize);

        x = -charSize;
        y = NaN;

        velocity = NaN;
        trailLength = NaN;
        nodes = [];

        shareColumns = [];
        shadowColumns = [];
        for (i = 0; i < windowColumns; i++) { shareColumns.push(i * charSize); }
    });

}

setInterval(mainframe, 1000 / fps);
