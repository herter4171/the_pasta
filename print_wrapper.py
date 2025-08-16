from pathlib import Path
import subprocess
from base_has_logs import BaseHasLogs
import tempfile


class PrintWrapper(BaseHasLogs):
    @property
    def print_tag(self):
        return "<print>"

    @property
    def line_char_count(self):
        return 48

    def __init__(self, printer_path = '/dev/usb/lp0'):
        super().__init__()
        self._printer_path = printer_path
        self._thread = None
    
    #def write_async(self, msg):
    #    self._thread = threading.Thread(target=self.write, args=(msg,))

    def print(self, msg):
        self._write_temp_file(msg)
        
    def _write_temp_file(self, msg: str, num_trail_lines=10, cut = True):
        """Dump message to printer with options for trail lines and cutting."""
        # Clean up lines to fixed width format, and write
        trunc_msg = self._truncate_lines(msg)
        temp_file = tempfile.NamedTemporaryFile(delete=False)
        temp_file.write(trunc_msg.encode("utf-8"))
        
        # Append whitespace to get what we wrote out
        for i in range(num_trail_lines):
            temp_file.write(b'\n')

        # If we want to cut, send the ASCII magic to do that
        if cut:
            temp_file.write(b'\x1b\x69')

        temp_file.close()
        cut_sfx = "" if cut else "didn't "
        self._logger.info(f"Printed with {num_trail_lines} trailing lines and {cut_sfx}cut the feed")

        cmd = f"cat {temp_file.name} | sudo tee {self._printer_path}"
        subprocess.run(cmd, shell=True)


    def _truncate_lines(self, msg: str)-> str:
        """Converts raw message to fixed width except where newlines are imposed."""

        # Don't tamper with imposed newlines
        orig_lines = msg.split('\n')
        lines = []

        for curr_ln in orig_lines:
            # Assume we want the whole line
            to_append = [curr_ln]

            # Truncate if too long for our character width
            if len(curr_ln) > self.line_char_count:
                to_append = self._truncate_single_line(curr_ln)
            
            lines += to_append

        return '\n'.join(lines)
    
    def _truncate_single_line(self, curr_ln: str)-> list:
        sub_lines = []

        while len(curr_ln) > self.line_char_count:
            # Whitespace can be left from prior line
            curr_ln = self._trim_lead_whitespace(curr_ln)
            end_ind = self.line_char_count
            
            # Remove trailing whitespace
            while curr_ln[end_ind] != ' ':
                end_ind -= 1
            
            # Add our sub-line, and trim current line
            sub_lines.append(curr_ln[:end_ind])
            curr_ln = curr_ln[end_ind:]
        
        # Put any trailing characters less than a full line last
        if len(curr_ln) > 0:
            curr_ln = self._trim_lead_whitespace(curr_ln)
            sub_lines.append(curr_ln)

        return sub_lines

    def _trim_lead_whitespace(self, curr_ln: str)-> str:
        """"Removes whitespace at the beginning of the given line"""
        begin_ind = 0

        while curr_ln[begin_ind] == ' ':
            begin_ind += 1
        
        return curr_ln[begin_ind:]

if __name__ == "__main__":
    pw = PrintWrapper()
    pw.write("<print>Test</print>")