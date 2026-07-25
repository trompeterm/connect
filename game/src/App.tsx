import { useMemo, useState } from 'react'
import './App.css'

const ROWS = 6
const COLUMNS = 7
const EMPTY = ''

type Player = 'red' | 'yellow'
type CellValue = Player | ''
type Board = CellValue[][]

function createBoard(): Board {
  return Array.from({ length: ROWS }, () => Array<CellValue>(COLUMNS).fill(EMPTY))
}

function getNextOpenRow(board: Board, column: number) {
  for (let row = ROWS - 1; row >= 0; row -= 1) {
    if (board[row][column] === EMPTY) {
      return row
    }
  }

  return -1
}

function countInDirection(
  board: Board,
  row: number,
  column: number,
  rowStep: number,
  columnStep: number,
  player: Player,
) {
  let matches = 0
  let currentRow = row + rowStep
  let currentColumn = column + columnStep

  while (
    currentRow >= 0 &&
    currentRow < ROWS &&
    currentColumn >= 0 &&
    currentColumn < COLUMNS &&
    board[currentRow][currentColumn] === player
  ) {
    matches += 1
    currentRow += rowStep
    currentColumn += columnStep
  }

  return matches
}

function hasWinner(board: Board, row: number, column: number, player: Player) {
  const directions = [
    [0, 1],
    [1, 0],
    [1, 1],
    [1, -1],
  ] as const

  return directions.some(([rowStep, columnStep]) => {
    const totalConnected =
      1 +
      countInDirection(board, row, column, rowStep, columnStep, player) +
      countInDirection(board, row, column, -rowStep, -columnStep, player)

    return totalConnected >= 4
  })
}

function App() {
  const [board, setBoard] = useState<Board>(createBoard)
  const [currentPlayer, setCurrentPlayer] = useState<Player>('red')
  const [winner, setWinner] = useState<Player | 'draw' | null>(null)

  const isBoardFull = useMemo(
    () => board.every((row) => row.every((cell) => cell !== EMPTY)),
    [board],
  )

  const statusMessage = winner
    ? winner === 'draw'
      ? "It's a draw."
      : `${winner === 'red' ? 'Red' : 'Yellow'} wins.`
    : `${currentPlayer === 'red' ? 'Red' : 'Yellow'} to move.`

  function handleColumnClick(column: number) {
    if (winner) {
      return
    }

    const row = getNextOpenRow(board, column)

    if (row === -1) {
      return
    }

    const nextBoard = board.map((boardRow) => [...boardRow])
    nextBoard[row][column] = currentPlayer

    if (hasWinner(nextBoard, row, column, currentPlayer)) {
      setBoard(nextBoard)
      setWinner(currentPlayer)
      return
    }

    const isDraw = nextBoard.every((boardRow) => boardRow.every((cell) => cell !== EMPTY))

    setBoard(nextBoard)
    setWinner(isDraw ? 'draw' : null)
    setCurrentPlayer(currentPlayer === 'red' ? 'yellow' : 'red')
  }

  function resetGame() {
    setBoard(createBoard())
    setCurrentPlayer('red')
    setWinner(null)
  }

  return (
    <main className="game-shell">
      <section className="hero-panel">
        <div>
          <p className="eyebrow">Connect 4</p>
          <h1>Drop discs, connect four.</h1>
          <p className="subtitle">Red starts first. Then Yellow takes the next turn.</p>
        </div>

        <div className="status-card" aria-live="polite">
          <span className={`turn-indicator ${winner ? 'idle' : currentPlayer}`} />
          <div>
            <p className="status-label">Status</p>
            <p className="status-message">{statusMessage}</p>
          </div>
          <button type="button" className="reset-button" onClick={resetGame}>
            New game
          </button>
        </div>
      </section>

      <section className="board-card" aria-label="Connect 4 board">
        <div className="board-header">
          {Array.from({ length: COLUMNS }, (_, column) => (
            <button
              key={column}
              type="button"
              className="drop-button"
              onClick={() => handleColumnClick(column)}
              disabled={Boolean(winner) || isBoardFull}
              aria-label={`Drop a disc in column ${column + 1}`}
            >
              {column + 1}
            </button>
          ))}
        </div>

        <div className="board-grid" role="grid" aria-label="Connect 4 grid">
          {board.map((row, rowIndex) =>
            row.map((cell, columnIndex) => (
              <div
                key={`${rowIndex}-${columnIndex}`}
                className={`cell ${cell || 'empty'}`}
                role="gridcell"
                aria-label={
                  cell === 'red'
                    ? `Row ${rowIndex + 1}, column ${columnIndex + 1}, red disc`
                    : cell === 'yellow'
                      ? `Row ${rowIndex + 1}, column ${columnIndex + 1}, yellow disc`
                      : `Row ${rowIndex + 1}, column ${columnIndex + 1}, empty`
                }
              >
                <span className="disc" />
              </div>
            )),
          )}
        </div>
      </section>
    </main>
  )
}

export default App
