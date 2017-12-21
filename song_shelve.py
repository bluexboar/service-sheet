__author__ = 'Will'


class Song:
    def __init__(self, song_key, title):
        self.song_key = song_key
        assert title is not None
        self.title = title.strip(line_end)
        self.verse = None
        self.chorus = None
        self.copyright = None

    def add_verse(self, text):
        if self.verse is None:
            self.verse = []
            self.verse.append(text)
        else:
            self.verse.append(text)

    def add_chorus(self, text):
        if self.chorus is None:
            self.chorus = []
            self.chorus.append(text)
        else:
            self.chorus.append(text)

    def add_cpright(self, text):
        self.copyright = text

    def print(self):
        print('id: ' + str(self.song_key) + ', title:' + self.title)
        print('verse: ' + str(self.verse))
        print('chorus: ' + str(self.chorus))
        print('copyright: ' + str(self.copyright))


class Bank:
    def __init__(self, version):
        self.version = version
        self.songlist = []
        self.song_id = 0

    def create_song(self, title):
        song = Song(self.song_id, title)
        self.song_id += 1
        self.songlist.append(song)

    def edit_song(self, indicator, text, index=None):
        if index is None:
            if len(self.songlist) == 0:
                index = 0
            else:
                index = -1

        song = self.songlist[index]
        if indicator == 'v':
            song.add_verse(text)
        elif indicator == 'r':
            song.add_chorus(text)
        elif indicator == 'c':
            song.add_cpright(text)

    def print(self, limit=5):
        for song in self.songlist:
            song.print()
            limit -= 1
            if limit == 0:
                break

    def shelve(self):
        import shelve
        db = shelve.open('song_bank')
        for i, item in enumerate(self.songlist):
            db[str(i)] = item
        db.close()


indicators = ['v', 'r', 'c', ']']
line_end = '\n'


if __name__ == '__main__':
    song_db = Bank('0816')
    with open('lyrics', 'r') as f:
        line = f.readline()
        while ']]]' not in line:  # set ']]]' is the end of the file
            # print(line)
            # start a new song
            if '[' in line:
                flag = None
                text = ''
                # extract title
                if f.readline().strip(line_end) == 't':  # title section
                    song_db.create_song(f.readline())
                    # extract content with indicator
                    while True:
                        line = f.readline()  # any conditions line move forward
                        if line.strip(line_end) in indicators:
                            if flag is None:  # first section
                                flag = line.strip(line_end)
                            else:  # arrive at a new section, table the last
                                assert text is not ''  # otherwise db corrupt
                                song_db.edit_song(flag, text)
                                flag = line.strip(line_end)
                                text = ''
                        else:
                            text += line
                        if ']' in line:
                            break
            line = f.readline()
    # song_db.print()
    song_db.shelve()
