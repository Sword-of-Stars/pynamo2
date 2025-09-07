import sys
import inspect
import traceback

class TracePrints(object):
  def __init__(self):    
    self.stdout = sys.stdout
  def write(self, s):
    self.stdout.write("Writing %r\n" % s)
    traceback.print_stack(file=self.stdout)

#sys.stdout = TracePrints()


def find_caller():
    # Get the current stack frame, which includes this function, and go back by 2 frames
    caller_frame = inspect.stack()[2]
    # Get the calling function's name and file information
    caller_name = caller_frame.function
    caller_filename = caller_frame.filename
    caller_lineno = caller_frame.lineno
    print(f"Called by {caller_name} in {caller_filename} at line {caller_lineno}")