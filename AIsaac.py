import ScoreReader
import GameInput
import Eyes
import sys
import random
import signal
import time


class AIsaac(object):
    def __init__(self, game):
        self.Game = game
        self.original_sigint = signal.getsignal(signal.SIGINT)

    def __del__(self):
        self.cleanup()

    def train(self):
        print("Not slacking off, no sir.")

    def act(self):
        actionVector = [0] * 12
        for i in range(0, 12):
            actionVector[i] = random.randint(0, 1)

        self.Game.send(actionVector)

    def cleanup(self):
        self.Game.send([0] * len(self.Game.actions))

    def exit_gracefully(self, signum, frame):
        # restore the original signal handler as otherwise evil things will happen
        # in raw_input when CTRL+C is pressed, and our signal handler is not
        # re-entrant
        self.cleanup()
        signal.signal(signal.SIGINT, self.original_sigint)

        try:
            if input("\nReally quit? (y/n)> ").lower().startswith('y'):
                sys.exit(1)

        except KeyboardInterrupt:
            print("Ok ok, quitting")
            sys.exit(1)

        # restore the exit gracefully handler here
        signal.signal(signal.SIGINT, self.exit_gracefully)


def main(title='Binding of Isaac: Afterbirth+'):
    scoreReader = ScoreReader.Reader(title)
    game = GameInput.Game(scoreReader, title)
    eye = Eyes.Eye(title)
    aIsaac = AIsaac(game)
    signal.signal(signal.SIGINT, aIsaac.exit_gracefully)
    aIsaac.train()
    i = 0
    j = 0
    while aIsaac.Game.getScore() > -1:
        aIsaac.act()
        i += 1
        if i % 1000 == 0:
            eye.savegs('gs{}.gif'.format(j))
            j += 1

    print("I lost? Inconceivable..", aIsaac.Game.getScore())
    return aIsaac


if __name__ == '__main__':
    main()
