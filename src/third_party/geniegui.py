# geniegui
# (c) Sven Rahmann, 2011--2012

# Source: https://code.google.com/p/amplikyzer/
# MIT License

"""
The functions of the geniegui module examine an argparse.ArgumentParser object
and create a tkinter GUI for it that allows to edit in all option values.
The given default values are shown,
and by default optional options are disabled.
"""

# This needs Python 3.2 and Tk/Tcl distribution 8.5. ++
#
# Windows:
# I found that it just works with standard Python 3.2.
# For using it with virtualenv, however, explicitly set
# the environment variable TCL_LIBRARY = D:\Python32\tcl\tcl85
# (or wherever the .dll is located)
#
# Mac:
# The best idea is to download the community edition from ActiveState.
# Also it cannot hurt to set TCL_LIBRARY.
#
# Linux:
# I also use the ActiveState distribution.
# If the only problem is that the tile package is missing,
# see http://sourceforge.net/projects/tktable/files/, 
# but I have never been able to install it properly.
#
# DEFINITELY read these pages:
# http://www.tkdocs.com/tutorial/

import sys
import shlex
import argparse
import multiprocessing
import io
from collections import OrderedDict
from contextlib import contextmanager

from tkinter import ttk
from tkinter import *
from tkinter.ttk import *
from tkinter import filedialog, scrolledtext


############################# DEBUG ###########################
def print_attributes(obj):
    for k,v in obj.items():
        print(k, ":", type(v))
    print()


############################# STUFF ###########################
def _optstr(fromdefault, nargs=None):
    if nargs is None:
        return str(fromdefault)
    # else return string from the list
    return "  ".join("'{}'".format(str(x)) for x in fromdefault)

def _optlist(fromstring, nargs=None):
    if nargs is None: return [fromstring]
    result = shlex.split(fromstring)
    if nargs=="+" and len(result)==0:
        # must return at least an empty string
        return [""]
    if nargs=="?" and len(result) > 1:
        return [fromstring]
    return result

def _expandingframe(tkmaster, sticky="NSWE"):
    frame = Frame(tkmaster)
    frame.configure(padding=2) 
    frame.grid(column=0, row=0, sticky=sticky)
    frame.columnconfigure(0, weight=1)  # expand on resize
    frame.rowconfigure(0, weight=1)  # expand on resize
    return frame


@contextmanager
def std_redirector(stdin=None, stdout=None, stderr=None):
    if stdin is None: stdin = sys.stdin
    if stdout is None: stdout = sys.stdout
    if stderr is None: stderr = sys.stderr
    tmp_fds = stdin, stdout, stderr
    orig_fds = sys.stdin, sys.stdout, sys.stderr
    sys.stdin, sys.stdout, sys.stderr = tmp_fds
    yield
    sys.stdin, sys.stdout, sys.stderr = orig_fds


############################# action handlers ###########################
# these handlers define how to extend a tk widget when given
# an argparse action

def _create_entry_field(element, action, textwidth=50, nargs=None,
                        checkbuttonvar=None, special=None):
    """create a text entry field and return the corresponding Tk string variable
    (or do nothing, depending on the action type.
    The 'checkbuttonvar' parameter can be a checkbutton's IntVar
    that is set to 1 if the text changes, or None.
    The 'special' parameter creates a file or directory dialog button if set
    to "file" or "dir" respectively.
    """
    t = type(action)
    if t is argparse._StoreTrueAction:
        return None
    elif t is argparse._StoreConstAction:
        return None
    elif t is argparse._StoreAction:
        # create a corresponding Tk variable, set default, bind checkbutton
        var = StringVar()
        if action.default is not None:
            var.set(_optstr(action.default, nargs=nargs))
        if checkbuttonvar is not None:
            def activateoption(varname,varindex,varaccess):
                if var != "":  checkbuttonvar.set(1)
            var.trace_variable("w", activateoption)
        # Create the appropriate entry field type (text or choice)
        if action.choices is None:
            # normal entry field
            entry = Entry(element, textvariable=var, width=textwidth)
            entry.grid(row=1, column=0, sticky="NW")
            if special is not None:
                if special == "dir":
                    def cmd():
                        result = filedialog.askdirectory(initialdir=var.get(), parent=element)
                        if result != "": var.set(result)
                elif special == "file":
                    def cmd():
                        result = filedialog.askopenfilename(initialdir=var.get(), parent=element)
                        if result != "": var.set(result)
                if special in {"dir","file"}:
                    btn = Button(element, text="...", width=2, command=cmd)
                    btn.grid(row=1, column=1, sticky="NE")
                else:
                    raise NotImplementedError("unknown special {}".format(special))
        else:  # action has choices -> do a Radiobox array
            radiobox = Frame(element)
            radiobox.grid(row=1, column=0, sticky="NW")
            for ch in action.choices:
                btn = Radiobutton(radiobox, text=ch, variable=var, value=ch)
                btn.pack(anchor=N, side=LEFT, ipadx=5)
        return var
    # action not defined?
    else:
        print(action.__class__)
        print(action.choices)
        raise NotImplementedError(str(t))


def _do_nothing(gui, action):
    pass

def _add_store_action(gui, action, optional=True):
    parent = gui.mainframe
    oprefix = gui.optionprefix
    if optional:
        name = dname = action.option_strings[0]
    else:
        dname = action.dest
        name = "__" + str(gui.nextpos) + "__" + dname
        gui.nextpos += 1
    # process nargs
    # gui.listoption is a dict() with nargs-values
    gui.listoption[name] = None
    helptext = ""
    if action.nargs:  # not None or 0
        helptext = "<{}> ".format(str(action.nargs))
        gui.listoption[name] = str(action.nargs)
    # lay out the GUI elements for this action
    optionlabel = Label(parent, text=dname)
    optionlabel.grid(row=gui.nrows, column=0, sticky="NW")
    state = NORMAL if optional else DISABLED
    required = not optional
    gui.useoptions[name] = IntVar()
    gui.useoptions[name].set(0 if optional else 1)
    optionbox = Checkbutton(parent, state=state, variable=gui.useoptions[name])
    optionbox.grid(row=gui.nrows, column=1, sticky="NW")
    element = Frame(parent)
    element.grid(row=gui.nrows, column=2, sticky="NW")
    helptext += action.help
    helplabel = Label(element, text=helptext, justify=LEFT)
    helplabel.grid(row=0, column=0, sticky="NW")
    mynargs = gui.listoption[name]
    myspecial = gui.specials.get(name, None)
    gui.options[name] = _create_entry_field(element, action, nargs=mynargs,
        checkbuttonvar=gui.useoptions[name], special=myspecial)
    # spacers
    #hspacer = Frame(parent, width=20)
    #hspacer.grid(row=gui.nrows, column=3, sticky="NW")
    gui.nrows += 1
    vspacer = Frame(parent, height=5)
    vspacer.grid(row=gui.nrows, column=0, columnspan=4, sticky="NSWE")
    gui.nrows += 1


def _add_subparsers_action(gui, action):
    subparsers = action.choices  # this is an OrderedDict.
    subcommands = [k for k in subparsers.keys() if k != "GUI"]
    #print("subparsers with subcommands:", subcommands)
    parent = gui.mainframe
    notebook = Notebook(parent)
    notebook.grid(row=gui.nrows, column=0, columnspan=3, sticky="NW")
    scdescription = dict()
    for pseudoaction in action._choices_actions:  # need to use internals
        scdescription[pseudoaction.dest] = pseudoaction.dest + ": " + pseudoaction.help
    for sc in subcommands:
        subframe = Frame(notebook)
        notebook.add(subframe, text=sc)
        subparser = ArgparseGUI(subparsers[sc], guimaster=gui, title=sc,
            tkmaster=subframe, description=scdescription[sc])
        gui.subparsers[sc]=subparser
    gui.nrows += 1
    gui.nofinalbuttons = True

def _add_posstore_action(gui, action):
    _add_store_action(gui, action, optional=False)


# define which function to call for the different types of argparse actions
optactionhandlers = {
    argparse._HelpAction: _do_nothing,
    argparse._StoreAction: _add_store_action,
    argparse._StoreTrueAction: _add_store_action,
    argparse._StoreConstAction: _add_store_action,
    }

posactionhandlers = {
    argparse._SubParsersAction: _add_subparsers_action,
    argparse._StoreAction: _add_posstore_action,
    }

########### the main GUI frame #######################################

class ArgparseGUI():
    def __init__(self, parser, mainmethod=None, guimaster=None,
                 tkmaster=None, title=None, description=None):
        """create a GUI instance from argparse instance 'parser'
        inside TK toplevel 'tkwindow' with an optional 'title'
        and 'description'"""
        if tkmaster is None:
            tkmaster = Tk()
            ttkstyle = Style()
            ttkstyle.configure("Information.TLabel", foreground="blue", wraplength=640, justify=LEFT)
        if guimaster is None:
            self.window = tkmaster
            if title is not None: tkmaster.title(title)
            self.name = "__main__"
        else:
            self.window = guimaster.window
            self.name = title
        self.mainmethod = mainmethod
        self.guimaster = guimaster
        self.parser = parser
        self.specials = parser._geniegui if hasattr(parser, "_geniegui") else dict()
        self.optionprefix = parser.prefix_chars[0]
        self.useoptions = OrderedDict()
        self.listoption = dict()
        self.options = dict()
        self.subparsers = dict()
        self.nofinalbuttons = False
        self.mainframe = _expandingframe(tkmaster)
        self.nrows = 0
        self.command = "__CANCEL__"
        self.nextpos = 0
        #print_attributes(parser.__dict__)
        self.processes = dict()  # running processes -- see runcommand
        self.create_gui(description)
        
    def create_gui(self, description=None):
        """create tkinter GUI with a given TK 'master' object
        from ArgumentParser object 'parser'."""
        # put mainframe into the root tkwindow using the grid manager
        mainframe = self.mainframe
        parser = self.parser
        # description of the program
        if description is None:
            desc = parser.description if parser.description is not None else ""
        else:
            desc = description
        ldesc = Label(mainframe, text=desc, style="Information.TLabel")
        ldesc.grid(row=self.nrows, column=0, columnspan=3, sticky="W", padx=5, pady=5)
        self.nrows += 1
        
        # examine parser for all options, option groups, mutex groups, subparsers
        for action in parser._get_optional_actions():
            handler = optactionhandlers[type(action)]
            handler(self, action)
        for action in parser._get_positional_actions():
            handler = posactionhandlers[type(action)]
            handler(self, action)
        # final start/cancel buttons and epilog
        self.create_final_buttons()
        mainframe.epilog = Label(mainframe, text=parser.epilog, style="Information.TLabel")
        mainframe.epilog.grid(row=self.nrows, column=0, columnspan=3, sticky="E")
        self.nrows += 1
        
    def create_final_buttons(self):
        if self.nofinalbuttons: return
        self.nrows += 1
        frame = Frame(self.mainframe)
        frame.grid(row=self.nrows, column=2, sticky="E")
        self.nrows += 1
        bstart = Button(frame, text="Start", padding=5,
                        command = lambda x=self.name: self.runcommand(x))
        bstart.pack(side=LEFT)
        bcancel = Button(frame, text="Quit", padding=5,
                         command = lambda x="__CANCEL__": self.runcommand(x))
        bcancel.pack(side=LEFT)

    def poll(self):
        toremove = []
        for pid, pdict in self.processes.items():
            #print("polling", pid)
            text = pdict["pipe"].read()
            pdict["outfield"].insert(END,text)
            p = pdict["process"]
            if not p.is_alive():
                toremove.append(pid)
                pdict["whenfinished"]()
        for pid in toremove:
            del self.processes[pid]
        self.window.after(1000, self.poll)

    def arguments(self):
        args = list()
        for name, tkvar in self.useoptions.items():
            if tkvar.get() == 0: continue  # option not used
            if name.startswith(self.optionprefix):
                # true option, not positional argument
                args.append(name)
            optvar = self.options[name]
            if optvar is None: continue  # flag only
            optstr = optvar.get()  # the string
            args.extend(_optlist(optstr, nargs=self.listoption[name]))
        if self.command in self.subparsers:
            args.append(self.command)
            args.extend(self.subparsers[self.command].arguments())
        return args

    def runcommand(self, cmd):
        # get topmost instance and its arguments
        instance = self
        while instance.guimaster is not None: instance = instance.guimaster
        if cmd == "__CANCEL__":
            self.window.destroy()  # not instance.window?
            return
        instance.command = cmd
        args = instance.arguments()
        processtitle = instance.window.title()+"  "+" ".join(args)
        pdict = newguiprocess(instance.window, processtitle, instance.mainmethod, args)
        pid = pdict["process"].pid
        instance.processes[pid] = pdict

############################# processing ###########################

class TextPipe():
    def __init__(self):
        self.connrecv, self.connsend = multiprocessing.Pipe(duplex=False)
    def write(self, string):
        self.connsend.send(string)
    def read(self):
        reader = self.connrecv
        textlist = []
        while reader.poll():
            textlist.append(reader.recv())
        return "".join(map(str,textlist))
    def flush(self):
        pass

def newguiprocess(tkmaster, processtitle, mainmethod, args):
    # Create a new window with a title, textbox and close button
    popup = Toplevel(tkmaster)
    popup.title(processtitle)
    pframe = _expandingframe(popup)
    plabel = Label(pframe, text=processtitle, style="Information.TLabel")
    plabel.grid(row=0, column=0, sticky="NW")
    poutputfield = scrolledtext.ScrolledText(pframe)
    poutputfield.grid(row=1, column=0, sticky="NW")
    pbottomframe = _expandingframe(pframe)
    pbottomframe.grid(row=2, column=0, sticky="SWE")
    pbottomlabel = Label(pbottomframe, text="Running...", style="Information.TLabel")
    pbottomlabel.grid(row=0, column=0, sticky="SW")
    pclose = Button(pbottomframe, text="Close", state=DISABLED, command=popup.destroy)
    pclose.grid(row=0, column=1, sticky="SE")
    def whenfinished():
        pclose.configure(state=NORMAL)
        pbottomlabel.configure(text="Finished.")
    mypipe = TextPipe()
    p = multiprocessing.Process(target=runguiprocess,
        args=(mainmethod,args,mypipe))
    p.start()
    return dict(process=p, whenfinished=whenfinished, outfield=poutputfield, pipe=mypipe)
        
def runguiprocess(mainmethod, arglist, thepipe):
    oldout, olderr = sys.stdout, sys.stderr
    sys.stdout, sys.stderr = thepipe, sys.stderr  # thepipe?
    mainmethod(arglist)
    sys.stdout, sys.stderr = oldout, olderr


############################# main methods ###########################

def get_argument_parser():
    """interface for geniegui.py"""
    return main_buildparser()

def main_buildparser():
    p = argparse.ArgumentParser(
        description = "geniegui: Genome Informatics GUI",
        epilog = "In development. Use at your own Risk!"
        )
    p.add_argument("--title", "-t",
                   help = "specify title of GUI window")
    p.add_argument("--mainfunction","-m", default="main",
                   help = "name of main function of called module")
    p.add_argument("--parserfunction","-p", default="get_argument_parser",
                   help = "name of get_argument_parser function of called module")
    p.add_argument("module",
                   help = "python module (without .py) to create GUI for")
    return p


def rungui(args):
    # get parser
    modulename = args.module
    #print("PATH is", sys.path)
    module = __import__(modulename)
    #print("MODULE is", module)
    parserfunction = getattr(module, args.parserfunction)
    parser = parserfunction()  # returns parser; it may have an attibute _geniegui
    # treat arguments
    title = args.title if args.title is not None else modulename
    # create and start GUI
    modulemain = getattr(module, args.mainfunction)  # will raise error if no main exists
    gui = ArgparseGUI(parser, mainmethod=modulemain, title=title)
    gui.poll()
    gui.window.mainloop()


def main(args=None):
    """main function"""
    p = get_argument_parser()
    pargs = p.parse_args() if args is None else p.parse_args(args)
    rungui(pargs)

############################# test methods ###########################

def test():
    #main(["geniegui","--title","Genie GUI"])
    main(["amplikyzer"])

if __name__ == "__main__":
    #test()
    main()

############################# END ###########################
