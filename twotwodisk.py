from exceptions import DuplicateParmError, MissingParmError

class TwoTwoDisk:

    required = ('density',
                'cylinders',
                'sides',
                'sectors',
                'side1',
                'bsh',
                'blm',
                'exm',
                'dsm',
                'drm',
                'al0',
                'al1',
                'ofs')
    
    def __init__(self, defname):
        self.defname = defname
        self.parameters = dict()
        self.comments = None

    # Attach a list of comments to the definition as a whole.
    def add_def_comments(self, list):
        if list is not None and len(list):
            self.def_comments = list

    # Add a parameter keyword and value to the definition
    def add_parameter(self, tok, val):
        name = tok.value.lower()
        if name in self.parameters:
            # Flag duplicated keyword
            raise DuplicateParmError(tok,None)
        else:
            self.parameters[name] = val

    def add_description(self, val):
        self.parameters['description'] = val
            
    # Return a dictionary of parameters
    def get_parameters(self):
        return self.parameters

    def finalize(self):
        missing = []
        for parm in TwoTwoDisk.required:
            if not parm in self.parameters:
                missing.append(parm.upper())
        if 'sides' in self.parameters and self.parameters['sides'] == 2:
            if not 'side2' in self.parameters:
                missing.append('SIDE2')
            if not 'order' in self.parameters:
                self.parameters['order'] = 'cylinders'
        if len(missing):
            raise MissingParmError(self.defname,missing)
        # Assume skew of 1 if not specified
        if not 'skew' in self.parameters:
            self.parameters['skew'] = 1
    
    def __str__(self):
        s = ""
        if self.comments is not None:
            for c in self.comments:
                s += "%s\n" % c
        s += "BEGIN %s %s\n" % (self.defname, self.parameters['description'])
        if 'see' in self.parameters:
            s += "SEE %s\n" % self.parameters['see'].upper()
        else:
            dens = self.parameters['density']
            s += "DENSITY %s,%s\n" % (dens[0].upper(), dens[1].upper())
            if 'complement' in self.parameters:
                s += "COMPLEMENT\n"
            if 'skip' in self.parameters:
                s += "SKIP\n"
            s += "CYLINDERS %d\n" % self.parameters['cylinders']
            s += "SIDES %d\n" % self.parameters['sides']
            s += "SECTORS %d,%d\n" % (self.parameters['sectors'][0], self.parameters['sectors'][1])
            value = self.parameters['side1']
            s += "SIDE1 %d %s\n" % (value[0], ','.join(str(i) for i in value[1]))
            if 'side2' in self.parameters:
                value = self.parameters['side2']
                s += "SIDE2 %d %s\n" % (value[0], ','.join(str(i) for i in value[1]))
            if 'order' in self.parameters:
                value = self.parameters['order']
                s += "ORDER %s" % value[0].upper()
                if value[1] is not None:
                    s += " %s" % value[1].upper()
                s += "\n"
            for parm in ('bsh','blm','exm','dsm','drm'):
                s += "%s %d " % (parm.upper(), self.parameters[parm])
            s += "\n"
            for parm in ('al0', 'al1'):
                s += parm.upper()
                value = self.parameters[parm]
                s += " {0:0{1}X}H ".format(value,3)
            s += "OFS %d\n" % self.parameters['ofs']
            s += "END\n"
        return s
