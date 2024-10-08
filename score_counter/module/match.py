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
    "red-melody-demand": "red.score.rankingPoints.melody_demand",
    "red-ensemble-demand": "red.score.rankingPoints.ensemble_demand",
    "blue-melody-demand": "blue.score.rankingPoints.melody_demand",
    "blue-ensemble-demand": "blue.score.rankingPoints.ensemble_demand"
}

resultToDBTable = {
    "red-total-score-with-penalty": "red.score.totalScoreWithPenalty",
    "blue-total-score-with-penalty": "blue.score.totalScoreWithPenalty",
    "red-melody": "red.score.rankingPoints.melody",
    "blue-melody": "blue.score.rankingPoints.melody",
    "red-ensemble": "red.score.rankingPoints.ensemble",
    "blue-ensemble": "blue.score.rankingPoints.ensemble",
    "winner": "winner"
}
detaToDBTable = {
    "match-level": "level",
    "match-id": "id",
    "red-team1": "red.team1",
    "blue-team1": "blue.team1",
    "red-team2": "red.team2",
    "blue-team2": "blue.team2",
    "red-auto-leave1": "red.score.auto.leave1",
    "blue-auto-leave1": "blue.score.auto.leave1",
    "red-auto-leave2": "red.score.auto.leave2",
    "blue-auto-leave2": "blue.score.auto.leave2",
    "red-auto-leavePoints": "red.score.auto.leavePoints",
    "blue-auto-leavePoints": "blue.score.auto.leavePoints",
    "red-auto-speaker": "red.score.auto.speaker",
    "blue-auto-speaker": "blue.score.auto.speaker",
    "red-auto-echo": "red.score.auto.echo",
    "blue-auto-echo": "blue.score.auto.echo",
    "red-auto-foul": "red.score.penalty.auto.foul",
    "blue-auto-foul": "blue.score.penalty.auto.foul",
    "red-auto-techFoul": "red.score.penalty.auto.techFoul",
    "blue-auto-techFoul": "blue.score.penalty.auto.techFoul",
    "red-auto-total-point": "red.score.auto.points",
    "blue-auto-total-point": "blue.score.auto.points",
    "red-telop-speaker": "red.score.telop.speaker",
    "blue-telop-speaker": "blue.score.telop.speaker",
    "red-telop-echo": "red.score.telop.echo",
    "blue-telop-echo": "blue.score.telop.echo",
    "red-telop-fortissimo": "red.score.telop.fortissimo",
    "blue-telop-fortissimo": "blue.score.telop.fortissimo",
    "red-telop-foul": "red.score.penalty.telop.foul",
    "blue-telop-foul": "blue.score.penalty.telop.foul",
    "red-telop-techFoul": "red.score.penalty.telop.techFoul",
    "blue-telop-techFoul": "blue.score.penalty.telop.techFoul",
    "red-telop-park1": "red.score.telop.park1",
    "blue-telop-park1": "blue.score.telop.park1",
    "red-telop-park2": "red.score.telop.park2",
    "blue-telop-park2": "blue.score.telop.park2",
    "red-telop-stagePoints": "red.score.telop.stagePoints",
    "blue-telop-stagePoints": "blue.score.telop.stagePoints",
    "red-telop-total-point": "red.score.telop.points",
    "blue-telop-total-point": "blue.score.telop.points",
    "red-melody-demand": "red.score.rankingPoints.melody_demand",
    "blue-melody-demand": "blue.score.rankingPoints.melody_demand",
    "red-ensemble-demand": "red.score.rankingPoints.ensemble_demand",
    "blue-ensemble-demand": "blue.score.rankingPoints.ensemble_demand",
    "red-total-score": "red.score.totalScore",
    "blue-total-score": "blue.score.totalScore",
    "red-total-penalty": "red.score.penalty.points",
    "blue-total-penalty": "blue.score.penalty.points"
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
        self.penalty.countScore()
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
            self.total = 0

        def reset(self):
            self.melody = 0
            self.melody_demand = 0
            self.ensemble = 0
            self.ensemble_demand = 0
            self.win = 0
            self.total = 0


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
        self.winner = ""
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

    def end_match_settle(self):
        self.countScore()
        self.red.score.totalScoreWithPenalty = self.red.score.totalScore + \
            self.blue.score.penalty.points
        self.blue.score.totalScoreWithPenalty = self.blue.score.totalScore + \
            self.red.score.penalty.points
        if self.red.score.totalScoreWithPenalty > self.blue.score.totalScoreWithPenalty:
            self.winner = "red"
            self.red.score.rankingPoints.win = 2
        elif self.red.score.totalScoreWithPenalty < self.blue.score.totalScoreWithPenalty:
            self.winner = "blue"
            self.blue.score.rankingPoints.win = 2
        else:
            self.winner = "tie"
            self.red.score.rankingPoints.win = 1
            self.blue.score.rankingPoints.win = 1
        self.red.score.rankingPoints.total = self.red.score.rankingPoints.melody + \
            self.red.score.rankingPoints.ensemble + \
            self.red.score.rankingPoints.win
        self.blue.score.rankingPoints.total = self.blue.score.rankingPoints.melody + \
            self.blue.score.rankingPoints.ensemble + \
            self.blue.score.rankingPoints.win

    def get_match_result(self):
        result_datas = []
        for key in resultToDBTable:
            result_data = {}
            result_data["id"] = key
            result_data["value"] = get_nested_attribute(
                self, resultToDBTable[key])
            result_datas.append(result_data)
        return result_datas

    def get_detail_data(self):
        result_datas = []
        for key in detaToDBTable:
            result_data = {}
            result_data["id"] = key
            result_data["value"] = get_nested_attribute(
                self, detaToDBTable[key])
            result_datas.append(result_data)
        return result_datas


if __name__ == "__main__":
    m = Match()
    m.level = "aaa"
    print(m.level)
    print(type(m.__dict__["blue"]) == type(classmethod))
    m.reset()
    print(m[""])
