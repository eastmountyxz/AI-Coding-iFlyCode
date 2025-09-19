document.addEventListener('DOMContentLoaded', () => {
    const gridContainer = document.getElementById('grid-container');
    const scoreElement = document.getElementById('score');
    const bestScoreElement = document.getElementById('best-score');
    const newGameButton = document.getElementById('new-game-button');
    const tryAgainButton = document.getElementById('try-again-button');
    const keepGoingButton = document.getElementById('keep-going-button');
    const tryAgainWinButton = document.getElementById('try-again-win-button');
    const gameOverMessage = document.getElementById('game-over');
    const gameWonMessage = document.getElementById('game-won');

    // Game variables
    let grid = [];
    let score = 0;
    let bestScore = localStorage.getItem('bestScore') || 0;
    let gameOver = false;
    let won = false;
    let keepPlaying = false;
    
    // Touch handling variables
    let touchStartX = 0;
    let touchStartY = 0;
    let touchEndX = 0;
    let touchEndY = 0;

    // Initialize the game
    function initGame() {
        // Reset game state
        grid = createEmptyGrid();
        score = 0;
        gameOver = false;
        won = false;
        keepPlaying = false;
        
        // Update UI
        updateScore();
        bestScoreElement.textContent = bestScore;
        
        // Clear the grid
        gridContainer.innerHTML = '';
        
        // Create grid cells
        for (let i = 0; i < 16; i++) {
            const gridCell = document.createElement('div');
            gridCell.className = 'grid-cell';
            gridContainer.appendChild(gridCell);
        }
        
        // Add initial tiles
        addRandomTile();
        addRandomTile();
        
        // Hide messages
        gameOverMessage.style.display = 'none';
        gameWonMessage.style.display = 'none';
    }

    // Create an empty 4x4 grid
    function createEmptyGrid() {
        const newGrid = [];
        for (let i = 0; i < 4; i++) {
            newGrid[i] = [0, 0, 0, 0];
        }
        return newGrid;
    }

    // Add a random tile (2 or 4) to an empty cell
    function addRandomTile() {
        const emptyCells = [];
        
        // Find all empty cells
        for (let row = 0; row < 4; row++) {
            for (let col = 0; col < 4; col++) {
                if (grid[row][col] === 0) {
                    emptyCells.push({ row, col });
                }
            }
        }
        
        // If there are empty cells
        if (emptyCells.length > 0) {
            // Choose a random empty cell
            const randomCell = emptyCells[Math.floor(Math.random() * emptyCells.length)];
            
            // Set the value (90% chance for 2, 10% chance for 4)
            const value = Math.random() < 0.9 ? 2 : 4;
            grid[randomCell.row][randomCell.col] = value;
            
            // Create and add the tile to the UI
            addTileToUI(randomCell.row, randomCell.col, value, true);
        }
    }

    // Add a tile to the UI
    function addTileToUI(row, col, value, isNew = false) {
        const tile = document.createElement('div');
        tile.className = `tile tile-${value}${isNew ? ' tile-new' : ''}`;
        tile.textContent = value;
        
        // Position the tile
        const posX = col * 25 + col * 15;
        const posY = row * 100 + row * 15;
        
        tile.style.left = `${posX}px`;
        tile.style.top = `${posY}px`;
        
        // Add data attributes for easier manipulation
        tile.dataset.row = row;
        tile.dataset.col = col;
        tile.dataset.value = value;
        
        gridContainer.appendChild(tile);
    }

    // Update the UI to match the grid state
    function updateUI() {
        // Remove all tiles
        const tiles = document.querySelectorAll('.tile');
        tiles.forEach(tile => tile.remove());
        
        // Add tiles based on the current grid
        for (let row = 0; row < 4; row++) {
            for (let col = 0; col < 4; col++) {
                if (grid[row][col] !== 0) {
                    addTileToUI(row, col, grid[row][col]);
                }
            }
        }
    }

    // Update the score display
    function updateScore() {
        scoreElement.textContent = score;
        
        if (score > bestScore) {
            bestScore = score;
            bestScoreElement.textContent = bestScore;
            localStorage.setItem('bestScore', bestScore);
        }
    }

    // Move tiles in a specific direction
    function moveTiles(direction) {
        if (gameOver && !keepPlaying) return;
        
        let moved = false;
        let addScore = 0;
        
        // Create a copy of the grid for comparison
        const previousGrid = JSON.parse(JSON.stringify(grid));
        
        // Process the grid based on direction
        switch (direction) {
            case 'up':
                for (let col = 0; col < 4; col++) {
                    const result = processTilesInColumn(col, true);
                    moved = moved || result.moved;
                    addScore += result.score;
                }
                break;
            case 'right':
                for (let row = 0; row < 4; row++) {
                    const result = processTilesInRow(row, false);
                    moved = moved || result.moved;
                    addScore += result.score;
                }
                break;
            case 'down':
                for (let col = 0; col < 4; col++) {
                    const result = processTilesInColumn(col, false);
                    moved = moved || result.moved;
                    addScore += result.score;
                }
                break;
            case 'left':
                for (let row = 0; row < 4; row++) {
                    const result = processTilesInRow(row, true);
                    moved = moved || result.moved;
                    addScore += result.score;
                }
                break;
        }
        
        // Update score
        if (addScore > 0) {
            score += addScore;
            updateScore();
        }
        
        // If tiles moved, update UI and add a new tile
        if (moved) {
            updateUI();
            setTimeout(() => {
                addRandomTile();
                
                // Check if game is over or won
                if (!canMove()) {
                    gameOver = true;
                    gameOverMessage.style.display = 'flex';
                }
            }, 150);
        }
    }

    // Process tiles in a row (left or right)
    function processTilesInRow(row, moveLeft) {
        let moved = false;
        let addScore = 0;
        
        // Get the tiles in the row
        const tiles = grid[row].filter(tile => tile !== 0);
        
        // Merge tiles if possible
        for (let i = moveLeft ? 0 : tiles.length - 1; 
             moveLeft ? i < tiles.length - 1 : i > 0; 
             moveLeft ? i++ : i--) {
            
            const currentIndex = moveLeft ? i : i;
            const nextIndex = moveLeft ? i + 1 : i - 1;
            
            if (tiles[currentIndex] === tiles[nextIndex]) {
                tiles[currentIndex] *= 2;
                tiles[nextIndex] = 0;
                addScore += tiles[currentIndex];
                moved = true;
                
                // Check if won
                if (tiles[currentIndex] === 2048 && !won && !keepPlaying) {
                    won = true;
                    gameWonMessage.style.display = 'flex';
                }
            }
        }
        
        // Remove zeros (merged tiles)
        const newTiles = tiles.filter(tile => tile !== 0);
        
        // Fill with zeros
        while (newTiles.length < 4) {
            moveLeft ? newTiles.push(0) : newTiles.unshift(0);
        }
        
        // Check if tiles moved
        for (let i = 0; i < 4; i++) {
            if (grid[row][i] !== newTiles[i]) {
                moved = true;
            }
            grid[row][i] = newTiles[i];
        }
        
        return { moved, score: addScore };
    }

    // Process tiles in a column (up or down)
    function processTilesInColumn(col, moveUp) {
        let moved = false;
        let addScore = 0;
        
        // Get the tiles in the column
        const tiles = [];
        for (let row = 0; row < 4; row++) {
            if (grid[row][col] !== 0) {
                tiles.push(grid[row][col]);
            }
        }
        
        // Merge tiles if possible
        for (let i = moveUp ? 0 : tiles.length - 1; 
             moveUp ? i < tiles.length - 1 : i > 0; 
             moveUp ? i++ : i--) {
            
            const currentIndex = moveUp ? i : i;
            const nextIndex = moveUp ? i + 1 : i - 1;
            
            if (tiles[currentIndex] === tiles[nextIndex]) {
                tiles[currentIndex] *= 2;
                tiles[nextIndex] = 0;
                addScore += tiles[currentIndex];
                moved = true;
                
                // Check if won
                if (tiles[currentIndex] === 2048 && !won && !keepPlaying) {
                    won = true;
                    gameWonMessage.style.display = 'flex';
                }
            }
        }
        
        // Remove zeros (merged tiles)
        const newTiles = tiles.filter(tile => tile !== 0);
        
        // Fill with zeros
        while (newTiles.length < 4) {
            moveUp ? newTiles.push(0) : newTiles.unshift(0);
        }
        
        // Check if tiles moved
        for (let row = 0; row < 4; row++) {
            if (grid[row][col] !== newTiles[row]) {
                moved = true;
            }
            grid[row][col] = newTiles[row];
        }
        
        return { moved, score: addScore };
    }

    // Check if any move is possible
    function canMove() {
        // Check for empty cells
        for (let row = 0; row < 4; row++) {
            for (let col = 0; col < 4; col++) {
                if (grid[row][col] === 0) {
                    return true;
                }
            }
        }
        
        // Check for possible merges horizontally
        for (let row = 0; row < 4; row++) {
            for (let col = 0; col < 3; col++) {
                if (grid[row][col] === grid[row][col + 1]) {
                    return true;
                }
            }
        }
        
        // Check for possible merges vertically
        for (let col = 0; col < 4; col++) {
            for (let row = 0; row < 3; row++) {
                if (grid[row][col] === grid[row + 1][col]) {
                    return true;
                }
            }
        }
        
        // No moves possible
        return false;
    }

    // Event listeners
    document.addEventListener('keydown', event => {
        switch (event.key) {
            case 'ArrowUp':
                moveTiles('up');
                event.preventDefault();
                break;
            case 'ArrowRight':
                moveTiles('right');
                event.preventDefault();
                break;
            case 'ArrowDown':
                moveTiles('down');
                event.preventDefault();
                break;
            case 'ArrowLeft':
                moveTiles('left');
                event.preventDefault();
                break;
        }
    });

    // Touch event handlers
    gridContainer.addEventListener('touchstart', event => {
        touchStartX = event.touches[0].clientX;
        touchStartY = event.touches[0].clientY;
        event.preventDefault();
    }, { passive: false });

    gridContainer.addEventListener('touchmove', event => {
        event.preventDefault();
    }, { passive: false });

    gridContainer.addEventListener('touchend', event => {
        touchEndX = event.changedTouches[0].clientX;
        touchEndY = event.changedTouches[0].clientY;
        
        const diffX = touchEndX - touchStartX;
        const diffY = touchEndY - touchStartY;
        
        // Determine the direction of the swipe
        if (Math.abs(diffX) > Math.abs(diffY)) {
            // Horizontal swipe
            if (diffX > 20) {
                moveTiles('right');
            } else if (diffX < -20) {
                moveTiles('left');
            }
        } else {
            // Vertical swipe
            if (diffY > 20) {
                moveTiles('down');
            } else if (diffY < -20) {
                moveTiles('up');
            }
        }
        
        event.preventDefault();
    }, { passive: false });

    // Button event listeners
    newGameButton.addEventListener('click', initGame);
    tryAgainButton.addEventListener('click', initGame);
    tryAgainWinButton.addEventListener('click', initGame);
    keepGoingButton.addEventListener('click', () => {
        keepPlaying = true;
        gameWonMessage.style.display = 'none';
    });

    // Initialize the game
    initGame();
});