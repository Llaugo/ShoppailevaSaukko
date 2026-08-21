class TimedSpeedEffects:
    """Tracks independent temporary speed effects without depending on Kivy."""

    def __init__(self, baseSpeed):
        self.baseSpeed = baseSpeed
        self._effects = {}

    @property
    def speed(self):
        activeSpeeds = [effect[0] for effect in self._effects.values()]
        return max([self.baseSpeed, *activeSpeeds])

    def setEffect(self, source, speed, duration):
        if not source:
            raise ValueError("A speed effect must have a source")
        if duration <= 0:
            self.clearEffect(source)
            return
        self._effects[source] = (speed, duration)

    def update(self, dt):
        if dt < 0:
            raise ValueError("Speed effects cannot be updated with negative time")
        for source, (speed, duration) in list(self._effects.items()):
            remaining = max(duration - dt, 0)
            if remaining:
                self._effects[source] = (speed, remaining)
            else:
                del self._effects[source]

    def clearEffect(self, source):
        self._effects.pop(source, None)

    def clear(self):
        self._effects.clear()

    def remaining(self, source):
        effect = self._effects.get(source)
        return effect[1] if effect else 0
