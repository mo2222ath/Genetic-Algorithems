class Fuzzy:

    def equ_VLowDown(x):
        return ((-x / 20) + 1.5)

    def equ_lowUp(x):
        return ((x / 20) - 0.5)

    def equ_lowDown(x):
        return ((-x / 20) + 3)

    def equ_mediumUp(x):
        return ((x / 20) - 2)

    def equ_mediumDown(x):
        return ((-x / 20) + 4.5)

    def equ_highUp(x):
        return ((x / 20) - 3.5)

    def equ_beginnerDown(x):
        return ((-x / 15) + 2)

    def equ_intermediateUp(x):
        return ((x / 15) - 1)

    def equ_intermediateDown(x):
        return ((-x / 15) + 3)

    def equ_expertUp(x):
        return ((x / 30) - 1)

    def getMembershipValuesForVariable1(x):

        dictionary = {}

        if x >= 0 and x <= 10:
            dictionary['VL'] = 1
            dictionary['L'] = 0
            dictionary['M'] = 0
            dictionary['H'] = 0

        if x > 10 and x < 30:
            dictionary['VL'] = Fuzzy.equ_VLowDown(x)
            dictionary['L'] = Fuzzy.equ_lowUp(x)
            dictionary['M'] = 0
            dictionary['H'] = 0

        if x >= 30 and x <= 40:
            dictionary['L'] = 1
            dictionary['VL'] = 0
            dictionary['M'] = 0
            dictionary['H'] = 0

        if x > 40 and x < 60:
            dictionary['L'] = Fuzzy.equ_lowDown(x)
            dictionary['M'] = Fuzzy.equ_mediumUp(x)
            dictionary['VL'] = 0
            dictionary['H'] = 0

        if x >= 60 and x <= 70:
            dictionary['M'] = 1
            dictionary['VL'] = 0
            dictionary['L'] = 0
            dictionary['H'] = 0

        if x > 70 and x < 90:
            dictionary['M'] = Fuzzy.equ_mediumDown(x)
            dictionary['H'] = Fuzzy.equ_highUp(x)
            dictionary['VL'] = 0
            dictionary['L'] = 0

        if x >= 90 and x <= 100:
            dictionary['H'] = 1
            dictionary['VL'] = 0
            dictionary['L'] = 0
            dictionary['M'] = 0

        return dictionary

    def getMembershipValuesForVariable2(x):

        dictionary = {}

        if x >= 0 and x <= 15:
            dictionary['B'] = 1
            dictionary['I'] = 0
            dictionary['E'] = 0

        if x > 15 and x < 30:
            dictionary['B'] = Fuzzy.equ_beginnerDown(x)
            dictionary['I'] = Fuzzy.equ_intermediateUp(x)
            dictionary['E'] = 0

        if x == 30:
            dictionary['I'] = 1
            dictionary['B'] = 0
            dictionary['E'] = 0

        if x > 30 and x < 45:
            dictionary['I'] = Fuzzy.equ_intermediateDown(x)
            dictionary['E'] = Fuzzy.equ_expertUp(x)
            dictionary['B'] = 0

        if x >= 45 and x <= 60:
            dictionary['E'] = Fuzzy.equ_expertUp(x)
            dictionary['B'] = 0
            dictionary['I'] = 0
        return dictionary

    def inferenceAndDefuzz(self,ruleList,projectFundDict,teamExpDict):
        defuzzList = list()
        fuzzList = list()
        for rule in ruleList:
            projectFuzzVal = 0
            teamExpFuzzVal = 0
            inferredRule = 0
            defuzzifiedVal = 0
            wordList = rule.split()
            for word in wordList:

                if word == 'or':
                   lst = rule.split('or')
                   projectFundRule = lst[0].split()                   #Project funding and its fuzzy value
                   teamExp_risk = lst[1].split('then')
                   teamExpRule = teamExp_risk[0]                        #Team Experience and its fuzzy value
                   riskRule = teamExp_risk[1]

                   if teamExpRule.__contains__('beginner'):
                        teamExpFuzzVal = teamExpDict['B']
                   elif teamExpRule.__contains__('intermediate'):
                       teamExpFuzzVal = teamExpDict['I']
                   elif teamExpRule.__contains__('expert'):
                       teamExpFuzzVal = teamExpDict['E']

                   if projectFundRule.__contains__('high'):
                        projectFuzzVal = projectFundDict['H']
                   elif projectFundRule.__contains__('medium'):
                       projectFuzzVal = projectFundDict['M']
                   elif projectFundRule.__contains__('low'):
                       projectFuzzVal = projectFundDict['L']
                   if projectFundRule.__contains__('very low'):
                       projectFuzzVal = projectFundDict['VL']

                   inferredRule = max(projectFuzzVal,teamExpFuzzVal)

                   if riskRule.__contains__('low'):
                       centroidLow = (50 + 100 + 100) / 3
                       defuzzifiedVal = centroidLow * inferredRule
                       break
                   if riskRule.__contains__('normal'):
                       centroidMed = (25 + 50 + 75) / 3
                       defuzzifiedVal = centroidMed * inferredRule
                       break
                   if riskRule.__contains__('high'):
                       centroidHigh = (0 + 25 + 50) / 3
                       defuzzifiedVal = centroidHigh * inferredRule
                       break


                elif word == 'and':
                    lst = rule.split('and')
                    projectFundRule = lst[0].split()            # Project funding and its fuzzy value
                    teamExp_risk = lst[1].split('then')
                    teamExpRule = teamExp_risk[0]               # Team Experience and its fuzzy value
                    riskRule = teamExp_risk[1]

                    if teamExpRule.__contains__('or'):          #Case of rule 2
                        teamExpFuzzVal1 = teamExpDict['I']
                        teamExpFuzzVal2 = teamExpDict['B']
                        teamExpFuzzVal = max(teamExpFuzzVal1,teamExpFuzzVal2)
                    elif teamExpRule.__contains__('and'):
                        teamExpFuzzVal1 = teamExpDict['I']
                        teamExpFuzzVal2 = teamExpDict['B']
                        teamExpFuzzVal = min(teamExpFuzzVal1,teamExpFuzzVal2)
                    else:
                        if teamExpRule.__contains__('beginner'):
                            teamExpFuzzVal = teamExpDict['B']
                        elif teamExpRule.__contains__('intermediate'):
                            teamExpFuzzVal = teamExpDict['I']
                        elif teamExpRule.__contains__('expert'):
                            teamExpFuzzVal = teamExpDict['E']

                    if projectFundRule.__contains__('high'):
                        projectFuzzVal = projectFundDict['H']
                    elif projectFundRule.__contains__('medium'):
                        projectFuzzVal = projectFundDict['M']
                    elif projectFundRule.__contains__('low'):
                        projectFuzzVal = projectFundDict['L']
                    if projectFundRule.__contains__('very low'):
                        projectFuzzVal = projectFundDict['VL']

                    inferredRule = min(projectFuzzVal, teamExpFuzzVal)

                    if riskRule.__contains__('low'):
                        centroidLow = (50 + 100 + 100) / 3
                        defuzzifiedVal = centroidLow * inferredRule
                        break
                    if riskRule.__contains__('normal'):
                        centroidMed = (25 + 50 + 75) / 3
                        defuzzifiedVal = centroidMed * inferredRule
                        break
                    if riskRule.__contains__('high'):
                        centroidHigh = (0 + 25 + 50) / 3
                        defuzzifiedVal = centroidHigh * inferredRule
                        break


                elif word == 'then':                                       #Case of rule 3
                    lst = rule.split('then')
                    projectFundRule = lst[0]
                    riskRule = lst[1]

                    if projectFundRule.__contains__('high'):
                        projectFuzzVal = projectFundDict['H']
                    elif projectFundRule.__contains__('medium'):
                        projectFuzzVal = projectFundDict['M']
                    elif projectFundRule.__contains__('low'):
                        projectFuzzVal = projectFundDict['L']
                    if projectFundRule.__contains__('very low'):
                        projectFuzzVal = projectFundDict['VL']

                    inferredRule = projectFuzzVal

                    if riskRule.__contains__('low'):
                        centroidLow = (50 + 100 + 100) / 3
                        defuzzifiedVal = centroidLow * inferredRule
                        break
                    if riskRule.__contains__('normal'):
                        centroidMed = (25 + 50 + 75) / 3
                        defuzzifiedVal = centroidMed * inferredRule
                        break
                    if riskRule.__contains__('high'):
                        centroidHigh = (0 + 25 + 50) / 3
                        defuzzifiedVal = centroidHigh * inferredRule
                        break

            defuzzList.append(defuzzifiedVal)
            fuzzList.append(inferredRule)

        predictedRiskValue = sum(defuzzList)/sum(fuzzList)

        return predictedRiskValue


#print(Fuzzy.equ_expertUp(20))
# print(Fuzzy.getMembershipValuesForVariable1(30))
# print(Fuzzy.getMembershipValuesForVariable2(29))

if __name__ == '__main__':
    rule1 = "If project_funding is high or team_experience_level is expert then risk is low."
    rule2 = "If project_funding is medium and team_experience_level is intermediate " \
            "or team_experience_level is beginner then risk is normal."
    rule3 = "If project_funding is very low then risk is high."
    rule4 = "If project_funding is low and team_experience_level is beginner then risk is high."

    rulelst = list()

    rulelst.append(rule1)
    rulelst.append(rule2)
    rulelst.append(rule3)
    rulelst.append(rule4)

    projectFundingFuzzDict = Fuzzy.getMembershipValuesForVariable1(50)
    teamExperienceFuzzDict = Fuzzy.getMembershipValuesForVariable2(40)

    predictedValue = Fuzzy.inferenceAndDefuzz(Fuzzy,rulelst,projectFundingFuzzDict,teamExperienceFuzzDict)
    print(predictedValue)