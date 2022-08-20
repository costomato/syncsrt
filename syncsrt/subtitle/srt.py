import re
from datetime import timedelta

class srt:
  __lst: list = []
  
  # contructor: initializes subtitles as a list
  def __init__(self, filename: str):
    file = open(filename, "r")
    lines = file.readlines()
    file.close()

    timestamp: str = ""
    text: str = ""
    for line in lines:
      if re.search('^[0-9]+:[0-9]+:[0-9]+', line):
        if timestamp:
          [start, end] = timestamp.split(" --> ")
          self.__lst.append(([self.create_delta(start), self.create_delta(end)], text.strip()))

        timestamp = line.strip()
        text = ""
      
      elif re.search('^[0-9]+$', line) is None and re.search('^$', line) is None:
        text += line.strip() + '\n'

    # edge-case: for last subtitle
    [start, end] = timestamp.split(" --> ")
    self.__lst.append(([self.create_delta(start), self.create_delta(end)], text.strip()))

  # prints subtitle to console
  def show_srt(self):
    for l in self.__lst:
      print(f"{self.deltatostr(l[0][0])[:-3]} --> {self.deltatostr(l[0][1])[:-3]}")
      print(l[1])
      print()

  # outputs subtitle to file
  def output_srt(self, filename='output.srt'):
    with open(filename, 'w') as file:
      for l in self.__lst:
        file.write(f"{self.deltatostr(l[0][0])[:-3]} --> {self.deltatostr(l[0][1])[:-3]}\n")
        file.write(l[1] + '\n\n')

  # shifts srt by <time>
  def shift_srt(self, time):
    for l in self.__lst:
      l[0][0] = l[0][0] + time
      l[0][1] = l[0][1] + time

  # converts string to timedelta
  def create_delta(self, time: str):
    delst = [int(x) for x in re.split('\D', time)]
    return timedelta(hours=delst[0], minutes=delst[1], seconds=delst[2], milliseconds=delst[3])

  # get first timestamp of srt in string
  def get_first_timestamp_str(self):
    return self.deltatostr(self.__lst[0][0][0])[:-3]

  # get first timestamp of srt in delta
  def get_first_timestamp_delta(self):
    return self.__lst[0][0][0]

  # converts timedelta to string
  def deltatostr(self, delta):
    delta = str(delta)
    if re.search('^[0-9]+:[0-9]+:[0-9]+$', delta):
      delta += ".000000"
    return delta
