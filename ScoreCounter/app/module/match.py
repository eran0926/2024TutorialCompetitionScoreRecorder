class Score:
    def __init__(self):
        self.auto = self.Auto()
        self.telop = self.Telop()
        self.penalty = self.Penalty()
        self.rankingPoints = self.RankingPoints()
        self.totalScore = 0

    def reset(self):
        self.auto.reset()
        self.telop.reset()
        self.penalty.reset()
        self.rankingPoints.reset()
        self.totalScore = 0

    def countScore(self):
        self.auto.countScore()
        self.telop.countScore()
        if (self.auto.speaker + self.auto.echo + self.telop.speaker + self.telop.echo >= 12):
            self.rankingPoints.melody = 1
        if (self.auto.leavePoints + self.telop.stagePoints >= 16):
            self.rankingPoints.ensemble = 1

    class Auto:
        def __init__(self):
            self.leave1 = 0
            self.leave2 = 0
            self.leavePoints = 0
            self.speaker = 0
            self.echo = 0
            self.points = 0

        def reset(self):
            self.leave1 = 0
            self.leave2 = 0
            self.speaker = 0
            self.echo = 0
            self.points = 0

        def countScore(self):
            self.points = 0
            self.leavePoints = 0
            if self.leave1 == 2:
                self.leavePoints += 6
            if self.leave1 == 1:
                self.leavePoints += 2
            if self.leave2 == 2:
                self.leavePoints += 6
            if self.leave2 == 1:
                self.leavePoints += 2

            self.points += self.leavePoints
            self.points += self.speaker*12
            self.points += self.echo*4

    class Telop:
        def __init__(self):
            self.speaker = 0
            self.echo = 0
            self.fortissiom = 0
            self.park1 = 0
            self.park2 = 0
            self.stagePoints = 0
            self.points = 0

        def reset(self):
            self.speaker = 0
            self.echo = 0
            self.fortissiom = 0
            self.park1 = 0
            self.park2 = 0
            self.stagePoints = 0
            self.points = 0

        def countScore(self):
            self.points = 0

            self.stagePoints = 0
            if self.park1 == 2:
                self.stagePoints += 5
            if self.park1 == 1:
                self.stagePoints += 3
            if self.park2 == 2:
                self.stagePoints += 5
            if self.park2 == 1:
                self.stagePoints += 3

            self.points += self.stagePoints
            self.points += self.speaker*5
            self.points += self.echo*(self.fortissiom+1)

    class Penalty:
        def __init__(self):
            self.foul = 0
            self.techFoul = 0
            self.points = 0

        def reset(self):
            self.foul = 0
            self.techFoul = 0
            self.points = 0

        def countScore(self):
            self.points = 0
            self.points += self.foul*5
            self.points += self.techFoul*8

    class RankingPoints:
        def __init__(self):
            self.melody = 0
            self.ensemble = 0
            self.win = 0

        def reset(self):
            self.melody = 0
            self.ensemble = 0
            self.win = 0


class Alliance:
    def __init__(self):
        self.team1 = ""
        self.team2 = ""
        self.score = Score()

    def reset(self):
        self.team1 = ""
        self.team2 = ""
        self.score.reset()

    def setTeam(self, team1, team2):
        self.team1 = team1
        self.team2 = team2


class Match:
    def __init__(self):
        self.status = "preparing"
        self.level = ""
        self.id = 0
        self.blue = Alliance()
        self.red = Alliance()

    def reset(self):
        self.status = "preparing"
        self.level = ""
        self.id = 0
        self.blue.reset()
        self.red.reset()


if __name__ == "__main__":
    m = Match()
    m.level = "aaa"
    print(m.level)
    m.reset()
    print(m.level)
