import dateutil.parser

class FMGSAnswer(object):
    def __init__(self, questionnumber, answer, actionplan=None, targetdate=None):
        self.quesionnumber = questionnumber
        self.answer = answer
        if answer == 'no':
            self.actionplan = actionplan
            self.targetdate = dateutil.parser.parse(targetdate)

class FMGS(object):
    def __init__(self, reference, type, subdate, answers=None):
        self.reference = reference
        self.type = type
        self.subdate = dateutil.parser.parse(subdate)
        if type == "FMGS":
            self.answers = answers

class RelationshipToSchool(object):
    def __init__(self, name, opendate, URN=None, UPIN=None, closeddate=None, tin=None, tout=None):
        self.name = name
        self.opendate = dateutil.parser.parse(opendate)

        if tin is None:
            self.hasTin = False
        else:
            self.hasTin = True
            self.tin = dateutil.parser.parse(tin)
        
        if URN is None:
            self.hasURN = False
        else:
            self.hasURN = True
            self.URN = int(URN)

        if UPIN is None:
            self.hasUPIN = False
        else:
            self.hasUPIN = True
            self.UPIN = int(UPIN)

        if closeddate is None:
            self.hasClosedDate = False
        else:
            self.hasClosedDate = True
            self.closeddate = dateutil.parser.parse(closeddate)

        if tout is None:
            self.hasTout = False
        else:
            self.hasTout = True
            self.tout = dateutil.parser.parse(tout)
        
class TrustHistory(object):
    def __init__(self, companyNumber, trustName, relationships, incorporationDate, dissolutionDate=None):
        self.companyNumber = int(companyNumber)
        self.trustName = trustName
        self.relationships = relationships
        self.incorporationDate = dateutil.parser.parse(incorporationDate)
        if dissolutionDate is None:
            self.hasDissolutionDate = False
        else:
            self.hasDissolutionDate = True
            self.dissolutionDate = dateutil.parser.parse(dissolutionDate)
        self.fmgsreturns = []

    def addFMGS(self, fmgs):
        self.fmgsreturns.append(fmgs)

class RelationshipToTrust(object):
    def __init__(self, name, incdate, coho, disdate=None, tin=None, tout=None):
        self.name = name
        self.incdate = dateutil.parser.parse(incdate)
        self.coho = int(coho)

        if disdate is None:
            self.hasDisDate = False
        else:
            self.hasDisDate = True
            self.disdate = dateutil.parser.parse(disdate)
        
        if tin is None:
            self.hasTin = False
        else:
            self.hasTin = True
            self.tin = dateutil.parser.parse(tin)
        
        if tout is None:
            self.hasTout = False
        else:
            self.hasTout = True
            self.tout = dateutil.parser.parse(tout)


class SchoolHistory(object):
    def __init__(self, schoolName, relationships, openDate, closedDate=None, URN=None, UPIN=None):
        self.schoolName = schoolName
        self.relationships = relationships
        self.openDate = dateutil.parser.parse(openDate)
        if closedDate is None:
            self.hasClosedDate = False
        else:
            self.hasClosedDate = True
            self.closedDate = dateutil.parser.parse(closedDate)

        if URN is None:
            self.hasURN = False
        else:
            self.hasURN = True
            self.URN = int(URN)

        if UPIN is None:
            self.hasUPIN = False
        else:
            self.hasUPIN = True
            self.UPIN = int(UPIN)

        self.fmgsreturns = []

    def addFMGS(self, fmgs):
        self.fmgsreturns.append(fmgs)