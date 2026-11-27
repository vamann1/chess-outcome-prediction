import os
import pandas as pd
import chess.pgn
from tqdm.auto import tqdm 

os.makedirs("parsed", exist_ok=True)
TOTAL_GAMES = 20_273_737 # from the lichess.org website
USED_GAMES = 500_000
rows = []
section = 0
count = 0

def to_winprob(s):
    return s.white().wdl(model="lichess").expectation()

with open("lichess_db_standard_rated_2018-06.pgn", encoding="utf-8") as pgn:
    for _ in tqdm(range(USED_GAMES)):
        game = chess.pgn.read_game(pgn)
        if game is None:
            break

        if section == 1:
            break

        headers = game.headers
        board = game.board()
        sans = []
        evals = []
        clocks = []

        for node in game.mainline():
            s = node.eval()

            evals.append(to_winprob(s) if s is not None else None)
            clocks.append(node.clock())
            sans.append(board.san(node.move))

            board.push(node.move)

        if len(evals) == 0 or evals[0] is None:
            continue

        rows.append({
            "Event": headers.get("Event"),
            "WhiteElo": headers.get("WhiteElo"),
            "BlackElo": headers.get("BlackElo"),
            "ResultRaw": headers.get("Result"),
            "ECO": headers.get("ECO"),
            "Opening": headers.get("Opening"),
            "Date": headers.get("UTCDate"),
            "Time": headers.get("UTCTime"),
            "TimeControl": headers.get("TimeControl"),
            "Termination": headers.get("Termination"),
            "Sans": sans,
            "WinProb": evals,
            "Clocks": clocks
        })

        if len(rows) == 100000:
            pd.DataFrame(rows).to_parquet(f"parsed/part_{section}.parquet")
            section += 1
            rows = []

df = pd.DataFrame(rows)
df.to_parquet(f"parsed/part_{section}.parquet")