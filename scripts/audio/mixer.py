import pygame

# Only to be used for backing tracks/longer sound files, not sound effects
class Mixer():
    '''
    The mixer object handles music, allowing for smooth 
    transitions between sound files

    events take the form of 
    fade_out: {"action":"fade_in", "time":100}
    play: {"action":"play", "track": "path/to/track.mp3", "patient":True}

    actions can be one of the following:
    play, fade out, change volume
    in the future, do fade_in and wait
    '''
    def __init__(self):
        self.events = []
        

    def add_event(self, event):
        '''
        Adds an event to the audio queue

        follows the form:
        fade_out: {"action":"fade_in", "time":100}
        play: {"action":"play", "track": "path/to/track.mp3", "patient":True}
        '''
        self.events.append(event)

    def play_track(self, track):
        '''
        Plays a track
        '''
        pygame.mixer_music.set_volume(0.5)
        pygame.mixer_music.unload() # Not sure if necessary, maybe a precaution to save memory
        pygame.mixer_music.load(track)
        pygame.mixer_music.play(-1) # Assume the track will be looped infinitely, update later

    def run(self):

        # if there's an event in the queue
        if len(self.events) != 0:
            event = self.events.pop(0)

            if event["action"] == "fade_out":
                pygame.mixer_music.fadeout(event["time"])

            elif event["action"] == "play":
                # if the track is patient (waiting its turn), then 
                # don't play it while the mixer is busy
                if event["patient"] and pygame.mixer_music.get_busy():
                    pass

                # otherwise, play the track
                else:
                    self.play_track(event["track"])
