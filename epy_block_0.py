import numpy as np
from gnuradio import gr

class am_to_char(gr.sync_block):
    def __init__(self, symbol_length=32.0):
        gr.sync_block.__init__(
            self,
            name='am to char',   # will show up in GRC
            in_sig=[np.uint8],
            out_sig=0
        )
        self.lastInput = 0
        self.lastInputCount = 0
        self.symbol_length = symbol_length

    def work(self, input_items,output_items):
        inp = input_items[0]
        for i in inp:
          if i == self.lastInput:
            self.lastInputCount += 1
            if self.lastInputCount > self.symbol_length:
              self.lastInputCount = 0
              print("%d" % self.lastInput)
          else:
            self.lastInputCount = 0
            self.lastInput = i
        return len(inp)