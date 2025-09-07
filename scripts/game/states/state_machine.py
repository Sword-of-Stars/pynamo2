class State():
    '''
    Defines a state, such as menu, main loop, or credits
    '''
    def __init__(self):
        self.state_machine = state_machine

    def on_first(self):
        '''
        Runs on every state transition 
        (not the global first time, just the local one)
        maybe implement that later
        '''
        pass

    def run(self):
        pass


class StateMachine():
    '''
    Handles all states and transitions between them

    States are stores as a dictionary, and the machine tracks the
    current and previous state
    '''
    def __init__(self, all_states={}, current_state=None):
        self.allStates = all_states # a dictionary of all possible states
        self.currentState = current_state
        self.prevState = None
        self.justChanged = True # Changed from nothing to on

    def init_states(self, states={}):
        '''
        Loads all states into the state machine

        allows states to be initialized after state machine creation
        '''
        self.allStates = states

    def set_state(self, state):
        '''
        Sets the current state of the state machine, detecting
        differences in state selection

        Args:
            state (State): a valid state object in self.allStates
        '''
        if state != self.currentState:
            self.justChanged = True
            self.prevState = self.currentState
        self.currentState = state

        assert state in self.allStates, f"{state} is not a valid state"

    def run(self):
        '''
        Runs and handles all states

        should be called by Game class
        '''
        if self.currentState != None:
            if self.justChanged:
                self.allStates[self.currentState].on_first()
                self.justChanged = False
            self.allStates[self.currentState].run()

state_machine = StateMachine()