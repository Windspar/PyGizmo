
class Recall:
    def __init__(self):
        self.pos = 0
        self.buffer = []

    def down(self):
        if self.pos > 0:
            self.pos -= 1
            text = self.buffer[self.pos]
            return text
        else:
            self.pos = -1

    def up(self):
        if self.pos < len(self.buffer) - 1:
            self.pos += 1
            return self.buffer[self.pos]

    def store(self, text):
        self.pos = -1
        if text not in self.buffer:
            if len(self.buffer) > 4:
                self.buffer = [text] + self.buffer[:4]
            else:
                self.buffer.insert(0, text)
        elif self.buffer[0] != text:
            self.buffer.remove(text)
            self.buffer.insert(0, text)
