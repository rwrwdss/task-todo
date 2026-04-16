const board = document.getElementById('board');
const cells = document.querySelectorAll('.cell');
const startButton = document.getElementById('startButton');
const resetButton = document.getElementById('resetButton');
const message = document.getElementById('message');

let currentPlayer = 'X';
let gameActive = false;
let gameState = ['', '', '', '', '', '', '', '', ''];

const winningConditions = [
    [0, 1, 2],
    [3, 4, 5],
    [6, 7, 8],
    [0, 3, 6],
    [1, 4, 7],
    [2, 5, 8],
    [0, 4, 8],
    [2, 4, 6]
];

function startGame() {
    gameActive = true;
    gameState = ['', '', '', '', '', '', '', '', ''];
    currentPlayer = 'X';
    message.textContent = `Player ${currentPlayer}'s turn`;
    cells.forEach(cell => {
        cell.textContent = '';
        cell.classList.remove('x', 'o');
    });
    board.classList.remove('hidden');
    resetButton.classList.remove('hidden');
    startButton.classList.add('hidden');
}

function handleCellClick(event) {
    const clickedCell = event.target;
    const clickedCellIndex = parseInt(clickedCell.getAttribute('data-index'));

    if (gameState[clickedCellIndex] !== '' || !gameActive) {
        return;
    }

    gameState[clickedCellIndex] = currentPlayer;
    clickedCell.textContent = currentPlayer;
    clickedCell.classList.add(currentPlayer.toLowerCase());

    if (checkWinner()) {
        message.textContent = `Player ${currentPlayer} wins!`;
        gameActive = false;
        return;
    }

    if (!gameState.includes('')) {
        message.textContent = 'Draw!';
        gameActive = false;
        return;
    }

    currentPlayer = currentPlayer === 'X' ? 'O' : 'X';
    message.textContent = `Player ${currentPlayer}'s turn`;
}

function checkWinner() {
    for (let condition of winningConditions) {
        const [a, b, c] = condition;
        if (gameState[a] && gameState[a] === gameState[b] && gameState[a] === gameState[c]) {
            return true;
        }
    }
    return false;
}

function resetGame() {
    gameActive = false;
    board.classList.add('hidden');
    resetButton.classList.add('hidden');
    startButton.classList.remove('hidden');
    message.textContent = '';
}

startButton.addEventListener('click', startGame);
resetButton.addEventListener('click', resetGame);
cells.forEach(cell => cell.addEventListener('click', handleCellClick));