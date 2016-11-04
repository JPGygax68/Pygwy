class Updater(object):
    """The Updater is an "aspect" that must be injected into the Widget class. Its task is to make sure that changes to the visual state of a Widget actually make it to the screen. This code has to be pluggable in order to support different types of display hardware and software layers, such as:
    - a free-running game loop (no code required since the UI is redrawn in full, along with everything else, in each cycle)
    - invalidation zones: the Updater collects and aggregates the zones (rectangles) that are modified in response to an input event, then triggers a redraw of the modified zones (this can be simplied to redrawing the whole UI after any input event, without registering update zones)
    """
    
    pass

class DummyUpdater(Updater):
    """This implementation of the Updater aspect does nothing. It can be used for free-running game loops where everything is redrawn anyway."""
    pass
    
class TrivialUpdater(Updater):
    """The Trivial Updater is the simplest (non-dummy) implementation of the Updater aspect. It does nothing more than set a boolean flag in response to any change, then triggers a redraw if and only if that flag has been set."""