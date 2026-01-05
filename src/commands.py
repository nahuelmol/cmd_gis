
class Command:
    def __init__(self, args):
        self.ac     = False
        self.args   = args[1:]
        self.all    = True
        self.availableCoupledFlags  = ['-o', '-r', '-n', '-me', '-mo', '-ft', 
                                       '-rs', '-ts', 'w', '-cls', 'is']
        self.availableAloneFlags    = ['-f', '-all', '-ac', '-h', '-help', 'cm', 'cat', 'dis', 'box']
        self.aloneFlags = {}
        self.boxplot = False
        self.categorics = False
        self.changeField = ''
        self.class_ = 0
        self.currentFlags = {}
        self.cond = ''
        self.corr_matrix = False
        self.datatarget = ''
        self.dispersion = False
        self.h = False
        self.manyArgs   = len(self.args)
        self.message    = ''
        self.meth   = None
        self.mod    = None
        self.ncomps = 2
        self.number = 0
        self.random_state = 42
        self.ref        = None
        self.rootCommand = None
        self.target = None
        self.targetType = None
        self.test_size  = 0.2
        self.forced = False
        self.output = None
        self.options = []
        self.unique = False
        self.varType = None

    def setReference(self, ref):
        self.ref = ref

    def setCommand(self):
        self.rootCommand = self.args[0]

    def helper(self):
        if self.all == True:
            msg = """
            These are the main root commands:
            """
            print(msg)
        elif self.rootCommand == 'app':
            msg = """
            reference can be previously specified, or now too
            """
            print(msg)
        elif self.rootCommand == 'ch':
            msg = """
            """
            print(msg)
        elif self.rootCommand == 'cl':
            msg = """
            """
            print(msg)
        elif self.rootCommand == 'del':
            msg = """
            """
            print(msg)
        elif self.rootCommand == 'see':
            msg = """
            """
            print(msg)
        elif self.rootCommand == 'set':
            msg = """
            """
            print(msg)
        elif self.rootCommand == 'order':
            msg = """
            """
            print(msg)
        elif self.rootCommand == 'list':
            msg = """
            """
            print(msg)
        else:
            True, 'not command specified'
        True, 'well provided command'

    def default(self, flag):
        if flag == '-n':
            return 2
        elif flag == '-r':
            return self.ref
        elif flag == 'o':
            return self.output

    def addFlags(self):
        if '-r' in self.currentFlags:
            self.ref = self.currentFlags['-r']
        if '-o' in self.currentFlags:
            self.output = self.currentFlags['-o']
        if '-n' in self.currentFlags:
            self.ncomps = self.currentFlags['-n']
        if '-rs' in self.currentFlags:
            self.random_state   = float(self.currentFlags['-rs'])
        if '-ts' in self.currentFlags:
            self.test_size      = float(self.currentFlags['-ts'])
        if 'w' in self.currentFlags:
            self.all = False
            self.cond = self.currentFlags['w']
        if 'is' in self.currentFlags:
            self.all = False
            self.unique = True
            self.number = self.currentFlags['is']
        if '-cls' in self.currentFlags:
            self.class_ = int(self.currentFlags['-cls'])

        if '-ac' in self.aloneFlags:
            self.ac = True
        if '-all' in self.aloneFlags:
            self.all = True
        if '-f' in self.aloneFlags:
            self.forced = True
        if '-h' in self.aloneFlags:
            self.h = True
            self.h_cmd = self.rootCommand
        if 'cm' in self.aloneFlags:
            self.all = False
            self.corr_matrix = True
        if 'cat' in self.aloneFlags:
            self.all =  False
            self.categorics = True
        if 'dis' in self.aloneFlags:
            self.all = False
            self.dispersion = True
        if 'box' in self.aloneFlags:
            self.all = False
            self.boxplot = True
        if 'hst' in self.aloneFlags:
            self.all   = False
            self.histo = True

    def flagSetting(self):
        for flag in self.options:
            if flag in self.availableCoupledFlags:
                idx = self.options.index(flag)
                if not self.args[idx+1]:
                    print('{} without arg'.format(flag))
                    self.currentFlags[flag] = self.default(flag)
                else:
                    self.currentFlags[flag] = self.options[idx + 1]
            elif flag in self.availableAloneFlags:
                self.aloneFlags[flag] = True
        self.addFlags()

    def setArgs(self):
        if '-h' in self.args:
            self.h = True
            self.all = False
            return True, 'done'
        if self.rootCommand == 'map':
            if self.manyArgs > 1:
                self.targetType = self.args[1]
                self.options = self.args[2:]
            else:
                print('----there are more arguments')
        else:
            return False, '----not recognized root'
        return True, '----args setting'


