
class ActivityRepoException(Exception):
    def __init__(self, msg = ''):
        self._msg = msg

    def __str__(self):
        return self._msg


class ActivityRepo:
    def __init__(self):
        self._activities = []

    @property
    def activities(self):
        return self._activities

    def add_activity(self, activity):
        self.activities.append(activity)

    def remove_activity(self, index):
        self._activities.pop(index)

    def update_activity(self, index, activity):
        self._activities[index] = activity