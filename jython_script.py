from java.lang import *
from java.util import *
from com.ti.debug.engine.scripting import *
from com.ti.ccstudio.scripting.environment import *

# Create our scripting environment object - which is the main entry point into any script and
# the factory for creating other Scriptable Servers and Sessions
script = ScriptingEnvironment.instance()

# Create a log file in the current directory to log script execution
script.traceBegin("BreakpointsTestLog_python.xml", "DefaultStylesheet.xsl")

# Set our TimeOut
script.setScriptTimeout(15000)

# Log everything
script.traceSetConsoleLevel(TraceLevel.ALL)
script.traceSetFileLevel(TraceLevel.ALL)

# Get the Debug Server and start a Debug Session
debugServer = script.getServer("DebugServer.1")
debugServer.setConfig("../msp430f5529/msp430f5529.ccxml");
debugSession = debugServer.openSession(".*")

debugSession.target.connect()

# Load a program
# (ScriptingEnvironment has a concept of a working folder and for all of the APIs which take
# path names as arguments you can either pass a relative path or an absolute path)
debugSession.memory.loadProgram("../msp430f5529/programs/modem.out")

# Set a breakpoint
address = debugSession.symbol.getAddress("ReadNextData")
bp = debugSession.breakpoint.add(address)

# Using an expression - get the current value of the PC
nPC = debugSession.expression.evaluate("PC")
scriptEnv.traceWrite("Current halted at {}. This should be at the start of main().".format(hex(nPC)))

# Run the target. Should halt at our breakpoint.
debugSession.target.run()

nPC = debugSession.expression.evaluate("PC")

# Verify we halted at the correct address.
if (nPC == address):
    script.traceWrite("SUCCESS: Halted at correct location")
else:
    script.traceWrite("FAIL: Expected halt at " + hex(address) + ", actually halted at " + hex(nPC))
    script.traceSetConsoleLevel(TraceLevel.INFO)
    script.traceWrite("TEST FAILED!")
    script.traceEnd()
    System.exit(1);

# All done
debugSession.terminate()
debugServer.stop()
~
