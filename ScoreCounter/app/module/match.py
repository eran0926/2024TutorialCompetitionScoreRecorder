from module.utils import get_nested_attribute

recorderIdToObjectNameTable = {
    "team1-select": "team1",
    "team2-select": "team2",
    "auto-leave-select1": "score.auto.leave1",
    "auto-leave-select2": "score.auto.leave2",
    "auto-speaker-btn": "score.auto.speaker",
    "auto-echo-btn": "score.auto.echo",
    "auto-foul-btn": "score.penalty.auto.foul",
    "auto-tech-foul-btn": "score.penalty.auto.techFoul",
    "telop-speaker-btn": "score.telop.speaker",
    "telop-echo-btn": "score.telop.echo",
    "telop-fortissimo-btn": "score.telop.fortissimo",
    "telop-park-select1": "score.telop.park1",
    "telop-park-select2": "score.telop.park2",
    "telop-foul-btn": "score.penalty.telop.foul",
    "telop-tech-foul-btn": "score.penalty.telop.techFoul"
}

boardIdToObjectNameTable = {
    "red-score": "red.score.totalScore",
    "blue-score": "blue.score.totalScore",
    "red-melody-demand": "red.score.rankingPoints.melody",
    "red-ensemble-demand": "red.score.rankingPoints.ensemble",
    "blue-melody-demand": "blue.score.rankingPoints.melody",
    "blue-ensemble-demand": "blue.score.rankingPoints.ensemble",
}


class Score:
    def __init__(self):
        self.auto = self.Auto()
        self.telop = self.Telop()
        self.penalty = self.Penalty()
        self.rankingPoints = self.RankingPoints()
        self.totalScore = 0
        self.totalScoreWithPenalty = 0

    def reset(self):
        self.auto.reset()
        self.telop.reset()
        self.penalty.reset()
        self.rankingPoints.reset()
        self.totalScore = 0
        self.totalScoreWithPenalty = 0

    def countScore(self):
        self.auto.countScore()
        self.telop.countScore()
        self.totalScore = self.auto.points + self.telop.points

        self.rankingPoints.melody_demand = self.auto.speaker + \
            self.auto.echo + self.telop.speaker + self.telop.echo
        self.rankingPoints.ensemble_demand = self.auto.leavePoints + self.telop.stagePoints

        if (self.rankingPoints.melody_demand >= 12):
            self.rankingPoints.melody = 1
        if (self.rankingPoints.ensemble_demand >= 16):
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
            self.fortissimo = 0
            self.park1 = 0
            self.park2 = 0
            self.stagePoints = 0
            self.points = 0

        def reset(self):
            self.speaker = 0
            self.echo = 0
            self.fortissimo = 0
            self.park1 = 0
            self.park2 = 0
            self.stagePoints = 0
            self.points = 0

        def countScore(self):
            self.points = 0

            if self.fortissimo > 2:
                self.fortissimo = 2

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
            self.points += self.echo*(self.fortissimo+1)

    class Penalty:
        def __init__(self):
            self.auto = self.Auto()
            self.telop = self.Telop()
            self.auto.foul = 0
            self.auto.techFoul = 0
            self.telop.foul = 0
            self.telop.techFoul = 0
            self.points = 0

        def reset(self):
            self.auto.foul = 0
            self.auto.techFoul = 0
            self.telop.foul = 0
            self.telop.techFoul = 0
            self.points = 0

        def countScore(self):
            self.points = 0
            self.points += (self.auto.foul + self.telop.foul)*5
            self.points += (self.telop.foul + self.telop.techFoul)*8

        class Auto:
            def __init__(self):
                self.foul = 0
                self.techFoul = 0

        class Telop:
            def __init__(self):
                self.foul = 0
                self.techFoul = 0

    class RankingPoints:
        def __init__(self):
            self.melody = 0
            self.melody_demand = 0
            self.ensemble = 0
            self.ensemble_demand = 0
            self.win = 0

        def reset(self):
            self.melody = 0
            self.melody_demand = 0
            self.ensemble = 0
            self.ensemble_demand = 0
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

    def countScore(self):
        self.score.countScore()

    def get_all_recorder_data(self):
        recorder_datas = []
        for key in recorderIdToObjectNameTable:
            recorder_data = {}
            recorder_data["id"] = key
            recorder_data["value"] = get_nested_attribute(
                self, recorderIdToObjectNameTable[key])
            recorder_datas.append(recorder_data)
        return recorder_datas

    # def recorderIdToObject(self, id):
    #     recorderIdToObjectNameTable = {
    #         "team1-select": self.team1,
    #         "team2-select": self.team2,
    #         "auto-leave-select1": self.score.auto.leave1,
    #         "auto-leave-select2": self.score.auto.leave2,
    #         "auto-speaker-btn": self.score.auto.speaker,
    #         "auto-echo-btn": self.score.auto.echo,
    #         "auto-foul-btn": self.score.penalty.auto.foul,
    #         "auto-tech-foul-btn": self.score.penalty.auto.techFoul,
    #         "telop-speaker-btn": self.score.telop.speaker,
    #         "telop-echo-btn": self.score.telop.echo,
    #         "telop-fortissimo-btn": self.score.telop.fortissimo,
    #         "telop-park-select1": self.score.telop.park1,
    #         "telop-park-select2": self.score.telop.park2,
    #         "telop-foul-btn": self.score.penalty.telop.foul,
    #         "telop-tech-foul-btn": self.score.penalty.telop.techFoul
    #     }

    #     return recorderIdToObjectTable[id]


class Match:
    def __init__(self):
        self.state = "Not Started"
        self.level = ""
        self.id = 0
        self.red = Alliance()
        self.blue = Alliance()
        self.alliance = {"red": self.red, "blue": self.blue}
        self.recorder = set()
        self.commitedRecorder = set()
        # self.recorder = list()
        # self.commitedRecorder = list()

    def reset(self):
        self.state = "Not Started"
        self.level = ""
        self.id = 0
        self.red.reset()
        self.blue.reset()
        # self.commitedRecorder = list()
        # self.recorder = set()
        self.commitedRecorder = set()

    def countScore(self):
        self.red.countScore()
        self.blue.countScore()

    def allCommited(self):
        # self.recorder.sort()
        # self.commitedRecorder.sort()
        return self.recorder == self.commitedRecorder

    def recorderIdToObject(self, id):
        recorderIdToObjectTable = {
            "level-select": self.level,
            "matchNumberInput": self.id,
        }
        return recorderIdToObjectTable[id]

    def get_all_recorder_data(self, alliance):
        if alliance == "red":
            return self.red.get_all_recorder_data()
        elif alliance == "blue":
            return self.blue.get_all_recorder_data()
        return []

    def get_all_board_data(self):
        board_datas = []
        for key in boardIdToObjectNameTable:
            board_data = {}
            board_data["id"] = key
            board_data["value"] = get_nested_attribute(
                self, boardIdToObjectNameTable[key])
            board_datas.append(board_data)
        return board_datas

    def loadMatch(self, match_data):
        self.reset()
        # self.level = match_data["level"]
        # self.id = match_data["id"]
        # self.red.setTeam(match_data["red"]["team1"],
        #                  match_data["red"]["team2"])
        # self.blue.setTeam(match_data["blue"]["team1"],
        #                   match_data["blue"]["team2"])
        self.level = match_data[0]
        self.id = match_data[1]
        self.red.setTeam(match_data[2],
                         match_data[3])
        self.blue.setTeam(match_data[4],
                          match_data[5])


if __name__ == "__main__":
    m = Match()
    m.level = "aaa"
    print(m.level)
    print(type(m.__dict__["blue"]) == type(classmethod))
    m.reset()
    print(m[""])
