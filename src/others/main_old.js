const MATRIX = document.getElementById("matrix");

const SEQUENCE = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"];
const NUMBER = ["U", "V", "W", "X", "Y", "Z"];
const width = window.innerWidth;
const height = window.innerHeight;

var fontSize = 1.5;
var charSize = fontSize * 16;
var columns = Math.floor(width / charSize);
var x = -16 * fontSize;
var y = Math.floor(width / 2);
var velocity = 8;
var trail = [];

var rows = [];
var cols = [];
var trailNodes = [];
var nodes = [];

function trailLength() {
    return Math.floor(Math.random() * 18 + 6);
}

function changeVelocity() {
    let getVelocity = [];
    for (i = 1; i < charSize; i++) {
        if (charSize % i == 0) {
            getVelocity.push(Math.floor(charSize / i));
        }
    }
    return getVelocity[Math.floor(Math.random() * getVelocity.length)];
}

function randomColumn() {
    return Math.floor(Math.random() * columns) * charSize;
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
    character.innerHTML = char

    return character;
}

function matrix(node) {
    let char = randomChar();

    if (x > height + charSize) {
        x = -charSize;
        y = randomColumn();
    }

    if (x / charSize == Math.floor(x / charSize)) {
        let trailLetter = createChar("darkgreen", char, fontSize, x, y, 0);
        trail.push(trailLetter);
        if (trail.length > 24) {
            trail[0].remove();
            trail.shift();
        }
        for (i = 0; i < trail.length; i++) {
            trail[i].style.opacity = i / trail.length;
        }
    }

    letter.innerHTML = char;
    letter.style.top = x + 'px';
    letter.style.left = y + 'px';

    x += velocity;
}

var letter = createChar("white", randomChar(), fontSize, x, y, 1);

function main() {

    // if (nodes.length <= columns) {
    //     nodes.push({
    //         node: createChar("white", randomChar(), fontSize, -16 * fontSize, randomColumn(), 1),
    //         length: trailLength(),
    //         velocity: changeVelocity()
    //     })
    // }

    // nodes.forEach(matrix(node))

    matrix();
}

setInterval(main, 1000 / 30);
