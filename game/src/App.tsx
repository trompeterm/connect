import { useEffect, useMemo, useState } from 'react'
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

function applyMove(board: Board, column: number, player: Player) {
  const row = getNextOpenRow(board, column)

  if (row === -1) {
    return null
  }

  const nextBoard = board.map((boardRow) => [...boardRow])
  nextBoard[row][column] = player

  return {
    nextBoard,
    isWinner: hasWinner(nextBoard, row, column, player),
    isDraw: nextBoard.every((boardRow) => boardRow.every((cell) => cell !== EMPTY)),
  }
}

function toPredictionBoard(board: Board, player: Player) {
  return board.map((row) =>
    row.map((cell) => {
      if (cell === EMPTY) {
        return 0
      }

      return cell === player ? 1 : -1
    }),
  )
}

function App() {
  const [board, setBoard] = useState<Board>(createBoard)
  const [currentPlayer, setCurrentPlayer] = useState<Player>('red')
  const [winner, setWinner] = useState<Player | 'draw' | null>(null)
  const [isComputerThinking, setIsComputerThinking] = useState(false)

  const isBoardFull = useMemo(
    () => board.every((row) => row.every((cell) => cell !== EMPTY)),
    [board],
  )

  const statusMessage = winner
    ? winner === 'draw'
      ? "It's a draw."
      : `${winner === 'red' ? 'Red' : 'Yellow'} wins.`
    : isComputerThinking
      ? 'Yellow is thinking...'
      : `${currentPlayer === 'red' ? 'Red' : 'Yellow'} to move.`

  function handleColumnClick(column: number) {
    if (winner || currentPlayer !== 'red' || isComputerThinking) {
      return
    }

    const move = applyMove(board, column, currentPlayer)

    if (!move) {
      return
    }

    const { nextBoard, isWinner, isDraw } = move

    setBoard(nextBoard)

    if (isWinner) {
      setWinner(currentPlayer)
      return
    }

    if (isDraw) {
      setWinner('draw')
      return
    }

    setCurrentPlayer('yellow')
  }

  useEffect(() => {
    if (winner || isBoardFull || currentPlayer !== 'yellow' || isComputerThinking) {
      return
    }

    let cancelled = false

    const makeComputerMove = async () => {
      setIsComputerThinking(true)

      try {
        const response = await fetch('http://localhost:8000/predict', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(toPredictionBoard(board, currentPlayer)),
        })

        if (!response.ok) {
          throw new Error(`Prediction failed with status ${response.status}`)
        }

        const data = await response.json()
        const predictedColumn = Number(data.predicted_move)
        const fallbackColumn = Array.from({ length: COLUMNS }, (_, index) => index).find((column) => getNextOpenRow(board, column) !== -1)
        const chosenColumn =
          Number.isInteger(predictedColumn) && predictedColumn >= 0 && predictedColumn < COLUMNS
            ? predictedColumn
            : fallbackColumn

        if (cancelled) {
          return
        }

        if (chosenColumn === undefined) {
          setWinner('draw')
          return
        }

        const move = applyMove(board, chosenColumn, currentPlayer)

        if (!move) {
          return
        }

        const { nextBoard, isWinner, isDraw } = move

        setBoard(nextBoard)

        if (isWinner) {
          setWinner(currentPlayer)
          return
        }

        if (isDraw) {
          setWinner('draw')
          return
        }

        setCurrentPlayer('red')
      } catch (error) {
        console.error('Could not fetch a computer move:', error)

        const fallbackColumn = Array.from({ length: COLUMNS }, (_, index) => index).find((column) => getNextOpenRow(board, column) !== -1)

        if (!cancelled && fallbackColumn !== undefined) {
          const move = applyMove(board, fallbackColumn, currentPlayer)

          if (move) {
            const { nextBoard, isWinner, isDraw } = move
            setBoard(nextBoard)

            if (isWinner) {
              setWinner(currentPlayer)
            } else if (isDraw) {
              setWinner('draw')
            } else {
              setCurrentPlayer('red')
            }
          }
        } else if (!cancelled) {
          setWinner('draw')
        }
      } finally {
        if (!cancelled) {
          setIsComputerThinking(false)
        }
      }
    }

    void makeComputerMove()

    return () => {
      cancelled = true
    }
  }, [board, currentPlayer, winner, isBoardFull, isComputerThinking])

  function resetGame() {
    setBoard(createBoard())
    setCurrentPlayer('red')
    setWinner(null)
    setIsComputerThinking(false)
  }

  return (
    <main className="game-shell">
      <section className="hero-panel">
        <div>
          <p className="eyebrow">Connect 4</p>
          <h1>Drop discs, connect four.</h1>
          <p className="subtitle">Red is you. Yellow is the computer.</p>
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
              disabled={Boolean(winner) || isBoardFull || isComputerThinking || currentPlayer !== 'red'}
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
